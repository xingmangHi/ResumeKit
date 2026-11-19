#!/usr/bin/env python3
"""浏览器实际验证模板
运行: cd /workspace && python3 browser_verify.py
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess

# 固定配置
VIEWPORT = {'width': 1280, 'height': 1024}
ARTIFACTS_DIR = Path('/opt/cursor/artifacts')
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

async def verify_template(page, template_path, template_name):
    """验证单个模板"""
    print(f"\n{'='*70}")
    print(f"验证: {template_name}")
    print('='*70)
    
    result = {
        'name': template_name,
        'success': False,
        'errors': [],
        'metrics': {}
    }
    
    # 加载模板
    file_url = f'file://{template_path.absolute()}'
    try:
        await page.goto(file_url, wait_until='networkidle', timeout=10000)
    except Exception as e:
        result['errors'].append(f"加载失败: {e}")
        return result
    
    # 等待字体就绪
    try:
        await page.evaluate('document.fonts.ready')
        print("✅ 字体就绪")
    except Exception as e:
        result['errors'].append(f"字体等待失败: {e}")
    
    # 获取.container实际高度
    try:
        container_height = await page.evaluate('''() => {
            const container = document.querySelector('.container') || document.querySelector('.page');
            if (!container) return null;
            return {
                offsetHeight: container.offsetHeight,
                clientHeight: container.clientHeight,
                scrollHeight: container.scrollHeight
            };
        }''')
        
        if container_height:
            result['metrics']['container_height_px'] = container_height['offsetHeight']
            result['metrics']['container_client_px'] = container_height['clientHeight']
            result['metrics']['container_scroll_px'] = container_height['scrollHeight']
            
            # 297mm @ 96dpi ≈ 1122px
            expected_px = 1122
            diff_px = abs(container_height['offsetHeight'] - expected_px)
            
            print(f"容器高度: {container_height['offsetHeight']}px (预期~{expected_px}px, 差{diff_px}px)")
            
            if diff_px > 20:  # 容忍20px
                result['errors'].append(f"容器高度偏差: {diff_px}px")
        else:
            result['errors'].append("未找到.container或.page")
    except Exception as e:
        result['errors'].append(f"高度测量失败: {e}")
    
    # 检查overflow
    try:
        overflow_info = await page.evaluate('''() => {
            const container = document.querySelector('.container') || document.querySelector('.page');
            if (!container) return null;
            
            const items = container.querySelectorAll('.item');
            if (items.length === 0) return {hasItems: false};
            
            const lastItem = items[items.length - 1];
            const containerRect = container.getBoundingClientRect();
            const lastItemRect = lastItem.getBoundingClientRect();
            
            return {
                hasItems: true,
                containerBottom: containerRect.bottom,
                lastItemBottom: lastItemRect.bottom,
                overflow: lastItemRect.bottom > containerRect.bottom,
                overflowPx: Math.max(0, lastItemRect.bottom - containerRect.bottom)
            };
        }''')
        
        if overflow_info and overflow_info['hasItems']:
            result['metrics']['last_item_overflow_px'] = overflow_info['overflowPx']
            if overflow_info['overflow']:
                print(f"⚠️ 末项溢出: {overflow_info['overflowPx']:.1f}px")
            else:
                print(f"✅ 末项未溢出")
    except Exception as e:
        result['errors'].append(f"溢出检查失败: {e}")
    
    # 截图
    screenshot_path = ARTIFACTS_DIR / f'{template_name.replace(".html", "")}_screen.png'
    try:
        await page.screenshot(path=str(screenshot_path), full_page=False)
        result['screenshot'] = str(screenshot_path)
        print(f"✅ 截图: {screenshot_path}")
    except Exception as e:
        result['errors'].append(f"截图失败: {e}")
    
    # 生成PDF
    pdf_path = ARTIFACTS_DIR / f'{template_name.replace(".html", "")}.pdf'
    try:
        await page.pdf(
            path=str(pdf_path),
            format='A4',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        result['pdf'] = str(pdf_path)
        print(f"✅ PDF: {pdf_path}")
        
        # 获取PDF页数
        try:
            pdf_info = subprocess.check_output(
                ['pdfinfo', str(pdf_path)],
                stderr=subprocess.DEVNULL
            ).decode('utf-8')
            
            for line in pdf_info.split('\n'):
                if line.startswith('Pages:'):
                    pages = int(line.split(':')[1].strip())
                    result['metrics']['pdf_pages'] = pages
                    print(f"PDF页数: {pages}")
                elif line.startswith('Page size:'):
                    result['metrics']['pdf_pagesize'] = line.split(':')[1].strip()
                    print(f"PDF页面尺寸: {result['metrics']['pdf_pagesize']}")
        except:
            pass
    except Exception as e:
        result['errors'].append(f"PDF生成失败: {e}")
    
    result['success'] = len(result['errors']) == 0
    return result

async def main():
    template_dir = Path('/workspace/template')
    files = sorted(template_dir.glob('*.html'))
    
    # 获取commit信息
    commit_sha = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
        cwd='/workspace'
    ).decode('utf-8').strip()
    
    print(f"测试commit: {commit_sha}")
    print(f"浏览器: Chromium Playwright")
    print(f"字体: Noto CJK")
    print(f"Viewport: {VIEWPORT}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        
        results = []
        for template_path in files:
            result = await verify_template(page, template_path, template_path.name)
            results.append(result)
        
        await browser.close()
    
    # 保存结果
    report_path = ARTIFACTS_DIR / 'verification_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'commit': commit_sha,
            'browser': 'Chromium Playwright',
            'viewport': VIEWPORT,
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print("汇总")
    print('='*70)
    
    for result in results:
        status = "✅" if result['success'] else "⚠️"
        print(f"{status} {result['name']}")
        if result['errors']:
            for err in result['errors'][:2]:
                print(f"   {err}")
        if 'pdf_pages' in result.get('metrics', {}):
            print(f"   PDF: {result['metrics']['pdf_pages']}页")
    
    print(f"\n报告: {report_path}")
    print(f"产物目录: {ARTIFACTS_DIR}")

if __name__ == '__main__':
    asyncio.run(main())
