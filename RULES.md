# RULES.md — 简历美化工作区强制规则

> 本文件优先级**高于** `CLAUDE.md` 与任何 skill 默认行为。
> 违反本文件中任何一条规则都属于操作失误，需立即修正。

---

## 1. 目录规则

### 1.1 `source/` — 用户源文件（只读）

- **禁止**对 `source/` 内的任何文件进行写入、修改、删除、重命名
- 读取后不得将源文件内容原样写回（即使是「轻微格式化」也不允许）
- 源文件的所有信息抽取都应在内存中完成，或复制到 `temp/` 下处理

### 1.2 `template/` — 模板库

- 只存放**可复用的 HTML 模板**
- 命名规范：**`{风格}_{行业}_{主色调}.html`**
  - 风格示例：`简约` / `清新` / `卡通` / `中式`
  - 行业示例：`互联网` / `金融` / `文化传媒` / `汽车` / `教育培训` / `制造业`
  - 主色调示例：`黑` / `紫` / `蓝` / `灰` / `白` / `青` / `绿` / `黄` / `橙` / `品红` / `红`
  - 完整示例：`简约_金融_黑.html`、`清新_互联网_蓝.html`、`中式_教育_红.html`
- 同一「风格 × 行业 × 主色调」组合只保留一份最新模板；旧版本需删除（不留版本号后缀）
- 模板中**禁止**填入真实个人信息（姓名、电话、邮箱等）

### 1.2.1 模板占位符约定（强制）

`template/` 下所有模板在数据填入位**必须**使用全角占位符，目的是「一眼能看出是占位」「搜索不到真人真事」，保证模板可复用、可公开。

| 类别 | 占位符 | 说明 |
|---|---|---|
| 姓名 | `姓  名` | 两字之间两个全角空格，与真实 2-3 字姓名等宽 |
| 电话 | `+86 XXX XXXX XXXX` | 11 位用 X 顶替 |
| 邮箱 | `name@example.com` | 标准 example 域 |
| GitHub / 博客 | `github.com/your-name` | handle 用 your-name |
| 学校 | `某某大学` | 不用真实校名（如「天津科技大学」） |
| 专业 / 方向 | `某某专业（某某方向）` | 包含「专业 + 方向」结构 |
| 学校层次 | `某某层次/荣誉` | 如「985 / 双一流 / 省重点」 |
| 奖项 | `XXX 一等奖(XXXX)` | 比赛名 / 等级 / 年份都用 X |
| 公司 | `某某公司` | 不用真实公司名（如「字节跳动」） |
| 品牌 / 项目名 | `xx活动`、`xx项目` | 统一用小写 xx 开头 |
| 日期 | `XXXX.XX - XXXX.XX`、`XXXX` | 年月日全用 X |

**禁止**：

- ❌ 真实存在的大学名、公司名、奖项名（即使加引号或注脚）
- ❌ 半虚构信息（如「清华某学院」「某 985 院校」）——必须让人一眼看出是占位
- ❌ 用真实人名（即使是历史人物、明星、虚构角色）做示例
- ❌ 留电话号码、邮箱后缀带真实特征的占位（如 `13800000000`、`zhangsan@`）

### 1.3 `temp/` — 中间产物

- 每个处理任务**必须**新建一个独立子目录
- 命名格式：**`YYYY-MM-DD-HH-MM`**（年月日时分，共 12 个数字 + 4 个连字符）
  - 示例：`2026-06-19-14-30`
- 子目录下可自由组织 HTML / CSS / 截图 / 草稿
- **允许**在 `draft.html` 末尾内联拖拽脚本（vanilla JS，详见 §8），让用户能在浏览器里自调排版
- **禁止**引用外部 JS / CDN / Web 字体（拖拽脚本必须自包含）
- 任务完成后**不强制**清理（用户可手动决定），但不应在 `temp/` 下出现「看起来像最终成品」的文件

### 1.4 `prospect/` — 最终输出

- **只**存放最终交付的 HTML 文件
- 文件名建议与简历所属人/岗位相关，例：`张三_硬件工程师_简历.html`
- 一份最终交付**对应一份** HTML，**禁止**存放中间过程文件
- 不存 PDF（PDF 由用户自行从 HTML 导出）

### 1.5 `.claude/skills/` — 技能

- 仅放已安装、已验证可用的 skill
- 不要在 `skills/` 下存放个人数据或草稿

### 1.6 模板结构规范（强制）

所有写入 `template/*.html` 的模板**必须**包含以下 A 类基础设施。缺一项视为不合格。

#### 1.6.1 `:root` CSS 变量
模板必须以 `:root` 定义主题色变量，**变量名固定**，值随风格/主色调调整：
```css
:root {
  --primary: <主色调>;
  --text:    <正文色>;
  --muted:   <次要色>;
  --divider: <分隔线色>;
  --bg:      #ffffff;
  --paper:   #ffffff;
}
```

#### 1.6.2 `@page` 规则
A4 打印固定写法：
```css
@page { size: A4; margin: 1.5cm 1.2cm; }
```

#### 1.6.3 盒模型重置
```css
* { box-sizing: border-box; margin: 0; padding: 0; }
```

#### 1.6.4 字体栈（**值固定**）
```css
font-family: "思源黑体", "Microsoft YaHei", "微软雅黑",
             -apple-system, BlinkMacSystemFont, "Segoe UI",
             "PingFang SC", "Hiragino Sans GB",
             "Helvetica Neue", Arial, sans-serif;
```

#### 1.6.5 字体平滑
```css
-webkit-font-smoothing: antialiased;
```

#### 1.6.6 屏幕 A4 模拟（`@media screen`）
`.container` 必须有 21cm × 29.7cm + 物理边线 + 阴影：
```css
@media screen {
  html { background: #888; }
  body { background: #888; padding: 20px; }
  .container {
    width: 21cm;
    min-height: 29.7cm;
    padding: 1.5cm 1.2cm;
    background: var(--paper);
    border: 1.5px solid #555;
    box-shadow: 0 0 12px rgba(0,0,0,0.25);
    margin: 0 auto;
  }
}
```

#### 1.6.7 打印微调（`@media print`）
```css
@media print {
  body { font-size: 12.5px; background: #fff; padding: 0; }
  .section { page-break-inside: avoid; }
}
```

#### 1.6.8 无外部资源
- **禁止**引入 Web 字体 / CDN / 远程图片 / 外部 JS
- 所有 CSS 内联或 `<style>` 内嵌
- 字体走系统字体栈（见 1.6.4）

#### 1.6.9 Markdown 标签的样式占位（强制）

当源文件含 Markdown 语法（`**加粗**`、`*斜体*`、`` `代码` ``、`[链接](url)`、`> 引用`），生成的 HTML **必须**使用语义化标签并提供对应样式。语义标签对无障碍阅读、PDF 文字提取、未来重构都更友好。

| Markdown 语法 | HTML 标签 | 模板 CSS 最低要求 |
|---|---|---|
| `**bold**` | `<strong>` | `font-weight: 700` |
| `*italic*` | `<em>` | `font-style: italic` |
| `***both***` | `<strong><em>` | 两者组合 |
| `` `code` `` | `<code>` | 等宽字体 + 浅灰底（`background: var(--tag-bg)`） |
| `[text](url)` | `<a href="...">` | 颜色与主色协调，下划线可选 |
| `> quote` | `<blockquote>` | 左竖条 + 内缩（`border-left + padding-left`） |

**禁止**：

- ❌ 用纯样式标签（`<b>`、`<i>`、`<u>`）代替语义标签（`<strong>`、`<em>`、`<a>`）
- ❌ 把 `<strong>` 默认色设成主色（会与章节标题抢眼，干扰视觉层级）——用 `var(--text)` 即可
- ❌ 链接无 hover / 打印样式 ——打印 PDF 时链接应是可点击的深色或带下划线
- ❌ 标签样式脱离 §1.6.1 的 CSS 变量（导致主题切换不生效）

### 1.7 灵活项（**不强制**）
以下设计维度由模板作者自由发挥，不作硬性要求：
- 主色调具体值
- 头部 banner 形状（矩形 / 长条 / 无 / 照片位）
- 联系信息布局（列数、是否带图标、是否在 banner 内）
- 章节标题样式（横线 / 虚线 / 点线 / 颜色 / 是否带星标）
- 项目符号（`●` / `▸` / `▻` / 自定义字符 / SVG）
- 字体大小、行距、间距、圆角等具体值
- 是否放照片、照片位置与尺寸
- 条目结构（`.item-head` 三段式 / 单段式 / 其他），列表符号、章节是否分页保护等

### 1.8 字号建议（半强制）

`body` 字号（含 print 模式）应落在下列推荐范围。模板可选用推荐值，也可在范围内自由取值；超出范围需在版本说明中说明理由。

| 元素 | 容差范围 | 推荐值 |
|---|---|---|
| `body`（屏幕） | `14px – 16px` | `15px` |
| `@media print` 中 `body` | `13.5px – 15px` | `14.5px` |

> 章节标题、联系项、姓名、图标、列表符号等其它层级仍归 §1.7 灵活项。

---

## 2. 文件格式规则

- **输入**：可以是 Markdown 或 HTML，最终处理时统一转为 HTML
- **输出**：**纯 HTML 单文件**（CSS 内联或 `<style>` 内嵌），方便浏览器打印
- HTML 必须包含**打印优化**：
  - `@page { size: A4; margin: 1.5cm 1.2cm; }`（或合理值）
  - 关键分页控制：`page-break-inside: avoid` 用在工作经历等不可拆分的块
  - 字体大小、间距针对打印优化（非屏幕显示）
- 避免使用：外部 CDN、JS 框架、Web 字体在线加载
- 优先使用：系统字体栈（`-apple-system, "PingFang SC", "Microsoft YaHei", ...`）

---

## 3. 工作流规则

### 3.1 标准流程

```
source/<某简历>     → 解析/抽取
template/<某模板>   → 复制到 temp
temp/<时间戳>/draft.html → 填充、排版、迭代
prospect/<最终命名>  → 交付
```

### 3.2 操作顺序

1. **先**读源文件、抽信息
2. **再**选模板（若无匹配，按需新建并放入 `template/`）
3. **然后**在 `temp/<时间戳>/` 下完成所有中间处理：
   - 复制模板 → `temp/<时间戳>/draft.html`
   - 填充个人数据
   - **嵌入拖拽脚本**（`</body>` 前，详见 §8）
4. **用户自调**：用户在自己浏览器里打开 `draft.html`，拖动 + 改字 → 点「导出调整参数」→ 粘 JSON 给 Claude
5. **Claude 应用**：Claude 读 JSON 改 `draft.html`（合并 style + 替换 text），写回原文件
6. **最后**才把成品 `cp` 到 `prospect/<姓名>_<岗位>_简历.html`

### 3.3 禁止的捷径

- ❌ 直接把成品写在 `temp/` 里就算交付
- ❌ 直接修改 `source/` 内文件以「修正格式」
- ❌ 把最终 HTML 命名为 `final.html` / `output.html` 等无意义名字放进 `prospect/`
- ❌ 在 `template/` 里留带个人信息的「示例」

---

## 4. 多轮确认流程（强制）

整个简历美化过程**必须**经过以下 4 轮确认。每轮都使用 `AskUserQuestion` 提供选项 + 默认项，禁止跳过。

### 4.1 第一轮：风格与行业（任务启动时）

向用户确认以下 5 项（每项用 `AskUserQuestion` 单独提问，提供默认项 + 备选项）：

| 项 | 默认项 | 备选项 |
|---|---|---|
| 行业 | 无固定默认（必选，不做推断） | 互联网 / 金融 / 文化传媒 / 汽车 / 教育培训 / 制造业 |
| 风格 | 简约 | 简约 / 清新 / 卡通 / 中式 |
| 主色调 | 蓝 (#2563eb) | 黑 (#000000) / 紫 (#6b21a8) / 蓝 (#2563eb) / 灰 (#6b7280) / 白 (#ffffff) / 青 (#06b6d4) / 绿 (#10b981) / 黄 (#eab308) / 橙 (#f97316) / 品红 (#ec4899) / 红 (#ef4444) |
| 布局 | 单页 | 单页 / 左右 |
| 目标页数 | 1 页 | 1 页 / 2 页 / 不限 |

> 行业**无固定默认**——第一轮必须由用户显式从备选项中选一个，禁止用 source 文件名/正文做自动推断。
> 主色调 hex 值仅为建议参考，用户可在「其他」中指定任意 hex。

### 4.2 第二轮：模板与字段（处理前）

向用户展示：

1. **抽出的字段清单**（姓名、教育经历、工作经历…）— 询问是否有遗漏/错误
2. **候选模板**（从 `template/` 匹配「风格 × 行业 × 主色调」）：
   - 若命中 → 列出模板文件路径
   - 若未命中 → 说明要新建，并给出新建方案的草图描述
3. **`temp/` 目录名**（按当前时间生成）— 告知用户即将创建

> 在用户明确确认前，**不**写入任何 `temp/<时间戳>/` 下的文件。

### 4.3 第三轮：用户自调（核心步骤）

第三轮是**用户主导**的调整阶段，不再是 Claude 改、用户看。流程：

1. Claude 在 `temp/<时间戳>/draft.html` 末尾嵌入拖拽脚本（§8），告知用户文件路径
2. 用户在浏览器打开该文件，自行：
   - 拖动元素调整 margin（移动 > 5px 触发）
   - 双击文字直接编辑（contenteditable）
   - 拖回原位 / 改回原文的条目自动从 localStorage 清除
3. 调完点「📋 导出调整参数」按钮（或按 `C`）：
   - 浏览器支持 clipboard API → 直接复制到剪贴板
   - `file://` 下大多被禁 → 弹模态框，JSON 自动全选，用户 `Ctrl/Cmd+C`
4. 用户把 JSON 粘到对话里给 Claude
5. Claude 读 JSON，按 `selector` 找到原 `draft.html` 里的元素：
   - `style` 字段：合并到元素的 `style` 属性（`margin-left` / `margin-top`）
   - `text` 字段：把 `old` 文本替换为 `new`
6. Claude 把改后的 `draft.html` 路径告知用户，让用户最终确认排版/文字 OK
7. 用户明确同意后，进入第 4 轮

> 关键：第三轮不是「Claude 问、用户答」，而是「用户自己动手、JSON 给 Claude 应用」。Claude 在这一步**不要**主动改 HTML 内容，只读 JSON 应用。

### 4.4 第四轮：交付前确认（写入 prospect/ 前）

向用户展示：

1. 最终 HTML 在 `temp/<时间戳>/` 下的路径
2. 即将写入 `prospect/` 的**目标文件名**（与用户确认）
3. 是否需要：
   - 保留 `temp/` 下的草稿 / 立即清理
   - 同步在 `template/` 沉淀新模板（若本任务新建了模板）

> 用户明确同意后，**才**执行复制/移动到 `prospect/`。

### 4.5 确认的形式要求

- 每次确认使用 `AskUserQuestion` 工具，**禁止**用纯文字叙述让用户回复
- 每个问题提供 2-4 个选项 + 默认项置顶并标注「（推荐）」
- 用户回复「默认」/「都按推荐」时，按默认项全部执行
- 关键确认（第 4 轮交付前）即使默认也必须显式问一次

---

## 5. 命名一致性

- 文件名、目录名使用中文/英文均可，但**全工作区风格应统一**
- 时间戳目录**严格**按 `YYYY-MM-DD-HH-MM` 格式，禁止出现 `2026-6-4-14-30` 这种省略前导零的写法

---

## 6. 变更与回滚

- 修改 `template/` 下的模板：需先复制到 `temp/<时间戳>/` 验证，确认无误后再回写到 `template/`，同时**删除旧版本**
- `prospect/` 下的历史交付**不删除**（用户可能需要回看），如需替换，使用更明确的新文件名

---

## 7. 预览方式（强制）

- **禁止**用 `python -m http.server`、`npx serve`、`npx http-server` 等方式起本地服务
- 静态 HTML 全部用 `file://` 协议在浏览器中直接打开
- 打开方式（Git Bash on Windows）：
  ```bash
  start "C:\绝对\路径\file.html"
  ```
  或在文件资源管理器中双击 HTML 文件
- 若确有跨域 / 模块化需求必须起服务，需**先**得到用户授权，**且**必须在任务结束时显式 kill 服务进程，命令示例：
  ```bash
  # 启动前记录 PID
  python -m http.server 8000 & echo $! > .server.pid
  # 任务结束
  kill $(cat .server.pid) 2>/dev/null && rm .server.pid
  ```
  PID 文件统一放在对应 `temp/<时间戳>/` 下，不污染根目录

---

## 8. temp 拖拽脚本与 JSON 格式（强制）

temp 目录下的 `draft.html` 末尾允许内联一段纯 vanilla JS 拖拽脚本，**让用户能在浏览器里自调排版**。`template/` 和 `prospect/` **禁止**含此脚本。

### 8.1 脚本位置与依赖

- 位置：`temp/<时间戳>/draft.html` 的 `</body>` 之前
- 依赖：**无外部依赖**。禁止引入 CDN / Web 字体 / 远程 JS
- 框架：**纯 vanilla JS**（不引入 jQuery / React / Vue 等）
- 大小：≈ 600 行（含注释）

### 8.2 行为规范

| 项 | 规则 |
|---|---|
| 拖动触发 | 鼠标按下并移动 ≥ 5px 才视为拖动；< 5px 视为文字选中 |
| 视觉反馈 | 用 `transform: translate(dx, dy)` 做位移，**元素保持原文档流** |
| 应用方式 | 松开时把累计位移落到 `element.style.marginLeft` / `marginTop`，**禁止切到 `position: absolute`** |
| 文字编辑 | 除照片外，文字元素加 `contenteditable="true"`，双击即编辑 |
| 拖回原位 | 累计 dx/dy 为 0 时**自动**从 localStorage 删除该条 |
| 改回原文 | textContent 与原文本一致时**自动**从 localStorage 删除该条 |
| 重置 | 按 `R` 键（弹 confirm 后）清掉所有 margin / text 条目并复位 |
| 拖拽开关 | 按 `D` 键切换（开/关），状态写 localStorage |
| 导出按钮 | 顶部右上「📋 导出调整参数」（快捷键 `C`） |
| 清数据按钮 | 顶部次级「🗑 清本地数据」+「💾 本地: N 条」实时计数 |

### 8.3 localStorage 命名空间

- `resume-drag-v1-pos-<dragKey>`：margin 调整（`{ marginLeft, marginTop }`）
- `resume-drag-v1-text-<dragKey>`：文字调整（直接存字符串）
- `resume-drag-v1-mode`：拖拽模式开关（`'on'` / `'off'`）
- `<dragKey>` 格式：`{tag}-{class}-{index}`，例：`span-banner-name-1`
- **改版本号**（`v1` → `v2`）→ 旧数据自动作废（被新的 key 前缀隔离）
- 启动时跑 `gcStaleEntries()`：清掉 dragKey 不在当前 DOM 里的孤儿条目
- 「🗑 清本地数据」按钮可一键清掉所有 `resume-drag-*` 前缀的 key

### 8.4 JSON 导出格式

粘到对话里给 Claude 的 JSON 结构：

```json
{
  "type": "resume-drag-adjustments",
  "template": "商务_互联网_蓝",
  "source_file": "temp/2026-06-20-16-10/draft.html",
  "timestamp": "2026-06-20 16:35:12",
  "summary": { "margin_changes": 3, "text_changes": 2, "total": 4 },
  "changes": [
    {
      "selector": "span.banner-name",
      "description": "span.banner-name — \"姓  名\"",
      "style": { "margin-left": "20px", "margin-top": "-3px" }
    },
    {
      "selector": "span.banner-name",
      "description": "span.banner-name — \"姓  名\"",
      "text": { "old": "姓  名", "new": "张三" }
    }
  ]
}
```

字段说明：
- `selector`：用 `.class` + 必要时 `:nth-of-type(N)` 兜底，**保证唯一**
- `description`：人类可读的元素描述（含 tag、class、文字预览），用于人工核对
- `style`：`margin-left` / `margin-top` 二选一或都选，**不包含 `position`**
- `text.old` / `text.new`：原文本与新文本（按字符串精确匹配）

### 8.5 Claude 应用 JSON 的步骤

收到 JSON 后按顺序执行（**用 `querySelector` 找元素，不要肉眼找**）：

1. 读 `source_file` 指向的 `temp/<时间戳>/draft.html`
2. 对每个 `changes[]`：
   - 用 `selector` 找到唯一元素
   - 若有 `style`：把 `margin-left` / `margin-top` 合并到元素的 `style` 属性（已有 inline style 则合并，无则新增）
   - 若有 `text`：在元素内找 `old` 文本，替换为 `new`
3. 写回 `source_file`（覆盖原文件）
4. 跟用户确认：调整是否已正确应用、是否进入第 4 轮
5. 用户确认后 `cp temp/<时间戳>/draft.html prospect/<姓名>_<岗位>_简历.html`

### 8.6 禁止项

- ❌ 拖拽脚本写进 `template/`（模板保持纯 HTML/CSS）
- ❌ 拖拽脚本写进 `prospect/`（最终交付要纯净）
- ❌ 用 `position: absolute` 替代 margin（破坏打印分页和原文档流）
- ❌ 引入外部 JS / CDN / 第三方库
- ❌ 监听键盘全局快捷键时不区分 `INPUT` / `TEXTAREA` / contenteditable 焦点（会与正常文字操作冲突）
