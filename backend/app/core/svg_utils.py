from __future__ import annotations

import html
import math
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

_SVG_STYLE = 'style="max-width:100%;height:auto;display:block;margin:0 auto;"'


def _esc(text: Any) -> str:
    return html.escape(str(text), quote=True)


def svg_coordinate_plane(
    *,
    x_min: int = -8,
    x_max: int = 8,
    y_min: int = -8,
    y_max: int = 8,
    width: int = 220,
    height: int = 220,
    lines: Optional[List[Dict[str, Any]]] = None,
    vertical_lines: Optional[List[Dict[str, Any]]] = None,
    points: Optional[Sequence[Any]] = None,
    shaded_half_planes: Optional[List[Dict[str, Any]]] = None,
    functions: Optional[List[Dict[str, Any]]] = None,
    asymptotes: Optional[List[Dict[str, Any]]] = None,
    circles_ellipses: Optional[List[Dict[str, Any]]] = None,
    circles: Optional[List[Dict[str, Any]]] = None,
    vectors: Optional[List[Dict[str, Any]]] = None,
    polygons: Optional[List[Dict[str, Any]]] = None,
    slope_field: Any = None,
    shaded_between: Optional[Dict[str, Any]] = None,
    riemann_boxes: Optional[Sequence[Any]] = None,
    axis_labels: Tuple[str, str] = ("x", "y"),
    show_numbers: bool = False,
    auto_expand: bool = True,
    symmetric: bool = True,
) -> str:
    """Render a clean vector coordinate plane with auto-expanding bounds so no plotted elements clip."""
    if circles and not circles_ellipses:
        circles_ellipses = circles
    if vertical_lines:
        asymptotes = list(asymptotes or []) + [
            {"x": vl["x"], "color": vl.get("color", "#dc2626")} for vl in vertical_lines
        ]

    # Auto-expand coordinate bounds so all points, circles, vectors, asymptotes, and intercepts fit with margin
    req_x: List[float] = []
    req_y: List[float] = []

    if points:
        for pt in points:
            if isinstance(pt, (tuple, list)):
                req_x.append(float(pt[0]))
                req_y.append(float(pt[1]))
            else:
                req_x.append(float(pt["x"]))
                req_y.append(float(pt["y"]))

    if circles_ellipses:
        for ce in circles_ellipses:
            ch = float(ce["h"])
            ck = float(ce["k"])
            rx_v = abs(float(ce.get("rx", ce.get("r", 1))))
            ry_v = abs(float(ce.get("ry", ce.get("r", 1))))
            req_x.extend([ch - rx_v, ch + rx_v])
            req_y.extend([ck - ry_v, ck + ry_v])

    if vectors:
        for vec in vectors:
            if "x1" in vec and "x2" in vec:
                x0, y0 = float(vec["x1"]), float(vec["y1"])
                x2_v, y2_v = float(vec["x2"]), float(vec["y2"])
            else:
                x0, y0 = float(vec.get("x0", 0.0)), float(vec.get("y0", 0.0))
                x2_v, y2_v = x0 + float(vec["dx"]), y0 + float(vec["dy"])
            req_x.extend([x0, x2_v])
            req_y.extend([y0, y2_v])

    if polygons:
        for poly in polygons:
            if poly.get("stroke") == "none":
                continue
            verts = poly.get("vertices") or poly.get("points") or []
            for vx, vy in verts:
                req_x.append(float(vx))
                req_y.append(float(vy))

    if asymptotes:
        for asym in asymptotes:
            if asym.get("x") is not None:
                req_x.append(float(asym["x"]))
            if asym.get("y") is not None:
                req_y.append(float(asym["y"]))

    if lines:
        for ln in lines:
            if ln.get("x_vert") is not None:
                req_x.append(float(ln["x_vert"]))
            else:
                b_val = float(ln.get("b", 0.0))
                if abs(b_val) <= 16:
                    req_y.append(b_val)

    if shaded_between:
        a_val = float(shaded_between["a"])
        b_val = float(shaded_between["b"])
        req_x.extend([a_val, b_val])
        fn1 = shaded_between.get("fn1") or shaded_between.get("fn_top") or (lambda _: 0.0)
        fn2 = shaded_between.get("fn2") or shaded_between.get("fn_bot") or (lambda _: 0.0)
        for i in range(9):
            xv = a_val + (b_val - a_val) * i / 8.0
            for f_chk in (fn1, fn2):
                try:
                    yv = float(f_chk(xv))
                    if math.isfinite(yv) and abs(yv) <= 30:
                        req_y.append(yv)
                except Exception:
                    pass

    if riemann_boxes:
        for box in riemann_boxes:
            if isinstance(box, (tuple, list)):
                bx0, bh, bw = float(box[0]), float(box[1]), float(box[2])
                bx1 = bx0 + bw
            else:
                bx0, bx1, bh = float(box["x0"]), float(box["x1"]), float(box["h"])
            req_x.extend([bx0, bx1])
            req_y.extend([0.0, bh])

    if functions:
        for fn_spec in functions:
            fn_c = fn_spec["fn"]
            for xv in (-3.0, -1.5, 0.0, 1.5, 3.0):
                if fn_spec.get("x_start") is not None and xv < float(fn_spec["x_start"]):
                    continue
                if fn_spec.get("x_end") is not None and xv > float(fn_spec["x_end"]):
                    continue
                try:
                    yv = float(fn_c(xv))
                    if math.isfinite(yv) and abs(yv) <= 18:
                        req_y.append(yv)
                except Exception:
                    pass

    if auto_expand and (req_x or req_y):
        if symmetric:
            b = max(abs(x_min), abs(x_max), abs(y_min), abs(y_max))
            if req_x:
                b = max(b, int(math.ceil(max(abs(v) for v in req_x))) + 2)
            if req_y:
                b = max(b, int(math.ceil(max(abs(v) for v in req_y))) + 2)
            b = min(14, b)
            x_min, x_max, y_min, y_max = -b, b, -b, b
        else:
            if req_x:
                x_min = min(x_min, int(math.floor(min(req_x))) - 2)
                x_max = max(x_max, int(math.ceil(max(req_x))) + 2)
            if req_y:
                y_min = min(y_min, int(math.floor(min(req_y))) - 2)
                y_max = max(y_max, int(math.ceil(max(req_y))) + 2)

    pad = 22.0
    plot_w = width - 2 * pad
    plot_h = height - 2 * pad
    dx = max(x_max - x_min, 1)
    dy = max(y_max - y_min, 1)

    def to_px(x: float, y: float) -> Tuple[float, float]:
        px = pad + (x - x_min) / dx * plot_w
        py = pad + (y_max - y) / dy * plot_h
        return round(px, 2), round(py, 2)

    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        "<defs>",
        f'<clipPath id="plot-clip"><rect x="{pad}" y="{pad}" width="{plot_w}" height="{plot_h}"/></clipPath>',
    ]

    # Add clip paths for shaded half planes if multiple (intersection)
    if shaded_half_planes:
        for idx, hp in enumerate(shaded_half_planes):
            poly_pts = _half_plane_polygon(hp, x_min, x_max, y_min, y_max, to_px)
            if poly_pts:
                pts_str = " ".join(f"{px},{py}" for px, py in poly_pts)
                parts.append(f'<clipPath id="hp-clip-{idx}"><polygon points="{pts_str}"/></clipPath>')

    parts.append("</defs>")

    # Background
    parts.append(f'<rect x="{pad}" y="{pad}" width="{plot_w}" height="{plot_h}" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>')

    # Grid lines
    grid_step_x = 1 if dx <= 20 else max(1, dx // 10)
    grid_step_y = 1 if dy <= 20 else max(1, dy // 10)
    for gx in range(int(math.ceil(x_min)), int(math.floor(x_max)) + 1, grid_step_x):
        px, _ = to_px(gx, 0)
        parts.append(f'<line x1="{px}" y1="{pad}" x2="{px}" y2="{height - pad}" stroke="#cbd5e1" stroke-width="0.7"/>')
    for gy in range(int(math.ceil(y_min)), int(math.floor(y_max)) + 1, grid_step_y):
        _, py = to_px(0, gy)
        parts.append(f'<line x1="{pad}" y1="{py}" x2="{width - pad}" y2="{py}" stroke="#cbd5e1" stroke-width="0.7"/>')

    # Shaded half-planes (or intersection of multiple)
    if shaded_half_planes:
        if len(shaded_half_planes) == 1:
            hp = shaded_half_planes[0]
            color = hp.get("color", "#3b82f6")
            poly_pts = _half_plane_polygon(hp, x_min, x_max, y_min, y_max, to_px)
            if poly_pts:
                pts_str = " ".join(f"{px},{py}" for px, py in poly_pts)
                parts.append(
                    f'<polygon points="{pts_str}" fill="{color}" fill-opacity="0.22" clip-path="url(#plot-clip)"/>'
                )
        else:
            color = shaded_half_planes[0].get("color", "#2563eb")
            inner = f'<rect x="{pad}" y="{pad}" width="{plot_w}" height="{plot_h}" fill="{color}" fill-opacity="0.26"/>'
            for idx in range(len(shaded_half_planes) - 1, -1, -1):
                inner = f'<g clip-path="url(#hp-clip-{idx})">{inner}</g>'
            parts.append(f'<g clip-path="url(#plot-clip)">{inner}</g>')

    # Shaded area between curves
    if shaded_between:
        fn1 = shaded_between.get("fn1") or shaded_between.get("fn_top") or (lambda _: 0.0)
        fn2 = shaded_between.get("fn2") or shaded_between.get("fn_bot") or (lambda _: 0.0)
        a_val = float(shaded_between["a"])
        b_val = float(shaded_between["b"])
        color = shaded_between.get("color", "#3b82f6")
        steps = 60
        top_pts: List[str] = []
        bot_pts: List[str] = []
        for i in range(steps + 1):
            xv = a_val + (b_val - a_val) * i / steps
            try:
                y1 = float(fn1(xv))
                y2 = float(fn2(xv))
                px1, py1 = to_px(xv, max(min(y1, y_max * 2), y_min * 2))
                px2, py2 = to_px(xv, max(min(y2, y_max * 2), y_min * 2))
                top_pts.append(f"{px1},{py1}")
                bot_pts.append(f"{px2},{py2}")
            except Exception:
                continue
        if top_pts and bot_pts:
            poly_str = " ".join(top_pts + list(reversed(bot_pts)))
            parts.append(
                f'<polygon points="{poly_str}" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="1" clip-path="url(#plot-clip)"/>'
            )

    # Riemann rectangles
    if riemann_boxes:
        for box in riemann_boxes:
            if isinstance(box, (tuple, list)):
                bx0, bh, bw = float(box[0]), float(box[1]), float(box[2])
                bx1 = bx0 + bw
            else:
                bx0, bx1, bh = float(box["x0"]), float(box["x1"]), float(box["h"])
            px0, py0 = to_px(bx0, max(0.0, bh))
            px1, py1 = to_px(bx1, min(0.0, bh))
            rw = max(1.0, abs(px1 - px0))
            rh = max(1.0, abs(py1 - py0))
            parts.append(
                f'<rect x="{min(px0, px1)}" y="{min(py0, py1)}" width="{rw}" height="{rh}" '
                f'fill="#60a5fa" fill-opacity="0.3" stroke="#2563eb" stroke-width="1" clip-path="url(#plot-clip)"/>'
            )

    # Axes
    ox, oy = to_px(0, 0)
    ox_clamped = min(max(ox, pad), width - pad)
    oy_clamped = min(max(oy, pad), height - pad)
    parts.append(f'<line x1="{pad}" y1="{oy_clamped}" x2="{width - pad}" y2="{oy_clamped}" stroke="#0f172a" stroke-width="2.0"/>')
    parts.append(f'<line x1="{ox_clamped}" y1="{pad}" x2="{ox_clamped}" y2="{height - pad}" stroke="#0f172a" stroke-width="2.0"/>')

    # Tick marks & optional numbers
    label_step_x = grid_step_x * 2 if dx >= 10 else grid_step_x
    label_step_y = grid_step_y * 2 if dy >= 10 else grid_step_y
    for gx in range(int(math.ceil(x_min)), int(math.floor(x_max)) + 1):
        if gx == 0:
            continue
        px, _ = to_px(gx, 0)
        parts.append(f'<line x1="{px}" y1="{oy_clamped - 2.5}" x2="{px}" y2="{oy_clamped + 2.5}" stroke="#0f172a" stroke-width="1.2"/>')
        if show_numbers and gx % label_step_x == 0 and pad + 8 <= px <= width - pad - 8:
            parts.append(f'<text x="{px}" y="{min(oy_clamped + 11, height - 5)}" font-family="sans-serif" font-size="10.5" font-weight="700" fill="#0f172a" text-anchor="middle">{gx}</text>')
    for gy in range(int(math.ceil(y_min)), int(math.floor(y_max)) + 1):
        if gy == 0:
            continue
        _, py = to_px(0, gy)
        parts.append(f'<line x1="{ox_clamped - 2.5}" y1="{py}" x2="{ox_clamped + 2.5}" y2="{py}" stroke="#0f172a" stroke-width="1.2"/>')
        if show_numbers and gy % label_step_y == 0 and pad + 6 <= py <= height - pad - 6:
            parts.append(f'<text x="{max(ox_clamped - 4, pad + 10)}" y="{py + 3}" font-family="sans-serif" font-size="10.5" font-weight="700" fill="#0f172a" text-anchor="end">{gy}</text>')

    # Axis names
    parts.append(f'<text x="{width - pad + 5}" y="{oy_clamped + 3.5}" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0f172a">{_esc(axis_labels[0])}</text>')
    parts.append(f'<text x="{ox_clamped}" y="{pad - 6}" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">{_esc(axis_labels[1])}</text>')

    # Slope field
    if slope_field is not None:
        sf_fn = slope_field["fn"] if isinstance(slope_field, dict) else slope_field
        sf_step = int(slope_field.get("step", grid_step_x)) if isinstance(slope_field, dict) else grid_step_x
        seg_len = 0.32 * min(grid_step_x, grid_step_y) * max(1, sf_step)
        for gx in range(int(math.ceil(x_min)) + 1, int(math.floor(x_max)), sf_step):
            for gy in range(int(math.ceil(y_min)) + 1, int(math.floor(y_max)), sf_step):
                try:
                    m_val = sf_fn(float(gx), float(gy))
                    if m_val is None or math.isnan(m_val) or math.isinf(m_val):
                        continue
                    ang = math.atan(m_val)
                    dx_s = seg_len * math.cos(ang)
                    dy_s = seg_len * math.sin(ang)
                    x1, y1 = to_px(gx - dx_s, gy - dy_s)
                    x2, y2 = to_px(gx + dx_s, gy + dy_s)
                    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#475569" stroke-width="1.1"/>')
                except Exception:
                    continue

    # Asymptotes
    if asymptotes:
        for asym in asymptotes:
            color = asym.get("color", "#475569")
            if asym.get("x") is not None:
                px, _ = to_px(float(asym["x"]), 0)
                parts.append(f'<line x1="{px}" y1="{pad}" x2="{px}" y2="{height - pad}" stroke="{color}" stroke-width="1.6" stroke-dasharray="5,3" clip-path="url(#plot-clip)"/>')
            if asym.get("y") is not None:
                _, py = to_px(0, float(asym["y"]))
                parts.append(f'<line x1="{pad}" y1="{py}" x2="{width - pad}" y2="{py}" stroke="{color}" stroke-width="1.6" stroke-dasharray="5,3" clip-path="url(#plot-clip)"/>')
            if asym.get("m") is not None and asym.get("b") is not None:
                m_a = float(asym["m"])
                b_a = float(asym["b"])
                x1, y1 = to_px(x_min, m_a * x_min + b_a)
                x2, y2 = to_px(x_max, m_a * x_max + b_a)
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.6" stroke-dasharray="5,3" clip-path="url(#plot-clip)"/>')

    # Polygons
    if polygons:
        for poly in polygons:
            verts = poly.get("vertices") or poly.get("points") or []
            if not verts:
                continue
            color = poly.get("color") or poly.get("stroke") or "#2563eb"
            fill = poly.get("fill", color)
            dash = ' stroke-dasharray="4,3"' if poly.get("dashed") else ""
            px_verts = [to_px(vx, vy) for vx, vy in verts]
            pts_str = " ".join(f"{px},{py}" for px, py in px_verts)
            parts.append(
                f'<polygon points="{pts_str}" fill="{fill}" fill-opacity="0.18" stroke="{color}" stroke-width="1.6"{dash} clip-path="url(#plot-clip)"/>'
            )
            labels = poly.get("labels", [])
            for idx, (px, py) in enumerate(px_verts):
                if poly.get("stroke") != "none":
                    parts.append(f'<circle cx="{px}" cy="{py}" r="2.5" fill="{color}"/>')
                if idx < len(labels) and labels[idx]:
                    anchor = "end" if px > width - pad - 28 else "start"
                    lx = round(px - 4, 2) if anchor == "end" else round(px + 4, 2)
                    ly = round(py + 10, 2) if py < pad + 14 else round(py - 4, 2)
                    parts.append(f'<text x="{lx}" y="{ly}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="{color}" text-anchor="{anchor}">{_esc(labels[idx])}</text>')

    # Circles / Ellipses
    if circles_ellipses:
        for ce in circles_ellipses:
            cx, cy = to_px(float(ce["h"]), float(ce["k"]))
            rx = abs(float(ce.get("rx", ce.get("r", 1)))) / dx * plot_w
            ry = abs(float(ce.get("ry", ce.get("r", 1)))) / dy * plot_h
            color = ce.get("color", "#dc2626")
            dash = ' stroke-dasharray="4,3"' if ce.get("dashed") else ""
            parts.append(
                f'<ellipse cx="{cx}" cy="{cy}" rx="{round(rx, 2)}" ry="{round(ry, 2)}" fill="none" stroke="{color}" stroke-width="1.8"{dash} clip-path="url(#plot-clip)"/>'
            )

    # Lines
    if lines:
        for ln in lines:
            color = ln.get("color", "#dc2626")
            dash = ' stroke-dasharray="4,3"' if ln.get("dashed") else ""
            if ln.get("x_vert") is not None:
                xv = float(ln["x_vert"])
                x1, y1 = to_px(xv, y_min)
                x2, y2 = to_px(xv, y_max)
            else:
                m_val = float(ln.get("m", 0.0))
                b_val = float(ln.get("b", 0.0))
                x1, y1 = to_px(x_min, m_val * x_min + b_val)
                x2, y2 = to_px(x_max, m_val * x_max + b_val)
            parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.4"{dash} clip-path="url(#plot-clip)"/>'
            )

    # Continuous functions
    if functions:
        for fn_spec in functions:
            fn = fn_spec["fn"]
            color = fn_spec.get("color", "#dc2626")
            dash = ' stroke-dasharray="4,3"' if fn_spec.get("dashed") else ""
            if fn_spec.get("x_start") is not None or fn_spec.get("x_end") is not None:
                ranges = [(float(fn_spec.get("x_start", x_min)), float(fn_spec.get("x_end", x_max)))]
            else:
                ranges = fn_spec.get("x_ranges") or [(float(x_min), float(x_max))]
            for r_start, r_end in ranges:
                samples = 140
                segment: List[str] = []
                prev_y: Optional[float] = None
                for i in range(samples + 1):
                    xv = r_start + (r_end - r_start) * i / samples
                    try:
                        yv = fn(xv)
                        if yv is None or isinstance(yv, complex) or math.isnan(yv) or math.isinf(yv):
                            if len(segment) >= 2:
                                parts.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{color}" stroke-width="2.4"{dash} clip-path="url(#plot-clip)"/>')
                            segment = []
                            prev_y = None
                            continue
                        if abs(yv) > max(abs(y_min), abs(y_max)) * 6 or (prev_y is not None and abs(yv - prev_y) > dy * 1.5):
                            if len(segment) >= 2:
                                parts.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{color}" stroke-width="2.4"{dash} clip-path="url(#plot-clip)"/>')
                            segment = []
                        px, py = to_px(xv, yv)
                        segment.append(f"{px},{py}")
                        prev_y = yv
                    except Exception:
                        if len(segment) >= 2:
                            parts.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{color}" stroke-width="2.4"{dash} clip-path="url(#plot-clip)"/>')
                        segment = []
                        prev_y = None
                if len(segment) >= 2:
                    parts.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{color}" stroke-width="2.4"{dash} clip-path="url(#plot-clip)"/>')

    # Vectors
    if vectors:
        for vec in vectors:
            if "x1" in vec and "x2" in vec:
                x0 = float(vec["x1"])
                y0 = float(vec["y1"])
                vx = float(vec["x2"]) - x0
                vy = float(vec["y2"]) - y0
            else:
                x0 = float(vec.get("x0", 0.0))
                y0 = float(vec.get("y0", 0.0))
                vx = float(vec["dx"])
                vy = float(vec["dy"])
            color = vec.get("color", "#dc2626")
            x1, y1 = to_px(x0, y0)
            x2, y2 = to_px(x0 + vx, y0 + vy)
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" clip-path="url(#plot-clip)"/>')
            ang = math.atan2(y2 - y1, x2 - x1)
            ah = 6.0
            ax1 = round(x2 - ah * math.cos(ang - 0.45), 2)
            ay1 = round(y2 - ah * math.sin(ang - 0.45), 2)
            ax2 = round(x2 - ah * math.cos(ang + 0.45), 2)
            ay2 = round(y2 - ah * math.sin(ang + 0.45), 2)
            parts.append(f'<polygon points="{x2},{y2} {ax1},{ay1} {ax2},{ay2}" fill="{color}"/>')
            if vec.get("label"):
                mx = round((x1 + x2) / 2, 2)
                my = round((y1 + y2) / 2, 2)
                anchor = "end" if mx > width - pad - 35 else "start"
                lx = round(mx - 4, 2) if anchor == "end" else round(mx + 4, 2)
                ly = round(my + 10, 2) if my < pad + 14 else round(my - 4, 2)
                parts.append(f'<text x="{lx}" y="{ly}" font-family="sans-serif" font-size="8" font-weight="bold" fill="{color}" text-anchor="{anchor}">{_esc(vec["label"])}</text>')

    # Points
    if points:
        for pt in points:
            if isinstance(pt, (tuple, list)):
                pt_x, pt_y = float(pt[0]), float(pt[1])
                lbl = str(pt[2]) if len(pt) > 2 else ""
                is_closed = bool(pt[3]) if len(pt) > 3 else True
                is_open = not is_closed
                color = "#dc2626"
            else:
                pt_x, pt_y = float(pt["x"]), float(pt["y"])
                color = pt.get("color", "#dc2626")
                is_open = bool(pt.get("open", False))
                lbl = str(pt.get("label", ""))

            # Skip points far outside visible coordinate bounds
            if pt_x < x_min - 0.5 or pt_x > x_max + 0.5 or pt_y < y_min - 0.5 or pt_y > y_max + 0.5:
                continue

            px, py = to_px(pt_x, pt_y)
            r_pt = 3.6
            px_c = round(max(r_pt + 0.5, min(width - r_pt - 0.5, px)), 2)
            py_c = round(max(r_pt + 0.5, min(height - r_pt - 0.5, py)), 2)
            fill = "#ffffff" if is_open else color
            parts.append(f'<circle cx="{px_c}" cy="{py_c}" r="{r_pt}" fill="{fill}" stroke="{color}" stroke-width="1.8"/>')
            if lbl:
                anchor = "end" if px_c > width - pad - 36 else "start"
                lx = round(px_c - 5, 2) if anchor == "end" else round(px_c + 5, 2)
                ly = round(py_c + 11, 2) if py_c < pad + 14 else round(py_c - 5, 2)
                lx_c = round(max(10.0, min(width - 10.0, lx)), 2)
                ly_c = round(max(10.0, min(height - 10.0, ly)), 2)
                parts.append(f'<text x="{lx_c}" y="{ly_c}" font-family="sans-serif" font-size="9" font-weight="bold" fill="{color}" text-anchor="{anchor}">{_esc(lbl)}</text>')

    parts.append("</svg>")
    return "".join(parts)

def svg_coordinate_plane_pair(
    *,
    x_min: int = -8,
    x_max: int = 8,
    y_min: int = -8,
    y_max: int = 8,
    width: int = 220,
    height: int = 220,
    axis_labels: Tuple[str, str] = ("x", "y"),
    show_numbers: bool = False,
    symmetric: bool = True,
    **kwargs: Any,
) -> Tuple[str, str]:
    """Generate (diagram_svg, answer_svg) guaranteed to have 100% identical bounds, aspect ratio, and origin."""
    req_x: List[float] = []
    req_y: List[float] = []
    if kwargs.get("points"):
        for pt in kwargs["points"]:
            if isinstance(pt, (tuple, list)):
                req_x.append(float(pt[0]))
                req_y.append(float(pt[1]))
            else:
                req_x.append(float(pt["x"]))
                req_y.append(float(pt["y"]))
    if kwargs.get("lines"):
        for ln in kwargs["lines"]:
            if ln.get("x_vert") is not None:
                req_x.append(float(ln["x_vert"]))
            else:
                b_val = float(ln.get("b", 0.0))
                if abs(b_val) <= 16:
                    req_y.append(b_val)
    if kwargs.get("asymptotes"):
        for asym in kwargs["asymptotes"]:
            if asym.get("x") is not None:
                req_x.append(float(asym["x"]))
            if asym.get("y") is not None:
                req_y.append(float(asym["y"]))

    b = max(abs(x_min), abs(x_max), abs(y_min), abs(y_max))
    if req_x:
        b = max(b, int(math.ceil(max(abs(v) for v in req_x))) + 2)
    if req_y:
        b = max(b, int(math.ceil(max(abs(v) for v in req_y))) + 2)
    b = min(14, b)

    final_min, final_max = (-b, b) if symmetric else (x_min, x_max)

    diagram = svg_coordinate_plane(
        x_min=final_min,
        x_max=final_max,
        y_min=final_min,
        y_max=final_max,
        width=width,
        height=height,
        axis_labels=axis_labels,
        show_numbers=show_numbers,
        auto_expand=False,
        symmetric=symmetric,
    )
    answer = svg_coordinate_plane(
        x_min=final_min,
        x_max=final_max,
        y_min=final_min,
        y_max=final_max,
        width=width,
        height=height,
        axis_labels=axis_labels,
        show_numbers=show_numbers,
        auto_expand=False,
        symmetric=symmetric,
        **kwargs,
    )
    return diagram, answer



def _half_plane_polygon(
    hp: Dict[str, Any],
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    to_px: Callable[[float, float], Tuple[float, float]],
) -> List[Tuple[float, float]]:
    op = str(hp.get("op", ">="))
    big = 100.0
    if hp.get("x_vert") is not None:
        xv = float(hp["x_vert"])
        if ">" in op:
            corners = [(xv, y_min - big), (x_max + big, y_min - big), (x_max + big, y_max + big), (xv, y_max + big)]
        else:
            corners = [(x_min - big, y_min - big), (xv, y_min - big), (xv, y_max + big), (x_min - big, y_max + big)]
    else:
        m = float(hp.get("m", 0.0))
        b = float(hp.get("b", 0.0))
        xl = x_min - big
        xr = x_max + big
        yl = m * xl + b
        yr = m * xr + b
        if ">" in op:
            corners = [(xl, yl), (xr, yr), (xr, y_max + big * 10), (xl, y_max + big * 10)]
        else:
            corners = [(xl, yl), (xr, yr), (xr, y_min - big * 10), (xl, y_min - big * 10)]
    return [to_px(cx, cy) for cx, cy in corners]


def svg_number_line(
    *,
    min_val: int = -10,
    max_val: int = 10,
    width: int = 240,
    height: int = 62,
    intervals: Optional[List[Dict[str, Any]]] = None,
    rays: Optional[Sequence[Tuple[float, str, bool]]] = None,
    segments: Optional[Sequence[Tuple[float, float, bool, bool]]] = None,
    points: Optional[Sequence[Any]] = None,
) -> str:
    """Render a number line with auto-expanding range so rays, segments, and points never clip."""
    intervals = list(intervals or [])
    if rays:
        for val, direction, closed in rays:
            intervals.append({"type": "ray", "val": val, "dir": direction, "closed": closed})
    if segments:
        for a, b, closed_a, closed_b in segments:
            intervals.append({"type": "segment", "a": a, "b": b, "closed_a": closed_a, "closed_b": closed_b})

    req_vals: List[float] = []
    for iv in intervals:
        if iv.get("type", "ray") == "ray":
            req_vals.append(float(iv["val"]))
        elif iv.get("type") == "segment":
            req_vals.extend([float(iv["a"]), float(iv["b"])])
    if points:
        for pt in points:
            req_vals.append(float(pt[0]) if isinstance(pt, (tuple, list)) else float(pt["val"]))
    if req_vals:
        min_val = min(min_val, int(math.floor(min(req_vals))) - 2)
        max_val = max(max_val, int(math.ceil(max(req_vals))) + 2)

    pad = 22.0
    line_y = 34.0
    span = max(max_val - min_val, 1)
    plot_w = width - 2 * pad

    def to_x(v: float) -> float:
        return round(pad + (v - min_val) / span * plot_w, 2)

    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<line x1="{pad - 8}" y1="{line_y}" x2="{width - pad + 8}" y2="{line_y}" stroke="#334155" stroke-width="1.5"/>',
        f'<polygon points="{pad - 10},{line_y} {pad - 4},{line_y - 3.5} {pad - 4},{line_y + 3.5}" fill="#334155"/>',
        f'<polygon points="{width - pad + 10},{line_y} {width - pad + 4},{line_y - 3.5} {width - pad + 4},{line_y + 3.5}" fill="#334155"/>',
    ]

    step = 1 if span <= 14 else (2 if span <= 24 else max(1, span // 10))
    for v in range(min_val, max_val + 1):
        xv = to_x(v)
        parts.append(f'<line x1="{xv}" y1="{line_y - 4}" x2="{xv}" y2="{line_y + 4}" stroke="#475569" stroke-width="1"/>')
        if v % step == 0:
            parts.append(f'<text x="{xv}" y="{line_y + 15}" font-family="sans-serif" font-size="7.5" fill="#334155" text-anchor="middle">{v}</text>')

    if intervals:
        for iv in intervals:
            color = iv.get("color", "#dc2626")
            kind = iv.get("type", "ray")
            if kind == "ray":
                val = float(iv["val"])
                xv = to_x(val)
                direction = iv.get("dir", "right")
                closed = bool(iv.get("closed", False))
                if direction == "right":
                    end_x = width - pad + 8
                    parts.append(f'<line x1="{xv}" y1="{line_y}" x2="{end_x}" y2="{line_y}" stroke="{color}" stroke-width="3.2"/>')
                    parts.append(f'<polygon points="{end_x + 3},{line_y} {end_x - 4},{line_y - 4} {end_x - 4},{line_y + 4}" fill="{color}"/>')
                else:
                    end_x = pad - 8
                    parts.append(f'<line x1="{xv}" y1="{line_y}" x2="{end_x}" y2="{line_y}" stroke="{color}" stroke-width="3.2"/>')
                    parts.append(f'<polygon points="{end_x - 3},{line_y} {end_x + 4},{line_y - 4} {end_x + 4},{line_y + 4}" fill="{color}"/>')
                fill = color if closed else "#ffffff"
                parts.append(f'<circle cx="{xv}" cy="{line_y}" r="4.2" fill="{fill}" stroke="{color}" stroke-width="2"/>')
            elif kind == "segment":
                x1 = to_x(float(iv["a"]))
                x2 = to_x(float(iv["b"]))
                c1 = color if iv.get("closed_a", False) else "#ffffff"
                c2 = color if iv.get("closed_b", False) else "#ffffff"
                parts.append(f'<line x1="{x1}" y1="{line_y}" x2="{x2}" y2="{line_y}" stroke="{color}" stroke-width="3.2"/>')
                parts.append(f'<circle cx="{x1}" cy="{line_y}" r="4.2" fill="{c1}" stroke="{color}" stroke-width="2"/>')
                parts.append(f'<circle cx="{x2}" cy="{line_y}" r="4.2" fill="{c2}" stroke="{color}" stroke-width="2"/>')

    if points:
        for pt in points:
            if isinstance(pt, (tuple, list)):
                xv = to_x(float(pt[0]))
                lbl = str(pt[1]) if len(pt) > 1 else ""
                color = "#2563eb"
            else:
                xv = to_x(float(pt["val"]))
                color = pt.get("color", "#2563eb")
                lbl = str(pt.get("label", ""))
            parts.append(f'<circle cx="{xv}" cy="{line_y}" r="4" fill="{color}" stroke="#ffffff" stroke-width="1"/>')
            if lbl:
                anchor = "start" if xv < pad + 18 else ("end" if xv > width - pad - 18 else "middle")
                parts.append(f'<text x="{xv}" y="{line_y - 8}" font-family="sans-serif" font-size="8" font-weight="bold" fill="{color}" text-anchor="{anchor}">{_esc(lbl)}</text>')

    parts.append("</svg>")
    return "".join(parts)


def svg_polar_grid(
    *,
    max_r: int = 5,
    width: int = 210,
    height: int = 210,
    points: Optional[List[Tuple[float, float, str]]] = None,
    curve_fn: Optional[Callable[[float], float]] = None,
    curve_points: Optional[Sequence[Tuple[float, float]]] = None,
) -> str:
    """Render a polar coordinate grid with optional plotted polar points or polar curve."""
    req_r: List[float] = []
    if points:
        for rv, _, _ in points:
            req_r.append(abs(float(rv)))
    if curve_points:
        for rv, _ in curve_points:
            req_r.append(abs(float(rv)))
    if req_r:
        max_r = max(max_r, int(math.ceil(max(req_r))) + 1)

    cx, cy = width / 2.0, height / 2.0
    max_px = min(width, height) / 2.0 - 22.0
    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
    ]
    for r in range(1, max_r + 1):
        rad = round(r / max_r * max_px, 2)
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="#cbd5e1" stroke-width="0.8"/>')
        parts.append(f'<text x="{round(cx + rad + 2, 1)}" y="{cy + 8}" font-family="sans-serif" font-size="6.5" fill="#64748b">{r}</text>')

    for deg in range(0, 360, 30):
        ang = math.radians(deg)
        x2 = round(cx + max_px * math.cos(ang), 2)
        y2 = round(cy - max_px * math.sin(ang), 2)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="#e2e8f0" stroke-width="0.8"/>')
        if deg in (0, 90, 180, 270):
            lx = round(cx + (max_px + 10) * math.cos(ang), 2)
            ly = round(cy - (max_px + 10) * math.sin(ang) + 3, 2)
            parts.append(f'<text x="{lx}" y="{ly}" font-family="sans-serif" font-size="7" fill="#334155" text-anchor="middle">{deg}°</text>')

    if curve_fn is not None:
        pts: List[str] = []
        steps = 180
        for i in range(steps + 1):
            th = 2 * math.pi * i / steps
            rv = curve_fn(th)
            px = round(cx + (rv / max_r * max_px) * math.cos(th), 2)
            py = round(cy - (rv / max_r * max_px) * math.sin(th), 2)
            pts.append(f"{px},{py}")
        parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#dc2626" stroke-width="1.8"/>')

    if curve_points:
        pts_c: List[str] = []
        for rv, deg_val in curve_points:
            th = math.radians(deg_val)
            px = round(cx + (rv / max_r * max_px) * math.cos(th), 2)
            py = round(cy - (rv / max_r * max_px) * math.sin(th), 2)
            pts_c.append(f"{px},{py}")
        parts.append(f'<polyline points="{" ".join(pts_c)}" fill="none" stroke="#dc2626" stroke-width="1.8"/>')

    if points:
        for rv, th_val, lbl in points:
            th_rad = math.radians(th_val) if abs(th_val) > 2 * math.pi + 0.1 else th_val
            px = round(cx + (rv / max_r * max_px) * math.cos(th_rad), 2)
            py = round(cy - (rv / max_r * max_px) * math.sin(th_rad), 2)
            parts.append(f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#2563eb" stroke-width="1.4"/>')
            parts.append(f'<circle cx="{px}" cy="{py}" r="3.5" fill="#dc2626"/>')
            if lbl:
                anchor = "end" if px > width - 38 else "start"
                lx = round(px - 5, 2) if anchor == "end" else round(px + 5, 2)
                ly = round(py + 11, 2) if py < 22 else round(py - 4, 2)
                parts.append(f'<text x="{lx}" y="{ly}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626" text-anchor="{anchor}">{_esc(lbl)}</text>')

    parts.append("</svg>")
    return "".join(parts)


def svg_dot_plot(data: Any, title: str = "Dot Plot") -> str:
    """Render a statistical dot plot for integer data or a frequency dictionary."""
    if isinstance(data, dict):
        counts: Dict[int, int] = {int(k): int(v) for k, v in data.items()}
        min_v = min(counts.keys()) - 1
        max_v = max(counts.keys()) + 1
    else:
        seq = list(data) if data else [1, 2, 2, 3]
        min_v = min(seq) - 1
        max_v = max(seq) + 1
        counts = {}
        for x in seq:
            counts[x] = counts.get(x, 0) + 1
    max_c = max(counts.values())
    width = 230
    height = max(78, 44 + max_c * 11)
    pad = 22.0
    line_y = height - 20.0
    span = max(max_v - min_v, 1)

    def to_x(v: int) -> float:
        return round(pad + (v - min_v) / span * (width - 2 * pad), 2)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<text x="{width / 2}" y="12" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(title)}</text>',
        f'<line x1="{pad}" y1="{line_y}" x2="{width - pad}" y2="{line_y}" stroke="#334155" stroke-width="1.5"/>',
    ]
    for v in range(min_v, max_v + 1):
        xv = to_x(v)
        parts.append(f'<line x1="{xv}" y1="{line_y - 3}" x2="{xv}" y2="{line_y + 3}" stroke="#334155" stroke-width="1"/>')
        parts.append(f'<text x="{xv}" y="{line_y + 12}" font-family="sans-serif" font-size="7.5" fill="#334155" text-anchor="middle">{v}</text>')
        for c in range(counts.get(v, 0)):
            cy = round(line_y - 9 - c * 10, 2)
            parts.append(f'<circle cx="{xv}" cy="{cy}" r="3.6" fill="#2563eb"/>')
    parts.append("</svg>")
    return "".join(parts)


def svg_histogram(bins: Sequence[Tuple[str, int]], title: str = "Histogram") -> str:
    """Render a statistical histogram / bar chart."""
    width, height = 230, 128
    pad_l, pad_r, pad_t, pad_b = 26.0, 16.0, 20.0, 24.0
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    max_freq = max([b[1] for b in bins] + [4])
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<text x="{width / 2}" y="12" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(title)}</text>',
    ]
    step_y = 1 if max_freq <= 6 else 2
    for fy in range(0, max_freq + 1, step_y):
        py = round(pad_t + plot_h - (fy / max_freq) * plot_h, 2)
        parts.append(f'<line x1="{pad_l}" y1="{py}" x2="{width - pad_r}" y2="{py}" stroke="#e2e8f0" stroke-width="0.7"/>')
        parts.append(f'<text x="{pad_l - 4}" y="{py + 2.5}" font-family="sans-serif" font-size="7" fill="#475569" text-anchor="end">{fy}</text>')

    parts.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#334155" stroke-width="1.3"/>')
    parts.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{width - pad_r}" y2="{pad_t + plot_h}" stroke="#334155" stroke-width="1.3"/>')

    nb = max(len(bins), 1)
    bw = plot_w / nb
    for idx, (lbl, freq) in enumerate(bins):
        bx = round(pad_l + idx * bw, 2)
        bh = round((freq / max_freq) * plot_h, 2)
        by = round(pad_t + plot_h - bh, 2)
        parts.append(f'<rect x="{bx}" y="{by}" width="{round(bw, 2)}" height="{bh}" fill="#60a5fa" fill-opacity="0.75" stroke="#1d4ed8" stroke-width="1"/>')
        parts.append(f'<text x="{round(bx + bw / 2, 2)}" y="{pad_t + plot_h + 12}" font-family="sans-serif" font-size="6.8" fill="#334155" text-anchor="middle">{_esc(lbl)}</text>')
        parts.append(f'<text x="{round(bx + bw / 2, 2)}" y="{max(by - 3, pad_t + 8)}" font-family="sans-serif" font-size="7" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{freq}</text>')

    parts.append("</svg>")
    return "".join(parts)


def svg_box_plot(
    min_v: float,
    q1: float,
    med: float,
    q3: float,
    max_v: float,
    title: str = "Box-and-Whisker Plot",
) -> str:
    """Render a 5-number summary box-and-whisker plot above a number line."""
    width, height = 240, 84
    pad = 22.0
    lo = int(math.floor(min_v)) - 1
    hi = int(math.ceil(max_v)) + 1
    span = max(hi - lo, 1)
    plot_w = width - 2 * pad
    line_y = 60.0
    box_y = 26.0
    box_h = 18.0
    mid_y = box_y + box_h / 2.0

    def to_x(v: float) -> float:
        return round(pad + (v - lo) / span * plot_w, 2)

    x_min, x_q1, x_med, x_q3, x_max = to_x(min_v), to_x(q1), to_x(med), to_x(q3), to_x(max_v)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<text x="{width / 2}" y="12" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(title)}</text>',
        f'<line x1="{pad}" y1="{line_y}" x2="{width - pad}" y2="{line_y}" stroke="#334155" stroke-width="1.3"/>',
    ]
    step = 1 if span <= 12 else (2 if span <= 24 else max(1, span // 8))
    for v in range(lo, hi + 1, step):
        xv = to_x(v)
        parts.append(f'<line x1="{xv}" y1="{line_y - 3}" x2="{xv}" y2="{line_y + 3}" stroke="#334155" stroke-width="1"/>')
        parts.append(f'<text x="{xv}" y="{line_y + 12}" font-family="sans-serif" font-size="7" fill="#334155" text-anchor="middle">{v}</text>')

    parts.append(f'<line x1="{x_min}" y1="{mid_y}" x2="{x_q1}" y2="{mid_y}" stroke="#1d4ed8" stroke-width="1.6"/>')
    parts.append(f'<line x1="{x_q3}" y1="{mid_y}" x2="{x_max}" y2="{mid_y}" stroke="#1d4ed8" stroke-width="1.6"/>')
    parts.append(f'<line x1="{x_min}" y1="{box_y + 3}" x2="{x_min}" y2="{box_y + box_h - 3}" stroke="#1d4ed8" stroke-width="1.6"/>')
    parts.append(f'<line x1="{x_max}" y1="{box_y + 3}" x2="{x_max}" y2="{box_y + box_h - 3}" stroke="#1d4ed8" stroke-width="1.6"/>')
    parts.append(f'<rect x="{x_q1}" y="{box_y}" width="{max(2.0, round(x_q3 - x_q1, 2))}" height="{box_h}" fill="#93c5fd" fill-opacity="0.45" stroke="#1d4ed8" stroke-width="1.6"/>')
    parts.append(f'<line x1="{x_med}" y1="{box_y}" x2="{x_med}" y2="{box_y + box_h}" stroke="#dc2626" stroke-width="2"/>')
    parts.append("</svg>")
    return "".join(parts)


def svg_pie_chart(slices: Sequence[Tuple[str, float, str]], title: str = "Circle Graph") -> str:
    """Render a labeled pie/circle graph. Each slice is (label, percentage_0_to_100, color)."""
    width, height = 225, 130
    cx, cy, r = 65.0, 70.0, 44.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<text x="{width / 2}" y="13" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(title)}</text>',
    ]
    angle_acc = -math.pi / 2
    for idx, (lbl, pct, color) in enumerate(slices):
        sweep = (pct / 100.0) * 2 * math.pi
        a1 = angle_acc
        a2 = angle_acc + sweep
        x1, y1 = round(cx + r * math.cos(a1), 2), round(cy + r * math.sin(a1), 2)
        x2, y2 = round(cx + r * math.cos(a2), 2), round(cy + r * math.sin(a2), 2)
        large = 1 if sweep > math.pi else 0
        parts.append(f'<path d="M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large} 1 {x2} {y2} Z" fill="{color}" stroke="#ffffff" stroke-width="1.2"/>')
        ly = 32 + idx * 18
        parts.append(f'<rect x="120" y="{ly - 7}" width="9" height="9" fill="{color}"/>')
        parts.append(f'<text x="133" y="{ly}" font-family="sans-serif" font-size="7.5" fill="#1e293b">{_esc(lbl)} ({pct:g}%)</text>')
        angle_acc = a2
    parts.append("</svg>")
    return "".join(parts)


def svg_venn_diagram(
    only_a: Any = 0,
    both: Any = 0,
    only_b: Any = 0,
    neither: Any = 0,
    label_a: str = "A",
    label_b: str = "B",
) -> str:
    """Render a two-set Venn diagram with counts."""
    width, height = 215, 120
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<rect x="4" y="4" width="{width - 8}" height="{height - 8}" fill="#f8fafc" stroke="#64748b" stroke-width="1.2"/>',
        '<circle cx="82" cy="62" r="38" fill="#60a5fa" fill-opacity="0.28" stroke="#2563eb" stroke-width="1.5"/>',
        '<circle cx="128" cy="62" r="38" fill="#f87171" fill-opacity="0.28" stroke="#dc2626" stroke-width="1.5"/>',
        f'<text x="65" y="20" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af" text-anchor="middle">{_esc(label_a)}</text>',
        f'<text x="145" y="20" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#991b1b" text-anchor="middle">{_esc(label_b)}</text>',
        f'<text x="64" y="65" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(only_a)}</text>',
        f'<text x="105" y="65" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(both)}</text>',
        f'<text x="146" y="65" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(only_b)}</text>',
        f'<text x="{width - 12}" y="{height - 10}" font-family="sans-serif" font-size="7.5" fill="#475569" text-anchor="end">{_esc(neither)}</text>',
        "</svg>",
    ]
    return "".join(parts)


def svg_data_table(
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    title: str = "",
) -> str:
    """Render a crisp vector data table with auto-sized column widths so cell text never overflows."""
    n_cols = max(len(headers), 1)
    n_rows = len(rows) + 1
    max_chars = max(
        [len(str(h)) for h in headers] + [len(str(c)) for row in rows for c in row] + [4]
    )
    col_w = max(40, min(92, max(220 // n_cols, max_chars * 5 + 14)))
    row_h = 18
    title_h = 16 if title else 4
    width = n_cols * col_w + 12
    height = title_h + n_rows * row_h + 8
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
    ]
    if title:
        parts.append(f'<text x="{width / 2}" y="12" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(title)}</text>')
    x0 = 6
    y0 = title_h
    parts.append(f'<rect x="{x0}" y="{y0}" width="{n_cols * col_w}" height="{row_h}" fill="#e2e8f0" stroke="#475569" stroke-width="1"/>')
    for c_idx, h_text in enumerate(headers):
        cx = x0 + c_idx * col_w + col_w / 2
        parts.append(f'<text x="{cx}" y="{y0 + 12.5}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#0f172a" text-anchor="middle">{_esc(h_text)}</text>')
        if c_idx > 0:
            parts.append(f'<line x1="{x0 + c_idx * col_w}" y1="{y0}" x2="{x0 + c_idx * col_w}" y2="{y0 + n_rows * row_h}" stroke="#64748b" stroke-width="0.8"/>')

    for r_idx, row in enumerate(rows):
        ry = y0 + (r_idx + 1) * row_h
        bg = "#ffffff" if r_idx % 2 == 0 else "#f8fafc"
        parts.append(f'<rect x="{x0}" y="{ry}" width="{n_cols * col_w}" height="{row_h}" fill="{bg}" stroke="#64748b" stroke-width="0.8"/>')
        for c_idx, val in enumerate(row):
            cx = x0 + c_idx * col_w + col_w / 2
            parts.append(f'<text x="{cx}" y="{ry + 12.5}" font-family="sans-serif" font-size="7.5" fill="#1e293b" text-anchor="middle">{_esc(val)}</text>')
            if c_idx > 0:
                parts.append(f'<line x1="{x0 + c_idx * col_w}" y1="{ry}" x2="{x0 + c_idx * col_w}" y2="{ry + row_h}" stroke="#64748b" stroke-width="0.8"/>')

    parts.append("</svg>")
    return "".join(parts)


def svg_right_triangle(
    side_a: str = "",
    side_b: str = "",
    side_c: str = "",
    angle_a: str = "",
    angle_b: str = "",
    a_label: str = "",
    b_label: str = "",
    c_label: str = "",
    theta_label: str = "",
) -> str:
    """Render a labeled right triangle diagram with wide side padding so labels never clip."""
    side_a = side_a or a_label
    side_b = side_b or b_label
    side_c = side_c or c_label
    angle_b = angle_b or theta_label
    width, height = 225, 118
    x1, y1 = 58, 92   # Right angle C
    x2, y2 = 166, 92  # Vertex B
    x3, y3 = 58, 22   # Vertex A
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" fill="#eff6ff" stroke="#1e40af" stroke-width="1.8"/>',
        f'<rect x="{x1}" y="{y1 - 10}" width="10" height="10" fill="none" stroke="#1e40af" stroke-width="1.2"/>',
        f'<text x="{x1 - 10}" y="{y1 + 11}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b">C</text>',
        f'<text x="{x2 + 6}" y="{y2 + 4}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b">B</text>',
        f'<text x="{x3 - 10}" y="{y3}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b">A</text>',
    ]
    if side_a:
        parts.append(f'<text x="{(x1 + x2) / 2}" y="{y1 + 14}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(side_a)}</text>')
    if side_b:
        parts.append(f'<text x="{x1 - 6}" y="{(y1 + y3) / 2 + 3}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="end">{_esc(side_b)}</text>')
    if side_c:
        parts.append(f'<text x="{(x2 + x3) / 2 + 6}" y="{(y2 + y3) / 2 - 4}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626">{_esc(side_c)}</text>')
    if angle_b:
        parts.append(f'<text x="{x2 - 28}" y="{y2 - 5}" font-family="sans-serif" font-size="7.5" fill="#0f172a" text-anchor="middle">{_esc(angle_b)}</text>')
    if angle_a:
        parts.append(f'<text x="{x3 + 5}" y="{y3 + 22}" font-family="sans-serif" font-size="7.5" fill="#0f172a">{_esc(angle_a)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_general_triangle(
    label_a: str = "A",
    label_b: str = "B",
    label_c: str = "C",
    ang_a: str = "",
    ang_b: str = "",
    ang_c: str = "",
    side_ab: str = "",
    side_bc: str = "",
    side_ac: str = "",
    ext_c: str = "",
    angle_a: str = "",
    angle_b: str = "",
    angle_c: str = "",
    side_a: str = "",
    side_b: str = "",
    side_c: str = "",
) -> str:
    """Render a labeled general triangle with ample horizontal padding so labels never clip."""
    ang_a = ang_a or angle_a
    ang_b = ang_b or angle_b
    ang_c = ang_c or angle_c
    side_bc = side_bc or side_a
    side_ac = side_ac or side_b
    side_ab = side_ab or side_c
    width, height = 235, 118
    xa, ya = 52, 92
    xc, yc = 158, 92
    xb, yb = 102, 22
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<polygon points="{xa},{ya} {xc},{yc} {xb},{yb}" fill="#f0fdf4" stroke="#15803d" stroke-width="1.8"/>',
        f'<text x="{xa - 9}" y="{ya + 4}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b">{_esc(label_a)}</text>',
        f'<text x="{xb}" y="{yb - 6}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(label_b)}</text>',
        f'<text x="{xc + 4}" y="{yc + 11}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e293b">{_esc(label_c)}</text>',
    ]
    if ext_c:
        parts.append(f'<line x1="{xc}" y1="{yc}" x2="215" y2="{yc}" stroke="#15803d" stroke-width="1.8"/>')
        parts.append(f'<text x="{xc + 12}" y="{yc - 6}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626">{_esc(ext_c)}</text>')
    if ang_a:
        parts.append(f'<text x="{xa + 14}" y="{ya - 5}" font-family="sans-serif" font-size="7.5" fill="#1e293b">{_esc(ang_a)}</text>')
    if ang_b:
        parts.append(f'<text x="{xb}" y="{yb + 18}" font-family="sans-serif" font-size="7.5" fill="#1e293b" text-anchor="middle">{_esc(ang_b)}</text>')
    if ang_c:
        parts.append(f'<text x="{xc - 20}" y="{yc - 5}" font-family="sans-serif" font-size="7.5" fill="#1e293b" text-anchor="middle">{_esc(ang_c)}</text>')
    if side_ac:
        parts.append(f'<text x="{(xa + xc) / 2}" y="{ya + 14}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1d4ed8" text-anchor="middle">{_esc(side_ac)}</text>')
    if side_ab:
        parts.append(f'<text x="{(xa + xb) / 2 - 6}" y="{(ya + yb) / 2}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1d4ed8" text-anchor="end">{_esc(side_ab)}</text>')
    if side_bc:
        parts.append(f'<text x="{(xb + xc) / 2 + 6}" y="{(yb + yc) / 2}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1d4ed8">{_esc(side_bc)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_parallel_transversal(
    ang1_label: str = "∠1",
    ang2_label: str = "∠2",
    mode: str = "alt_interior",
    angle1_label: str = "",
    angle2_label: str = "",
) -> str:
    """Render two parallel lines cut by a transversal with labeled angles."""
    ang1_label = angle1_label or ang1_label
    ang2_label = angle2_label or ang2_label
    width, height = 215, 114
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        '<line x1="20" y1="35" x2="195" y2="35" stroke="#1e293b" stroke-width="1.8"/>',
        '<line x1="20" y1="80" x2="195" y2="80" stroke="#1e293b" stroke-width="1.8"/>',
        '<line x1="60" y1="10" x2="135" y2="104" stroke="#2563eb" stroke-width="1.8"/>',
        f'<text x="72" y="48" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626">{_esc(ang1_label)}</text>',
    ]
    if mode == "alt_interior":
        parts.append(f'<text x="115" y="74" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626">{_esc(ang2_label)}</text>')
    elif mode == "consecutive_interior":
        parts.append(f'<text x="82" y="74" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626">{_esc(ang2_label)}</text>')
    else:
        parts.append(f'<text x="122" y="94" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626">{_esc(ang2_label)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_angle_diagram(
    angle_degrees: float = 45.0,
    angle_label: str = "",
    vertex_label: str = "B",
    ray1_label: str = "C",
    ray2_label: str = "A",
    interior_angle: Optional[float] = None,
    interior_label: str = "D",
    interior_angle_label: str = "",
    mode: str = "single",
    shade: bool = False,
    bottom_label: str = "",
) -> str:
    """Render a geometrically accurate angle diagram:
    - single: One angle ∠ABC of measure angle_degrees
    - interior_ray: Angle ∠ABC with interior ray BD (Angle Addition Postulate or Bisector)
    - linear_pair: Straight line AC with vertex B and ray BD forming a linear pair
    """
    width, height = 210, 124

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        '<defs>',
        '  <marker id="ang-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '    <path d="M 1 2 L 8 5 L 1 8 z" fill="#1e40af"/>',
        '  </marker>',
        '</defs>',
    ]

    if mode == "linear_pair":
        theta = float(angle_degrees)
        theta = max(15.0, min(165.0, theta))
        bx, by = 105.0, 85.0
        line_len = 80.0

        ax = bx - line_len
        cx = bx + line_len
        rad = math.radians(theta)
        dx = round(bx + line_len * 0.85 * math.cos(rad), 2)
        dy = round(by - line_len * 0.85 * math.sin(rad), 2)

        parts.append(f'<line x1="{ax}" y1="{by}" x2="{cx}" y2="{by}" stroke="#1e40af" stroke-width="2" marker-start="url(#ang-arrow)" marker-end="url(#ang-arrow)"/>')
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{dx}" y2="{dy}" stroke="#1e40af" stroke-width="2" marker-end="url(#ang-arrow)"/>')

        if shade:
            parts.append(f'<path d="M {bx} {by} L {cx - 20} {by} A 60 60 0 0 0 {dx} {dy} Z" fill="#bfdbfe" fill-opacity="0.25" stroke="none"/>')

        parts.append(f'<circle cx="{bx}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{bx}" y="{by + 14}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">B</text>')

        parts.append(f'<circle cx="{cx - 25}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{cx - 25}" y="{by + 14}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">C</text>')

        parts.append(f'<circle cx="{ax + 25}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{ax + 25}" y="{by + 14}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">A</text>')

        parts.append(f'<circle cx="{round(bx + line_len * 0.6 * math.cos(rad), 2)}" cy="{round(by - line_len * 0.6 * math.sin(rad), 2)}" r="2.5" fill="#1e293b"/>')
        off_d_x = round(bx + (line_len * 0.6 + 9) * math.cos(rad), 2)
        off_d_y = round(by - (line_len * 0.6 + 9) * math.sin(rad) + 3, 2)
        parts.append(f'<text x="{off_d_x}" y="{off_d_y}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">D</text>')

        r_arc1 = 20.0
        a1_x = round(bx + r_arc1 * math.cos(rad), 2)
        a1_y = round(by - r_arc1 * math.sin(rad), 2)
        parts.append(f'<path d="M {bx + r_arc1} {by} A {r_arc1} {r_arc1} 0 0 0 {a1_x} {a1_y}" fill="none" stroke="#2563eb" stroke-width="1.6"/>')

        lbl1 = angle_label if angle_label else f"{int(theta)}&#176;"
        mid_rad1 = math.radians(theta / 2.0)
        lx1 = round(bx + 32.0 * math.cos(mid_rad1), 2)
        ly1 = round(by - 32.0 * math.sin(mid_rad1) + 3, 2)
        parts.append(f'<text x="{lx1}" y="{ly1}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af" text-anchor="middle">{lbl1}</text>')

        if interior_angle_label:
            r_arc2 = 24.0
            a2_x = round(bx + r_arc2 * math.cos(rad), 2)
            a2_y = round(by - r_arc2 * math.sin(rad), 2)
            parts.append(f'<path d="M {a2_x} {a2_y} A {r_arc2} {r_arc2} 0 0 0 {bx - r_arc2} {by}" fill="none" stroke="#16a34a" stroke-width="1.6"/>')

            mid_rad2 = math.radians(180 - (180 - theta) / 2.0)
            lx2 = round(bx + 36.0 * math.cos(mid_rad2), 2)
            ly2 = round(by - 36.0 * math.sin(mid_rad2) + 3, 2)
            parts.append(f'<text x="{lx2}" y="{ly2}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#16a34a" text-anchor="middle">{_esc(interior_angle_label)}</text>')

    elif mode == "interior_ray":
        a1 = float(angle_degrees)
        a2 = float(interior_angle if interior_angle is not None else 30.0)
        tot = a1 + a2

        if tot <= 85:
            bx, by = 55.0, 92.0
            ray_len = 80.0
        elif tot <= 115:
            bx, by = 80.0, 92.0
            ray_len = 75.0
        else:
            bx, by = 115.0, 92.0
            ray_len = 75.0

        rad1 = math.radians(a1)
        rad_tot = math.radians(tot)

        cx = round(bx + ray_len, 2)
        cy = by
        dx = round(bx + ray_len * math.cos(rad1), 2)
        dy = round(by - ray_len * math.sin(rad1), 2)
        ax = round(bx + ray_len * math.cos(rad_tot), 2)
        ay = round(by - ray_len * math.sin(rad_tot), 2)

        parts.append(f'<line x1="{bx}" y1="{by}" x2="{cx}" y2="{cy}" stroke="#1e40af" stroke-width="2" marker-end="url(#ray-arrow)"/>')
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{dx}" y2="{dy}" stroke="#1e40af" stroke-width="2" marker-end="url(#ray-arrow)"/>')
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{ax}" y2="{ay}" stroke="#1e40af" stroke-width="2" marker-end="url(#ray-arrow)"/>')

        if shade:
            parts.append(f'<path d="M {bx} {by} L {cx} {cy} A {ray_len} {ray_len} 0 0 0 {ax} {ay} Z" fill="#bfdbfe" fill-opacity="0.25" stroke="none"/>')

        parts.append(f'<circle cx="{bx}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{bx - 7}" y="{by + 13}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b">B</text>')

        p_c_x = round(bx + ray_len * 0.65, 2)
        parts.append(f'<circle cx="{p_c_x}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{p_c_x}" y="{by + 13}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">C</text>')

        p_d_x = round(bx + ray_len * 0.65 * math.cos(rad1), 2)
        p_d_y = round(by - ray_len * 0.65 * math.sin(rad1), 2)
        parts.append(f'<circle cx="{p_d_x}" cy="{p_d_y}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{p_d_x + 9}" y="{p_d_y + 4}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">D</text>')

        p_a_x = round(bx + ray_len * 0.65 * math.cos(rad_tot), 2)
        p_a_y = round(by - ray_len * 0.65 * math.sin(rad_tot), 2)
        parts.append(f'<circle cx="{p_a_x}" cy="{p_a_y}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{p_a_x - 7}" y="{p_a_y - 4}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">A</text>')

        r_arc1 = 18.0
        a1_x = round(bx + r_arc1 * math.cos(rad1), 2)
        a1_y = round(by - r_arc1 * math.sin(rad1), 2)
        parts.append(f'<path d="M {bx + r_arc1} {by} A {r_arc1} {r_arc1} 0 0 0 {a1_x} {a1_y}" fill="none" stroke="#2563eb" stroke-width="1.5"/>')
        lbl1 = angle_label if angle_label else f"{int(a1)}&#176;"
        mid1 = rad1 / 2.0
        parts.append(f'<text x="{round(bx + 30 * math.cos(mid1), 2)}" y="{round(by - 30 * math.sin(mid1) + 3, 2)}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e40af" text-anchor="middle">{lbl1}</text>')

        r_arc2 = 24.0
        a2_start_x = round(bx + r_arc2 * math.cos(rad1), 2)
        a2_start_y = round(by - r_arc2 * math.sin(rad1), 2)
        a2_end_x = round(bx + r_arc2 * math.cos(rad_tot), 2)
        a2_end_y = round(by - r_arc2 * math.sin(rad_tot), 2)
        parts.append(f'<path d="M {a2_start_x} {a2_start_y} A {r_arc2} {r_arc2} 0 0 0 {a2_end_x} {a2_end_y}" fill="none" stroke="#16a34a" stroke-width="1.5"/>')
        lbl2 = interior_angle_label if interior_angle_label else f"{int(a2)}&#176;"
        mid2 = math.radians(a1 + a2 / 2.0)
        parts.append(f'<text x="{round(bx + 38 * math.cos(mid2), 2)}" y="{round(by - 38 * math.sin(mid2) + 3, 2)}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#16a34a" text-anchor="middle">{lbl2}</text>')

    else:
        theta = float(angle_degrees)
        theta = max(5.0, min(180.0, theta))

        if theta <= 80:
            bx, by = 55.0, 92.0
            ray_len = 80.0
        elif theta <= 105:
            bx, by = 80.0, 92.0
            ray_len = 75.0
        else:
            bx, by = 118.0, 92.0
            ray_len = 75.0

        rad = math.radians(theta)
        ax = round(bx + ray_len * math.cos(rad), 2)
        ay = round(by - ray_len * math.sin(rad), 2)
        cx = round(bx + ray_len, 2)
        cy = by
        large_arc = 1 if theta > 180 else 0

        if shade:
            if abs(theta - 180.0) < 1e-2:
                parts.append(f'<path d="M {ax} {by} A {ray_len} {ray_len} 0 0 0 {cx} {by} Z" fill="#bfdbfe" fill-opacity="0.3" stroke="none"/>')
            else:
                parts.append(f'<path d="M {bx} {by} L {cx} {cy} A {ray_len} {ray_len} 0 {large_arc} 0 {ax} {ay} Z" fill="#bfdbfe" fill-opacity="0.28" stroke="none"/>')

        parts.append(f'<line x1="{bx}" y1="{by}" x2="{cx}" y2="{cy}" stroke="#1e40af" stroke-width="2" marker-end="url(#ray-arrow)"/>')
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{ax}" y2="{ay}" stroke="#1e40af" stroke-width="2" marker-end="url(#ray-arrow)"/>')

        p_c_x = round(bx + ray_len * 0.65, 2)
        p_c_y = cy
        p_a_x = round(bx + ray_len * 0.65 * math.cos(rad), 2)
        p_a_y = round(by - ray_len * 0.65 * math.sin(rad), 2)

        parts.append(f'<circle cx="{bx}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<circle cx="{p_c_x}" cy="{p_c_y}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<circle cx="{p_a_x}" cy="{p_a_y}" r="2.5" fill="#1e293b"/>')

        parts.append(f'<text x="{bx - 7}" y="{by + 13}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b">{_esc(vertex_label)}</text>')
        parts.append(f'<text x="{p_c_x}" y="{p_c_y + 13}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(ray1_label)}</text>')

        perp_rad = rad + math.pi / 2.0
        off_a_x = round(p_a_x + 9 * math.cos(perp_rad), 2)
        off_a_y = round(p_a_y - 9 * math.sin(perp_rad) + 3, 2)
        parts.append(f'<text x="{off_a_x}" y="{off_a_y}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">{_esc(ray2_label)}</text>')

        if abs(theta - 90.0) < 1e-2:
            sz = 12.0
            parts.append(f'<path d="M {bx + sz} {by} L {bx + sz} {by - sz} L {bx} {by - sz}" fill="none" stroke="#2563eb" stroke-width="1.6"/>')
        elif abs(theta - 180.0) < 1e-2:
            r_arc = 18.0
            parts.append(f'<path d="M {bx + r_arc} {by} A {r_arc} {r_arc} 0 0 0 {bx - r_arc} {by}" fill="none" stroke="#2563eb" stroke-width="1.6"/>')
        else:
            r_arc = 20.0
            abx = round(bx + r_arc * math.cos(rad), 2)
            aby = round(by - r_arc * math.sin(rad), 2)
            parts.append(f'<path d="M {bx + r_arc} {by} A {r_arc} {r_arc} 0 {large_arc} 0 {abx} {aby}" fill="none" stroke="#2563eb" stroke-width="1.6"/>')

        lbl_text = angle_label if angle_label else f"{int(theta) if theta.is_integer() else theta}&#176;"
        mid_rad = math.radians(theta / 2.0)
        r_lbl = 34.0 if theta >= 50 else 44.0
        lx = round(bx + r_lbl * math.cos(mid_rad), 2)
        ly = round(by - r_lbl * math.sin(mid_rad) + 3, 2)
        parts.append(f'<text x="{lx}" y="{ly}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af" text-anchor="middle">{lbl_text}</text>')

    if bottom_label:
        parts.append(f'<text x="105" y="115" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af" text-anchor="middle">{_esc(bottom_label)}</text>')

    parts.append("</svg>")
    return "".join(parts)


def svg_circle_diagram(
    radius_label: str = "",
    angle_label: str = "",
    chord_label: str = "",
    angle_degrees: Optional[float] = None,
    show_sector: bool = False,
    shade_sector: bool = False,
    show_points: bool = True,
    mode: str = "auto",
    inscribed_angle: Optional[float] = None,
    intercepted_arc: Optional[float] = None,
    far_arc: Optional[float] = None,
    near_arc: Optional[float] = None,
    chord_segments: Optional[Sequence[str]] = None,
    bottom_label: str = "",
) -> str:
    """Render a clean vector circle diagram supporting central angles, inscribed angles,
    intersecting chords, exterior secants, sectors, and radius labels."""
    width, height = 210, 130
    cx, cy, r = 105.0, 60.0, 42.0

    # Auto-detect mode from labels if auto
    if mode == "auto":
        lbl_low = (angle_label + " " + chord_label).lower()
        if "inscribed" in lbl_low or inscribed_angle is not None:
            mode = "inscribed"
        elif "arc" in lbl_low and ("," in lbl_low or "far" in lbl_low or far_arc is not None):
            mode = "secants"
        elif chord_segments is not None or ("=" in chord_label and "*" in chord_label) or ("chords" in lbl_low):
            mode = "chords"
        elif angle_degrees is not None or (angle_label and any(c.isdigit() for c in angle_label)):
            mode = "central"
        else:
            mode = "radius"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f8fafc" stroke="#1e40af" stroke-width="1.8"/>',
    ]

    if mode == "inscribed":
        ins_deg = inscribed_angle
        if ins_deg is None and angle_label:
            m = re.search(r"(\d+(?:\.\d+)?)", angle_label)
            if m:
                ins_deg = float(m.group(1))
        ins_deg = ins_deg if ins_deg is not None else 40.0
        arc_deg = intercepted_arc if intercepted_arc is not None else (2.0 * ins_deg)

        vx, vy = cx - r, cy
        half_arc = math.radians(arc_deg / 2.0)
        ax = round(cx + r * math.cos(half_arc), 2)
        ay = round(cy - r * math.sin(half_arc), 2)
        bx = round(cx + r * math.cos(-half_arc), 2)
        by = round(cy - r * math.sin(-half_arc), 2)

        parts.append(f'<line x1="{vx}" y1="{vy}" x2="{ax}" y2="{ay}" stroke="#1e40af" stroke-width="1.8"/>')
        parts.append(f'<line x1="{vx}" y1="{vy}" x2="{bx}" y2="{by}" stroke="#1e40af" stroke-width="1.8"/>')
        parts.append(f'<path d="M {bx} {by} A {r} {r} 0 0 0 {ax} {ay}" fill="none" stroke="#2563eb" stroke-width="2.6"/>')

        r_arc = 16.0
        v_rad_a = math.atan2(vy - ay, ax - vx)
        v_rad_b = math.atan2(vy - by, bx - vx)
        vax = round(vx + r_arc * math.cos(v_rad_a), 2)
        vay = round(vy - r_arc * math.sin(v_rad_a), 2)
        vbx = round(vx + r_arc * math.cos(v_rad_b), 2)
        vby = round(vy - r_arc * math.sin(v_rad_b), 2)
        parts.append(f'<path d="M {vbx} {vby} A {r_arc} {r_arc} 0 0 0 {vax} {vay}" fill="none" stroke="#2563eb" stroke-width="1.4"/>')

        parts.append(f'<circle cx="{vx}" cy="{vy}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{vx - 8}" y="{vy + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b">V</text>')

        parts.append(f'<circle cx="{ax}" cy="{ay}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{ax + 6}" y="{ay + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b">A</text>')

        parts.append(f'<circle cx="{bx}" cy="{by}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{bx + 6}" y="{by + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b">B</text>')

        parts.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="#94a3b8"/>')
        parts.append(f'<text x="{cx}" y="{cy + 10}" font-family="sans-serif" font-size="7" font-weight="bold" fill="#94a3b8" text-anchor="middle">O</text>')

        parts.append(f'<text x="{vx + 26}" y="{vy + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af">{int(ins_deg)}&#176;</text>')

        arc_text = f"Arc = {int(arc_deg)}&#176;" if shade_sector else f"Arc: {int(arc_deg)}&#176;"
        parts.append(f'<text x="{cx + r + 12}" y="{cy + 3}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#2563eb">{arc_text}</text>')

    elif mode == "chords":
        c_segs = list(chord_segments) if chord_segments else []
        if not c_segs and chord_label:
            nums = re.findall(r"\d+", chord_label)
            if len(nums) >= 3:
                c_segs = [nums[0], nums[1], nums[2], "x"]
            else:
                c_segs = ["a", "b", "c", "x"]
        while len(c_segs) < 4:
            c_segs.append("x")

        ix, iy = cx + 8.0, cy - 4.0
        c1_p1 = (round(cx - r * math.cos(math.radians(35)), 2), round(cy + r * math.sin(math.radians(35)), 2))
        c1_p2 = (round(cx + r * math.cos(math.radians(55)), 2), round(cy - r * math.sin(math.radians(55)), 2))
        c2_p1 = (round(cx - r * math.cos(math.radians(45)), 2), round(cy - r * math.sin(math.radians(45)), 2))
        c2_p2 = (round(cx + r * math.cos(math.radians(25)), 2), round(cy + r * math.sin(math.radians(25)), 2))

        parts.append(f'<line x1="{c1_p1[0]}" y1="{c1_p1[1]}" x2="{c1_p2[0]}" y2="{c1_p2[1]}" stroke="#15803d" stroke-width="1.8"/>')
        parts.append(f'<line x1="{c2_p1[0]}" y1="{c2_p1[1]}" x2="{c2_p2[0]}" y2="{c2_p2[1]}" stroke="#2563eb" stroke-width="1.8"/>')
        parts.append(f'<circle cx="{ix}" cy="{iy}" r="2" fill="#1e293b"/>')

        s_a, s_b, s_c, s_d = c_segs[0], c_segs[1], c_segs[2], c_segs[3]
        mid1_a = ((c1_p1[0] + ix) / 2.0 - 5, (c1_p1[1] + iy) / 2.0 + 8)
        mid1_b = ((c1_p2[0] + ix) / 2.0 + 5, (c1_p2[1] + iy) / 2.0 - 5)
        mid2_a = ((c2_p1[0] + ix) / 2.0 - 5, (c2_p1[1] + iy) / 2.0 - 5)
        mid2_b = ((c2_p2[0] + ix) / 2.0 + 5, (c2_p2[1] + iy) / 2.0 + 8)

        parts.append(f'<text x="{mid1_a[0]}" y="{mid1_a[1]}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#15803d">{s_a}</text>')
        parts.append(f'<text x="{mid1_b[0]}" y="{mid1_b[1]}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#15803d">{s_b}</text>')
        parts.append(f'<text x="{mid2_a[0]}" y="{mid2_a[1]}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#2563eb">{s_c}</text>')
        parts.append(f'<text x="{mid2_b[0]}" y="{mid2_b[1]}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#2563eb">{s_d}</text>')

    elif mode == "secants":
        px, py = 25.0, cy
        f_arc = far_arc
        n_arc = near_arc
        if (f_arc is None or n_arc is None) and angle_label:
            nums = re.findall(r"\d+", angle_label)
            if len(nums) >= 2:
                f_arc, n_arc = float(nums[0]), float(nums[1])
        f_arc = f_arc if f_arc is not None else 130.0
        n_arc = n_arc if n_arc is not None else 40.0
        ext_ang = round((f_arc - n_arc) / 2.0, 1)

        p1_near = (round(cx - r * math.cos(math.radians(30)), 2), round(cy - r * math.sin(math.radians(30)), 2))
        p1_far = (round(cx + r * math.cos(math.radians(45)), 2), round(cy - r * math.sin(math.radians(45)), 2))
        p2_near = (round(cx - r * math.cos(math.radians(30)), 2), round(cy + r * math.sin(math.radians(30)), 2))
        p2_far = (round(cx + r * math.cos(math.radians(45)), 2), round(cy + r * math.sin(math.radians(45)), 2))

        parts.append(f'<line x1="{px}" y1="{py}" x2="{p1_far[0]}" y2="{p1_far[1]}" stroke="#1e40af" stroke-width="1.8"/>')
        parts.append(f'<line x1="{px}" y1="{py}" x2="{p2_far[0]}" y2="{p2_far[1]}" stroke="#1e40af" stroke-width="1.8"/>')
        parts.append(f'<path d="M {p2_near[0]} {p2_near[1]} A {r} {r} 0 0 1 {p1_near[0]} {p1_near[1]}" fill="none" stroke="#16a34a" stroke-width="2.5"/>')
        parts.append(f'<path d="M {p2_far[0]} {p2_far[1]} A {r} {r} 0 0 0 {p1_far[0]} {p1_far[1]}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')

        parts.append(f'<circle cx="{px}" cy="{py}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<text x="{px - 6}" y="{py + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b">P</text>')

        parts.append(f'<text x="{px + 14}" y="{py + 3}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e40af">{int(ext_ang)}&#176;</text>')
        parts.append(f'<text x="{cx - 24}" y="{cy + 3}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#16a34a" text-anchor="middle">{int(n_arc)}&#176;</text>')
        parts.append(f'<text x="{cx + r + 8}" y="{cy + 3}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#2563eb">{int(f_arc)}&#176;</text>')

    elif mode == "central":
        if angle_degrees is None and angle_label:
            m = re.search(r"(\d+(?:\.\d+)?)", angle_label)
            if m:
                val = float(m.group(1))
                if 0 < val <= 360:
                    angle_degrees = val
        theta = float(angle_degrees if angle_degrees is not None else 60.0)

        rad = math.radians(theta)
        bx = round(cx + r * math.cos(rad), 2)
        by = round(cy - r * math.sin(rad), 2)
        large_arc = 1 if theta > 180 else 0

        if shade_sector:
            parts.append(f'<path d="M {cx} {cy} L {cx + r} {cy} A {r} {r} 0 {large_arc} 0 {bx} {by} Z" fill="#93c5fd" fill-opacity="0.38" stroke="none"/>')

        parts.append(f'<path d="M {cx + r} {cy} A {r} {r} 0 {large_arc} 0 {bx} {by}" fill="none" stroke="#2563eb" stroke-width="2.6"/>')
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#1e40af" stroke-width="1.8"/>')
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{bx}" y2="{by}" stroke="#1e40af" stroke-width="1.8"/>')

        if abs(theta - 90.0) < 1e-2:
            sz = 10.0
            parts.append(f'<path d="M {cx + sz} {cy} L {cx + sz} {cy - sz} L {cx} {cy - sz}" fill="none" stroke="#2563eb" stroke-width="1.4"/>')
        else:
            r_arc = 14.0
            abx = round(cx + r_arc * math.cos(rad), 2)
            aby = round(cy - r_arc * math.sin(rad), 2)
            parts.append(f'<path d="M {cx + r_arc} {cy} A {r_arc} {r_arc} 0 {large_arc} 0 {abx} {aby}" fill="none" stroke="#2563eb" stroke-width="1.4"/>')

        if show_points:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#1e293b"/>')
            parts.append(f'<text x="{cx - 7}" y="{cy + 10}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b">O</text>')

            parts.append(f'<circle cx="{cx + r}" cy="{cy}" r="2.5" fill="#1e293b"/>')
            parts.append(f'<text x="{cx + r + 5}" y="{cy + 4}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b">A</text>')

            parts.append(f'<circle cx="{bx}" cy="{by}" r="2.5" fill="#1e293b"/>')
            off_bx = round(bx + 8 * math.cos(rad), 2)
            off_by = round(by - 8 * math.sin(rad) + 3, 2)
            parts.append(f'<text x="{off_bx}" y="{off_by}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e293b" text-anchor="middle">B</text>')

            major_mid_rad = math.radians(theta + (360.0 - theta) / 2.0)
            cx_c = round(cx + r * math.cos(major_mid_rad), 2)
            cy_c = round(cy - r * math.sin(major_mid_rad), 2)
            off_cx = round(cx + (r + 8) * math.cos(major_mid_rad), 2)
            off_cy = round(cy - (r + 8) * math.sin(major_mid_rad) + 3, 2)
            parts.append(f'<circle cx="{cx_c}" cy="{cy_c}" r="2.5" fill="#64748b"/>')
            parts.append(f'<text x="{off_cx}" y="{off_cy}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">C</text>')

        mid_rad = math.radians(theta / 2.0)
        r_lbl = 24.0 if theta >= 60 else 28.0
        lx = round(cx + r_lbl * math.cos(mid_rad), 2)
        ly = round(cy - r_lbl * math.sin(mid_rad) + 3, 2)
        deg_str = f"{int(theta) if theta.is_integer() else theta}&#176;"
        parts.append(f'<text x="{lx}" y="{ly}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af" text-anchor="middle">{deg_str}</text>')

    else:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#1e293b"/>')
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#dc2626" stroke-width="1.8"/>')
        if radius_label:
            parts.append(f'<text x="{cx + r / 2}" y="{cy + 12}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(radius_label)}</text>')

    if chord_label and mode != "chords":
        parts.append(f'<line x1="{cx - 30}" y1="{cy - 28}" x2="{cx + 30}" y2="{cy - 28}" stroke="#15803d" stroke-width="1.8"/>')
        parts.append(f'<text x="{cx}" y="{cy - 32}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#15803d" text-anchor="middle">{_esc(chord_label)}</text>')

    if bottom_label or (angle_label and ("minor" in angle_label.lower() or "major" in angle_label.lower())):
        lbl = bottom_label if bottom_label else angle_label
        parts.append(f'<text x="{cx}" y="{height - 3}" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e40af" text-anchor="middle">{_esc(lbl)}</text>')

    parts.append("</svg>")
    return "".join(parts)


def svg_solid_3d(solid: str = "prism", dim1: str = "", dim2: str = "", dim3: str = "") -> str:
    """Render a clean 3D geometric solid (prism, cylinder, cone, sphere, pyramid)."""
    width, height = 220, 118
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>']
    if solid == "cylinder":
        parts.extend([
            '<ellipse cx="98" cy="26" rx="38" ry="11" fill="#dbeafe" stroke="#1e40af" stroke-width="1.5"/>',
            '<line x1="60" y1="26" x2="60" y2="86" stroke="#1e40af" stroke-width="1.5"/>',
            '<line x1="136" y1="26" x2="136" y2="86" stroke="#1e40af" stroke-width="1.5"/>',
            '<ellipse cx="98" cy="86" rx="38" ry="11" fill="#eff6ff" stroke="#1e40af" stroke-width="1.5" stroke-dasharray="3,2"/>',
            '<line x1="98" y1="26" x2="136" y2="26" stroke="#dc2626" stroke-width="1.5"/>',
            f'<text x="117" y="21" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(dim1)}</text>',
            f'<text x="142" y="58" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1e293b">{_esc(dim2)}</text>',
        ])
    elif solid == "cone":
        parts.extend([
            '<ellipse cx="98" cy="88" rx="38" ry="11" fill="#eff6ff" stroke="#1e40af" stroke-width="1.5"/>',
            '<line x1="60" y1="88" x2="98" y2="18" stroke="#1e40af" stroke-width="1.5"/>',
            '<line x1="136" y1="88" x2="98" y2="18" stroke="#1e40af" stroke-width="1.5"/>',
            '<line x1="98" y1="18" x2="98" y2="88" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>',
            '<line x1="98" y1="88" x2="136" y2="88" stroke="#dc2626" stroke-width="1.5"/>',
            f'<text x="117" y="100" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(dim1)}</text>',
            f'<text x="92" y="58" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1e293b" text-anchor="end">{_esc(dim2)}</text>',
        ])
    elif solid == "sphere":
        parts.extend([
            '<circle cx="105" cy="58" r="40" fill="#eff6ff" stroke="#1e40af" stroke-width="1.6"/>',
            '<ellipse cx="105" cy="58" rx="40" ry="12" fill="none" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>',
            '<line x1="105" y1="58" x2="145" y2="58" stroke="#dc2626" stroke-width="1.6"/>',
            f'<text x="125" y="53" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(dim1)}</text>',
        ])
    else:
        parts.extend([
            '<rect x="52" y="38" width="72" height="52" fill="#eff6ff" fill-opacity="0.7" stroke="#1e40af" stroke-width="1.5"/>',
            '<polygon points="52,38 75,20 147,20 124,38" fill="#dbeafe" fill-opacity="0.7" stroke="#1e40af" stroke-width="1.5"/>',
            '<polygon points="124,38 147,20 147,72 124,90" fill="#bfdbfe" fill-opacity="0.7" stroke="#1e40af" stroke-width="1.5"/>',
            f'<text x="88" y="103" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(dim1)}</text>',
            f'<text x="141" y="88" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#15803d">{_esc(dim2)}</text>',
            f'<text x="46" y="66" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1e3a8a" text-anchor="end">{_esc(dim3)}</text>',
        ])
    parts.append("</svg>")
    return "".join(parts)


def svg_tape_or_hanger(
    mode: str = "tape",
    parts_labels: Optional[Sequence[str]] = None,
    total_label: str = "",
) -> str:
    """Render a Grade 6 tape diagram or balanced hanger diagram."""
    width, height = 215, 78
    labels = list(parts_labels or ["x", "x", "4"])
    n = max(len(labels), 1)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>']
    if mode == "hanger":
        parts.extend([
            '<line x1="107" y1="8" x2="107" y2="20" stroke="#334155" stroke-width="1.8"/>',
            '<polygon points="107,18 47,32 167,32" fill="none" stroke="#334155" stroke-width="1.6"/>',
            '<rect x="25" y="36" width="56" height="26" rx="4" fill="#dbeafe" stroke="#1d4ed8" stroke-width="1.4"/>',
            '<rect x="133" y="36" width="56" height="26" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.4"/>',
            f'<text x="53" y="53" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(" + ".join(labels))}</text>',
            f'<text x="161" y="53" font-family="sans-serif" font-size="9" font-weight="bold" fill="#92400e" text-anchor="middle">{_esc(total_label)}</text>',
        ])
    else:
        x0, y0, tw, th = 18.0, 32.0, 179.0, 24.0
        bw = tw / n
        if total_label:
            parts.append(f'<text x="{x0 + tw / 2}" y="22" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#dc2626" text-anchor="middle">Total = {_esc(total_label)}</text>')
            parts.append(f'<line x1="{x0}" y1="26" x2="{x0 + tw}" y2="26" stroke="#dc2626" stroke-width="1.2"/>')
        for idx, lbl in enumerate(labels):
            bx = round(x0 + idx * bw, 2)
            parts.append(f'<rect x="{bx}" y="{y0}" width="{round(bw, 2)}" height="{th}" fill="#eff6ff" stroke="#1d4ed8" stroke-width="1.4"/>')
            parts.append(f'<text x="{round(bx + bw / 2, 2)}" y="{y0 + 15}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(lbl)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_area_model(
    top_labels: Sequence[str],
    side_label: str,
    cell_labels: Sequence[str],
    title: str = "Area Diagram",
) -> str:
    """Render a rectangular area model / box diagram for distributive property or decimal operations."""
    width, height = 215, 92
    n = max(len(top_labels), 1)
    x0, y0, tw, th = 38.0, 32.0, 156.0, 44.0
    bw = tw / n
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>',
        f'<text x="{width / 2}" y="12" font-family="sans-serif" font-size="8" font-weight="bold" fill="#334155" text-anchor="middle">{_esc(title)}</text>',
        f'<text x="{x0 - 6}" y="{y0 + th / 2 + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#dc2626" text-anchor="end">{_esc(side_label)}</text>',
    ]
    colors = ["#eff6ff", "#fef3c7", "#dcfce7"]
    for idx, t_lbl in enumerate(top_labels):
        bx = round(x0 + idx * bw, 2)
        c_lbl = cell_labels[idx] if idx < len(cell_labels) else "?"
        parts.append(f'<text x="{round(bx + bw / 2, 2)}" y="{y0 - 6}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(t_lbl)}</text>')
        parts.append(f'<rect x="{bx}" y="{y0}" width="{round(bw, 2)}" height="{th}" fill="{colors[idx % len(colors)]}" stroke="#1e40af" stroke-width="1.4"/>')
        parts.append(f'<text x="{round(bx + bw / 2, 2)}" y="{y0 + th / 2 + 3}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#0f172a" text-anchor="middle">{_esc(c_lbl)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_polygon_diagram(
    shape: str = "parallelogram",
    dim1: str = "",
    dim2: str = "",
    dim3: str = "",
) -> str:
    """Render a 2D polygon (parallelogram, trapezoid, rhombus, kite, regular, net)."""
    width, height = 215, 114
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" {_SVG_STYLE}>']
    if shape == "trapezoid":
        parts.extend([
            '<polygon points="56,26 136,26 160,82 32,82" fill="#eff6ff" stroke="#1e40af" stroke-width="1.6"/>',
            '<line x1="56" y1="26" x2="56" y2="82" stroke="#dc2626" stroke-width="1.3" stroke-dasharray="3,2"/>',
            f'<text x="96" y="20" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(dim1)}</text>',
            f'<text x="96" y="96" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(dim2)}</text>',
            f'<text x="60" y="56" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626">{_esc(dim3)}</text>',
        ])
    elif shape in ("rhombus", "kite"):
        top_y, mid_y, bot_y = (18, 54, 90) if shape == "rhombus" else (18, 44, 92)
        parts.extend([
            f'<polygon points="102,{top_y} 156,{mid_y} 102,{bot_y} 48,{mid_y}" fill="#eff6ff" stroke="#1e40af" stroke-width="1.6"/>',
            f'<line x1="48" y1="{mid_y}" x2="156" y2="{mid_y}" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="3,2"/>',
            f'<line x1="102" y1="{top_y}" x2="102" y2="{bot_y}" stroke="#15803d" stroke-width="1.2" stroke-dasharray="3,2"/>',
            f'<text x="132" y="{mid_y - 4}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626">{_esc(dim1)}</text>',
            f'<text x="106" y="{bot_y - 12}" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#15803d">{_esc(dim2)}</text>',
        ])
    elif shape == "net":
        parts.extend([
            '<rect x="78" y="14" width="38" height="24" fill="#dbeafe" stroke="#1e40af" stroke-width="1.3"/>',
            '<rect x="40" y="38" width="38" height="28" fill="#eff6ff" stroke="#1e40af" stroke-width="1.3"/>',
            '<rect x="78" y="38" width="38" height="28" fill="#bfdbfe" stroke="#1e40af" stroke-width="1.3"/>',
            '<rect x="116" y="38" width="38" height="28" fill="#eff6ff" stroke="#1e40af" stroke-width="1.3"/>',
            '<rect x="154" y="38" width="26" height="28" fill="#dbeafe" stroke="#1e40af" stroke-width="1.3"/>',
            '<rect x="78" y="66" width="38" height="24" fill="#dbeafe" stroke="#1e40af" stroke-width="1.3"/>',
            f'<text x="97" y="55" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(dim1)}</text>',
            f'<text x="97" y="102" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626" text-anchor="middle">{_esc(dim2)}</text>',
        ])
    elif shape == "regular":
        parts.extend([
            '<polygon points="102,16 146,38 132,84 72,84 58,38" fill="#eff6ff" stroke="#1e40af" stroke-width="1.6"/>',
            '<circle cx="102" cy="54" r="2.2" fill="#1e293b"/>',
            '<line x1="102" y1="54" x2="102" y2="84" stroke="#dc2626" stroke-width="1.4" stroke-dasharray="3,2"/>',
            f'<text x="106" y="72" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626">{_esc(dim1)}</text>',
            f'<text x="102" y="96" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(dim2)}</text>',
        ])
    else:
        parts.extend([
            '<polygon points="48,26 152,26 132,82 28,82" fill="#eff6ff" stroke="#1e40af" stroke-width="1.6"/>',
            '<line x1="48" y1="26" x2="48" y2="82" stroke="#dc2626" stroke-width="1.3" stroke-dasharray="3,2"/>',
            f'<text x="80" y="96" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">{_esc(dim1)}</text>',
            f'<text x="53" y="58" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#dc2626">{_esc(dim2)}</text>',
            f'<text x="146" y="58" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#15803d">{_esc(dim3)}</text>',
        ])
    parts.append("</svg>")
    return "".join(parts)
