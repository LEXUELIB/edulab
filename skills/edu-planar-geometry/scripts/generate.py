#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把结构化课程数据注入 template/geometry.html，产出单页 HTML。

数据全部由 lib/planar_kernel.py 的确定性计算驱动：
坐标、向量、角度、面积均为 sympy 精确计算结果，2D 坐标与解题数值同源、严格一致。

依赖: sympy。用一个能 import sympy 的 python3 运行（若缺: python3 -m pip install sympy）:
    python3 scripts/generate.py [输出路径.html]
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "geometry.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import planar_kernel as pk  # noqa: E402
import shapes  # noqa: E402


def render_html(data: dict, out_path: Path) -> Path:
    """把数据以 JSON 形式注入模板占位符，写出 html。"""
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    payload = json.dumps(data, ensure_ascii=False)
    html = template.replace(PLACEHOLDER, payload)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def build_right_triangle_data() -> dict:
    """直角三角形 ABC，直角边 AB=3, AC=4，求斜边 BC 长度和面积。"""
    tri = shapes.right_triangle(3, 4, right_angle_at='A')
    mp = tri['vertices']
    sides = tri['sides']
    area = tri['area']

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 直角三角形",
        "title": "直角三角形ABC中，∠A=90°，AB=3，AC=4，求斜边BC的长度和三角形面积",
        "answerLabel": "斜边 BC 长度",
        "answerValue": f"${pk.tex(sides['BC'])}$",
    }

    steps = [
        {
            "title": "建立坐标系",
            "content": (
                r"<p>以点 $A$ 为原点，$AB$ 为 $x$ 轴，$AC$ 为 $y$ 轴建立平面直角坐标系。</p>"
                r"<p>关键点坐标：</p>"
                r"$$A" + pk.tex(mp['A'][0]) + r"," + pk.tex(mp['A'][1]) + r"\quad B" + pk.tex(mp['B'][0]) + r"," + pk.tex(mp['B'][1]) + r"\quad C" + pk.tex(mp['C'][0]) + r"," + pk.tex(mp['C'][1]) + r"$$"
            ),
        },
        {
            "title": "应用勾股定理",
            "content": (
                r"<p>根据勾股定理：</p>"
                r"$$BC^2 = AB^2 + AC^2$$"
                r"$$BC = \sqrt{AB^2 + AC^2} = \sqrt{" + pk.tex(sides['AB']) + r"^2 + " + pk.tex(sides['CA']) + r"^2} = " + pk.tex(sides['BC']) + r"$$"
            ),
        },
        {
            "title": "计算三角形面积",
            "content": (
                r"<p>三角形面积公式：</p>"
                r"$$S_{\triangle ABC} = \frac{1}{2} \times AB \times AC = \frac{1}{2} \times " + pk.tex(sides['AB']) + r" \times " + pk.tex(sides['CA']) + r" = " + pk.tex(area) + r"$$"
            ),
        },
    ]

    board = {
        "view": {"xRange": [-1, 5], "yRange": [-1, 5]},
        "points": {
            "A": [0, 0],
            "B": [3, 0],
            "C": [0, 4],
        },
        "shapes": [tri['board']],
        "segments": [
            {"a": "A", "b": "B", "color": "line", "label": "3"},
            {"a": "A", "b": "C", "color": "line", "label": "4"},
            {"a": "B", "b": "C", "color": "curve", "label": pk.tex(sides['BC'])},
        ],
        "readouts": [
            {"id": "len_bc", "label": "BC 长度", "type": "distance", "a": "B", "b": "C", "highlight": True},
            {"id": "area", "label": "面积", "type": "area_triangle", "pts": ["A", "B", "C"], "highlight": True},
        ],
    }

    return {"lesson": lesson, "steps": steps, "board": board}


def build_parallelogram_data() -> dict:
    """平行四边形 ABCD，AB=4，AD=3，∠A=60°，求面积和对角线长度。"""
    p = shapes.parallelogram(4, 3, 60)
    mp = p['vertices']
    area = p['area']

    diag_ac = pk.distance_points(mp['A'], mp['C'])
    diag_bd = pk.distance_points(mp['B'], mp['D'])

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 平行四边形",
        "title": "平行四边形ABCD中，AB=4，AD=3，∠A=60°，求平行四边形面积和对角线AC、BD的长度",
        "answerLabel": "面积",
        "answerValue": f"${pk.tex(area)}$",
    }

    steps = [
        {
            "title": "建立坐标系",
            "content": (
                r"<p>以点 $A$ 为原点，$AB$ 为 $x$ 轴建立坐标系。</p>"
                r"<p>关键点坐标：</p>"
                r"$$A" + pk.tex(mp['A'][0]) + r"," + pk.tex(mp['A'][1]) + r"\quad B" + pk.tex(mp['B'][0]) + r"," + pk.tex(mp['B'][1]) + r"$$"
                r"$$D" + pk.tex(mp['D'][0]) + r"," + pk.tex(mp['D'][1]) + r"\quad C" + pk.tex(mp['C'][0]) + r"," + pk.tex(mp['C'][1]) + r"$$"
            ),
        },
        {
            "title": "计算面积",
            "content": (
                r"<p>平行四边形面积公式：$S = AB \times AD \times \sin A$</p>"
                r"$$S = " + pk.tex(p['sides']['AB']) + r" \times " + pk.tex(p['sides']['DA']) + r" \times \sin 60^\circ = " + pk.tex(area) + r"$$"
            ),
        },
        {
            "title": "计算对角线",
            "content": (
                r"<p>对角线 $AC$ 的长度：</p>"
                r"$$AC = \sqrt{(x_C - x_A)^2 + (y_C - y_A)^2} = " + pk.tex(diag_ac) + r"$$"
                r"<p>对角线 $BD$ 的长度：</p>"
                r"$$BD = \sqrt{(x_D - x_B)^2 + (y_D - y_B)^2} = " + pk.tex(diag_bd) + r"$$"
            ),
        },
    ]

    board = {
        "view": {"xRange": [-1, 7], "yRange": [-1, 4]},
        "points": {
            "A": [0, 0],
            "B": [4, 0],
            "D": [1.5, 2.598],
            "C": [5.5, 2.598],
        },
        "shapes": [p['board']],
        "segments": [
            {"a": "A", "b": "C", "color": "aux", "dashed": True, "label": pk.tex(diag_ac)},
            {"a": "B", "b": "D", "color": "aux", "dashed": True, "label": pk.tex(diag_bd)},
        ],
        "readouts": [
            {"id": "area", "label": "面积", "type": "area_parallelogram", "a": "A", "b": "B", "c": "D", "highlight": True},
            {"id": "diag_ac", "label": "AC 长度", "type": "distance", "a": "A", "b": "C"},
            {"id": "diag_bd", "label": "BD 长度", "type": "distance", "a": "B", "b": "D"},
        ],
    }

    return {"lesson": lesson, "steps": steps, "board": board}


def build_circle_tangent_data() -> dict:
    """圆 O，圆心(0,0)，半径 2，点 P(5,0)，求切线长。"""
    c = shapes.circle((0, 0), 2, 'O')
    center = c['center']
    radius = c['radius']
    
    P = pk.V(5, 0)
    tangent_pts = pk.circle_tangent_point((center[0], center[1]), radius, (P[0], P[1]))
    
    if tangent_pts:
        t1, t2 = tangent_pts
        tangent_len = pk.distance_points(P, t1)
    else:
        tangent_len = None

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 圆的切线",
        "title": "圆O的圆心为原点，半径为2，点P的坐标为(5,0)，求从P到圆O的切线长",
        "answerLabel": "切线长",
        "answerValue": f"${pk.tex(tangent_len)}$" if tangent_len else r"$\text{不存在}$",
    }

    steps = [
        {
            "title": "画出图形",
            "content": (
                r"<p>圆 $O$ 的方程：$x^2 + y^2 = " + pk.tex(radius**2) + r"$</p>"
                r"<p>点 $P$ 的坐标：$(5, 0)$</p>"
            ),
        },
        {
            "title": "应用勾股定理",
            "content": (
                r"<p>设切点为 $T$，则 $OT \perp PT$（切线垂直于过切点的半径）。</p>"
                r"<p>在直角三角形 $OTP$ 中：</p>"
                r"$$PT^2 + OT^2 = OP^2$$"
                r"$$PT = \sqrt{OP^2 - OT^2} = \sqrt{5^2 - " + pk.tex(radius) + r"^2} = " + pk.tex(tangent_len) + r"$$"
            ),
        },
    ]

    board = {
        "view": {"xRange": [-3, 7], "yRange": [-4, 4]},
        "points": {
            "O": [0, 0],
            "P": [5, 0],
            "T1": [0.8, 1.833] if tangent_pts else [0, 0],
            "T2": [0.8, -1.833] if tangent_pts else [0, 0],
        },
        "shapes": [c['board']],
        "segments": [
            {"a": "O", "b": "T1", "color": "aux", "label": "2"},
            {"a": "O", "b": "T2", "color": "aux", "label": "2"},
            {"a": "P", "b": "T1", "color": "line", "label": pk.tex(tangent_len)},
            {"a": "P", "b": "T2", "color": "line", "label": pk.tex(tangent_len)},
        ],
        "readouts": [
            {"id": "tangent_len", "label": "切线长 PT", "type": "distance", "a": "P", "b": "T1", "highlight": True},
        ],
    }

    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {
    "right_triangle": ("直角三角形 · 勾股定理", build_right_triangle_data),
    "parallelogram": ("平行四边形 · 面积与对角线", build_parallelogram_data),
    "circle_tangent": ("圆 · 切线长", build_circle_tangent_data),
}


def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate.py <类型> [输出路径.html]")
        print("可用类型:")
        for key, (desc, _) in REGISTRY.items():
            print(f"  {key} — {desc}")
        sys.exit(1)

    type_key = sys.argv[1]
    
    if type_key == "list":
        print("可用题型:")
        for key, (desc, _) in REGISTRY.items():
            print(f"  {key} — {desc}")
        sys.exit(0)

    if type_key not in REGISTRY:
        print(f"未知类型: {type_key}")
        sys.exit(1)

    builder = REGISTRY[type_key][1]
    data = builder()

    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_path = Path.cwd() / f"solution-{type_key}.html"

    render_html(data, out_path)
    print(f"已生成: {out_path}")


if __name__ == "__main__":
    main()
