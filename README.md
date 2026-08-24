# 简历排版项目(Resume Polishing)

把 Markdown / HTML 源文件做成 A4 简历,最终通过浏览器「打印 → 另存为 PDF」导出。

## 目录结构

```
resume_polishing/
├── .claude/          # 技能库(本仓库已忽略个人内容,这里放通用 skill)
├── source/           # 你的简历源文件(.md / .html),只读,不入 git
├── template/         # 模板库,命名规则:风格_行业_主色调.html
├── temp/             # 中间产物(草稿、自调文件),不入 git
├── prospect/         # 最终成品 HTML(可直接打印/导出 PDF),不入 git
├── CLAUDE.md         # 给 AI agent 的项目约束说明
├── RULES.md          # 强制性规则(冲突时以 RULES.md 为准)
└── README.md         # 本文件
```

> `source/`、`temp/`、`prospect/` 三个目录涉及个人隐私,已通过 `.gitignore` + `.gitkeep` 隔离:
> - 目录壳子被 git 跟踪,clone 后能拿到完整结构
> - 目录里的**任何文件**都不会被 git 跟踪

## 工作流(4 轮确认 + 1 步自调)

```
1. 第 1 轮:确认风格 / 行业 / 颜色 / 布局 / 页数 / 照片 / 联系方式
2. 第 2 轮:确认字段抽取 + 模板选择 + temp 目录名
3. 第 3 轮(自调):在 temp/.../draft.html 里直接拖动 / 双击编辑,然后导出 JSON
4. 第 3b 步:把 JSON 粘给 AI,AI 应用调整并复述
5. 第 4 轮:确认最终文件名 + 是否清理 temp + 是否沉淀模板
```

## temp 自调(浏览器里直接调)

打开 `temp/<时间戳>/draft.html` 后:

| 动作 | 行为 |
|---|---|
| 鼠标按下移动 < 5px | 视为文字选中 / 光标定位 |
| 鼠标按下移动 ≥ 5px | 拖动元素(用 transform 视觉反馈) |
| 松开鼠标 | 位移落到元素的 `margin-left` / `margin-top` |
| 双击文字 | 直接进入编辑模式(contenteditable) |
| 点「📋 导出调整参数」或按 `C` | 导出 JSON 到剪贴板 |
| 点「🗑 清本地数据」 | 清掉 localStorage 里的所有调整记录 |

调完把 JSON 粘给 AI,AI 会应用调整到 `draft.html` 并复述,确认后 `cp` 到 `prospect/<姓名>_<岗位>_简历.html`。

## 预览方式

**不要起任何本地服务**,全部用 `file://` 协议:

```powershell
# Windows
start "C:\AGENT-Temp\resume_polishing\temp\2026-06-19-14-30\draft.html"
```

或在文件资源管理器双击 HTML。打印 / 导出 PDF 用浏览器内置的 `Ctrl+P`。

## 模板规范

- 文件名:`{风格}_{行业}_{主色调}.html`,例:`简约_金融_黑.html`
- 单文件 HTML,CSS 内联或 `<style>` 内嵌(便于打印)
- 必须为 A4 优化:`@page { size: A4; margin: ...; }`
- 不使用需要联网的字体或资源
- 颜色 / 排版用 CSS 变量(便于复用)

## 重要约束

- ❌ **不要**修改 `source/` 任何文件
- ❌ **不要**把最终成品留在 `temp/`
- ❌ **不要**把中间产物写入 `prospect/`
- ❌ **不要**用 Python / Node 起本地 server(除非你明确同意并配 PID 管控)
- ❌ **不要**跳过 4 轮确认中的任何一轮
- ❌ **不要**把拖拽脚本写进 `template/`(模板保持纯 HTML/CSS)
- ❌ **不要**在 `prospect/` 文件里保留拖拽脚本(最终交付要纯净)

详细与例外见 [`RULES.md`](./RULES.md) / [`CLAUDE.md`](./CLAUDE.md)。
