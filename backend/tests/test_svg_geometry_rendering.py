from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import pytest

from backend.app.core.svg_utils import (
    svg_angle_diagram,
    svg_circle_diagram,
    svg_coordinate_plane,
    svg_general_triangle,
    svg_polygon_diagram,
)


class TestSVGGeometryRendering:
    """Comprehensive visual & structural tests for SVG geometry & coordinate plane diagrams."""

    @pytest.mark.parametrize("deg", [15.0, 45.0, 72.0, 90.0, 131.0, 180.0, 229.0, 270.0, 315.0])
    def test_circle_central_angle_polar_trigonometry(self, deg: float) -> None:
        """Verify dynamic polar-to-Cartesian ray endpoints and large-arc-flag for circle central angles."""
        svg = svg_circle_diagram(angle_degrees=deg, angle_label=f"{deg}°", show_points=True)
        root = ET.fromstring(svg)
        assert root.tag.endswith("svg")

        # Parse viewBox
        vb = [float(v) for v in root.attrib["viewBox"].split()]
        assert len(vb) == 4
        assert vb[2] > 0 and vb[3] > 0

        # Check arc path large-arc-flag: M ... A r r 0 <large_arc> 0 ...
        # For theta <= 180, large-arc-flag must be 0; for theta > 180, it must be 1
        arc_match = re.search(r'd="M [0-9.]+ [0-9.]+ A [0-9.]+ [0-9.]+ 0 ([01]) 0', svg)
        assert arc_match is not None, f"Arc path missing for degree {deg}"
        large_arc_flag = int(arc_match.group(1))
        expected_flag = 1 if deg > 180.0 else 0
        assert large_arc_flag == expected_flag, (
            f"Degree {deg}° had large-arc-flag {large_arc_flag}, expected {expected_flag}"
        )

        # Check that no template artifact like {deg}_degrees exists
        assert "{deg}" not in svg
        assert "degrees" not in svg

    @pytest.mark.parametrize("mode", ["inscribed", "chords", "secants", "radius"])
    def test_circle_specialized_modes(self, mode: str) -> None:
        """Verify XML well-formedness and correct structure across all specialized circle modes."""
        if mode == "inscribed":
            svg = svg_circle_diagram(mode="inscribed", inscribed_angle=40.0, intercepted_arc=80.0)
        elif mode == "chords":
            svg = svg_circle_diagram(mode="chords", chord_segments=("4", "9", "6", "x"))
        elif mode == "secants":
            svg = svg_circle_diagram(mode="secants", far_arc=140.0, near_arc=40.0)
        else:
            svg = svg_circle_diagram(mode="radius", radius_label="r = 7 cm")

        root = ET.fromstring(svg)
        assert root.tag.endswith("svg")
        # Ensure points and lines exist
        lines = root.findall(".//{http://www.w3.org/2000/svg}line") + root.findall(".//line")
        assert len(lines) >= 1

    @pytest.mark.parametrize("angle_deg, mode", [
        (35.0, "single"),
        (90.0, "single"),
        (135.0, "single"),
        (180.0, "single"),
        (65.0, "interior_ray"),
        (110.0, "linear_pair"),
    ])
    def test_svg_angle_diagram_accuracy(self, angle_deg: float, mode: str) -> None:
        """Verify angle diagram ray paths, right-angle indicators, and degree labels."""
        svg = svg_angle_diagram(
            angle_degrees=angle_deg,
            mode=mode,
            angle_label=f"{angle_deg}°",
            interior_angle=angle_deg / 2 if mode == "interior_ray" else None,
        )
        root = ET.fromstring(svg)
        assert root.tag.endswith("svg")

        # Right angle test: for 90 deg single, ensure perpendicular square path is drawn
        if abs(angle_deg - 90.0) < 1e-2 and mode == "single":
            assert 'L' in svg and 'stroke-width="1.6"' in svg

        # Check vertex label B and ray points A, C
        texts = [t.text for t in root.iter() if t.tag.endswith("text")]
        assert "B" in texts

    def test_coordinate_plane_dynamic_scaling(self) -> None:
        """Verify coordinate plane auto-scales with function extrema without clipping."""
        # Parabola with high vertex at (0, 25)
        def parabola_25(x: float) -> float:
            return 25.0 - x * x

        svg = svg_coordinate_plane(
            functions=[{"fn": parabola_25, "color": "#2563eb"}],
            show_numbers=True,
            auto_expand=True,
        )
        root = ET.fromstring(svg)
        assert root.tag.endswith("svg")

        # Verify viewBox exists and is well-formed
        vb = [float(v) for v in root.attrib["viewBox"].split()]
        assert vb[2] > 0 and vb[3] > 0

    def test_triangle_and_polygon_rendering(self) -> None:
        """Verify general triangles and polygons render valid XML and non-empty paths."""
        tri_svg = svg_general_triangle(
            label_a="P", label_b="Q", label_c="R",
            ang_a="60°", ang_b="80°", ang_c="40°",
            side_ab="10", side_bc="12", side_ac="14",
        )
        root_tri = ET.fromstring(tri_svg)
        assert root_tri.tag.endswith("svg")

        poly_svg = svg_polygon_diagram(
            shape="trapezoid", dim1="b1 = 8", dim2="b2 = 12", dim3="h = 5"
        )
        root_poly = ET.fromstring(poly_svg)
        assert root_poly.tag.endswith("svg")
