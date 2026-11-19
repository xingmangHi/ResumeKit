#!/usr/bin/env python3
"""正确修复模板 A4 几何：统一策略 @page margin 0 + 完整盒"""
import re
from pathlib import Path

def fix_template(filepath):
    """修复单个模板"""
    print(f"\n处理: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 统一 @page margin 为 0（简化几何账）
    content = re.sub(
        r'@page\s*{\s*size:\s*A4[^}]*margin:[^;}]+',
        '@page { size: A4 portrait; margin: 0',
        content
    )
    
    # 2. 提取 @media screen 中的 .container 规则
    screen_pattern = r'(@media\s+screen\s*\{)(.*?)(\n\s*\})'
    screen_match = re.search(screen_pattern, content, re.DOTALL)
    
    if not screen_match:
        print("  ❌ 未找到 @media screen")
        return False
    
    screen_start = screen_match.group(1)
    screen_body = screen_match.group(2)
    screen_end = screen_match.group(3)
    
    # 提取 .container 块
    container_pattern = r'\s*(\.container\s*\{[^}]+\})'
    container_match = re.search(container_pattern, screen_body)
    
    if not container_match:
        print("  ❌ 未找到 .container")
        return False
    
    container_block = container_match.group(1)
    
    # 解析 .container 规则
    width_match = re.search(r'width:\s*([^;]+);', container_block)
    min_height_match = re.search(r'min-height:\s*([^;]+);', container_block)
    padding_match = re.search(r'padding:\s*([^;]+);', container_block)
    background_match = re.search(r'background:\s*([^;]+);', container_block)
    margin_match = re.search(r'margin:\s*([^;]+);', container_block)
    border_match = re.search(r'border:\s*([^;]+);', container_block)
    box_shadow_match = re.search(r'box-shadow:\s*([^;]+);', container_block)
    
    width = width_match.group(1).strip() if width_match else '210mm'
    padding = padding_match.group(1).strip() if padding_match else '0'
    background = background_match.group(1).strip() if background_match else 'var(--paper)'
    margin = margin_match.group(1).strip() if margin_match else '0 auto'
    border = border_match.group(1).strip() if border_match else '1.5px solid #555'
    box_shadow = box_shadow_match.group(1).strip() if box_shadow_match else '0 0 12px rgba(0,0,0,0.25)'
    
    # 3. 构建新的通用规则（在 @media screen 之前插入）
    common_rule = f"""  /* ========== 通用：固定 A4 纸张盒（屏幕和打印共享） ========== */
  .container {{
    width: 210mm;
    height: 297mm;
    padding: {padding};
    background: {background};
    margin: {margin};
    box-sizing: border-box;
    overflow: visible;
  }}

"""
    
    # 4. 构建新的 @media screen（只保留外装饰）
    new_screen = f"""  @media screen {{
    html {{ background: #888; }}
    body {{ background: #888; padding: 20px; }}
    .container {{
      outline: {border.replace('border', 'outline') if 'border' in border else border};
      box-shadow: {box_shadow};
    }}
  }}
"""
    
    # 5. 找到 @media screen 的位置并替换
    # 先找到 @media screen 前的位置（通常在 body 样式之后）
    insert_pos = content.find('@media screen')
    if insert_pos == -1:
        print("  ❌ 无法定位 @media screen")
        return False
    
    # 删除旧的 @media screen 块
    content = content[:screen_match.start()] + content[screen_match.end():]
    
    # 在原位置插入新规则
    insert_pos = screen_match.start()
    content = content[:insert_pos] + common_rule + new_screen + '\n' + content[insert_pos:]
    
    # 6. 修正 @media print
    # 移除字号覆盖（如果有）
    print_pattern = r'(@media\s+print\s*\{)(.*?)(\n\s*\})'
    print_match = re.search(print_pattern, content, re.DOTALL)
    
    if print_match:
        print_body = print_match.group(2)
        
        # 移除 body { font-size: ... } 行
        print_body = re.sub(r'\s*body\s*\{[^}]*font-size:[^}]*\}', '', print_body)
        
        # 移除各元素的 font-size 覆盖
        print_body = re.sub(r'\s*\.[a-z-]+\s*\{\s*font-size:[^}]*\}', '', print_body)
        
        # 替换 .section { page-break-inside: avoid; } 为细粒度规则
        print_body = re.sub(
            r'\s*\.section\s*\{\s*page-break-inside:\s*avoid;\s*\}',
            '',
            print_body
        )
        
        # 构建新的 @media print
        new_print = f"""  @media print {{
    html, body {{ background: #fff; padding: 0; margin: 0; }}
    .container {{
      outline: none;
      box-shadow: none;
    }}
    .section-title {{ break-after: avoid; }}
    .item {{ break-inside: avoid; }}
    .header {{ break-after: avoid; }}
  }}
"""
        content = content[:print_match.start()] + new_print + content[print_match.end():]
    
    # 7. 移除多余的通用 .container { max-width: 21cm; ... } 定义
    content = re.sub(
        r'\n\s*\.container\s*\{\s*max-width:\s*21cm;\s*margin:\s*0\s+auto;\s*\}\s*\n',
        '\n',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ 已修正")
        return True
    else:
        print("  - 无变化")
        return False

def main():
    template_dir = Path('/workspace/template')
    files = sorted(template_dir.glob('*.html'))
    
    modified = 0
    for filepath in files:
        if fix_template(filepath):
            modified += 1
    
    print(f"\n总计: {len(files)} 个文件, 修正了 {modified} 个")

if __name__ == '__main__':
    main()
