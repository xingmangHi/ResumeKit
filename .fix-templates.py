#!/usr/bin/env python3
"""
批量修正模板的 A4 共享几何问题
"""
import re
import sys
from pathlib import Path

def fix_template(filepath):
    """修正单个模板文件"""
    print(f"处理: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 修正 @page 声明
    content = re.sub(
        r'@page\s*{\s*size:\s*A4;',
        '@page { size: A4 portrait;',
        content
    )
    
    # 2. 查找并修正 .container 或 .paper 的结构
    # 模式A: 在 @media screen 中定义
    pattern_a = re.compile(
        r'(@media\s+screen\s*{[^}]*?)(\.(?:container|paper)\s*{[^}]*?min-height:\s*29\.7cm;[^}]*?})',
        re.DOTALL
    )
    
    match = pattern_a.search(content)
    if match:
        media_screen_block = match.group(1)
        container_block = match.group(2)
        
        # 提取 container 的属性
        width_match = re.search(r'width:\s*([^;]+);', container_block)
        padding_match = re.search(r'padding:\s*([^;]+);', container_block)
        background_match = re.search(r'background:\s*([^;]+);', container_block)
        margin_match = re.search(r'margin:\s*([^;]+);', container_block)
        
        width = width_match.group(1) if width_match else '210mm'
        padding = padding_match.group(1) if padding_match else '1.5cm 1.2cm'
        background = background_match.group(1) if background_match else 'var(--paper)'
        margin = margin_match.group(1) if margin_match else '0 auto'
        
        # 确定类名
        class_name = 'container' if '.container' in container_block else 'paper'
        
        # 构建新的通用规则
        common_rule = f"""  /* ========== 通用：固定 A4 纸张盒（屏幕和打印共享） ========== */
  .{class_name} {{
    width: 210mm;
    height: 297mm;
    padding: {padding};
    background: {background};
    margin: {margin};
    box-sizing: border-box;
    overflow: visible;
  }}
"""
        
        # 构建新的屏幕规则（只保留外装饰）
        screen_rule = f"""  /* ========== 屏幕：外装饰 ========== */
  @media screen {{
    html {{ background: #888; }}
    body {{ background: #888; padding: 20px; }}
    .{class_name} {{
      border: 1.5px solid #555;
      box-shadow: 0 0 12px rgba(0,0,0,0.25);
    }}
  }}
"""
        
        # 插入位置：在 body 样式之后
        body_pattern = re.compile(r'(body\s*{[^}]+})\s*\n', re.DOTALL)
        body_match = body_pattern.search(content)
        if body_match:
            insert_pos = body_match.end()
            # 移除旧的 @media screen 块
            content = pattern_a.sub('', content)
            # 插入新规则
            content = content[:insert_pos] + '\n' + common_rule + '\n' + screen_rule + '\n' + content[insert_pos:]
    
    # 3. 修正 @media print
    # 移除 font-size 覆盖
    content = re.sub(
        r'(@media\s+print\s*{[^}]*?)font-size:\s*[^;]+;',
        r'\1',
        content,
        flags=re.DOTALL
    )
    
    # 添加打印规则
    print_pattern = re.compile(r'@media\s+print\s*{([^}]*?)}', re.DOTALL)
    print_match = print_pattern.search(content)
    if print_match:
        class_name = 'container' if '.container' in content[:10000] else 'paper'
        new_print_block = f"""@media print {{
    html, body {{ background: #fff; padding: 0; margin: 0; }}
    .{class_name} {{
      border: none;
      box-shadow: none;
    }}
    .section-title {{ break-after: avoid; }}
    .item {{ break-inside: avoid; }}
  }}"""
        content = print_pattern.sub(new_print_block, content)
    
    # 4. 移除 .section 的 page-break-inside: avoid
    content = re.sub(
        r'(\.section\s*{[^}]*?)page-break-inside:\s*avoid;\s*',
        r'\1',
        content
    )
    
    # 5. 移除重复的 .container 定义
    content = re.sub(
        r'\.(?:container|paper)\s*{\s*max-width:\s*21cm;\s*margin:\s*0\s+auto;\s*}',
        '',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 已修正")
        return True
    else:
        print(f"  - 无需修改或模式不匹配")
        return False

def main():
    template_dir = Path('/workspace/template')
    files = sorted(template_dir.glob('*.html'))
    
    # 跳过已修正的
    skip = ['简约_互联网_黑.html', '简约_金融_黑.html']
    files = [f for f in files if f.name not in skip]
    
    modified = 0
    for filepath in files:
        if fix_template(filepath):
            modified += 1
    
    print(f"\n总计: {len(files)} 个文件, 修正了 {modified} 个")

if __name__ == '__main__':
    main()
