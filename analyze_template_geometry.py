#!/usr/bin/env python3
"""分析每个模板的 A4 几何配置"""
import re
from pathlib import Path

def extract_page_margin(html):
    """提取 @page margin"""
    match = re.search(r'@page\s*{\s*size:\s*A4[^}]*margin:\s*([^;}]+)', html)
    if match:
        return match.group(1).strip()
    return None

def extract_container_rules(html):
    """提取 .container 或 .page 的关键规则"""
    # 查找 @media screen 中的 .container
    screen_match = re.search(
        r'@media\s+screen\s*{([^}]*(?:{[^}]*})*)}', 
        html, 
        re.DOTALL
    )
    
    result = {
        'screen_min_height': None,
        'screen_width': None,
        'screen_padding': None,
        'screen_border': None,
        'common_rules': None
    }
    
    if screen_match:
        screen_block = screen_match.group(1)
        # 查找 .container 或 .page
        container_match = re.search(
            r'\.(container|page)\s*{([^}]+)}',
            screen_block
        )
        if container_match:
            rules = container_match.group(2)
            
            width = re.search(r'width:\s*([^;]+)', rules)
            min_height = re.search(r'min-height:\s*([^;]+)', rules)
            padding = re.search(r'padding:\s*([^;]+)', rules)
            border = re.search(r'border:\s*([^;]+)', rules)
            
            if width:
                result['screen_width'] = width.group(1).strip()
            if min_height:
                result['screen_min_height'] = min_height.group(1).strip()
            if padding:
                result['screen_padding'] = padding.group(1).strip()
            if border:
                result['screen_border'] = border.group(1).strip()
    
    # 查找通用规则中的 .container（在 @media 外）
    lines = html.split('\n')
    in_media = False
    for i, line in enumerate(lines):
        if '@media' in line:
            in_media = True
        if in_media and '}' in line and line.strip() == '}':
            in_media = False
        if not in_media and re.search(r'\.(container|page)\s*{', line):
            # 找到通用规则
            block_start = i
            j = i + 1
            while j < len(lines) and '}' not in lines[j]:
                j += 1
            block = '\n'.join(lines[block_start:j+1])
            result['common_rules'] = block.strip()
            break
    
    return result

def analyze_template(filepath):
    """分析单个模板"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    page_margin = extract_page_margin(html)
    container = extract_container_rules(html)
    
    # 检查是否有 .paper（双层结构）
    has_paper = '.paper' in html
    
    return {
        'name': filepath.name,
        'page_margin': page_margin,
        'container': container,
        'double_layer': has_paper
    }

def main():
    template_dir = Path('/workspace/template')
    files = sorted(template_dir.glob('*.html'))
    
    print("=" * 80)
    print("模板几何配置分析")
    print("=" * 80)
    
    for filepath in files:
        info = analyze_template(filepath)
        print(f"\n【{info['name']}】")
        print(f"  @page margin: {info['page_margin']}")
        print(f"  双层结构: {'是' if info['double_layer'] else '否'}")
        print(f"  @media screen .container:")
        print(f"    width: {info['container']['screen_width']}")
        print(f"    min-height: {info['container']['screen_min_height']}")
        print(f"    padding: {info['container']['screen_padding']}")
        print(f"    border: {info['container']['screen_border']}")
        print(f"  通用规则: {info['container']['common_rules']}")
        
        # 计算建议
        if info['page_margin'] == '0':
            print("  ✅ 建议: @page margin 0, 可用 210mm×297mm 盒")
        else:
            print(f"  ⚠️  建议: @page margin 非零 ({info['page_margin']}), HTML 盒需缩小或 margin 改为 0")

if __name__ == '__main__':
    main()
