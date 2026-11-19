# 模板修正状态报告

## 当前状态概要

**基准 commit**: 06f9fa8 (docs: 添加模板验证报告，已过时)
**当前 HEAD**: 7b79aef (fix: 阶段 3 - 修正 8 模板 A4 几何与共享布局)

8 个模板已完成静态 CSS 结构修正，通过静态几何账验证。待动态验证（需浏览器/PDF）。

---

## 模板修正清单

| 模板 | 静态几何 | CSS 结构 | 占位保留 | 共享布局 | 待动态验证 |
|------|---------|---------|---------|---------|-----------|
| 商务_互联网_蓝 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 简约_互联网_黑 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 简约_金融_黑 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 简约_互联网_蓝黑 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 简约_制造业_紫 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 清新_教师_紫 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 简约_读研_蓝 | ✅ | ✅ | ✅ | ✅ | 浏览器测量 |
| 简约_文化传媒_蓝 | ✅ | ✅ | ✅ | ✅ | 浏览器测量+双层 |

**说明**：
- **静态几何**：@page margin 0, HTML 盒 210×297mm, padding 分层账正确
- **CSS 结构**：大括号配对，@media 块完整，选择器有效
- **占位保留**："姓  名", "+86 XXX", "教育背景", "工作经历"等占位文字保留
- **共享布局**：screen/print 共享字体字号行高间距，screen 装饰用 outline（不占空间）
- **待动态验证**：需浏览器开发者工具测量实际高度、溢出、PDF 页数

---

## 静态修正详情

### 统一几何策略

所有模板采用统一分层账：

```
物理纸张: 210mm × 297mm（A4 标准）
@page margin: 0（统一）
页面区域: 210mm × 297mm
HTML 纸张盒: width: 210mm, height: 297mm（固定，非 min-height）
正文可用区: 210mm × 297mm − padding（各模板保留原设计）
```

### 各模板 padding（保留原 screen 设计）

| 模板 | padding |
|------|---------|
| 商务_互联网_蓝 | 0 |
| 简约_互联网_黑 | 1.4cm 1.2cm |
| 简约_金融_黑 | 1.5cm 1.2cm |
| 简约_互联网_蓝黑 | 0.9cm 0.9cm |
| 简约_制造业_紫 | 1.5cm 1.2cm |
| 清新_教师_紫 | 0（内层 .body 控制） |
| 简约_读研_蓝 | 0.75cm 0.8cm |
| 简约_文化传媒_蓝 | .paper 1.5cm 1.2cm（双层） |

### 特殊处理

#### 简约_互联网_蓝黑
- **原问题**：@media print 有 30+ 行密集压缩（body 12px/1.3, 所有元素缩小）
- **修正**：移除全部 print 压缩，保留 screen 设计（14px/1.55）
- **原因**：违反共享布局原则，不能"全端照搬最紧压缩"

#### 清新_教师_紫
- **原问题**：overflow: hidden（掩盖溢出）
- **修正**：改为 overflow: visible
- **特点**：无 container padding，内层 .body 控制间距

#### 简约_文化传媒_蓝
- **特点**：双层结构
  - .container: 210×297mm, 浅蓝背景
  - .paper: margin 16px, 圆角 18px, padding 1.5cm 1.2cm
  - .paper min-height: calc(297mm - 32px)
- print 移除装饰：background #fff, border-radius 0, margin 0

---

## 分页规则

所有模板统一使用细粒度分页：

```css
@media print {
  .section-title { break-after: avoid; }  /* 标题后不分页 */
  .item { break-inside: avoid; }          /* 条目内不分页 */
  .header { break-after: avoid; }         /* 头部后不分页 */
  .banner { break-after: avoid; }         /* Banner 后不分页 */
}
```

**移除**：`.section { page-break-inside: avoid; }`（整章禁止分页）

**注意**：选择器 `.section-title`, `.item` 需在实际 HTML 中存在，动态验证时需确认。

---

## 外装饰处理

### screen（保留视觉边框）
```css
@media screen {
  .container {
    outline: 1.5px solid #555;     /* 不占空间 */
    box-shadow: 0 0 12px rgba(0,0,0,0.25);
  }
}
```

### print（移除）
```css
@media print {
  .container {
    outline: none;
    box-shadow: none;
  }
}
```

---

## 静态验证结果

### ✅ 已完成

1. **git diff --check**
   ```bash
   $ git diff --check
   # 无输出，通过
   ```

2. **占位文字保留**
   ```bash
   $ grep -c "姓  名\|+86 XXX\|教育背景\|工作经历" template/*.html
   商务_互联网_蓝: 2
   清新_教师_紫: 1
   简约_互联网_蓝黑: 2
   简约_互联网_黑: 2
   简约_制造业_紫: 2
   简约_文化传媒_蓝: 2
   简约_读研_蓝: 2
   简约_金融_黑: 4
   ```

3. **HTML 正文未修改**
   - 仅修改 `<style>` 标签内 CSS
   - 所有 HTML body 内容保持不变

4. **CSS 变量保留**
   - 所有 `:root` 颜色变量保持原设计
   - 未统一颜色/字号/间距

5. **四层几何账自洽**
   - 所有模板：HTML 盒 210×297 ≤ 页面区域 210×297
   - padding 值各不相同，保留原设计
   - 无重复扣减

---

## 待动态验证项

### 需浏览器开发者工具

1. **纸张盒实际高度**
   - 测量 `.container` 实际渲染高度是否为 297mm
   - 方法：开发者工具 → Elements → Computed → height

2. **正文四边溢出**
   - 测量末项元素 bottom 坐标
   - 对比 `.container` height - padding-bottom
   - 检查左右列表标记是否侵入

3. **字体就绪**
   - 等待 `document.fonts.ready`
   - 重测行数是否变化

4. **分页选择器命中**
   - 确认 `.section-title` 存在于 HTML
   - 确认 `.item` 存在于 HTML
   - 验证 `break-after` / `break-inside` 生效

### 需实际 PDF

1. **页数**
   - Chrome → 打印 → 另存为 PDF
   - 检查实际页数

2. **末项完整性**
   - 在 PDF 中检查最后一项是否被截断

3. **MediaBox 尺寸**
   - 用 PDF 工具检查实际 MediaBox
   - 记录与 210×297mm 的偏差

---

## 不声称的内容

### ❌ 未进行

- 实际浏览器打开
- 实际 PDF 生成
- 跨浏览器测试
- 不同操作系统测试

### ❌ 不声称

- "排版精确 A4"（需实测）
- "无溢出"（需测量）
- "强制 1 页"（未统一压缩）
- "所有选择器命中"（需 HTML 确认）

---

## 与原 main 的对比

### main (69b1be3) 问题

1. 所有模板 `.container` 用 `min-height: 29.7cm`（可撑高）
2. 7 个模板 @page margin 非零 + 完整 210×297 盒（超页面区域）
3. 部分模板 @media print 有字号/间距覆盖（违反共享布局）
4. 所有模板用 `border: 1.5px`（占空间，border-box 下扣正文）
5. 整章禁止分页：`.section { page-break-inside: avoid; }`

### 当前分支修正

1. 改为固定 `height: 297mm`
2. 统一 @page margin 0，HTML 盒 210×297
3. 移除 print 字号/间距覆盖（除简约_互联网_蓝黑全移除）
4. 改用 `outline: 1.5px`（不占空间）
5. 细粒度分页：`.section-title`, `.item`

---

## 诚实声明

### 本报告基于

- 代码静态审查
- CSS 规则逻辑推理
- 几何账数学计算

### 未包含

- 任何浏览器渲染
- 任何 PDF 生成
- 任何开发者工具测量
- 任何实际溢出检测

### 下一步

**管理员安排**：实际浏览器预览与 PDF 验证

---

**报告更新**: 2026-11-19 阶段 3 完成
**基准**: main 69b1be3
**当前**: 7b79aef
