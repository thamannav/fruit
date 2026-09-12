"""
Fruit Angle Detector - Main Web Server
FastAPI backend handling multi-image uploads, computer-vision orientation detection,
and serving the modern UI.
"""

import base64
import os
import io
from typing import List
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from detector import FruitOrientationDetector

# Initialize FastAPI application
app = FastAPI(
    title="Fruit Angle Detector",
    description="Multi-image fruit orientation & angle detection API",
    version="1.0.0"
)

# Enable CORS for flexible development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize computer vision detector
print("[Server] Initializing FruitOrientationDetector...")
detector = FruitOrientationDetector(conf_thresh=0.30)
print("[Server] Detector initialized successfully.")

# Ensure static directories exist
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
SAMPLES_DIR = os.path.join(STATIC_DIR, "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def bgr_to_base64_jpeg(bgr_img: np.ndarray, quality: int = 90) -> str:
    """Encodes an OpenCV BGR image to a base64 Data URL JPEG string."""
    success, buffer = cv2.imencode(".jpg", bgr_img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not success:
        return ""
    b64_str = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_str}"


@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serves the main web app index.html."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h2>Fruit Angle Detector is starting up... Please refresh in a moment.</h2>")


@app.get("/api/health")
async def health_check():
    """Returns system and model health status."""
    return {
        "status": "online",
        "model_type": detector.model_type,
        "supported_fruits": len(detector.model.names) if hasattr(detector.model, "names") else 80
    }


@app.post("/api/analyze")
async def analyze_images(files: List[UploadFile] = File(...)):
    """
    Analyzes multiple uploaded fruit images simultaneously.
    Processes every image independently and returns fruit detection,
    orientation angle (-90° to +90°), and annotated images.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No images provided.")

    results = []

    for file in files:
        filename = file.filename or "uploaded_image.jpg"
        try:
            # Read file bytes
            contents = await file.read()
            if not contents:
                results.append({
                    "filename": filename,
                    "detected": False,
                    "fruit_name": "Unknown",
                    "confidence": 0.0,
                    "angle_deg": 0.0,
                    "message": "Empty file received",
                    "original_image": "",
                    "annotated_image": ""
                })
                continue

            # Decode image with OpenCV
            nparr = np.frombuffer(contents, np.uint8)
            img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img_bgr is None:
                # Try Pillow fallback
                try:
                    pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
                    img_rgb = np.array(pil_img)
                    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                except Exception:
                    img_bgr = None

            if img_bgr is None:
                results.append({
                    "filename": filename,
                    "detected": False,
                    "fruit_name": "Unknown",
                    "confidence": 0.0,
                    "angle_deg": 0.0,
                    "message": "Could not decode image file",
                    "original_image": "",
                    "annotated_image": ""
                })
                continue

            # Keep original base64 for UI comparison
            original_b64 = bgr_to_base64_jpeg(img_bgr, quality=85)

            # Analyze fruit & compute orientation angle
            analysis = detector.analyze_image(img_bgr, filename=filename)

            # Encode annotated image
            annotated_bgr = analysis["annotated_bgr"]
            annotated_b64 = bgr_to_base64_jpeg(annotated_bgr, quality=90)

            results.append({
                "filename": filename,
                "detected": analysis["detected"],
                "fruit_name": analysis["fruit_name"],
                "confidence": analysis["confidence"],
                "angle_deg": analysis["angle_deg"],
                "message": analysis["message"],
                "box": analysis.get("box"),
                "center": analysis.get("center"),
                "axis_vector": analysis.get("axis_vector"),
                "original_image": original_b64,
                "annotated_image": annotated_b64
            })

        except Exception as err:
            print(f"[Server] Error processing {filename}: {err}")
            results.append({
                "filename": filename,
                "detected": False,
                "fruit_name": "Error",
                "confidence": 0.0,
                "angle_deg": 0.0,
                "message": f"Processing error: {str(err)}",
                "original_image": "",
                "annotated_image": ""
            })

    return JSONResponse(content={"total": len(results), "results": results})


@app.get("/api/samples")
async def get_sample_list():
    """Lists available demo sample images."""
    if not os.path.exists(SAMPLES_DIR):
        return []
    samples = [
        f for f in os.listdir(SAMPLES_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ]
    return samples


if __name__ == "__main__":
    import uvicorn
    print("\n========================================================")
    print("   Starting Fruit Angle Detector Web Server on port 8000")
    print("   Access via: http://localhost:8000")
    print("========================================================\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
