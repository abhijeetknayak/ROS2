import math

import pytest

from ros2_intro_nodes.student_helpers import (
    image_megapixels,
    planar_speed,
    yaw_from_quaternion,
)


def test_image_megapixels() -> None:
    assert image_megapixels(1000, 1000) == pytest.approx(1.0)
    assert image_megapixels(640, 360) == pytest.approx(0.2304)


def test_planar_speed() -> None:
    assert planar_speed(3.0, 4.0) == pytest.approx(5.0)
    assert planar_speed(0.0, 0.0) == pytest.approx(0.0)


def test_yaw_from_quaternion() -> None:
    half_angle = math.pi / 4.0
    yaw = yaw_from_quaternion(0.0, 0.0, math.sin(half_angle), math.cos(half_angle))
    assert yaw == pytest.approx(math.pi / 2.0)
