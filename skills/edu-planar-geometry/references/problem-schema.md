# 平面几何技能数据格式

## 顶层结构

```json
{
    "lesson": {...},
    "steps": [...],
    "board": {...}
}
```

## lesson

题目元信息。

```json
{
    "language": "zh-CN",
    "meta": "交互解题 · 直角三角形",
    "title": "直角三角形ABC中，∠A=90°，求斜边BC的长度",
    "answerLabel": "斜边 BC 长度",
    "answerValue": "$5$",
    "ui": {
        "consoleTitle": "动态控制台",
        "solutionTitle": "详细解析",
        "collapse": "收起解析",
        "expand": "展开解析"
    }
}
```

## steps

分步解析。

```json
[
    {
        "title": "建立坐标系",
        "content": "<p>以点 $A$ 为原点...</p>"
    }
]
```

## board

画板数据（驱动前端渲染引擎）。

### view

视窗范围。

```json
"view": {
    "xRange": [-1, 5],
    "yRange": [-1, 5]
}
```

### points

静态点。

```json
"points": {
    "A": [0, 0],
    "B": [3, 0],
    "C": {
        "xy": [0, 4],
        "color": "ptA",
        "label": "C",
        "emphasis": true
    }
}
```

### shapes

图形（三角形/四边形/圆/多边形）。

```json
"shapes": [
    {
        "kind": "triangle",
        "color": "#facc15",
        "label": "ABC",
        "points": {"A": [0,0], "B": [3,0], "C": [0,4]},
        "sides": [{"a": "A", "b": "B"}, {"a": "B", "b": "C"}, {"a": "C", "b": "A"}]
    },
    {
        "kind": "circle",
        "color": "#f472b6",
        "label": "O",
        "center": [0, 0],
        "radius": 2
    }
]
```

### segments

线段（辅助线等）。

```json
"segments": [
    {"a": "A", "b": "B", "color": "line", "label": "3"},
    {"a": "A", "b": "C", "color": "line", "label": "4", "dashed": true}
]
```

### derived

动态派生构造。

```json
"derived": [
    {"type": "midpoint", "name": "M", "a": "A", "b": "B"},
    {"type": "intersect_line_line", "name": "P", "a": "line1", "b": "line2"},
    {"type": "foot_perp", "name": "F", "point": "P", "line": "line1"},
    {"type": "vector", "name": "vec_AB", "from": "A", "to": "B", "color": "vec"},
    {"type": "line_through_points", "name": "line1", "a": "A", "b": "B", "color": "aux", "dashed": true}
]
```

### param

参数滑块。

```json
"param": {
    "name": "t",
    "label": "点位置",
    "min": 0,
    "max": 1,
    "step": 0.01,
    "value": 0.5,
    "unit": ""
}
```

### readouts

实时读数。

```json
"readouts": [
    {"id": "len_bc", "label": "BC 长度", "type": "distance", "a": "B", "b": "C", "highlight": true},
    {"id": "area", "label": "面积", "type": "area_triangle", "pts": ["A", "B", "C"]},
    {"id": "coord_p", "label": "P 坐标", "type": "coord", "of": "P"},
    {"id": "slope_ab", "label": "AB 斜率", "type": "slope", "of": "line_ab"}
]
```

### rangeBar

范围指示器。

```json
"rangeBar": {
    "of": "readout_id",
    "min": 0,
    "max": 10,
    "label": "$[0, 10]$"
}
```

### constant

定值指示器。

```json
"constant": {
    "label": "$\\equiv 5$"
}
```

### legend

图例。

```json
"legend": [
    {"color": "#facc15", "text": "三角形"},
    {"color": "#2dd4bf", "text": "辅助线"}
]
```

## readouts 类型

| 类型 | 参数 | 说明 |
|---|---|---|
| coord | of: 点名 | 点坐标 |
| distance | a, b: 点名 | 两点距离 |
| length | of: 向量名 或 a, b: 点名 | 长度 |
| dot | a, b: 向量名 | 向量点积 |
| slope | of: 线名 | 斜率 |
| area_triangle | pts: [点名, 点名, 点名] | 三角形面积 |
| area_parallelogram | a, b, c: 点名 | 平行四边形面积 |
| distance_point_line | point: 点名, line: 线名 | 点到直线距离 |
| expr | expr: 表达式字符串 | 表达式求值 |
| status | expr, op, rhs, okText, badText | 条件状态 |

## derived 类型

| 类型 | 参数 | 说明 |
|---|---|---|
| midpoint | name, a, b | 中点 |
| foot_perp | name, point, line | 垂足 |
| intersect_line_line | name, a, b | 两直线交点 |
| line_through_points | name, a, b | 过两点直线 |
| line_through_angle | name, point, angle | 过点定角直线 |
| line_through_slope | name, point, slope | 过点定斜率直线 |
| line_through_point_dir | name, point, dir | 过点定向直线 |
| vector | name, from, to | 向量 |
| segment | name, a, b | 线段 |
| polygon | name, pts | 多边形 |

## shapes kind

| kind | 说明 |
|---|---|
| triangle | 三角形 |
| quadrilateral | 四边形 |
| circle | 圆 |
| polygon | 多边形 |

## color 语义名

| 语义名 | 颜色 | 用途 |
|---|---|---|
| line | #2dd4bf | 主要线条 |
| line2 | #38bdf8 | 次要线条 |
| aux | #94a3b8 | 辅助线 |
| curve | #facc15 | 曲线 |
| curve2 | #f472b6 | 第二条曲线 |
| point | #e2e8f0 | 普通点 |
| ptA | #f87171 | 点A |
| ptB | #60a5fa | 点B |
| fixed | #34d399 | 定点 |
| vec | #fbbf24 | 向量 |
| locus | #38bdf8 | 轨迹 |
| area | rgba(45,212,191,0.16) | 面积填充 |
