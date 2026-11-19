#!/usr/bin/env python3
"""可靠的模板CSS和HTML验证
运行: cd /workspace && python3 verify_templates.py
依赖: pip install tinycss2 beautifulsoup4 html5lib
"""
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import tinycss2

def parse_css_rules(css_text):
    """递归解析CSS所有规则"""
    tokens = tinycss2.parse_stylesheet(css_text, skip_comments=False, skip_whitespace=True)
    errors = []
    rules = {'at_rules': {}, 'normal': [], 'all_declarations': []}
    
    def extract_declarations(content):
        """递归提取所有声明"""
        decls = []
        for item in content:
            if hasattr(item, 'type'):
                if item.type == 'declaration':
                    decls.append({
                        'property': item.lower_name,
                        'value': tinycss2.serialize(item.value).strip()
                    })
                elif item.type == 'at-rule' and hasattr(item, 'content'):
                    decls.extend(extract_declarations(item.content))
                elif item.type == 'qualified-rule' and hasattr(item, 'content'):
                    decls.extend(extract_declarations(item.content))
        return decls
    
    for token in tokens:
        if token.type == 'error':
            errors.append(f"CSS解析错误: {token}")
        elif token.type == 'at-rule':
            rule_name = token.lower_at_keyword
            if rule_name not in rules['at_rules']:
                rules['at_rules'][rule_name] = []
            rules['at_rules'][rule_name].append(token)
            # 递归提取声明
            if hasattr(token, 'content'):
                rules['all_declarations'].extend(extract_declarations(token.content))
        elif token.type == 'qualified-rule':
            rules['normal'].append(token)
            if hasattr(token, 'content'):
                rules['all_declarations'].extend(extract_declarations(token.content))
    
    return rules, errors

def check_geometry_overrides(css_text):
    """检查print中width/height/padding/margin覆盖"""
    rules, _ = parse_css_rules(css_text)
    overrides = []
    
    if 'media' in rules['at_rules']:
        for media_rule in rules['at_rules']['media']:
            prelude = tinycss2.serialize(media_rule.prelude)
            if 'print' in prelude:
                content = tinycss2.serialize(media_rule.content) if hasattr(media_rule, 'content') else ''
                # 检查关键几何属性
                geometry_props = ['width', 'height', 'padding', 'margin']
                for prop in geometry_props:
                    # 排除伪元素和特定前缀
                    if re.search(rf'(?<!min-|max-){prop}\s*:', content):
                        matches = re.finditer(rf'([.#\w-]+)\s*{{[^}}]*(?<!min-|max-){prop}\s*:[^}}]*}}', content)
                        for m in matches:
                            selector = m.group(1)
                            # 已知必要例外: 重置body/html, container/paper几何
                            if selector not in ['.container', '.paper', 'body', 'html']:
                                overrides.append(f"print中{prop}覆盖: {selector}")
    
    return overrides

def check_print_overrides(css_text):
    """检查print中字号/颜色覆盖"""
    rules, _ = parse_css_rules(css_text)
    overrides = []
    
    if 'media' in rules['at_rules']:
        for media_rule in rules['at_rules']['media']:
            prelude = tinycss2.serialize(media_rule.prelude)
            if 'print' in prelude:
                content = tinycss2.serialize(media_rule.content) if hasattr(media_rule, 'content') else ''
                # font-size
                if re.search(r'font-size\s*:', content):
                    matches = re.finditer(r'([.#\w-]+)\s*\{[^}]*font-size\s*:[^}]*\}', content)
                    for m in matches:
                        overrides.append(f"print字号: {m.group(1)}")
                # color (非border-color)
                if re.search(r'(?<!border-)(?<!outline-)color\s*:', content):
                    matches = re.finditer(r'([.#\w-]+)\s*\{[^}]*(?<!border-)(?<!outline-)color\s*:[^}]*\}', content)
                    for m in matches:
                        overrides.append(f"print颜色: {m.group(1)}")
    
    return overrides

def check_page_break(css_text):
    """检查整章page-break-inside"""
    issues = []
    if re.search(r'\.section\s*\{[^}]*page-break-inside\s*:\s*avoid', css_text):
        issues.append("存在 .section { page-break-inside: avoid }")
    return issues

def check_selector_match(html_path, selectors):
    """检查选择器是否命中HTML元素"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html5lib')
    results = {}
    
    for selector in selectors:
        try:
            matches = soup.select(selector)
            results[selector] = len(matches)
        except Exception as e:
            results[selector] = f"错误: {str(e)}"
    
    return results

def compare_html_with_main(template_path):
    """对比HTML与main的正文"""
    # 从git获取main版本
    import subprocess
    try:
        main_html = subprocess.check_output(
            ['git', 'show', f'main:{template_path}'],
            cwd=template_path.parent.parent,
            stderr=subprocess.DEVNULL
        ).decode('utf-8')
    except:
        return {'available': False}
    
    with open(template_path, 'r', encoding='utf-8') as f:
        current_html = f.read()
    
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
    
    # 比较class属性
    main_classes = set()
    current_classes = set()
    for tag in main_soup.find_all(True):
        if tag.get('class'):
            main_classes.update(tag['class'])
    for tag in current_soup.find_all(True):
        if tag.get('class'):
            current_classes.update(tag['class'])
    
    return {
        'available': True,
        'text_match': main_text == current_text,
        'text_diff_chars': abs(len(main_text) - len(current_text)),
        'links_match': main_links == current_links,
        'main_links': len(main_links),
        'current_links': len(current_links),
        'classes_match': main_classes == current_classes,
        'classes_diff': current_classes - main_classes
    }

def verify_template(template_path):
    """验证单个模板"""
    print(f"\n{'='*70}")
    print(f"验证: {template_path.name}")
    print('='*70)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html5lib')
    style_tags = soup.find_all('style')
    css_text = '\n'.join(tag.string or '' for tag in style_tags)
    
    issues = []
    
    # 1. CSS解析错误
    rules, css_errors = parse_css_rules(css_text)
    if css_errors:
        print(f"❌ CSS解析错误: {len(css_errors)}")
        issues.append('CSS解析错误')
    else:
        print("✅ CSS解析无错误")
    
    # 2. print几何覆盖
    geom_overrides = check_geometry_overrides(css_text)
    if geom_overrides:
        print(f"⚠️ print几何覆盖 ({len(geom_overrides)}):")
        for o in geom_overrides[:3]:
            print(f"   {o}")
        issues.append('print几何覆盖')
    else:
        print("✅ 无print几何覆盖")
    
    # 3. print字号/颜色覆盖
    overrides = check_print_overrides(css_text)
    if overrides:
        print(f"❌ print样式覆盖 ({len(overrides)}):")
        for o in overrides[:3]:
            print(f"   {o}")
        issues.append('print样式覆盖')
    else:
        print("✅ 无print字号/颜色覆盖")
    
    # 4. 整章page-break
    pb_issues = check_page_break(css_text)
    if pb_issues:
        print(f"❌ 整章分页:")
        for issue in pb_issues:
            print(f"   {issue}")
        issues.append('整章分页')
    else:
        print("✅ 无整章page-break-inside")
    
    # 5. 选择器命中
    key_selectors = ['.section-title', '.item', 'h2', '.banner', '.header']
    matches = check_selector_match(template_path, key_selectors)
    print("选择器命中:")
    has_paging = False
    for sel in ['.section-title', 'h2', '.item']:
        count = matches.get(sel, 0)
        if isinstance(count, int) and count > 0:
            has_paging = True
            print(f"  ✅ {sel}: {count}")
        elif sel in matches:
            print(f"  ⚠️ {sel}: {matches[sel]}")
    
    if not has_paging:
        print("  ⚠️ 警告: 未找到分页标题选择器")
        issues.append('分页选择器')
    
    # 6. 与main对比
    comparison = compare_html_with_main(template_path)
    if comparison['available']:
        if comparison['text_match']:
            print("✅ HTML正文与main一致")
        else:
            print(f"❌ HTML正文差异: {comparison['text_diff_chars']} 字符")
            issues.append('HTML差异')
        
        if comparison['links_match']:
            print(f"✅ 链接与main一致 ({comparison['main_links']} 个)")
        else:
            print(f"⚠️ 链接数: main {comparison['main_links']}, 当前 {comparison['current_links']}")
        
        if not comparison['classes_match'] and comparison['classes_diff']:
            print(f"⚠️ 新增class: {comparison['classes_diff']}")
    else:
        print("⚠️ 无法获取main版本对比")
        issues.append('无main基准')
    
    return {
        'passed': len(issues) == 0,
        'issues': issues,
        'selectors': matches
    }

def main():
    script_dir = Path(__file__).parent
    template_dir = script_dir / 'template'
    
    if not template_dir.exists():
        print(f"错误: {template_dir} 不存在")
        print("请从仓库根目录运行: python3 verify_templates.py")
        return 1
    
    files = sorted(template_dir.glob('*.html'))
    
    all_results = {}
    for filepath in files:
        result = verify_template(filepath)
        all_results[filepath.name] = result
    
    print(f"\n{'='*70}")
    print("汇总")
    print('='*70)
    
    passed = 0
    for name, result in all_results.items():
        status = "✅" if result['passed'] else "⚠️"
        print(f"{status} {name}")
        if result['issues']:
            print(f"   问题: {', '.join(result['issues'])}")
        passed += 1 if result['passed'] else 0
    
    print(f"\n通过: {passed}/{len(all_results)}")
    
    return 0 if passed == len(all_results) else 1

if __name__ == '__main__':
    sys.exit(main())
