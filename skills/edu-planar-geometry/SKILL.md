---
name: edu-planar-geometry
description: >-
  把一道平面几何题解成一个自包含的交互教学网页：左栏题面 + 动态控制台（可变参数滑块驱动实时重算），中栏 KaTeX 分步解析，右栏 2D Canvas 动态几何画板（三角形/四边形/圆 + 动直线/动点 + 辅助线 + 标注 + 画笔涂鸦）。支持三入口——给定文字题、随机出题、上传题目图片识别后解题。覆盖三角形全等/相似、圆与切线/割线、角度计算、线段长度、面积、勾股定理、平行四边形、梯形等题型，统一由 sympy 精确计算驱动。其他 agent 也可调用本技能生成此类网页。
  触发词：平面几何, 三角形, 全等三角形, 相似三角形, 圆, 切线, 割线, 勾股定理, 平行四边形, 梯形, 辅助线, 角度计算, 线段长度, 面积计算, 解这道几何题, 随机出一道平面几何题, 这张图里的平面几何题; planar geometry, triangle, congruent, similar, circle, tangent, secant, Pythagorean theorem, parallelogram, trapezoid, auxiliary line, angle calculation, interactive geometry solution page.
---

# 平面几何解题 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块（如点位置参数 t / 角度 θ）驱动实时重算的几何量（交点坐标、角度、长度、面积…），以及"理论范围条"或"定值指示"。
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板。
- **右栏**：2D Canvas 动态几何画板（三角形/四边形/圆 + 动直线/动点 + 辅助线 + 点标注 + 网格坐标轴），叠加画笔涂鸦工具栏。

## 依赖（重要）
计算核心 `lib/planar_kernel.py` 依赖 **sympy**。运行脚本前先确认有能 import sympy 的解释器：`python3 -c "import sympy"`。

**缺库时**：若 import 报错，**先询问用户是否安装**，同意后再装（`python3 -m pip install <库名>`）或换一个已装该库的解释器；**不要未经询问直接装**。下文 `python3` 均指这个能跑通依赖的解释器。

## 工作流程

### 第 1 步：得到 problem spec（三入口归一）
把题目整理成结构化 spec（图形类型与参数、已知点/条件、所求类型与对象、语言）。
- **文字题**：直接抽取。
- **图片**：视觉读图抽取，并**把识别到的题目回显给用户确认**（题面/图形/参数/所求/语言）再继续。
- **随机出题**：选图形 + 题型，随机参数 → kernel 求解，用 `planar_kernel.is_clean(...)` 判答案是否规整，不规整就重抽。

> **输出语言跟随提示词语言**：英文提示 → 英文网页，中文 → 中文。spec 记下 `language`。

### 第 2 步：用 kernel 精确计算（不要心算）
按 `references/conventions.md` 的解法配方，调用 `lib/planar_kernel.py` 与 `lib/shapes.py`：
- `shapes.triangle/quadrilateral/circle(...)` 得图形对象（精确顶点坐标、边长、角度、`eq_latex`、以及给前端引擎的 `board` dict）。
- 目标量：`angle_between_lines` / `distance_points` / `area_triangle` / `circle_tangent` / `intersection` …
- 取值范围：`range_over_param(expr)` —— 含开闭端点判定。
- 定值：`is_constant_in_param(expr)`。

可命令行自检 kernel：
```bash
python3 lib/planar_kernel.py      # 内置样例自检
```

### 第 3 步：组装数据并注入模板

> 📍 **输出位置 & 唯一产物（最重要）**：交付给用户的**只有一个 `.html`**，写到**当前工作目录（`Path.cwd()`）**（除非用户显式指定路径）。cwd 里**不要留任何别的文件**——构建脚本（`.py`）、`__pycache__`、自检截图（`.png`）、临时文件都**不是交付物**，一律放 `/tmp` 或用完即删。也**绝不要**写进技能自身目录。

把"组装数据 + 注入模板"的**构建脚本写到临时目录**（如 `/tmp/pg_build.py`），让它**只把 `.html` 写到 cwd**；脚本拼出 `lesson` / `steps` / `board` 数据（schema 见 `references/problem-schema.md`），调用 `generate.render_html(data, out)` 注入 `template/geometry.html`，**跑完即删脚本**：

```python
import sys; sys.dont_write_bytecode = True
sys.path.insert(0, "<技能目录>/scripts")
import generate
from pathlib import Path
data = {"lesson": {...}, "steps": [...], "board": {...}}
out = Path.cwd() / "solution-<题目简述>.html"
generate.render_html(data, out)
```

```bash
python3 -B /tmp/pg_build.py && rm -f /tmp/pg_build.py
```

### 第 4 步：自检（正确性方案）
- kernel 答案 == 答案卡 `lesson.answer` == 末步骤展示值 == **JS 标准位/扫段重算值**，四者一致。
- 起本地静态服务（服务**输出文件所在目录**，即 cwd）用预览检查：无控制台报错、KaTeX 正常、滑块实时重算正确、辅助线/定值/定点行为符合、画笔与收起面板可用。

> ⚠️ **必须关闭你开过的端口/服务**：预览一结束立即停掉，**绝不留占用端口的进程**。交付前确认端口已释放再告诉用户。

### 第 5 步：交付
成品写在**用户当前工作目录（cwd）**，命名形如 `solution-<题目简述>.html`，把路径告诉用户，可直接浏览器打开。

## 扩展
- **加题型**：在 `planar_kernel.py` 加目标量函数 + 复用 `range_over_param` / `is_constant_in_param`；在 `generate.py` 加一个 `build_*`，选定交互范式（范围条 / 定值 / 定点 / 辅助线）。
- **加图形**：`shapes.py` 已有三角形/四边形/圆；前端 `geometry.html` 引擎已支持三类渲染。新图形在两处各加一份即可。
- **加交互构造**：`geometry.html` 的 `buildScene` switch 是构造库（`line_through_points`、`intersect_lines`、`midpoint`、`foot_perp`、`tangent_circle`、`parallel_line`…），按需扩充并在 schema 文档登记。

## 目录
- `template/geometry.html` — 数据驱动模板（通用 2D 渲染器 + 参数引擎 + 数据岛 `__LESSON_DATA__`）
- `lib/shapes.py` — 平面图形 sympy 精确定义库（特殊点 / LaTeX / board dict）
- `lib/planar_kernel.py` — sympy 精确求解核心（角度·距离·面积·交点·范围·定值）
- `scripts/generate.py` — 注入模板 + build_* 范本 + 批量/单题出题
- `references/problem-schema.md` — 数据格式（board 引擎 schema）
- `references/conventions.md` — 标准式、解法配方表、自检
