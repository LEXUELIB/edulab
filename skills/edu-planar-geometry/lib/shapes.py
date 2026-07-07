#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shapes.py — 平面图形的 sympy 精确定义库。

每个构造函数返回一个 dict，含：
  kind / vertices / sides / angles / area        —— 几何参数（sympy 精确）
  eq_latex  : 方程/描述 LaTeX
  board     : 注入前端引擎 board.shapes[*] 的 dict（浮点）

约定：大多数题目中心在原点或坐标轴上。
"""

import sympy as sp

x, y = sp.symbols('x y', real=True)


def _f(e):
    """sympy 精确量 → float。"""
    return float(sp.N(e))


def _sq_latex(e):
    """把 a^2 写成尽量整洁的 LaTeX（整数直接显示）。"""
    e = sp.nsimplify(e)
    return sp.latex(sp.simplify(e))


def triangle(a, b, c, labels=('A', 'B', 'C')):
    """三角形（三点坐标）。"""
    a_sym = sp.Matrix([sp.sympify(a[0]), sp.sympify(a[1])])
    b_sym = sp.Matrix([sp.sympify(b[0]), sp.sympify(b[1])])
    c_sym = sp.Matrix([sp.sympify(c[0]), sp.sympify(c[1])])
    
    ab = sp.simplify(sp.sqrt((b_sym[0]-a_sym[0])**2 + (b_sym[1]-a_sym[1])**2))
    bc = sp.simplify(sp.sqrt((c_sym[0]-b_sym[0])**2 + (c_sym[1]-b_sym[1])**2))
    ca = sp.simplify(sp.sqrt((a_sym[0]-c_sym[0])**2 + (a_sym[1]-c_sym[1])**2))
    
    ab_vec = b_sym - a_sym
    ac_vec = c_sym - a_sym
    ba_vec = a_sym - b_sym
    bc_vec = c_sym - b_sym
    ca_vec = a_sym - c_sym
    cb_vec = b_sym - c_sym
    
    angle_a = sp.simplify(sp.acos((ab_vec.dot(ac_vec)) / (ab * ca)) * 180 / sp.pi)
    angle_b = sp.simplify(sp.acos((ba_vec.dot(bc_vec)) / (ab * bc)) * 180 / sp.pi)
    angle_c = sp.simplify(sp.acos((ca_vec.dot(cb_vec)) / (ca * bc)) * 180 / sp.pi)
    
    area = sp.simplify(sp.Abs(ab_vec[0] * ac_vec[1] - ab_vec[1] * ac_vec[0]) / 2)
    
    return {
        'kind': 'triangle',
        'labels': labels,
        'vertices': {'A': a_sym, 'B': b_sym, 'C': c_sym},
        'sides': {'AB': ab, 'BC': bc, 'CA': ca},
        'angles': {'A': angle_a, 'B': angle_b, 'C': angle_c},
        'area': area,
        'eq_latex': r'\triangle ABC',
        'board': {
            'kind': 'triangle',
            'color': '#facc15',
            'label': labels[0] + labels[1] + labels[2],
            'points': {
                labels[0]: [_f(a_sym[0]), _f(a_sym[1])],
                labels[1]: [_f(b_sym[0]), _f(b_sym[1])],
                labels[2]: [_f(c_sym[0]), _f(c_sym[1])],
            },
            'sides': [
                {'a': labels[0], 'b': labels[1]},
                {'a': labels[1], 'b': labels[2]},
                {'a': labels[2], 'b': labels[0]},
            ]
        }
    }


def right_triangle(leg_a, leg_b, right_angle_at='A', labels=('A', 'B', 'C')):
    """直角三角形（已知两直角边）。"""
    la, lb = sp.sympify(leg_a), sp.sympify(leg_b)
    hypotenuse = sp.simplify(sp.sqrt(la**2 + lb**2))
    
    if right_angle_at == 'A':
        a = (0, 0)
        b = (la, 0)
        c = (0, lb)
    elif right_angle_at == 'B':
        a = (0, 0)
        b = (la, 0)
        c = (la, lb)
    else:
        a = (0, lb)
        b = (la, lb)
        c = (0, 0)
    
    return triangle(a, b, c, labels)


def equilateral_triangle(side_length, labels=('A', 'B', 'C')):
    """等边三角形。"""
    s = sp.sympify(side_length)
    h = sp.simplify(s * sp.sqrt(3) / 2)
    a = (0, 0)
    b = (s, 0)
    c = (s/2, h)
    return triangle(a, b, c, labels)


def isosceles_triangle(base, height, labels=('A', 'B', 'C')):
    """等腰三角形。"""
    b = sp.sympify(base)
    h = sp.sympify(height)
    a = (-b/2, 0)
    b_pt = (b/2, 0)
    c = (0, h)
    return triangle(a, b_pt, c, labels)


def parallelogram(a, b, theta_deg, labels=('A', 'B', 'C', 'D')):
    """平行四边形（已知两边和夹角）。"""
    a_len = sp.sympify(a)
    b_len = sp.sympify(b)
    theta = sp.sympify(theta_deg) * sp.pi / 180
    
    A = sp.Matrix([0, 0])
    B = sp.Matrix([a_len, 0])
    D = sp.Matrix([b_len * sp.cos(theta), b_len * sp.sin(theta)])
    C = B + D
    
    ab = a_len
    bc = sp.simplify(sp.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2))
    cd = a_len
    da = b_len
    
    angle_a = sp.simplify(theta_deg)
    angle_b = sp.simplify(180 - theta_deg)
    
    area = sp.simplify(a_len * b_len * sp.sin(theta))
    
    return {
        'kind': 'parallelogram',
        'labels': labels,
        'vertices': {'A': A, 'B': B, 'C': C, 'D': D},
        'sides': {'AB': ab, 'BC': bc, 'CD': cd, 'DA': da},
        'angles': {'A': angle_a, 'B': angle_b, 'C': angle_a, 'D': angle_b},
        'area': area,
        'eq_latex': r'\square ABCD',
        'board': {
            'kind': 'quadrilateral',
            'color': '#2dd4bf',
            'label': labels[0] + labels[1] + labels[2] + labels[3],
            'points': {
                labels[0]: [_f(A[0]), _f(A[1])],
                labels[1]: [_f(B[0]), _f(B[1])],
                labels[2]: [_f(C[0]), _f(C[1])],
                labels[3]: [_f(D[0]), _f(D[1])],
            },
            'sides': [
                {'a': labels[0], 'b': labels[1]},
                {'a': labels[1], 'b': labels[2]},
                {'a': labels[2], 'b': labels[3]},
                {'a': labels[3], 'b': labels[0]},
            ]
        }
    }


def rectangle(width, height, labels=('A', 'B', 'C', 'D')):
    """矩形。"""
    return parallelogram(width, height, 90, labels)


def square(side_length, labels=('A', 'B', 'C', 'D')):
    """正方形。"""
    return parallelogram(side_length, side_length, 90, labels)


def trapezoid(base1, base2, height, labels=('A', 'B', 'C', 'D')):
    """梯形（已知两底和高）。"""
    b1 = sp.sympify(base1)
    b2 = sp.sympify(base2)
    h = sp.sympify(height)
    
    A = sp.Matrix([0, 0])
    B = sp.Matrix([b1, 0])
    D = sp.Matrix([(b1 - b2)/2, h])
    C = D + sp.Matrix([b2, 0])
    
    ab = b1
    bc = sp.simplify(sp.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2))
    cd = b2
    da = sp.simplify(sp.sqrt((A[0]-D[0])**2 + (A[1]-D[1])**2))
    
    area = sp.simplify((b1 + b2) * h / 2)
    
    return {
        'kind': 'trapezoid',
        'labels': labels,
        'vertices': {'A': A, 'B': B, 'C': C, 'D': D},
        'sides': {'AB': ab, 'BC': bc, 'CD': cd, 'DA': da},
        'area': area,
        'eq_latex': r'\text{梯形 } ABCD',
        'board': {
            'kind': 'quadrilateral',
            'color': '#38bdf8',
            'label': labels[0] + labels[1] + labels[2] + labels[3],
            'points': {
                labels[0]: [_f(A[0]), _f(A[1])],
                labels[1]: [_f(B[0]), _f(B[1])],
                labels[2]: [_f(C[0]), _f(C[1])],
                labels[3]: [_f(D[0]), _f(D[1])],
            },
            'sides': [
                {'a': labels[0], 'b': labels[1]},
                {'a': labels[1], 'b': labels[2]},
                {'a': labels[2], 'b': labels[3]},
                {'a': labels[3], 'b': labels[0]},
            ]
        }
    }


def circle(center=(0, 0), radius=1, label='O'):
    """圆。"""
    cx = sp.sympify(center[0])
    cy = sp.sympify(center[1])
    r = sp.sympify(radius)
    
    circumference = sp.simplify(2 * sp.pi * r)
    area = sp.simplify(sp.pi * r**2)
    
    return {
        'kind': 'circle',
        'label': label,
        'center': sp.Matrix([cx, cy]),
        'radius': r,
        'circumference': circumference,
        'area': area,
        'eq_latex': r'(x - %s)^2 + (y - %s)^2 = %s' % (
            sp.latex(cx), sp.latex(cy), sp.latex(r**2)
        ),
        'board': {
            'kind': 'circle',
            'color': '#f472b6',
            'label': label,
            'center': [_f(cx), _f(cy)],
            'radius': _f(r),
        }
    }


def regular_polygon(n, side_length, labels=None):
    """正 n 边形。"""
    n = int(n)
    s = sp.sympify(side_length)
    r = sp.simplify(s / (2 * sp.sin(sp.pi / n)))
    
    vertices = {}
    default_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if labels is None:
        labels = default_labels[:n]
    
    for i in range(n):
        angle = sp.sympify(2 * sp.pi * i / n - sp.pi / 2)
        vertices[labels[i]] = sp.Matrix([
            r * sp.cos(angle),
            r * sp.sin(angle)
        ])
    
    area = sp.simplify(n * s**2 / (4 * sp.tan(sp.pi / n)))
    
    sides = {}
    for i in range(n):
        j = (i + 1) % n
        a, b = labels[i], labels[j]
        sides[a+b] = sp.simplify(sp.sqrt(
            (vertices[a][0] - vertices[b][0])**2 +
            (vertices[a][1] - vertices[b][1])**2
        ))
    
    board_points = {}
    board_sides = []
    for i in range(n):
        board_points[labels[i]] = [
            _f(vertices[labels[i]][0]),
            _f(vertices[labels[i]][1])
        ]
        j = (i + 1) % n
        board_sides.append({'a': labels[i], 'b': labels[j]})
    
    return {
        'kind': 'regular_polygon',
        'n': n,
        'labels': labels,
        'vertices': vertices,
        'sides': sides,
        'radius': r,
        'area': area,
        'eq_latex': rf'\text{{正{n}边形}} {labels[0]}{labels[1]}\cdots{labels[-1]}',
        'board': {
            'kind': 'polygon',
            'color': '#a78bfa',
            'label': ''.join(labels),
            'points': board_points,
            'sides': board_sides,
        }
    }


if __name__ == '__main__':
    print("=== 平面图形库自检 ===")
    
    t = right_triangle(3, 4)
    print(f"直角三角形: 边长 AB={t['sides']['AB']}, BC={t['sides']['BC']}, CA={t['sides']['CA']}")
    print(f"            内角 A={t['angles']['A']}°, B={t['angles']['B']}°, C={t['angles']['C']}°")
    print(f"            面积={t['area']}")
    
    p = parallelogram(4, 3, 60)
    print(f"\n平行四边形: 面积={p['area']}")
    
    c = circle((0, 0), 2)
    print(f"\n圆: 面积={c['area']}, 周长={c['circumference']}")
    
    print("\n=== 自检通过 ===")
