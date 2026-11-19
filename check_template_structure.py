#!/usr/bin/env python3
"""检查模板 HTML/CSS 结构完整性"""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

def check_css_brackets(css_text):
    """检查 CSS 大括号配对"""
    stack = []
    line_num = 1
    errors = []
    
    for i, char in enumerate(css_text):
        if char == '\n':
            line_num += 1
        elif char == '{':
            stack.append(('open', line_num, i))
        elif char == '}':
            if not stack:
                errors.append(f"行 {line_num}: 多余的 '}}' 未匹配")
            else:
                stack.pop()
    
    if stack:
        for bracket_type, line, pos in stack:
            errors.append(f"行 {line}: 未闭合的 '{{'")
    
    return errors

def check_media_queries(css_text):
    """检查 @media 块完整性"""
    issues = []
    
    # 检查 @media screen
    screen_pattern = r'@media\s+screen\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
    screen_matches = list(re.finditer(screen_pattern, css_text, re.DOTALL))
    
    if not screen_matches:
        issues.append("未找到完整的 @media screen 块")
    else:
        for match in screen_matches:
            content = match.group(1)
            # 检查是否有嵌套规则
            if '{' in content:
                nested_rules = re.findall(r'([.\w-]+)\s*\{', content)
                if nested_rules:
                    issues.append(f"@media screen 内有嵌套规则: {nested_rules[:3]}")
    
    # 检查 @media print
    print_pattern = r'@media\s+print\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
    print_matches = list(re.finditer(print_pattern, css_text, re.DOTALL))
    
    if not print_matches:
        issues.append("未找到完整的 @media print 块")
    
    return issues

def check_template(filepath):
    """检查单个模板"""
    print(f"\n{'='*60}")
    print(f"检查: {filepath.name}")
    print('='*60)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析 HTML
    soup = BeautifulSoup(html_content, 'html5lib')
    
    # 提取 CSS
    style_tags = soup.find_all('style')
    if not style_tags:
        print("❌ 未找到 <style> 标签")
        return False
    
    css_text = '\n'.join(tag.string or '' for tag in style_tags)
    
    # 1. 检查大括号配对
    bracket_errors = check_css_brackets(css_text)
    if bracket_errors:
        print(f"❌ CSS 大括号配对错误 ({len(bracket_errors)} 处):")
        for err in bracket_errors[:5]:
            print(f"   {err}")
    else:
        print("✅ CSS 大括号配对正确")
    
    # 2. 检查 @media 块
    media_issues = check_media_queries(css_text)
    if media_issues:
        print(f"❌ @media 块问题:")
        for issue in media_issues:
            print(f"   {issue}")
    else:
        print("✅ @media 块结构完整")
    
    # 3. 检查关键规则
    has_container = '.container' in css_text or '.page' in css_text
    has_page_rule = '@page' in css_text
    has_min_height_in_screen = bool(re.search(r'@media\s+screen[^}]*min-height:', css_text, re.DOTALL))
    
    print(f"\n关键规则检查:")
    print(f"  纸张盒容器: {'✅' if has_container else '❌'}")
    print(f"  @page 声明: {'✅' if has_page_rule else '❌'}")
    print(f"  @media screen 中有 min-height: {'⚠️ 需迁移' if has_min_height_in_screen else '✅'}")
    
    # 4. 检查占位文字
    placeholder_texts = ['姓  名', '+86 XXX', '教育背景', '工作经历']
    found_placeholders = sum(1 for text in placeholder_texts if text in html_content)
    print(f"  占位文字保留: {found_placeholders}/{len(placeholder_texts)}")
    
    passed = (not bracket_errors and not media_issues and 
              has_container and has_page_rule and not has_min_height_in_screen)
    
    return passed

def main():
    template_dir = Path('/workspace/template')
    files = sorted(template_dir.glob('*.html'))
    
    results = {}
    for filepath in files:
        passed = check_template(filepath)
        results[filepath.name] = passed
    
    print(f"\n{'='*60}")
    print("汇总结果")
    print('='*60)
    
    for name, passed in results.items():
        status = '✅ 通过' if passed else '❌ 需修复'
        print(f"{name}: {status}")
    
    total = len(results)
    passed_count = sum(1 for p in results.values() if p)
    print(f"\n总计: {passed_count}/{total} 通过")
    
    return 0 if passed_count == total else 1

if __name__ == '__main__':
    sys.exit(main())
