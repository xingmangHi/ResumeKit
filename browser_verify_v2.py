#!/usr/bin/env python3
"""浏览器实际验证模板 v2 - 完整截图和逐页PDF"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess

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
        'errors': [],
        'metrics': {},
        'geometry': {}
    }
    
    file_url = f'file://{template_path.absolute()}'
    try:
        await page.goto(file_url, wait_until='networkidle', timeout=10000)
        await page.evaluate('document.fonts.ready')
        print("✅ 加载完成，字体就绪")
    except Exception as e:
        result['errors'].append(f"加载失败: {e}")
        return result
    
    # 完整页面截图
    screenshot_path = ARTIFACTS_DIR / f'{template_name.replace(".html", "")}_fullpage.png'
    try:
        await page.screenshot(path=str(screenshot_path), full_page=True)
        result['screenshot'] = str(screenshot_path)
        print(f"✅ 完整截图: {screenshot_path.name}")
    except Exception as e:
        result['errors'].append(f"截图失败: {e}")
    
    # 获取完整几何信息
    try:
        geom = await page.evaluate('''() => {
            const container = document.querySelector('.container') || document.querySelector('.page');
            if (!container) return null;
            
            const rect = container.getBoundingClientRect();
            const items = container.querySelectorAll('.item');
            
            let itemsInfo = [];
            items.forEach((item, idx) => {
                const r = item.getBoundingClientRect();
                itemsInfo.push({
                    index: idx,
                    top: r.top,
                    bottom: r.bottom,
                    left: r.left,
                    right: r.right,
                    text: item.textContent.substring(0, 50)
                });
            });
            
            return {
                container: {
                    top: rect.top,
                    left: rect.left,
                    right: rect.right,
                    bottom: rect.bottom,
                    width: rect.width,
                    height: rect.height,
                    offsetHeight: container.offsetHeight,
                    scrollHeight: container.scrollHeight
                },
                items: itemsInfo,
                allText: document.body.textContent.length
            };
        }''')
        
        if geom:
            result['geometry'] = geom
            print(f"容器: {geom['container']['offsetHeight']:.0f}px高")
            print(f"Items: {len(geom['items'])}个")
    except Exception as e:
        result['errors'].append(f"几何测量失败: {e}")
    
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
        
        # PDF信息
        try:
            pdf_info = subprocess.check_output(
                ['pdfinfo', str(pdf_path)],
                stderr=subprocess.DEVNULL
            ).decode('utf-8')
            
            for line in pdf_info.split('\n'):
                if line.startswith('Pages:'):
                    result['metrics']['pdf_pages'] = int(line.split(':')[1].strip())
                elif line.startswith('Page size:'):
                    result['metrics']['pdf_pagesize'] = line.split(':')[1].strip()
            
            print(f"✅ PDF: {result['metrics'].get('pdf_pages', '?')}页, {result['metrics'].get('pdf_pagesize', 'unknown')}")
        except:
            pass
            
        # PDF文本提取
        try:
            pdf_text = subprocess.check_output(
                ['pdftotext', str(pdf_path), '-'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8', errors='ignore')
            result['metrics']['pdf_text_length'] = len(pdf_text)
        except:
            pass
            
    except Exception as e:
        result['errors'].append(f"PDF失败: {e}")
    
    return result

async def main():
    template_dir = Path('/workspace/template')
    files = sorted(template_dir.glob('*.html'))
    
    commit_sha = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
        cwd='/workspace'
    ).decode('utf-8').strip()
    
    print(f"测试commit: {commit_sha}")
    print(f"浏览器: Chromium Playwright")
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
    report_path = ARTIFACTS_DIR / 'verification_report_v2.json'
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
        status = "✅" if not result['errors'] else "⚠️"
        pages = result.get('metrics', {}).get('pdf_pages', '?')
        print(f"{status} {result['name']}: {pages}页")
    
    print(f"\n报告: {report_path}")

if __name__ == '__main__':
    asyncio.run(main())
