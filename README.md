# Resume Polishing · 简历排版项目

> 把 Markdown / HTML 简历源文件做成 A4 简历,支持浏览器内拖拽自调、零依赖、零服务、隐私隔离。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
![Dependencies: 0](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)
![Platform: Browser](https://img.shields.io/badge/platform-browser-lightgrey.svg)

---

## ✨ 核心特性

- 🎨 **多套开箱即用模板** — 覆盖简约 / 商务 / 清新 3 种风格,适配互联网 / 金融 / 制造 / 教师 / 文化传媒 5 个行业,主色黑 / 蓝 / 紫三色可选
- 🖱 **拖拽自调** — 浏览器里直接拖元素调间距、双击改文字,所见即所得,不需要任何 IDE
- 📋 **参数化导出** — 调整结果可导出 JSON,AI 一键应用,二次微调时无需从头再来
- 🖨 **A4 直出 PDF** — 走浏览器原生「打印 → 另存为 PDF」,排版零损耗,排版定义完全在 `@media print` 里
- 🔒 **零依赖、零网络** — HTML / CSS / JS 全部内联,无 CDN、无打包工具、无外部资源请求
- 🛡 **隐私隔离** — `source/`(源文件)、`temp/`(草稿)、`prospect/`(成品)三个目录默认 git 忽略,本地的个人简历不会被提交

---

## 📸 预览

> 暂无截图。如要贡献预览图,请将 PNG 放到 `docs/screenshots/` 后在本节用 Markdown 引用:
>
> ```markdown
> ![简约_互联网_黑](./docs/screenshots/简约_互联网_黑.png)
> ```

模板示例(`template/` 目录):

- `简约_互联网_黑.html`
- `简约_互联网_蓝.html`
- `简约_金融_黑.html`
- `简约_制造业_紫.html`
- `简约_文化传媒_蓝.html`
- `商务_互联网_蓝.html`
- `清新_教师_紫.html`

---

## 🚀 快速开始

### 环境要求

- 任意现代浏览器(Chrome / Edge / Firefox / Safari 任一)
- 任意文本编辑器(VSCode / Sublime / 记事本都行)
- 无需 Node.js、无需 Python、无需任何构建工具

### 5 分钟上手

```bash
# 1. 克隆仓库
git clone https://github.com/xingmangHi/resume_polishing.git
cd resume_polishing

# 2. 在浏览器里打开任意一份模板看效果
# Windows
start "template\简约_互联网_黑.html"
# macOS
open template/简约_互联网_黑.html
# Linux
xdg-open template/简约_互联网_黑.html

# 3. 复制模板到 temp/ 目录开始改
mkdir -p temp/$(date +%Y-%m-%d-%H-%M)
cp template/简约_互联网_黑.html temp/<时间戳>/draft.html
```

接下来:
1. 用编辑器把 `draft.html` 里的占位符(`某某大学` / `某某公司` / `姓名` 等)替换成你自己的内容
2. 浏览器打开 `draft.html`,Ctrl+P 试打一页 A4 验证排版
3. 满意后把成品复制到 `prospect/<姓名>_<岗位>_简历.html`

---

## 📖 使用方法

### 工作流概览(4 轮确认 + 1 步自调)

```
1. 与 AI 确认:风格 / 行业 / 颜色 / 布局 / 页数 / 照片 / 联系方式
2. 确认:字段抽取结果 + 模板选择 + temp 目录名
3. [可选] 在浏览器里拖拽自调,导出 JSON
4. AI 应用你的 JSON 调整,复述给你确认
5. 最终:确认成品文件名 + temp 清理 + 模板沉淀
```

> 详细规则与异常处理见 [`RULES.md`](./RULES.md)。给 AI agent 看的项目说明见 [`CLAUDE.md`](./CLAUDE.md)。

### 拖拽脚本速查

打开 `temp/<时间戳>/draft.html` 后,内联的拖拽脚本会启用以下操作:

| 动作 | 效果 |
|---|---|
| 鼠标按下移动 < 5px | 视为文字选中 / 光标定位(不触发拖动) |
| 鼠标按下移动 ≥ 5px | 进入拖动,元素跟随鼠标移动(用 `transform` 视觉反馈) |
| 松开鼠标 | 把累计位移落到元素的 `margin-left` / `margin-top` |
| 双击文字 | 直接进入编辑模式(`contenteditable`) |
| 点右上「📋 导出调整参数」或按 `C` | 导出 JSON 到剪贴板 |
| 点右上「🗑 清本地数据」 | 清掉 localStorage 里的所有调整记录 |

JSON 格式:

```json
{
  "type": "resume-drag-adjustments",
  "template": "简约_互联网_黑",
  "source_file": "temp/2026-06-20-16-10/draft.html",
  "timestamp": "2026-06-20 16:35:12",
  "summary": { "margin_changes": 3, "text_changes": 2, "total": 4 },
  "changes": [
    { "selector": "span.banner-name", "style": { "margin-left": "20px", "margin-top": "-3px" } },
    { "selector": "span.banner-name", "text": { "old": "姓  名", "new": "张三" } }
  ]
}
```

把 JSON 粘回对话给 AI,AI 会自动应用调整到 `draft.html` 并复述你改了什么。

---

## 🎨 模板规范

如果你要**新增**或**修改**模板,请遵守以下规范:

- **文件命名**:`{风格}_{行业}_{主色调}.html`,如 `简约_金融_黑.html`
- **单文件 HTML**:CSS 内联或写在 `<style>` 内(便于打印)
- **A4 优化**:`@page { size: A4; margin: ...; }` 必须有,且屏幕模式要模拟 A4 视觉
- **零外部资源**:不用 CDN 字体、不用外链图片,所有资源内联
- **CSS 变量**:颜色、间距、字号等用 CSS 变量定义(便于复用)
- **不含拖拽脚本**:拖拽脚本只在 `temp/` 阶段的 draft.html 里使用,**不要**写进 `template/`
- **占位符约定**:
  - 姓名 / 联系方式:`姓  名` / `+86 XXX XXXX XXXX`
  - 学校 / 专业:`某某大学` / `某某专业`
  - 奖项:`XXX 一等奖(XXXX)`
  - 公司 / 品牌:`某某公司` / `xx校园讲师`
  - 日期:`XXXX.XX - XXXX.XX`

### 当前模板清单

| 模板 | 风格 | 行业 | 主色 |
|---|---|---|---|
| `简约_互联网_黑` | 简约 | 互联网 | 黑 |
| `简约_互联网_蓝` | 简约 | 互联网 | 蓝 |
| `简约_金融_黑` | 简约 | 金融 | 黑 |
| `简约_制造业_紫` | 简约 | 制造业 | 紫 |
| `简约_文化传媒_蓝` | 简约 | 文化传媒 | 蓝 |
| `商务_互联网_蓝` | 商务 | 互联网 | 蓝 |
| `清新_教师_紫` | 清新 | 教师 | 紫 |

---

## 🤝 贡献

欢迎 PR!主要的贡献方向有三种:

### 1. 新增模板

1. Fork → 新建分支 `feat/template-<描述>`,如 `feat/template-tech-cyber-green`
2. 仿照 `template/` 下任意一份创建新文件,遵守 [§ 模板规范](#-模板规范)
3. 本地验证 checklist:
   - 浏览器打开,布局正常
   - 把姓名改成一个超长字符串(如 20 个汉字),看会不会溢出
   - Ctrl+P → 实际打印预览,确认一页 A4 内,无内容被切
4. 提交 PR,描述里附:
   - 模板定位(目标行业 / 风格)
   - 浏览器打印预览截图
   - 用什么字体 / 配色参考

### 2. 改进拖拽脚本

拖拽脚本目前内联在 `temp/<时间戳>/draft.html` 末尾。要改进它,先在 temp 目录新建一份 draft.html 改,然后把你修改后的整段 `<script>` 贴到 PR 里说明。**(注意:不要把脚本写进 `template/` 下任何文件。)**

### 3. 修正 / 改进工作流

工作流定义在 [`RULES.md`](./RULES.md)。如果发现流程有 bug 或可优化:

- **小改动**(错别字、表述不清晰):直接 PR
- **结构性改动**(改流程、新增阶段):先开 Issue 讨论,确认方向后再 PR

### 提 Issue

- Bug 报告:附浏览器版本 + 操作系统 + 复现步骤 + 期望 vs 实际
- Feature Request:说清楚解决什么问题、目标用户是谁、你的方案是什么
- 模板建议:说明目标行业 / 风格,最好附参考样例

---

## 🗂 目录结构

```
resume_polishing/
├── .claude/          # 技能库(本项目使用的 AI 协作能力定义)
├── template/         # 模板库(单文件 HTML,纯 HTML/CSS,无脚本)
├── source/           # 你的简历源文件(.md / .html),不入 git
├── temp/             # 草稿(填内容 + 自调阶段),不入 git
├── prospect/         # 最终成品 HTML(可直接打印 / 导出 PDF),不入 git
├── CLAUDE.md         # 给 AI agent 看的项目说明
├── RULES.md          # 强制性规则(冲突时以 RULES.md 为准)
├── README.md         # 本文件
└── LICENSE           # MIT 协议
```

**隐私设计说明**:`source/`、`temp/`、`prospect/` 三个目录通过 `.gitignore` + `.gitkeep` 实现:
- 目录壳子被 git 跟踪,clone 后能拿到完整结构
- 任何放进这三个目录的**实际文件**都不会被 git 跟踪,本地的个人简历永远不会被提交

---

## 📄 许可证

[MIT](./LICENSE) © 2026 余灿

详细的项目运行规则与异常处理见 [`RULES.md`](./RULES.md);给 AI agent 看的项目说明见 [`CLAUDE.md`](./CLAUDE.md)。

---

## 🙏 致谢

- 模板设计参考了若干公开的简历排版样例(具体引用见各模板注释)
- 拖拽自调的想法受 Figma / 即时设计等所见即所得工具启发
- 工作流设计与 Claude Code / MiniMax Code 协作验证

---

## 🗺 Roadmap

- [ ] 加入更多行业模板(医疗 / 法律 / 设计 / 销售)
- [ ] 拖拽脚本的 GC 与命名空间版本管理(详见 RULES.md §8)
- [ ] 提供英文 README(`README.en.md`)
- [ ] GitHub Actions 模板 HTML 语法校验
- [ ] VSCode 插件:右键 Markdown → 一键转简历

---

<sub>本项目采用 MIT 协议 — 欢迎 fork、修改、商用,只需保留版权声明即可。</sub>
