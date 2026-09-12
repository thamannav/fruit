# 🍌 Fruit Angle Detector 🍎📐

A complete computer-vision web application that detects multiple fruit species simultaneously and calculates their main orientation axis and angle (in degrees relative to horizontal) using contour extraction and **Principal Component Analysis (PCA)**.

Built for **College Mini-Projects & Hackathons**.

---

## 🌟 Key Features

1. **Multi-Fruit Detection (Not Banana-Only!)**:
   - Detects a wide variety of fruits including:
     - 🍌 Banana
     - 🍎 Apple
     - 🍊 Orange
     - 🍉 Watermelon
     - 🥭 Mango
     - 🍍 Pineapple
     - 🍈 Papaya
     - 🍋 Lemon
     - 🥒 Cucumber
     - 🍐 Pear
     - 🥝 Kiwi
     - and other common fruits.
2. **Zero Guessing Policy**:
   - Uses real computer-vision object detection rather than filename guessing.
   - If an image does not contain a recognized fruit with high confidence, it explicitly reports:
     `"Fruit not confidently detected"` instead of guessing.
3. **Simultaneous Multi-Image Upload**:
   - Select 1, 2, 5, 10, or more images at once.
   - Drag-and-drop support with live thumbnail preview tray.
   - Independent parallel processing for every image.
   - Clean, responsive results grid with "Clear All" functionality.
4. **Mathematical Orientation & Angle Detection**:
   - Uses **Principal Component Analysis (PCA)** and **Minimum-Area Bounding (minAreaRect)** on the segmented fruit body.
   - Calculates the angle relative to horizontal axis:
     - Horizontal right = $0^\circ$
     - Counter-clockwise rotation = positive angle
     - Normalized to $[-90^\circ, +90^\circ]$
   - Does **not** simply use bounding box aspect ratio; computes the true major axis of the fruit contour.
5. **Rich Visual Overlay**:
   - High-contrast major orientation axis line with terminal points.
   - Centroid marker and horizontal reference line.
   - Direct on-image badge: e.g. `"Apple — +32.5°"`.
   - Interactive UI toggle to switch between Annotated and Original images.
   - Real-time animated compass gauge needle showing orientation.

---

## 🚀 How to Run

### Method 1: Double-Click Launcher (Easiest)
Simply double-click:
```bash
run.bat
```
This activates the local Python environment and launches the server at `http://localhost:8000`.

### Method 2: Command Line
```powershell
# Activate the virtual environment
.venv\Scripts\activate

# Launch the FastAPI application
python main.py
```
Open your browser and navigate to:
```
http://localhost:8000
```

---

## 📐 Mathematical Formulation

### 1. Fruit Segmentation
Inside the detected fruit bounding box $(x_1, y_1, x_2, y_2)$, adaptive multi-channel color thresholding (Otsu luminance + HSV saturation) is applied to extract the foreground fruit mask and external boundary contour $\mathcal{C} = \{(x_i, y_i)\}_{i=1}^N$.

### 2. Centroid & Covariance Matrix
$$\bar{x} = \frac{1}{N} \sum_{i=1}^N x_i, \quad \bar{y} = \frac{1}{N} \sum_{i=1}^N y_i$$

$$\mathbf{C} = \frac{1}{N} \sum_{i=1}^N \begin{bmatrix} x_i - \bar{x} \\ y_i - \bar{y} \end{bmatrix} \begin{bmatrix} x_i - \bar{x} \\ y_i - \bar{y} \end{bmatrix}^T$$

### 3. Principal Direction Vector
The eigenvectors of $\mathbf{C}$ are computed:
$$\mathbf{C} \vec{v}_1 = \lambda_1 \vec{v}_1 \quad (\lambda_1 \ge \lambda_2)$$
The principal eigenvector $\vec{v}_1 = (v_x, v_y)$ defines the fruit's major physical axis.

### 4. Angle Normalization to $[-90^\circ, +90^\circ]$
Because image coordinates have $y$ directed downwards:
$$\Delta x = v_x, \quad \Delta y = -v_y$$
$$\theta = \text{atan2}(\Delta y, \Delta x) \times \frac{180}{\pi}$$
Normalized to $[-90^\circ, +90^\circ]$ where counter-clockwise relative to horizontal right ($0^\circ$) is positive.

---

## 📁 Project Structure

```
FruitAngleDetector/
│
├── main.py              # FastAPI server & API endpoints (/api/analyze)
├── detector.py          # Vision object detector & PCA orientation math
├── run.bat              # 1-click Windows runner
├── requirements.txt     # Python dependencies
├── README.md            # Documentation & project guide
│
├── static/              # Frontend web application
│   ├── index.html       # Modern responsive web layout
│   ├── style.css        # Glassmorphic dark theme & animations
│   └── app.js           # Drag-and-drop, compass gauge, batch processing
│
└── .venv/               # Isolated Python 3.11 environment
```

---

## 🧪 Testing with Demo Images
If you don't have fruit images immediately handy:
1. Open `http://localhost:8000`.
2. Click the **"✨ Load Demo Images"** button.
3. Click **"⚡ Analyze Images"** to watch the computer-vision engine detect the fruits, draw the orientation vectors, and calculate angles in real time!
