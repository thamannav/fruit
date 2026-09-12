"""
Fruit Angle Detector - Core Vision & Orientation Engine
Detects fruits (banana, apple, orange, watermelon, mango, pineapple, papaya, lemon, cucumber, pear, kiwi, etc.)
and computes the mathematical orientation (major axis & angle in degrees [-90°, +90°]).
"""

import math
import numpy as np
import cv2
from typing import Dict, Any, Optional, Tuple, List

# Target fruit classes for open-vocabulary and standard detectors
SUPPORTED_FRUITS = [
    "banana", "apple", "orange", "watermelon", "mango", "pineapple",
    "papaya", "lemon", "cucumber", "pear", "kiwi", "strawberry",
    "grape", "peach", "avocado", "pomegranate", "plum", "guava",
    "dragon fruit", "cantaloupe", "lime"
]

# Alternate label mappings to normalize detections
FRUIT_ALIASES = {
    "granny smith": "apple",
    "custard apple": "apple",
    "citrus": "orange",
    "mandarin": "orange",
    "tangerine": "orange",
    "rock melon": "watermelon",
    "water melon": "watermelon",
    "pine apple": "pineapple",
    "kiwifruit": "kiwi",
    "kiwi fruit": "kiwi",
}


class FruitOrientationDetector:
    """
    Combines deep-learning object detection with mathematical contour
    and Principal Component Analysis (PCA) to find the orientation angle of fruits.
    """

    def __init__(self, model_name: str = "yolov8n.pt", conf_thresh: float = 0.30):
        self.conf_thresh = conf_thresh
        self.model = None
        self.model_type = "yolov8n"
        self._load_model(model_name)

    def _load_model(self, model_name: str):
        """Attempts to load YOLO-World for open vocabulary fruits, with graceful fallback to standard YOLOv8."""
        try:
            from ultralytics import YOLO
            print(f"[Detector] Loading primary model: {model_name}...")
            try:
                self.model = YOLO(model_name)
                # Configure custom fruit classes for YOLO-World
                if hasattr(self.model, "set_classes"):
                    self.model.set_classes(SUPPORTED_FRUITS)
                print(f"[Detector] Successfully loaded {model_name}")
            except Exception as e:
                print(f"[Detector] Failed to load {model_name} ({e}), falling back to yolov8n.pt...")
                self.model = YOLO("yolov8n.pt")
                self.model_type = "yolov8n"
                print("[Detector] Successfully loaded yolov8n.pt")
        except Exception as e:
            print(f"[Detector] Warning: Could not initialize Ultralytics YOLO: {e}")
            self.model = None

    def analyze_image(self, image_bgr: np.ndarray, filename: str = "") -> Dict[str, Any]:
        """
        Analyze a single fruit image:
        1. Detect fruit bounding box and class (confidence check).
        2. Extract fruit contour & segment foreground.
        3. Compute major axis using PCA & minimum-area rectangle.
        4. Calculate angle relative to horizontal in [-90°, +90°].
        5. Draw major axis, angle arc, and label badge onto image.
        """
        h_img, w_img = image_bgr.shape[:2]

        # Step 1: Detect fruit
        detection = self._detect_fruit(image_bgr)
        if not detection:
            # Cannot confidently identify a fruit
            annotated = self._draw_unconfident_badge(image_bgr)
            return {
                "detected": False,
                "fruit_name": "Unknown",
                "confidence": 0.0,
                "angle_deg": 0.0,
                "message": "Fruit not confidently detected",
                "annotated_bgr": annotated,
                "box": None,
                "major_axis": None
            }

        fruit_name = detection["class_name"]
        conf = round(float(detection["conf"]) * 100, 1)
        x1, y1, x2, y2 = detection["box"]

        # Step 2: Crop fruit region with small padding for contour analysis
        pad_x = max(10, int((x2 - x1) * 0.08))
        pad_y = max(10, int((y2 - y1) * 0.08))
        crop_x1 = max(0, x1 - pad_x)
        crop_y1 = max(0, y1 - pad_y)
        crop_x2 = min(w_img, x2 + pad_x)
        crop_y2 = min(h_img, y2 + pad_y)

        crop = image_bgr[crop_y1:crop_y2, crop_x1:crop_x2]

        # Step 3: Segment fruit & compute mathematical orientation
        contour_global, center, axis_vector, angle_deg, axis_len = self._compute_orientation(
            image_bgr, crop, (crop_x1, crop_y1, crop_x2, crop_y2), (x1, y1, x2, y2)
        )

        # Step 4: Draw visual annotations on image
        annotated = self._draw_annotations(
            image_bgr.copy(),
            fruit_name=fruit_name,
            angle_deg=angle_deg,
            conf=conf,
            center=center,
            axis_vector=axis_vector,
            axis_len=axis_len,
            box=(x1, y1, x2, y2),
            contour=contour_global
        )

        return {
            "detected": True,
            "fruit_name": fruit_name.capitalize(),
            "confidence": conf,
            "angle_deg": angle_deg,
            "message": f"Successfully detected {fruit_name.capitalize()} at {angle_deg}°",
            "annotated_bgr": annotated,
            "box": [int(x1), int(y1), int(x2), int(y2)],
            "center": [float(center[0]), float(center[1])],
            "axis_vector": [float(axis_vector[0]), float(axis_vector[1])]
        }

    def _detect_fruit(self, image_bgr: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Uses deep-learning model to find fruit objects.
        If deep learning is initializing or unavailable, utilizes computer-vision
        calibrated color/contour segmentation as a resilient fallback.
        """
        if self.model is not None:
            try:
                results = self.model(image_bgr, verbose=False)
                if results and len(results) > 0:
                    best_detection = None
                    best_conf = 0.0

                    for r in results:
                        boxes = r.boxes
                        if boxes is None:
                            continue

                        for box in boxes:
                            cls_id = int(box.cls[0].item())
                            conf = float(box.conf[0].item())
                            raw_name = r.names.get(cls_id, "").lower().strip()

                            # Normalize alias if any
                            norm_name = FRUIT_ALIASES.get(raw_name, raw_name)

                            # Check if it matches supported fruits or is recognized as fruit
                            is_fruit = False
                            matched_name = norm_name

                            for sf in SUPPORTED_FRUITS:
                                if sf in norm_name or norm_name in sf:
                                    is_fruit = True
                                    matched_name = sf
                                    break

                            # Also accept generic standard COCO fruit indices if using standard YOLO
                            if not is_fruit and self.model_type == "yolov8n":
                                coco_fruit_map = {46: "banana", 47: "apple", 49: "orange"}
                                if cls_id in coco_fruit_map:
                                    is_fruit = True
                                    matched_name = coco_fruit_map[cls_id]

                            if is_fruit and conf >= self.conf_thresh:
                                if conf > best_conf:
                                    best_conf = conf
                                    coords = box.xyxy[0].tolist()
                                    best_detection = {
                                        "class_name": matched_name,
                                        "conf": conf,
                                        "box": [int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])]
                                    }

                    if best_detection is not None:
                        return best_detection
            except Exception as e:
                print(f"[Detector] YOLO inference warning: {e}. Switching to CV fallback.")

        # Computer-Vision Fallback (Color Space & Morphology Segmentation)
        return self._detect_fruit_cv_fallback(image_bgr)

    def _detect_fruit_cv_fallback(self, image_bgr: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Computer-vision color & morphology segmentation engine.
        Identifies fruit species based on calibrated HSV/LAB color profiles and contour area.
        Ensures strict confidence: non-fruit images return None ('Fruit not confidently detected').
        """
        h_img, w_img = image_bgr.shape[:2]
        total_pixels = h_img * w_img

        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        # Fruit color definition profiles: (name, lower_hsv, upper_hsv, min_aspect, name_display)
        profiles = [
            ("banana", np.array([18, 80, 80]), np.array([36, 255, 255])),
            ("lemon", np.array([24, 100, 120]), np.array([38, 255, 255])),
            ("orange", np.array([9, 120, 100]), np.array([23, 255, 255])),
            ("apple_red_1", np.array([0, 100, 70]), np.array([8, 255, 255])),
            ("apple_red_2", np.array([170, 100, 70]), np.array([180, 255, 255])),
            ("apple_green", np.array([36, 70, 60]), np.array([75, 255, 255])),
            ("cucumber", np.array([36, 60, 30]), np.array([85, 255, 220])),
            ("watermelon", np.array([35, 50, 20]), np.array([85, 255, 180])),
            ("kiwi", np.array([12, 50, 40]), np.array([28, 160, 160])),
        ]

        best_cand = None
        max_fruit_area = 0

        # Check for red apple combined mask
        mask_red1 = cv2.inRange(hsv, np.array([0, 100, 70]), np.array([8, 255, 255]))
        mask_red2 = cv2.inRange(hsv, np.array([170, 100, 70]), np.array([180, 255, 255]))
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        test_masks = [
            ("apple", mask_red),
            ("banana", cv2.inRange(hsv, np.array([18, 80, 80]), np.array([36, 255, 255]))),
            ("orange", cv2.inRange(hsv, np.array([9, 120, 100]), np.array([23, 255, 255]))),
            ("lemon", cv2.inRange(hsv, np.array([24, 110, 130]), np.array([38, 255, 255]))),
            ("cucumber", cv2.inRange(hsv, np.array([36, 60, 30]), np.array([85, 255, 220]))),
        ]

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

        for fruit_name, raw_mask in test_masks:
            cleaned = cv2.morphologyEx(raw_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel, iterations=1)

            contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue

            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            # Strict threshold: Must occupy at least 3% of the image to be a foreground fruit
            # and not exceed 95% (which would be a solid background screen)
            if area > (total_pixels * 0.03) and area < (total_pixels * 0.95):
                if area > max_fruit_area:
                    max_fruit_area = area
                    bx, by, bw, bh = cv2.boundingRect(largest)
                    # Confidence calculated based on color density and area
                    conf = min(0.95, max(0.55, area / (bw * bh + 1e-5)))
                    best_cand = {
                        "class_name": fruit_name,
                        "conf": round(conf, 2),
                        "box": [bx, by, bx + bw, by + bh]
                    }

        return best_cand

    def _compute_orientation(
        self,
        full_img: np.ndarray,
        crop: np.ndarray,
        crop_coords: Tuple[int, int, int, int],
        fruit_box: Tuple[int, int, int, int]
    ) -> Tuple[Optional[np.ndarray], Tuple[float, float], Tuple[float, float], float, float]:
        """
        Extracts contour using adaptive color segmentation and computes
        the major axis using Principal Component Analysis (PCA) and minAreaRect.
        """
        cx1, cy1, cx2, cy2 = crop_coords
        bx1, by1, bx2, by2 = fruit_box
        w_crop = cx2 - cx1
        h_crop = cy2 - cy1

        # 1. Segment the fruit contour inside the crop
        mask = self._extract_fruit_mask(crop, (bx1 - cx1, by1 - cy1, bx2 - cx1, by2 - cy1))

        # 2. Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not contours:
            # Fallback to bounding box center and diagonal/major axis
            ctr_x = (bx1 + bx2) / 2.0
            ctr_y = (by1 + by2) / 2.0
            bw = bx2 - bx1
            bh = by2 - by1
            axis_len = max(bw, bh) * 0.9
            if bw >= bh:
                vec = (1.0, 0.0)
                angle = 0.0
            else:
                vec = (0.0, -1.0)
                angle = 90.0
            return None, (ctr_x, ctr_y), vec, angle, axis_len

        # Select the largest contour by area
        primary_contour = max(contours, key=cv2.contourArea)

        # 3. Principal Component Analysis (PCA) on contour points
        pts = primary_contour.reshape(-1, 2).astype(np.float32)

        # Minimum points check
        if len(pts) < 10:
            rect = cv2.minAreaRect(primary_contour)
            center_crop, (rw, rh), rect_angle = rect
            vec, angle, axis_len = self._angle_from_min_area_rect(rect)
            center_global = (center_crop[0] + cx1, center_crop[1] + cy1)
            contour_global = primary_contour + np.array([cx1, cy1])
            return contour_global, center_global, vec, angle, axis_len

        # Compute Mean and Covariance Matrix
        mean, eigenvectors, eigenvalues = cv2.PCACompute2(pts, mean=np.empty((0)))
        center_crop = (mean[0, 0], mean[0, 1])

        # Principal eigenvector (first row) corresponds to the largest eigenvalue / major axis
        vx = eigenvectors[0, 0]
        vy = eigenvectors[0, 1]

        # Calculate angle relative to horizontal axis
        # In image coordinates, y increases downwards.
        # So math dy = -vy, dx = vx.
        math_angle_rad = math.atan2(-vy, vx)
        math_angle_deg = math.degrees(math_angle_rad)

        # Normalize angle strictly to [-90°, +90°]
        norm_angle = self._normalize_angle(math_angle_deg)

        # Calculate major axis extent along the fruit contour
        axis_len = self._calculate_contour_span(pts, center_crop, (vx, vy))

        # Cross-verify with minAreaRect for stability
        rect = cv2.minAreaRect(primary_contour)
        rect_vec, rect_angle, rect_len = self._angle_from_min_area_rect(rect)

        # If PCA eigenvalue ratio is close to 1 (near-circular fruit like orange),
        # or if minAreaRect provides sharper major direction, blend or verify:
        if eigenvalues[0, 0] > 0 and (eigenvalues[1, 0] / eigenvalues[0, 0]) > 0.85:
            # Round fruit: use contour minAreaRect
            norm_angle = rect_angle
            vx, vy = rect_vec

        # Direction vector in image space
        # We ensure standard unit vector matching normalized angle:
        # math_angle = norm_angle -> vx = cos(norm_angle), vy = -sin(norm_angle)
        rad = math.radians(norm_angle)
        unit_vec = (math.cos(rad), -math.sin(rad))

        center_global = (center_crop[0] + cx1, center_crop[1] + cy1)
        contour_global = primary_contour + np.array([cx1, cy1])

        return contour_global, center_global, unit_vec, round(norm_angle, 1), axis_len

    def _extract_fruit_mask(self, crop: np.ndarray, local_box: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Segments fruit foreground from background inside crop using color spaces and thresholding.
        """
        h_crop, w_crop = crop.shape[:2]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # Otsu thresholding
        _, thresh_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Also check color saturation in HSV to catch vibrant fruits on light/dark backgrounds
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        sat = hsv[:, :, 1]
        _, thresh_sat = cv2.threshold(sat, 30, 255, cv2.THRESH_BINARY)

        # Combine cues
        combined = cv2.bitwise_or(thresh_otsu, thresh_sat)

        # Morphological filtering to close holes and remove background speckles
        kernel_clean = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel_clean, iterations=2)
        opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_clean, iterations=1)

        # Ensure mask is focused around the fruit detection box center
        lbx1, lby1, lbx2, lby2 = local_box
        box_mask = np.zeros((h_crop, w_crop), dtype=np.uint8)
        box_mask[max(0, lby1):min(h_crop, lby2), max(0, lbx1):min(w_crop, lbx2)] = 255

        final_mask = cv2.bitwise_and(opened, box_mask)
        # If masked area is too sparse, fall back to opened mask
        if cv2.countNonZero(final_mask) < 100:
            final_mask = opened

        return final_mask

    def _angle_from_min_area_rect(self, rect: Tuple[Tuple[float, float], Tuple[float, float], float]) -> Tuple[Tuple[float, float], float, float]:
        """
        Derives angle in [-90°, +90°] from cv2.minAreaRect.
        Horizontal right = 0°, CCW = positive.
        """
        (cx, cy), (w, h), angle = rect

        # In OpenCV, angle is between -90 and 0 (or 0 and 90 depending on version).
        # We find the orientation of the longer side (major axis):
        box_pts = cv2.boxPoints(rect)
        edge1 = box_pts[1] - box_pts[0]
        edge2 = box_pts[2] - box_pts[1]

        len1 = np.linalg.norm(edge1)
        len2 = np.linalg.norm(edge2)

        if len1 >= len2:
            major_vec = edge1
            major_len = len1
        else:
            major_vec = edge2
            major_len = len2

        # Convert image vector (x right, y down) to Cartesian (x right, y up)
        dx = float(major_vec[0])
        dy = -float(major_vec[1])

        deg = math.degrees(math.atan2(dy, dx))
        norm_deg = self._normalize_angle(deg)

        rad = math.radians(norm_deg)
        unit_vec = (math.cos(rad), -math.sin(rad))
        return unit_vec, round(norm_deg, 1), float(major_len)

    def _normalize_angle(self, angle_deg: float) -> float:
        """
        Normalizes an axis angle to [-90°, +90°].
        Horizontal right = 0°.
        Counter-clockwise = positive (+1° to +90°).
        Clockwise = negative (-1° to -90°).
        """
        while angle_deg > 90.0:
            angle_deg -= 180.0
        while angle_deg <= -90.0:
            angle_deg += 180.0
        return angle_deg

    def _calculate_contour_span(self, pts: np.ndarray, center: Tuple[float, float], unit_vec: Tuple[float, float]) -> float:
        """Calculates extent of contour points projected onto the major axis unit vector."""
        cx, cy = center
        ux, uy = unit_vec
        # Project each point onto the axis vector
        projections = (pts[:, 0] - cx) * ux + (pts[:, 1] - cy) * uy
        span = float(np.max(projections) - np.min(projections))
        return max(span * 0.95, 40.0)

    def _draw_annotations(
        self,
        img: np.ndarray,
        fruit_name: str,
        angle_deg: float,
        conf: float,
        center: Tuple[float, float],
        axis_vector: Tuple[float, float],
        axis_len: float,
        box: Tuple[int, int, int, int],
        contour: Optional[np.ndarray]
    ) -> np.ndarray:
        """
        Renders clear, professional computer-vision visualization:
        1. Detected bounding box with subtle accent.
        2. Fruit contour highlight.
        3. Major axis line with glowing double-stroke and terminal points.
        4. Centroid circle.
        5. Horizontal dashed reference line at center.
        6. Angle arc showing direction from horizontal.
        7. Clean floating label badge: "[Fruit] — [Angle]°".
        """
        h_img, w_img = img.shape[:2]
        cx, cy = int(center[0]), int(center[1])
        ux, uy = axis_vector
        half_len = max(axis_len / 2.0, 35.0)

        # 1. Subtle fruit contour outline
        if contour is not None:
            cv2.drawContours(img, [contour], -1, (0, 230, 118), 2, lineType=cv2.LINE_AA)

        # 2. Horizontal baseline reference (dashed or subtle gray line through center)
        ref_x1 = max(10, cx - int(half_len * 0.8))
        ref_x2 = min(w_img - 10, cx + int(half_len * 0.8))
        self._draw_dashed_line(img, (ref_x1, cy), (ref_x2, cy), (200, 200, 200), 1, gap=6)

        # 3. Major orientation axis endpoints
        p1 = (int(cx - ux * half_len), int(cy - uy * half_len))
        p2 = (int(cx + ux * half_len), int(cy + uy * half_len))

        # Double-stroke major line for maximum visibility on any background (light or dark)
        # Background shadow line
        cv2.line(img, p1, p2, (15, 23, 42), 6, lineType=cv2.LINE_AA)
        # Foreground vibrant neon line (Cyan / Electric Blue)
        cv2.line(img, p1, p2, (0, 229, 255), 3, lineType=cv2.LINE_AA)

        # Terminal dots for major axis
        cv2.circle(img, p1, 5, (0, 229, 255), -1, lineType=cv2.LINE_AA)
        cv2.circle(img, p1, 7, (15, 23, 42), 2, lineType=cv2.LINE_AA)
        cv2.circle(img, p2, 5, (0, 229, 255), -1, lineType=cv2.LINE_AA)
        cv2.circle(img, p2, 7, (15, 23, 42), 2, lineType=cv2.LINE_AA)

        # 4. Centroid anchor
        cv2.circle(img, (cx, cy), 6, (255, 255, 255), -1, lineType=cv2.LINE_AA)
        cv2.circle(img, (cx, cy), 8, (15, 23, 42), 2, lineType=cv2.LINE_AA)
        cv2.circle(img, (cx, cy), 3, (0, 229, 255), -1, lineType=cv2.LINE_AA)

        # 5. Angle arc (between horizontal right and major axis vector)
        arc_radius = min(35, int(half_len * 0.5))
        if arc_radius > 12 and abs(angle_deg) > 2:
            # OpenCV ellipse angles: 0 is horizontal right, clockwise is positive in ellipse API.
            # In our system, positive angle_deg is counter-clockwise (so -angle_deg in OpenCV ellipse)
            if angle_deg > 0:
                start_a = int(-angle_deg)
                end_a = 0
            else:
                start_a = 0
                end_a = int(-angle_deg)
            cv2.ellipse(img, (cx, cy), (arc_radius, arc_radius), 0, start_a, end_a, (255, 191, 0), 2, lineType=cv2.LINE_AA)

        # 6. Label Badge directly on the image: e.g. "Apple — 32.5°"
        sign_str = "+" if angle_deg > 0 else ""
        label_text = f"{fruit_name.capitalize()}  {sign_str}{angle_deg:.1f}°"
        badge_y = max(40, box[1] - 12)
        badge_x = max(15, box[0])
        self._draw_pill_badge(img, label_text, (badge_x, badge_y), bg_color=(15, 23, 42), text_color=(255, 255, 255), accent_color=(0, 229, 255))

        return img

    def _draw_unconfident_badge(self, img: np.ndarray) -> np.ndarray:
        """Renders the required 'Fruit not confidently detected' label when detection fails."""
        out = img.copy()
        h, w = out.shape[:2]
        text = "Fruit not confidently detected"
        pos = (w // 2, h // 2)
        self._draw_centered_pill_badge(out, text, pos, bg_color=(20, 24, 33), text_color=(248, 113, 113), border_color=(239, 68, 68))
        return out

    def _draw_pill_badge(
        self,
        img: np.ndarray,
        text: str,
        pos: Tuple[int, int],
        bg_color: Tuple[int, int, int] = (15, 23, 42),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        accent_color: Tuple[int, int, int] = (0, 229, 255)
    ):
        """Draws a modern badge with rounded appearance and accent dot."""
        x, y = pos
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.65
        thickness = 2
        (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        pad_x = 14
        pad_y = 8
        bx1 = x
        by1 = max(5, y - th - pad_y * 2)
        bx2 = min(img.shape[1] - 5, bx1 + tw + pad_x * 2 + 16)
        by2 = by1 + th + pad_y * 2

        # Semi-transparent pill background
        overlay = img.copy()
        cv2.rectangle(overlay, (bx1, by1), (bx2, by2), bg_color, -1)
        cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)

        # Border
        cv2.rectangle(img, (bx1, by1), (bx2, by2), accent_color, 1, lineType=cv2.LINE_AA)

        # Accent dot
        dot_center = (bx1 + 10, by1 + (by2 - by1) // 2)
        cv2.circle(img, dot_center, 4, accent_color, -1, lineType=cv2.LINE_AA)

        # Text
        text_pos = (bx1 + 22, by2 - pad_y - 2)
        cv2.putText(img, text, text_pos, font, font_scale, text_color, thickness, lineType=cv2.LINE_AA)

    def _draw_centered_pill_badge(
        self,
        img: np.ndarray,
        text: str,
        center_pos: Tuple[int, int],
        bg_color: Tuple[int, int, int],
        text_color: Tuple[int, int, int],
        border_color: Tuple[int, int, int]
    ):
        """Draws a centered warning pill badge."""
        cx, cy = center_pos
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        pad_x = 18
        pad_y = 10
        bx1 = max(5, cx - tw // 2 - pad_x)
        by1 = max(5, cy - th // 2 - pad_y)
        bx2 = min(img.shape[1] - 5, cx + tw // 2 + pad_x)
        by2 = min(img.shape[0] - 5, cy + th // 2 + pad_y)

        overlay = img.copy()
        cv2.rectangle(overlay, (bx1, by1), (bx2, by2), bg_color, -1)
        cv2.addWeighted(overlay, 0.90, img, 0.10, 0, img)
        cv2.rectangle(img, (bx1, by1), (bx2, by2), border_color, 2, lineType=cv2.LINE_AA)

        text_pos = (bx1 + pad_x, by2 - pad_y - 2)
        cv2.putText(img, text, text_pos, font, font_scale, text_color, thickness, lineType=cv2.LINE_AA)

    def _draw_dashed_line(
        self,
        img: np.ndarray,
        pt1: Tuple[int, int],
        pt2: Tuple[int, int],
        color: Tuple[int, int, int],
        thickness: int = 1,
        gap: int = 5
    ):
        """Draws a dashed line between pt1 and pt2."""
        dist = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
        if dist == 0:
            return
        dx = (pt2[0] - pt1[0]) / dist
        dy = (pt2[1] - pt1[1]) / dist

        curr = 0.0
        draw = True
        while curr < dist:
            next_step = min(curr + gap, dist)
            if draw:
                p_start = (int(pt1[0] + dx * curr), int(pt1[1] + dy * curr))
                p_end = (int(pt1[0] + dx * next_step), int(pt1[1] + dy * next_step))
                cv2.line(img, p_start, p_end, color, thickness, lineType=cv2.LINE_AA)
            draw = not draw
            curr = next_step
