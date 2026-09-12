<img width="1280" height="640" alt="Fruit Angle Detector" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Fruit Angle Detector 🍌📐

> “We solved a problem nobody had. Powered by questionable science.”

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![YOLOv8](https://img.shields.io/badge/Detector-Ultralytics_YOLOv8-00FFFF?style=flat)](https://ultralytics.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![TinkerHub](https://img.shields.io/badge/TinkerHub-Useless_Projects_2026-FFB300?style=flat)](https://tinkerhub.org/)

A computer-vision web application that detects multiple fruit species simultaneously and calculates their exact major orientation axis and angle (in degrees relative to horizontal) using contour extraction and **Principal Component Analysis (PCA)** — complete with 11 hilarious, scientifically questionable, and completely useless features.

---

## 👥 Team
- **Thamanna V** — Team Lead
- **Adisha** — Team Member

---

## 💡 Why This Project Exists

For generations, humans have looked at fruit and asked standard, boring questions: *“Is it ripe?”*, *“Is it organic?”*, *“Can I eat it?”* 

Nobody stopped to ask the really important question: 
> **“At what precise mathematical angle is this banana leaning relative to the Cartesian horizontal axis?”**

Fruit Angle Detector bravely fills this profound void in human knowledge.

---

## 🧐 The Problem (That Doesn't Exist)

For millions of years, humans have picked up bananas, sliced apples, and chopped cucumbers without ever knowing whether their fruit was:
- Lying down in horizontal zen mode ($0^\circ$),
- Feeling diagonal and ambitious ($+45^\circ$),
- Standing tall with authority ($90^\circ$), or
- Experiencing an existential crisis at $-42.1^\circ$.

The global scientific community has remained shockingly silent on the precise angular inclination of a watermelon. We decided enough was enough.

---

## 🚀 The Solution (That Nobody Asked For)

**Fruit Angle Detector** is an end-to-end computer-vision system that:
1. **Detects Multiple Fruits Simultaneously**: Identifies bananas, apples, oranges, watermelons, cucumbers, lemons, and more using deep learning without ever guessing from filenames.
2. **Segments the Fruit Contour**: Isolates the fruit pixels from the background using multi-channel color thresholding.
3. **Applies Principal Component Analysis (PCA)**: Calculates the true major orientation axis of the fruit contour points.
4. **Measures Angle in Degrees**: Normalizes the angle relative to horizontal right ($0^\circ$) strictly into $[-90^\circ, +90^\circ]$.
5. **Draws Rich Overlays**: Renders glowing orientation vectors, centroid markers, angle arcs, and badges directly on the image.
6. **Delivers 11 Pointless Features**: From roasting the fruit's posture to generating printable official certificates.

---

## ⚙️ How It Works

The end-to-end pipeline processes every uploaded image independently:

```
[ Upload Image(s) ] 
       │
       ▼
[ 1. Object Detection ] ──► YOLOv8 locates fruit bounding ROI (Zero-guessing confidence check)
       │
       ▼
[ 2. Fruit Segmentation ] ──► Otsu & HSV color filtering extracts boundary contour C
       │
       ▼
[ 3. PCA Mathematics ] ────► Centroid (x̄, ȳ) & Covariance Matrix C are computed
       │
       ▼
[ 4. Eigenvector Analysis ] ─► Principal eigenvector v₁ defines the major physical axis
       │
       ▼
[ 5. Angle Normalization ] ─► atan2(-Δy, Δx) maps orientation strictly to [-90°, +90°]
       │
       ▼
[ 6. Visual Annotation ] ──► Vector lines, baseline, angle arc & label badge rendered
       │
       ▼
[ 7. Fun Engine ] ─────────► Personalities, horoscopes, moods, roasts & certificate generated
```

---

## 🧠 Why PCA? (Principal Component Analysis)

### The Limitation of Bounding Boxes
A naive approach to finding an object's angle is checking the width and height of an axis-aligned bounding box. **This completely fails** when a fruit is diagonal or rotated:
- A $45^\circ$ diagonal banana has a square bounding box ($W \approx H$), which gives zero information about its true tilt.
- Fitting arbitrary bounding boxes can easily flip or jitter with minor edge noise.

### The PCA Advantage
**Principal Component Analysis** treats all pixels along the segmented fruit contour as a 2D data distribution:
1. It computes the **center of mass (centroid)** of the fruit.
2. It computes the **covariance matrix** representing how the contour points spread out in 2D space.
3. The **eigenvector corresponding to the largest eigenvalue** points exactly along the direction of maximum variance — which is the true physical major axis of the fruit.

This ensures accurate angle detection whether the fruit is horizontal, vertical, diagonal, or rotated.

---

## 🍓 11 Hilariously Useless Features

| # | Feature | Description | Example |
|---|---|---|---|
| **1** | **Fruit Personality** | Funny personality assigned based on species | 🍌 Banana: *“Chill guy. Just hanging around.”* |
| **2** | **Fruit Horoscope** | Silly cosmic prediction for the fruit | *“Today's prediction: You will probably become a smoothie.”* |
| **3** | **Angle-Based Mood** | Mood derived from the **REAL detected angle** | $45^\circ$: *“I'm feeling diagonal today. 📐”* |
| **4** | **Uselessness Score** | Scientific audit of pointlessness | **Score: 97%** • Scientific Importance: 0.3% • Fun: 100% |
| **5** | **🔥 Roast My Fruit** | Playful roast based on species & angle | *“Your banana is at 35°. Even it doesn't know where it's going.”* |
| **6** | **🍴 Should I Eat It?** | Kitchen oracle advice button | *“The angle is acceptable. Proceed.”* |
| **7** | **❓ WHY? Button** | Dramatic 3-step animated modal | *“Why? Nobody knows. But at least we know it's 37.4°.”* |
| **8** | **🔬 Funny Loading Messages** | Rotating messages during image analysis | *“Consulting the banana council...”* |
| **9** | **🏆 Fruit Certificate** | Printable official certificate modal | Official Fruit Angle Certificate with gold seal |
| **10** | **❤️ Fruit Compatibility** | Chemistry match when 2+ fruits are analyzed | Apple + Banana: 87% (*“Probably a smoothie.”*) |
| **11** | **🏆 Useless Leaderboard** | Hall of Fame across batch images | **Most Tilted**, **Most Confused**, **Most Dramatic** |

---

## 🛠️ Technical Details

### Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| **Backend Framework** | FastAPI & Uvicorn | High-performance asynchronous API for batch processing |
| **Computer Vision** | OpenCV & Ultralytics YOLOv8 | Object detection, contour extraction & image annotation |
| **Math & Matrix Ops** | NumPy | Covariance calculation, eigenvectors & angle trigonometry |
| **Image Processing** | Pillow (PIL) | Multi-format image decoding fallback & transformations |
| **Frontend Structure** | Semantic HTML5 | Clean accessible layout with modal dialogs & preview tray |
| **Styling & Theme** | Vanilla CSS (Glassmorphism) | Dark theme, neon accents, responsive grid, dynamic dials |
| **Client Interactivity** | Vanilla JavaScript | Drag-and-drop, dynamic gauges, certificates & popovers |

---

## 📐 Mathematical Formulation

### 1. Contour Extraction & Centroid
Inside the detected bounding box $(x_1, y_1, x_2, y_2)$, adaptive thresholding extracts the boundary contour $\mathcal{C} = \{(x_i, y_i)\}_{i=1}^N$:

$$\bar{x} = \frac{1}{N} \sum_{i=1}^N x_i, \quad \bar{y} = \frac{1}{N} \sum_{i=1}^N y_i$$

*Calculates the center of mass (centroid) of the fruit contour.*

### 2. Covariance Matrix
$$\mathbf{C} = \frac{1}{N} \sum_{i=1}^N \begin{bmatrix} x_i - \bar{x} \\ y_i - \bar{y} \end{bmatrix} \begin{bmatrix} x_i - \bar{x} \\ y_i - \bar{y} \end{bmatrix}^T = \begin{bmatrix} \sigma_{xx} & \sigma_{xy} \\ \sigma_{xy} & \sigma_{yy} \end{bmatrix}$$

*Measures the directional spread and physical dispersion of the fruit points in 2D space.*

### 3. Principal Direction Vector
The eigenvalues and eigenvectors of $\mathbf{C}$ satisfy:

$$\mathbf{C} \vec{v}_1 = \lambda_1 \vec{v}_1, \quad \mathbf{C} \vec{v}_2 = \lambda_2 \vec{v}_2 \quad (\lambda_1 \ge \lambda_2)$$

*The principal eigenvector $\vec{v}_1 = (v_x, v_y)$ points along the major axis of the fruit.*

### 4. Angle Normalization to $[-90^\circ, +90^\circ]$
Because image coordinates have $y$ directed downwards, we invert $\Delta y$:

$$\Delta x = v_x, \quad \Delta y = -v_y$$

$$\theta = \text{atan2}(\Delta y, \Delta x) \times \frac{180}{\pi}$$

The angle is normalized to $[-90^\circ, +90^\circ]$ where:
- Horizontal right = $0^\circ$
- Counter-clockwise tilt = positive angle ($+1^\circ$ to $+90^\circ$)
- Clockwise tilt = negative angle ($-1^\circ$ to $-90^\circ$)

---

## 📖 How to Use

1. **Launch the App**: Run `run.bat` or start `python main.py` and navigate to `http://localhost:8000`.
2. **Select Fruit Images**:
   - Drag & drop 1, 2, 5, 10+ fruit photos into the upload zone, **OR**
   - Click **“📁 Upload Images”** to browse your computer, **OR**
   - Click **“✨ Load Demo Images”** for instant sample fruits.
3. **Analyze**: Click **“⚡ Analyze Images”** and watch the rotating funny loading messages.
4. **Explore the Results**:
   - Inspect the detected fruit name, confidence, and major axis line.
   - Watch the animated compass gauge align with the real fruit angle.
   - Click **“👁️ View Original”** to toggle between the raw photo and annotated visual.
   - Read the fruit's **Personality**, **Horoscope**, and **Angle Mood**.
   - Click **“🔥 Roast My Fruit”** for a playful custom burn.
   - Click **“🍴 Should I Eat It?”** for culinary oracle advice.
   - Click **“❓ WHY?”** for existential clarity.
   - Click **“🏆 Certificate”** to view and print your official certificate.
5. **Multi-Fruit Batches**: Check the **Fruit Compatibility** score and **Useless Leaderboard** (Most Tilted, Most Confused, Most Dramatic).

---

## 🚀 Implementation & How to Run

### Quick Run (Windows)
Double-click:
```cmd
run.bat
```
*This automatically activates `.venv`, verifies dependencies, launches the server, and opens `http://localhost:8000` in your browser.*

### Manual Setup
```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the web application
python main.py
```
Open your browser at `http://localhost:8000`.

---

## 📁 Project Structure

```
FruitAngleDetector/
├── main.py              # FastAPI server & /api/analyze batch endpoint
├── detector.py          # Vision object detector & PCA orientation engine
├── run.bat              # One-click Windows runner
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── test_detector.py     # Automated verification unit tests
└── static/              # Web application
    ├── index.html       # Responsive UI layout, modals & leaderboard
    ├── style.css        # Glassmorphic dark design system & animations
    ├── app.js           # Multi-image upload, dials, roasts & certificate
    └── samples/         # Demo fruit images for instant testing
```

---

## 🔮 Future (Useless) Improvements

- [ ] **Bluetooth Smart Fruit Protractor**: Hardware integration to physically measure fruit on kitchen counters.
- [ ] **Fruit Astrology 2.0**: Full birth chart calculation based on when the fruit was harvested.
- [ ] **Audio Fruit Roasts**: Text-to-speech voice roasting the fruit out loud.
- [ ] **3D Fruit Gyroscope**: Interactive Three.js 3D model mirroring the fruit's real-time orientation.

---

Made with ❤️ at TinkerHub Useless Projects

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
