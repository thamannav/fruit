<img width="1280" height="640" alt="Fruit Angle Detector" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Fruit Angle Detector 🍌📐

> “We solved a problem nobody had. Powered by questionable science.”

---

## Basic Details

### Team Name: Questionable Botanists

### Team Members
- Team Lead: Thamanna V

### Project Description
A computer-vision web application that detects multiple fruit species simultaneously and calculates their exact major orientation axis and angle (in degrees relative to horizontal) using contour extraction and **Principal Component Analysis (PCA)** — complete with 11 hilarious, scientifically questionable, and completely useless features.

### The Problem (that doesn't exist)
For millions of years, humans have picked up bananas, sliced apples, and chopped cucumbers without ever knowing whether their fruit was lying down at 0°, feeling diagonal at 45°, or having an existential crisis at -42.1°. The global scientific community was shockingly silent on the precise angular inclination of a watermelon.

### The Solution (that nobody asked for)
**Fruit Angle Detector**: An end-to-end computer-vision system that:
1. Detects diverse fruits (banana, apple, orange, watermelon, mango, pineapple, lemon, cucumber, pear, kiwi, etc.) using deep-learning object detection (never guessing from filenames).
2. Extracts the fruit contour and computes its major orientation axis using **Principal Component Analysis (PCA)** on the contour covariance matrix.
3. Normalizes the angle relative to horizontal right ($0^\circ$) to $[-90^\circ, +90^\circ]$.
4. Draws the major axis line, centroid, angle arc, and label directly onto the image.
5. Equips every fruit with a personality, horoscope, mood, uselessness score, playful roast, kitchen verdict, and official printable certificate.

---

## 🍓 11 Hilariously Useless Features

1. **Fruit Personality**: Randomized funny personality based on species (e.g. *Banana → “Chill guy. Just hanging around.”*, *Apple → “Teacher's pet energy.”*, *Watermelon → “Thinks it's a bowling ball.”*).
2. **Fruit Horoscope**: Silly predictions (e.g. *“Today's prediction: You will probably become a smoothie.”*).
3. **Angle-Based Mood**: Uses the **REAL detected angle** to assign moods (e.g. *0° → “I'm lying down. Don't disturb me.”*, *45° → “I'm feeling diagonal today.”*, *90° → “Standing tall 💪”*, *-45° → “Questioning my life choices.”*).
4. **Uselessness Score**: Displays *Uselessness Score: 97%*, *Scientific importance: 0.3%*, *Entertainment value: 100%*.
5. **🔥 Roast My Fruit**: Playfully roasts the fruit using its actual species and angle (*“Your banana is at 35°. Even it doesn't know where it's going.”*).
6. **🍴 Should I Eat It?**: Randomized kitchen oracle responses (*“YES.”*, *“Why are you asking an app?”*, *“The angle is acceptable. Proceed.”*).
7. **❓ WHY? Button**: Dramatic animated 3-step reveal explaining that nobody knows why we measure fruit angles, but at least we know the exact angle.
8. **🔬 Rotating Loading Messages**: Rotating progress indicators during analysis (*“Consulting the banana council...”*, *“AI is judging your fruit...”*).
9. **🏆 Official Fruit Angle Certificate**: Generates a printable certificate certifying the fruit's position for no important reason.
10. **❤️ Fruit Compatibility**: Pairs multiple detected fruits with compatibility percentages and relationship statuses (*“Probably a smoothie.”*, *“Better as a fruit salad.”*).
11. **🏆 Useless Leaderboard**: Crowns the *Most Tilted Fruit*, *Most Confused Fruit*, and *Most Dramatic Fruit*.

---

## Technical Details

### Technologies Used
- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Computer Vision & Math**: OpenCV, Ultralytics YOLOv8, NumPy, Pillow, Principal Component Analysis (PCA)
- **Frontend**: Vanilla CSS (Glassmorphism dark theme, dynamic SVG dials), Vanilla JavaScript, HTML5

---

## Implementation & How to Run

### Quick Run (Windows)
Double-click:
```cmd
run.bat
```
This automatically sets up the environment and opens `http://localhost:8000`.

### Manual Setup
```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # On Windows
source .venv/bin/activate # On Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python main.py
```
Open your browser at `http://localhost:8000`.

---

## 📐 Mathematical Formulation

### 1. Centroid & Covariance Matrix
Inside the detected bounding box $(x_1, y_1, x_2, y_2)$, adaptive thresholding extracts the boundary contour $\mathcal{C} = \{(x_i, y_i)\}_{i=1}^N$:
$$\bar{x} = \frac{1}{N} \sum_{i=1}^N x_i, \quad \bar{y} = \frac{1}{N} \sum_{i=1}^N y_i$$
$$\mathbf{C} = \frac{1}{N} \sum_{i=1}^N \begin{bmatrix} x_i - \bar{x} \\ y_i - \bar{y} \end{bmatrix} \begin{bmatrix} x_i - \bar{x} \\ y_i - \bar{y} \end{bmatrix}^T$$

### 2. Principal Direction Vector
The eigenvectors of $\mathbf{C}$ give the principal axis:
$$\mathbf{C} \vec{v}_1 = \lambda_1 \vec{v}_1 \quad (\lambda_1 \ge \lambda_2)$$

### 3. Angle Normalization
$$\theta = \text{atan2}(-\Delta y_{img}, \Delta x_{img}) \times \frac{180}{\pi} \in [-90^\circ, +90^\circ]$$
where counter-clockwise from horizontal right ($0^\circ$) is positive.

---

## Project Structure
```
FruitAngleDetector/
├── main.py              # FastAPI server & endpoints
├── detector.py          # Vision object detector & PCA orientation math
├── run.bat              # One-click Windows runner
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── test_detector.py     # Verification tests
└── static/              # Web application
    ├── index.html       # Responsive UI with modals & leaderboard
    ├── style.css        # Glassmorphic dark theme & animations
    ├── app.js           # Multi-image upload, gauges & fun widgets
    └── samples/         # Demo fruit images
```

---

Made with ❤️ at TinkerHub Useless Projects

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
