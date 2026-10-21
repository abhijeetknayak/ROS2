import math


def image_megapixels(width: int, height: int) -> float:
    """Return the number of megapixels in an image.

    Example: a 1000 x 1000 image contains 1.0 megapixel.
    """
    # TODO(student): multiply width and height, then convert pixels to
    # megapixels. This should be a one-line calculation.
    return (width * height) / 1e6


def planar_speed(vx: float, vy: float) -> float:
    """Return the magnitude of a planar velocity vector in metres/second."""
    # TODO(student): use the Pythagorean theorem. The math module is already
    # imported above.
    return 0.0


def yaw_from_quaternion(x: float, y: float, z: float, w: float) -> float:
    """Return planar yaw in radians from a quaternion.

    Use the standard ROS quaternion-to-yaw expression based on atan2.
    """
    # TODO(student): compute the numerator and denominator for atan2, then
    # return math.atan2(numerator, denominator).
    return 0.0
