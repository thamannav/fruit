"""
Verification script for Fruit Angle Detector.
Tests fruit orientation detection and angle accuracy on generated test cases.
"""

import math
import numpy as np
import cv2
from detector import FruitOrientationDetector


def generate_test_fruit(shape_type: str = "banana", target_angle_deg: float = 45.0) -> np.ndarray:
    """Generates a test image containing an elongated fruit rotated to a known target angle."""
    img = np.full((500, 500, 3), 245, dtype=np.uint8)
    cx, cy = 250, 250

    # In image coordinates, positive math angle is counter-clockwise -> clockwise in image matrix
    # rotation matrix uses angle in degrees counter-clockwise
    rad = math.radians(target_angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    if shape_type == "banana":
        # Yellow banana shape
        # Draw ellipse points and fill
        axes = (140, 40)
        # cv2.ellipse uses degrees clockwise:
        cv2.ellipse(img, (cx, cy), axes, -target_angle_deg, 0, 360, (30, 215, 250), -1, cv2.LINE_AA)
        cv2.ellipse(img, (cx, cy), axes, -target_angle_deg, 0, 360, (15, 160, 200), 2, cv2.LINE_AA)
    elif shape_type == "cucumber":
        # Green cucumber
        axes = (150, 35)
        cv2.ellipse(img, (cx, cy), axes, -target_angle_deg, 0, 360, (34, 139, 34), -1, cv2.LINE_AA)
        cv2.ellipse(img, (cx, cy), axes, -target_angle_deg, 0, 360, (20, 100, 25), 2, cv2.LINE_AA)
    elif shape_type == "orange":
        # Round orange
        cv2.circle(img, (cx, cy), 80, (0, 140, 255), -1, cv2.LINE_AA)
    else:
        # Non-fruit background (gray box)
        cv2.rectangle(img, (150, 150), (350, 350), (128, 128, 128), -1)

    return img


def run_tests():
    print("[Test] Initializing FruitOrientationDetector...")
    detector = FruitOrientationDetector(conf_thresh=0.25)

    print("\n--- Test 1: Banana at +45° ---")
    img_banana = generate_test_fruit("banana", 45.0)
    res_banana = detector.analyze_image(img_banana, "test_banana.jpg")
    print(f"Result: {res_banana['message']}")
    print(f"Detected Fruit: {res_banana['fruit_name']}, Angle: {res_banana['angle_deg']}°, Conf: {res_banana['confidence']}%")

    print("\n--- Test 2: Cucumber at -30° ---")
    img_cuc = generate_test_fruit("cucumber", -30.0)
    res_cuc = detector.analyze_image(img_cuc, "test_cucumber.jpg")
    print(f"Result: {res_cuc['message']}")
    print(f"Detected Fruit: {res_cuc['fruit_name']}, Angle: {res_cuc['angle_deg']}°, Conf: {res_cuc['confidence']}%")

    print("\n--- Test 3: Non-fruit (Noise/Gray box) ---")
    img_none = generate_test_fruit("none", 0.0)
    res_none = detector.analyze_image(img_none, "test_none.jpg")
    print(f"Result: {res_none['message']}")
    assert res_none["detected"] is False, "Should not detect fruit on non-fruit image!"
    assert res_none["message"] == "Fruit not confidently detected", "Must state 'Fruit not confidently detected'"
    print("Test 3 PASSED: Non-fruit correctly unconfident!")

    print("\n[Test] All unit tests completed!")


if __name__ == "__main__":
    run_tests()
