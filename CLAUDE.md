# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

简历美化工作区。输入源文件（Markdown / HTML），输出可在浏览器中通过「打印 → 另存为 PDF」导出的 HTML 简历。

> 强制性规则集中在 `RULES.md`，**任何冲突一律以 RULES.md 为准**。

## 目录架构

```
resume_polishing/
├── .claude/skills/     # 技能库（当前含 zhanlincui-ui-ux-pro-max）
├── source/             # 用户源文件，只读
├── template/           # 模板库，按「风格_行业_主色调.html」命名
├── temp/               # 中间产物，按时间戳建子目录
└── prospect/           # 最终输出 HTML
```

每个目录的详细约束见 `RULES.md`。

## 标准工作流（含 4 轮确认 + temp 自调步骤）

简历美化**必须**经过 4 轮确认 + 1 个用户自调步骤，详见 `RULES.md` 第 4 节。流程概览：

```
source/<某简历>
  ↓ 第 1 轮确认：风格 + 行业 + 颜色 + 布局 + 页数 + 照片 + 联系方式
template/<某模板>  (或新建)
  ↓ 第 2 轮确认：字段抽取 + 模板选择 + temp 目录名
temp/<YYYY-MM-DD-HH-MM>/draft.html
    ← Claude 复制模板 + 填充个人数据 + 嵌入拖拽脚本（§8）
  ↓
  ┌──── 第 3a 步：用户在浏览器自调 ────┐
  │ 打开 draft.html                       │
  │ 拖动元素调整 margin                   │
  │ 双击文字直接编辑                      │
  │ 点「📋 导出调整参数」/ 按 C          │
  │ 弹模态框 / 自动复制 JSON 到剪贴板    │
  │ 粘到对话里 → Claude                  │
  └──────────────────────────────────────┘
  ↓ 第 3b 轮：Claude 读 JSON 改 draft.html + 复述调整让用户确认
prospect/<姓名>_<岗位>_简历.html
  ↓ 第 4 轮确认：目标文件名 + temp 是否清理 + 模板是否沉淀
```

> 关键变化：第 3 轮从「Claude 改、用户看」变成「用户自调、粘 JSON 给 Claude 应用」。拖拽脚本的细节在 `RULES.md` §8。

## temp 自调流程（拖拽脚本）

temp 目录下 `draft.html` 末尾会内联一段纯 vanilla JS 拖拽脚本（≈ 600 行），**不依赖任何外部资源**，仅服务于用户在浏览器里自由调整。

**可调整的粒度**（每个都是独立元素 / 文字单元，非整块）：

- banner 内 5 个：照片、姓名、性别行、求职意向、装饰文字
- 基础信息块 6 格
- 章节标题色块
- 每个 item 的 head 3 段 + desc 1 段
- 技能证书每格
- 自我评价

**操作方式**：

| 动作 | 行为 |
|---|---|
| 鼠标按下并移动 < 5px | 视为文字选中 / cursor placement（不触发拖动） |
| 鼠标按下并移动 ≥ 5px | 进入拖动：用 `transform: translate` 视觉反馈 |
| 松开 | 把累计位移落到 `element.style.marginLeft` / `marginTop`（**不切 absolute**） |
| 双击文字 | 直接编辑（contenteditable="true"） |
| 拖回原位 / 改回原文 | 该条 localStorage 自动删除 |

**导出参数**：右上角「📋 导出调整参数」或快捷键 `C`：

- 优先用 `navigator.clipboard.writeText`（`file://` 下大多被禁）
- 失败则弹模态框：JSON 自动全选 → 用户 `Ctrl/Cmd+C`
- 模态框内的「尝试复制」用 `document.execCommand('copy')` 兜底

**JSON 格式**（粘到对话给 Claude）：

```json
{
  "type": "resume-drag-adjustments",
  "template": "商务_互联网_蓝",
  "source_file": "temp/2026-06-20-16-10/draft.html",
  "timestamp": "2026-06-20 16:35:12",
  "summary": { "margin_changes": 3, "text_changes": 2, "total": 4 },
  "changes": [
    { "selector": "span.banner-name", "style": { "margin-left": "20px", "margin-top": "-3px" } },
    { "selector": "span.banner-name", "text": { "old": "姓  名", "new": "张三" } }
  ]
}
```

**Claude 收到 JSON 后的应用步骤**：

1. 读 `source_file` 指向的 `temp/.../draft.html`
2. 对每个 `changes[]`：
   - `selector` 定位元素（用 `querySelector`，不是肉眼找）
   - 若有 `style`：把 `margin-left` / `margin-top` 合并进元素的 `style` 属性
   - 若有 `text`：把 `old` 替换为 `new`
3. 写回 `temp/.../draft.html`
4. 用户确认后 `cp` 到 `prospect/<姓名>_<岗位>_简历.html`

**localStorage 命名空间**（详见 `RULES.md` §8）：

- `resume-drag-v1-pos-<dragKey>`：margin 调整
- `resume-drag-v1-text-<dragKey>`：文字调整
- `resume-drag-v1-mode`：拖拽模式开关
- 改 `v1` → 旧数据自动作废
- 启动时 gc 孤儿条目；右上「🗑 清本地数据」按钮可一键全清

## 预览方式

**不要起任何本地服务**，全部用 `file://` 协议在浏览器中直接打开。

Git Bash on Windows 中打开 HTML：

```bash
start "C:\Claude\resume_polishing\temp\2026-06-19-14-30\draft.html"
```

或在文件资源管理器中双击 HTML 文件。

> 详细规则与例外情况（确需起服务时的 PID 管控）见 `RULES.md` 第 7 节。

## 模板规范

- 文件名：`{风格}_{行业}_{主色调}.html`，例：`简约_金融_黑.html`、`清新_互联网_蓝.html`
- 单文件 HTML，CSS 内联或 `<style>` 内嵌（便于打印）
- 必须为 A4 纸张优化（`@page { size: A4; margin: ...; }`）
- 避免使用需联网的字体或资源
- 颜色与排版应可配置（CSS 变量优先）

## 重要约束速查

- **绝不要**修改 `source/` 内任何文件
- **绝不要**把最终成品留在 `temp/`
- **绝不要**把中间产物写入 `prospect/`
- **绝不要**用 Python / Node 起本地 server（除非用户明确授权并配 PID 管控）
- **绝不要**跳过 4 轮确认中的任何一轮
- **绝不要**把拖拽脚本写进 `template/`（模板保持纯 HTML/CSS）
- **绝不要**在 `prospect/` 文件里保留拖拽脚本（最终交付要纯净）
- 详细与例外见 `RULES.md`
