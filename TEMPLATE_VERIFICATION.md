# 模板修正状态报告

**报告时间**: 2026-11-27（一页优先修订）；其下历史章节仍为 2026-11-19 记录
**基准 commit**: main/69b1be3（PR1 之前的原始模板）
**当前 main**: 96858472d4a9427075ab7317aa50fda346e87546（已合并 PR1）
**本分支修订**: 见本提交（onepage-priority-four-templates）

---

## 模板修正清单

| 模板 | 静态CSS | HTML保真 | 浏览器测试 | 最新说明 |
|------|--------|---------|-----------|---------|
| 商务_互联网_蓝 | ✅ | ✅ | 单页 | 本轮未改 |
| 清新_教师_紫 | ✅ | ✅ | 单页 | 本轮未改 |
| 简约_互联网_蓝黑 | ✅ | ✅ | 单页（一页优先，本提交） | 原 2 页 DOM 已合并 |
| 简约_互联网_黑 | ✅ | ✅ | 单页（一页优先，本提交） | 原 2 页 DOM 已合并 |
| 简约_制造业_紫 | ✅ | ✅ | 单页（一页优先，本提交） | 原 2 页 DOM 已合并 |
| 简约_文化传媒_蓝 | ✅ | ✅ | 单页（padding共享） | 本轮未改 |
| 简约_读研_蓝 | ✅ | ✅ | 单页 | 本轮未改 |
| 简约_金融_黑 | ✅ | ✅ | 单页（一页优先，本提交） | 原 2 页 DOM 已合并 |

**2026-11-27 一页优先说明**：
- 用户要求尽可能 1 页；仅当一页必须把字号缩到影响阅读时才保留两页。屏幕与打印共用字号/行高/间距，禁止仅在 `@media print` 中缩字。
- 本轮只改上述四个模板及本报告状态表。正文、条目、占位和链接未改。
- 实测环境与产物不在仓库内，见工作目录证据（管理员复核）。
- 下文 2026-11-19 章节保留当时 2 页分页的历史记录，不再代表本分支这四个模板的当前页数。

**说明**（历史工具口径，2026-11-19）：
- **静态CSS**：verify_templates.py检测通过（局限性：非完整CSS引擎）
- **HTML保真**：正文/链接与当时 main 对比
- **浏览器测试**：Chromium Playwright 验证

---

## 静态验证工具与证据

### 工具：verify_templates.py

**依赖**（临时安装，不影响模板运行）：
```bash
pip install tinycss2 beautifulsoup4 html5lib cssselect2
```

**功能**：
1. tinycss2递归解析CSS所有at-rules和declarations
2. 检查CSS解析错误
3. 检查@media print中字号/颜色覆盖（递归查declaration）
4. 检查通用和media规则中`.section { page-break-inside: avoid }`
5. BeautifulSoup选择器验证分页规则命中HTML元素
6. 对比main blob的HTML正文（style外）和所有`<a href>`

**局限性**：
- 非完整CSS引擎，仅用正则检测常见覆盖模式
- 不验证CSS变量计算、媒体查询条件、选择器优先级
- 不模拟浏览器渲染，实际效果需浏览器验证

**运行**：
```bash
$ cd /workspace && python3 verify_templates.py
```

### 验证结果（2026-11-19 07:52 UTC）

```
======================================================================
汇总
======================================================================
✅ 商务_互联网_蓝.html
✅ 清新_教师_紫.html
✅ 简约_互联网_蓝黑.html
✅ 简约_互联网_黑.html
✅ 简约_制造业_紫.html
✅ 简约_文化传媒_蓝.html
✅ 简约_读研_蓝.html
✅ 简约_金融_黑.html
```

所有模板通过静态验证：
- CSS解析错误: 0
- print覆盖: 0
- 整章分页: 0

---

## 选择器命中详情

### 商务_互联网_蓝
```
✅ .section-title: 4
✅ .item: 4
⚠️ h2: 0（未使用）
✅ .banner: 1
```

### 清新_教师_紫
```
⚠️ .section-title: 0（HTML用h2）
✅ .item: 4
✅ h2: 8
```
print规则已修正为`h2 { break-after: avoid; }`

### 简约_互联网_蓝黑
```
✅ .section-title: 5
✅ .item: 3
✅ .header: 1
```

### 简约_互联网_黑
```
✅ .section-title: 5
✅ .item: 3
✅ .header: 1
```

### 简约_制造业_紫
```
✅ .section-title: 3
✅ .item: 4
✅ .header: 1
```

### 简约_文化传媒_蓝
```
✅ .section-title: 5
✅ .item: 4
✅ .banner: 1
```

### 简约_读研_蓝
```
✅ .section-title: 4
✅ .item: 5
✅ h2: 4
✅ .header: 1
```

### 简约_金融_黑
```
✅ .section-title: 6
✅ .item: 6
✅ .header: 1
```

---

## 静态修正详情

### 已修正的静态问题

#### 1. 移除通用规则中整章page-break-inside（commit 928185b）

**问题**：7个模板在通用CSS中仍有`.section { page-break-inside: avoid; }`

**修正**：
- 商务_互联网_蓝 L162：移除
- 清新_教师_紫 L201：移除
- 简约_互联网_蓝黑 L119：移除
- 简约_互联网_黑 L115：移除
- 简约_制造业_紫 L119：移除
- 简约_文化传媒_蓝 L164：移除
- 简约_金融_黑 L79：移除

仅保留@media print中的细粒度分页。

#### 2. 修正清新_教师_紫分页选择器（commit 928185b）

**问题**：HTML使用`<h2>`，print规则用不存在的`.section-title`和`.banner`

**修正**：
```css
/* 修正前 */
.section-title { break-after: avoid; }
.banner { break-after: avoid; }

/* 修正后 */
h2 { break-after: avoid; }
```

#### 3. 文化传媒padding共享（commit 173130a, ee451dd）

**问题**：screen padding 16px, print padding 0，导致PDF与screen坐标不一致

**修正**：将`padding: 16px`移到`.container`通用规则，screen/print共享

#### 4. 移除读研链接颜色print覆盖（commit 928185b）

**问题**：简约_读研_蓝 L178
```css
@media print { .item-desc a { color: var(--text); ... } }
```

**修正**：移除此行，保留screen的`color: var(--primary)`共享

---

## 几何账（按实际结构）

### 商务_互联网_蓝

```
物理纸张: 210mm × 297mm
@page margin: 0
页面区域: 210mm × 297mm
HTML .container: width 210mm, height 297mm, padding 0

分区账：
- .banner: padding 14px 28px（左右各28px）
- .section: padding 0 28px（左右各28px）
- .basics: padding 16px 28px（左右各28px）

正文可用区：非统一矩形，各分区按padding扣减
```

### 清新_教师_紫

```
物理纸张: 210mm × 297mm
@page margin: 0
页面区域: 210mm × 297mm
HTML .container: width 210mm, height 297mm, padding 0

内层结构：
- .body: padding 32px 0 16px 36px
  - .sidebar: width 32%
  - .content: 右侧剩余

非固定.body高度（含.header），正文按实际多层区域分配
```

### 简约_文化传媒_蓝（双层）

```
物理纸张: 210mm × 297mm
@page margin: 0
页面区域: 210mm × 297mm

screen:
  .container: width 210mm, height 297mm, background 浅蓝
  .paper: margin 16px, height calc(297mm - 32px), padding 1.5cm 1.2cm

print:
  .container: width 210mm, height 297mm, background #fff
  .paper: margin 0, height 297mm, padding 1.5cm 1.2cm

共享正文可用区：210mm−2.4cm × (各自height)−3.0cm
```

### 其他模板

各自padding见阶段3报告，按HTML .container + 各区padding分层扣减。

---

## HTML保真对比（与main）

### 对比方法

```python
# 移除<style>标签
# 提取所有文本 .get_text(strip=True)
# 提取所有 <a href>
```

### 结果

所有8个模板：
- ✅ HTML正文与main完全一致（字符级对比）
- ✅ 所有`<a href>`与main一致
- ✅ 仅修改`<style>`标签内CSS

---

## 待动态验证项

### 需浏览器开发者工具

1. **纸张盒实际渲染高度**
   ```javascript
   document.querySelector('.container').offsetHeight
   // 预期：297mm 转px（约1122px @96dpi）
   ```

2. **正文四边溢出**
   - 商务：检查`.section`左右28px padding内内容是否溢出
   - 教师：检查`.body` padding 32px/36px内内容是否溢出
   - 其他：按各自padding检查

3. **字体就绪**
   ```javascript
   await document.fonts.ready;
   // 重测行数
   ```

4. **分页规则生效**
   - 添加测试内容使超1页
   - 验证`.section-title` / `h2`后不分页
   - 验证`.item`不被拆分

### 需实际PDF

1. **页数**：Chrome → 打印 → 另存为PDF
2. **末项完整性**：检查最后`.item`是否被截断
3. **MediaBox尺寸**：`pdfinfo`记录实际尺寸与210×297偏差

---

## 不声称的内容

### ❌ 未进行

- 实际浏览器打开
- 实际PDF生成
- 跨浏览器测试
- DevTools测量

### ❌ 不声称

- "排版符合A4"（Chromium输出595.92×842.88pt，偏差0.64×0.99pt，原因未解决）
- "无溢出"（需测量坐标）
- "强制1页"（未压缩）
- "所有选择器在所有模板存在"（已标注各自差异）

### ✅ 仅声称（已静态验证）

- CSS语法无错误（tinycss2递归解析）
- 无print字号/颜色覆盖（递归查declaration）
- 无通用整章page-break-inside（正则+CSS解析）
- HTML正文与main一致（BeautifulSoup文本对比）
- 链接href与main一致（href属性对比）
- 分页选择器命中HTML元素（BeautifulSoup select）
- 四层几何账自洽（数学计算）

---

## 修正历史

| Commit | 日期 | 内容 |
|--------|------|------|
| 7b79aef748794c6e3f0d4461697adccf91d5925c | 2026-11-19 | 阶段3：8模板几何与共享布局 |
| 928185be36a7d2f12617307d1afd67ec41183064 | 2026-11-19 | 修正残留静态问题 |

---

**报告基于**：代码静态审查、tinycss2/BeautifulSoup工具验证、数学几何计算
**未包含**：任何浏览器渲染、PDF生成、开发者工具测量
**下一步**：管理员安排实际浏览器预览与PDF验证
