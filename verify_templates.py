#!/usr/bin/env python3
"""可靠的模板CSS和HTML验证"""
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import tinycss2
from cssselect2 import ElementWrapper

def parse_css_rules(css_text):
    """解析CSS并检查错误"""
    tokens = tinycss2.parse_stylesheet(css_text, skip_comments=False, skip_whitespace=True)
    errors = []
    rules = {'at_rules': {}, 'normal': []}
    
    for token in tokens:
        if token.type == 'error':
            errors.append(f"CSS解析错误: {token}")
        elif token.type == 'at-rule':
            rule_name = token.lower_at_keyword
            if rule_name not in rules['at_rules']:
                rules['at_rules'][rule_name] = []
            rules['at_rules'][rule_name].append(token)
        elif token.type == 'qualified-rule':
            rules['normal'].append(token)
    
    return rules, errors

def check_print_overrides(css_text):
    """检查print中的字号/颜色覆盖"""
    rules, _ = parse_css_rules(css_text)
    overrides = []
    
    if 'media' in rules['at_rules']:
        for media_rule in rules['at_rules']['media']:
            # 检查是否是 print
            prelude = tinycss2.serialize(media_rule.prelude)
            if 'print' in prelude:
                content = tinycss2.serialize(media_rule.content)
                # 检查 font-size
                if re.search(r'font-size\s*:', content):
                    matches = re.finditer(r'([.#\w-]+)\s*\{[^}]*font-size\s*:[^}]*\}', content)
                    for m in matches:
                        overrides.append(f"print中字号覆盖: {m.group(1)}")
                # 检查 color
                if re.search(r'(?<!border-)color\s*:', content):
                    matches = re.finditer(r'([.#\w-]+)\s*\{[^}]*(?<!border-)color\s*:[^}]*\}', content)
                    for m in matches:
                        overrides.append(f"print中颜色覆盖: {m.group(1)}")
    
    return overrides

def check_page_break(css_text):
    """检查整章page-break-inside"""
    issues = []
    # 在通用规则和media中都检查
    if re.search(r'\.section\s*\{[^}]*page-break-inside\s*:\s*avoid', css_text):
        issues.append("通用规则中存在 .section { page-break-inside: avoid }")
    
    return issues

def check_selector_match(html_path, selectors):
    """检查选择器是否命中HTML元素"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html5lib')
    results = {}
    
    for selector in selectors:
        try:
            # 使用 BeautifulSoup 的 CSS 选择器
            matches = soup.select(selector)
            results[selector] = len(matches)
        except Exception as e:
            results[selector] = f"错误: {str(e)}"
    
    return results

def compare_html_text(main_html, current_html):
    """比较HTML正文（style外）"""
    main_soup = BeautifulSoup(main_html, 'html5lib')
    current_soup = BeautifulSoup(current_html, 'html5lib')
    
    # 移除style标签
    for style in main_soup.find_all('style'):
        style.decompose()
    for style in current_soup.find_all('style'):
        style.decompose()
    
    main_text = main_soup.get_text(strip=True)
    current_text = current_soup.get_text(strip=True)
    
    # 比较所有链接href
    main_links = [a.get('href') for a in main_soup.find_all('a', href=True)]
    current_links = [a.get('href') for a in current_soup.find_all('a', href=True)]
    
    return {
        'text_match': main_text == current_text,
        'text_diff_chars': abs(len(main_text) - len(current_text)),
        'links_match': main_links == current_links,
        'main_links': len(main_links),
        'current_links': len(current_links)
    }

def verify_template(template_path, main_blob_path=None):
    """验证单个模板"""
    print(f"\n{'='*70}")
    print(f"验证: {template_path.name}")
    print('='*70)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html5lib')
    style_tags = soup.find_all('style')
    css_text = '\n'.join(tag.string or '' for tag in style_tags)
    
    # 1. CSS解析错误
    rules, css_errors = parse_css_rules(css_text)
    if css_errors:
        print(f"❌ CSS解析错误: {len(css_errors)}")
        for err in css_errors[:3]:
            print(f"   {err}")
    else:
        print("✅ CSS解析无错误")
    
    # 2. print覆盖
    overrides = check_print_overrides(css_text)
    if overrides:
        print(f"❌ print覆盖 ({len(overrides)}):")
        for o in overrides[:5]:
            print(f"   {o}")
    else:
        print("✅ 无print字号/颜色覆盖")
    
    # 3. 整章page-break
    pb_issues = check_page_break(css_text)
    if pb_issues:
        print(f"❌ 整章分页:")
        for issue in pb_issues:
            print(f"   {issue}")
    else:
        print("✅ 无整章page-break-inside")
    
    # 4. 选择器命中
    key_selectors = ['.section-title', '.item', 'h2', '.banner', '.header']
    matches = check_selector_match(template_path, key_selectors)
    print("选择器命中:")
    for sel, count in matches.items():
        status = "✅" if isinstance(count, int) and count > 0 else "⚠️"
        print(f"  {status} {sel}: {count}")
    
    # 5. 与main对比（如果提供）
    if main_blob_path and main_blob_path.exists():
        with open(main_blob_path, 'r', encoding='utf-8') as f:
            main_html = f.read()
        
        comparison = compare_html_text(main_html, html)
        if comparison['text_match']:
            print("✅ HTML正文与main一致")
        else:
            print(f"⚠️ HTML正文差异: {comparison['text_diff_chars']} 字符")
        
        if comparison['links_match']:
            print(f"✅ 链接href与main一致 ({comparison['main_links']} 个)")
        else:
            print(f"⚠️ 链接数差异: main {comparison['main_links']}, 当前 {comparison['current_links']}")
    
    return {
        'css_errors': len(css_errors),
        'print_overrides': len(overrides),
        'page_break_issues': len(pb_issues),
        'selectors': matches
    }

def main():
    template_dir = Path(__file__).parent / 'template'
    files = sorted(template_dir.glob('*.html'))
    
    # 尝试获取main的blob（如果存在）
    main_dir = Path(__file__).parent / '.git-main-blob'
    
    all_results = {}
    for filepath in files:
        main_blob = main_dir / filepath.name if main_dir.exists() else None
        result = verify_template(filepath, main_blob)
        all_results[filepath.name] = result
    
    print(f"\n{'='*70}")
    print("汇总")
    print('='*70)
    
    for name, result in all_results.items():
        status = "✅" if (result['css_errors'] == 0 and 
                         result['print_overrides'] == 0 and 
                         result['page_break_issues'] == 0) else "⚠️"
        print(f"{status} {name}")
        if result['css_errors']:
            print(f"   CSS错误: {result['css_errors']}")
        if result['print_overrides']:
            print(f"   print覆盖: {result['print_overrides']}")
        if result['page_break_issues']:
            print(f"   整章分页: {result['page_break_issues']}")

if __name__ == '__main__':
    main()
