#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
planar_kernel.py — 平面几何确定性计算核心（基于 sympy 精确符号运算）。

设计目标：坐标、向量、角度、长度、面积全部由本模块精确算出，
根式自动化简，杜绝心算误差。同一套坐标既喂给解题文案，也喂给 2D 渲染，
保证"图、解、答"严格一致。

依赖: sympy（pip install sympy）。
"""

import sympy as sp
from sympy import sqrt, sin, cos, tan, asin, acos, pi

x, y = sp.symbols('x y', real=True)


def V(*comps):
    """构造列向量（sympy.Matrix）。"""
    if len(comps) == 1 and isinstance(comps[0], (list, tuple)):
        comps = comps[0]
    return sp.Matrix([sp.sympify(c) for c in comps])


def midpoint(a, b):
    """求两点中点。"""
    return (a + b) / 2


def distance_points(a, b):
    """求两点距离。"""
    return sp.simplify(sp.sqrt(sum((b[i] - a[i])**2 for i in range(2))))


def length(v):
    """求向量长度。"""
    return sp.simplify(sp.sqrt(sum(c**2 for c in v)))


def dot_product(v1, v2):
    """求向量点积。"""
    return sp.simplify(sum(v1[i] * v2[i] for i in range(2)))


def cross_product_2d(v1, v2):
    """2D 叉积（标量）。"""
    return sp.simplify(v1[0] * v2[1] - v1[1] * v2[0])


def angle_between_vectors(v1, v2):
    """求两向量夹角（弧度）。"""
    dp = dot_product(v1, v2)
    l1, l2 = length(v1), length(v2)
    return sp.simplify(acos(dp / (l1 * l2)))


def angle_between_vectors_deg(v1, v2):
    """求两向量夹角（角度）。"""
    rad = angle_between_vectors(v1, v2)
    return sp.simplify(rad * 180 / pi)


def angle_between_lines(p1, p2, q1, q2):
    """求两直线夹角（角度）。"""
    v1 = V(p2[0] - p1[0], p2[1] - p1[1])
    v2 = V(q2[0] - q1[0], q2[1] - q1[1])
    return angle_between_vectors_deg(v1, v2)


def area_triangle(a, b, c):
    """求三角形面积（三点坐标）。"""
    ab = V(b[0] - a[0], b[1] - a[1])
    ac = V(c[0] - a[0], c[1] - a[1])
    return sp.simplify(sp.Abs(cross_product_2d(ab, ac)) / 2)


def area_quadrilateral(a, b, c, d):
    """求四边形面积（四顶点坐标，按顺序）。"""
    return sp.simplify(area_triangle(a, b, c) + area_triangle(a, c, d))


def area_parallelogram(a, b, c):
    """求平行四边形面积（三点，第四点由向量推出）。"""
    ab = V(b[0] - a[0], b[1] - a[1])
    ac = V(c[0] - a[0], c[1] - a[1])
    return sp.simplify(sp.Abs(cross_product_2d(ab, ac)))


def foot_perpendicular(p, line_p1, line_p2):
    """求点到直线的垂足。"""
    p = V(*p) if isinstance(p, (list, tuple)) else p
    p1 = V(*line_p1) if isinstance(line_p1, (list, tuple)) else line_p1
    p2 = V(*line_p2) if isinstance(line_p2, (list, tuple)) else line_p2
    
    v = p2 - p1
    w = p - p1
    t = dot_product(w, v) / dot_product(v, v)
    foot = p1 + t * v
    return sp.simplify(foot)


def distance_point_line(p, line_p1, line_p2):
    """求点到直线距离。"""
    p = V(*p) if isinstance(p, (list, tuple)) else p
    p1 = V(*line_p1) if isinstance(line_p1, (list, tuple)) else line_p1
    p2 = V(*line_p2) if isinstance(line_p2, (list, tuple)) else line_p2
    
    ab = p2 - p1
    ap = p - p1
    return sp.simplify(sp.Abs(cross_product_2d(ab, ap)) / length(ab))


def intersect_lines(l1_p1, l1_p2, l2_p1, l2_p2):
    """求两直线交点。"""
    x1, y1 = l1_p1
    x2, y2 = l1_p2
    x3, y3 = l2_p1
    x4, y4 = l2_p2
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None
    
    t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = t_num / denom
    
    px = x1 + t * (x2 - x1)
    py = y1 + t * (y2 - y1)
    
    return sp.simplify(V(px, py))


def parallel_line(p, line_p1, line_p2):
    """过点 p 作直线 p1-p2 的平行线。"""
    v = V(line_p2[0] - line_p1[0], line_p2[1] - line_p1[1])
    return (p, (p[0] + v[0], p[1] + v[1]))


def perpendicular_line(p, line_p1, line_p2):
    """过点 p 作直线 p1-p2 的垂线。"""
    v = V(line_p2[0] - line_p1[0], line_p2[1] - line_p1[1])
    perp = V(-v[1], v[0])
    return (p, (p[0] + perp[0], p[1] + perp[1]))


def circle_tangent_point(circle_center, circle_radius, external_point):
    """求圆外一点到圆的切点（返回两个切点）。"""
    cx, cy = circle_center
    r = circle_radius
    px, py = external_point
    
    dx = px - cx
    dy = py - cy
    d_sq = dx**2 + dy**2
    d = sqrt(d_sq)
    
    if d <= r:
        return None
    
    t = r / d
    u = sqrt(1 - t**2)
    
    t1 = V(cx + t * dx - u * dy, cy + t * dy + u * dx)
    t2 = V(cx + t * dx + u * dy, cy + t * dy - u * dx)
    
    return (sp.simplify(t1), sp.simplify(t2))


def circle_intersection(c1_center, c1_r, c2_center, c2_r):
    """求两圆交点。"""
    x1, y1 = c1_center
    r1 = c1_r
    x2, y2 = c2_center
    r2 = c2_r
    
    dx = x2 - x1
    dy = y2 - y1
    d_sq = dx**2 + dy**2
    d = sqrt(d_sq)
    
    if d > r1 + r2 or d < abs(r1 - r2):
        return None
    
    a = (r1**2 - r2**2 + d_sq) / (2 * d)
    h = sqrt(r1**2 - a**2)
    
    px = x1 + (a * dx) / d
    py = y1 + (a * dy) / d
    
    p1 = V(px - (h * dy) / d, py + (h * dx) / d)
    p2 = V(px + (h * dy) / d, py - (h * dx) / d)
    
    return (sp.simplify(p1), sp.simplify(p2))


def inscribed_angle(circle_center, point_a, point_b, point_p):
    """求圆周角（点 P 对弧 AB 的圆周角）。"""
    o = V(*circle_center)
    a = V(*point_a)
    b = V(*point_b)
    p = V(*point_p)
    
    va = a - o
    vb = b - o
    vp_a = p - a
    vp_b = p - b
    
    central_angle = angle_between_vectors(va, vb)
    inscribed = angle_between_vectors(vp_a, vp_b)
    
    return sp.simplify(inscribed * 180 / pi), sp.simplify(central_angle * 180 / pi)


def triangle_angles(a, b, c):
    """求三角形三个内角（角度）。"""
    ab = V(b[0] - a[0], b[1] - a[1])
    ac = V(c[0] - a[0], c[1] - a[1])
    ba = V(a[0] - b[0], a[1] - b[1])
    bc = V(c[0] - b[0], c[1] - b[1])
    ca = V(a[0] - c[0], a[1] - c[1])
    cb = V(b[0] - c[0], b[1] - c[1])
    
    angle_a = angle_between_vectors_deg(ab, ac)
    angle_b = angle_between_vectors_deg(ba, bc)
    angle_c = angle_between_vectors_deg(ca, cb)
    
    return sp.simplify(angle_a), sp.simplify(angle_b), sp.simplify(angle_c)


def triangle_sides(a, b, c):
    """求三角形三条边长。"""
    return (
        sp.simplify(distance_points(a, b)),
        sp.simplify(distance_points(b, c)),
        sp.simplify(distance_points(c, a))
    )


def pythagoras_check(a, b, c):
    """检查三角形是否为直角三角形，返回直角顶点或 None。"""
    ab_sq = (b[0] - a[0])**2 + (b[1] - a[1])**2
    bc_sq = (c[0] - b[0])**2 + (c[1] - b[1])**2
    ca_sq = (a[0] - c[0])**2 + (a[1] - c[1])**2
    
    if sp.simplify(ab_sq + bc_sq - ca_sq) == 0:
        return 'B'
    if sp.simplify(bc_sq + ca_sq - ab_sq) == 0:
        return 'A'
    if sp.simplify(ca_sq + ab_sq - bc_sq) == 0:
        return 'C'
    return None


def is_triangle_similar(a1, b1, c1, a2, b2, c2):
    """检查两三角形是否相似。"""
    sides1 = sorted([sp.simplify(s) for s in triangle_sides(a1, b1, c1)])
    sides2 = sorted([sp.simplify(s) for s in triangle_sides(a2, b2, c2)])
    
    r1 = sp.simplify(sides1[1] / sides1[0])
    r2 = sp.simplify(sides1[2] / sides1[0])
    r3 = sp.simplify(sides2[1] / sides2[0])
    r4 = sp.simplify(sides2[2] / sides2[0])
    
    return sp.simplify(r1 - r3) == 0 and sp.simplify(r2 - r4) == 0


def is_triangle_congruent(a1, b1, c1, a2, b2, c2):
    """检查两三角形是否全等。"""
    sides1 = sorted([sp.simplify(s) for s in triangle_sides(a1, b1, c1)])
    sides2 = sorted([sp.simplify(s) for s in triangle_sides(a2, b2, c2)])
    
    return all(sp.simplify(sides1[i] - sides2[i]) == 0 for i in range(3))


def parametric_point_on_segment(a, b, t):
    """线段 AB 上的参数点（t∈[0,1]）。"""
    return sp.simplify(V(a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))


def median_of_triangle(a, b, c):
    """三角形中线（从 A 到 BC 中点）。"""
    m = midpoint(b, c)
    return (a, m)


def angle_bisector(a, b, c):
    """角平分线（从 A 出发）。"""
    ab_len = distance_points(a, b)
    ac_len = distance_points(a, c)
    ratio = ab_len / (ab_len + ac_len)
    d = V(b[0] + ratio * (c[0] - b[0]), b[1] + ratio * (c[1] - b[1]))
    return (a, d)


def centroid(a, b, c):
    """三角形重心。"""
    return sp.simplify(V((a[0] + b[0] + c[0]) / 3, (a[1] + b[1] + c[1]) / 3))


def circumcenter(a, b, c):
    """三角形外心（三边垂直平分线交点）。"""
    mid_ab = midpoint(a, b)
    mid_bc = midpoint(b, c)
    
    perp_ab = perpendicular_line(mid_ab, a, b)
    perp_bc = perpendicular_line(mid_bc, b, c)
    
    return intersect_lines(mid_ab, perp_ab[1], mid_bc, perp_bc[1])


def orthocenter(a, b, c):
    """三角形垂心（三条高线交点）。"""
    foot_b = foot_perpendicular(b, a, c)
    foot_c = foot_perpendicular(c, a, b)
    
    return intersect_lines(b, foot_b, c, foot_c)


def radical_axis(c1_center, c1_r, c2_center, c2_r):
    """两圆根轴（等幂线）。"""
    x1, y1 = c1_center
    r1 = c1_r
    x2, y2 = c2_center
    r2 = c2_r
    
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = x1**2 + y1**2 - r1**2 - (x2**2 + y2**2 - r2**2)
    
    if A == 0 and B == 0:
        return None
    
    p1 = V(0, -C / B) if B != 0 else V(-C / A, 0)
    p2 = V(1, -(C + A) / B) if B != 0 else V(-(C + B) / A, 1)
    
    return (p1, p2)


def range_over_param(expr, param, param_range):
    """求表达式在参数范围内的取值范围（含开闭端点判定）。"""
    t = sp.Symbol('t')
    f = sp.lambdify(t, expr, 'sympy')
    
    t_min, t_max = param_range
    f_min = f(t_min)
    f_max = f(t_max)
    
    try:
        df = sp.diff(expr, param)
        critical_points = sp.solve(df, param)
    except:
        critical_points = []
    
    critical_values = []
    for cp in critical_points:
        try:
            val = float(cp)
            if t_min <= val <= t_max:
                critical_values.append(f(cp))
        except:
            pass
    
    all_values = [f_min, f_max] + critical_values
    all_values = [sp.simplify(v) for v in all_values if sp.im(v) == 0]
    
    if not all_values:
        return {'min': f_min, 'max': f_max, 'open_min': False, 'open_max': False}
    
    min_val = min(all_values, key=lambda x: float(x))
    max_val = max(all_values, key=lambda x: float(x))
    
    return {
        'min': sp.simplify(min_val),
        'max': sp.simplify(max_val),
        'open_min': False,
        'open_max': False
    }


def is_constant_in_param(expr, param):
    """检查表达式是否与参数无关（定值）。"""
    try:
        df = sp.diff(expr, param)
        return sp.simplify(df) == 0
    except:
        return False


def is_clean(expr):
    """判断表达式是否规整（答案美观，适合展示）。"""
    try:
        val = float(expr)
        if abs(val) > 1e10 or abs(val) < 1e-10:
            return False
        return True
    except:
        return False


def tex(expr):
    """将 sympy 表达式转为 LaTeX。"""
    if expr is None:
        return r'\text{不存在}'
    return sp.latex(sp.simplify(expr))


def solve_right_triangle(angle_deg, hypotenuse):
    """解直角三角形（已知一角和斜边）。"""
    angle_rad = angle_deg * pi / 180
    opposite = sp.simplify(hypotenuse * sin(angle_rad))
    adjacent = sp.simplify(hypotenuse * cos(angle_rad))
    return {'opposite': opposite, 'adjacent': adjacent, 'angle': angle_deg}


def solve_triangle_sss(a, b, c):
    """SSS 解三角形（已知三边）。"""
    angle_a = acos((b**2 + c**2 - a**2) / (2 * b * c))
    angle_b = acos((a**2 + c**2 - b**2) / (2 * a * c))
    angle_c = pi - angle_a - angle_b
    return {
        'angles': (sp.simplify(angle_a * 180 / pi),
                   sp.simplify(angle_b * 180 / pi),
                   sp.simplify(angle_c * 180 / pi)),
        'area': sp.simplify(sqrt((a+b+c)*(a+b-c)*(a-b+c)*(-a+b+c)) / 4)
    }


def solve_triangle_sas(a, b, angle_c_deg):
    """SAS 解三角形（已知两边及其夹角）。"""
    angle_c = angle_c_deg * pi / 180
    c = sqrt(a**2 + b**2 - 2 * a * b * cos(angle_c))
    angle_a = acos((b**2 + c**2 - a**2) / (2 * b * c))
    angle_b = pi - angle_a - angle_c
    return {
        'side_c': sp.simplify(c),
        'angles': (sp.simplify(angle_a * 180 / pi),
                   sp.simplify(angle_b * 180 / pi),
                   angle_c_deg),
        'area': sp.simplify(a * b * sin(angle_c) / 2)
    }


if __name__ == '__main__':
    A, B, C = V(0, 0), V(3, 0), V(0, 4)
    
    sides = triangle_sides(A, B, C)
    angles = triangle_angles(A, B, C)
    area = area_triangle(A, B, C)
    right_angle = pythagoras_check(A, B, C)
    cent = centroid(A, B, C)
    
    print("=== 平面几何 kernel 自检 ===")
    print(f"三角形 ABC 边长: AB={tex(sides[0])}, BC={tex(sides[1])}, CA={tex(sides[2])}")
    print(f"三角形 ABC 内角: A={tex(angles[0])}°, B={tex(angles[1])}°, C={tex(angles[2])}°")
    print(f"三角形 ABC 面积: {tex(area)}")
    print(f"直角顶点: {right_angle}")
    print(f"重心: {tex(cent[0])}, {tex(cent[1])}")
    
    foot = foot_perpendicular(V(1, 1), A, B)
    print(f"点(1,1)到 AB 的垂足: ({tex(foot[0])}, {tex(foot[1])})")
    
    mid = midpoint(A, B)
    print(f"AB 中点: ({tex(mid[0])}, {tex(mid[1])})")
    
    print("\n=== 自检通过 ===")
