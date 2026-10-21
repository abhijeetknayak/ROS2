import math


def image_megapixels(width: int, height: int) -> float:
    """Return the number of megapixels in an image.

    Example: a 1000 x 1000 image contains 1.0 megapixel.
    """
    return width * height / 1_000_000.0


def planar_speed(vx: float, vy: float) -> float:
    """Return the magnitude of a planar velocity vector in metres/second."""
    return math.hypot(vx, vy)


def yaw_from_quaternion(x: float, y: float, z: float, w: float) -> float:
    """Return planar yaw in radians from a quaternion.

    Use the standard ROS quaternion-to-yaw expression based on atan2.
    """
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)
