import io
import json
import base64
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image


from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
from xai.gradcam import get_gradcam, overlay_gradcam

# =====================================================
# APP CONFIG
# =====================================================
app = FastAPI(title="PlantCare AI")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =====================================================
# PATHS & CONSTANTS
# =====================================================
MODEL_PATH = "model/best_v2b3_frozen.keras"
CLASS_PATH = "model/class_names.txt"
ADVICE_PATH = "data/advice.json"

IMG_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.60


# =====================================================
# LOAD MODEL & DATA
# =====================================================
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

with open(CLASS_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

with open(ADVICE_PATH, "r", encoding="utf-8") as f:
    advice_data = json.load(f)

# =====================================================
# IMAGE PREPROCESSING (EfficientNetV2)
# =====================================================
def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)
    img_array = np.array(image, dtype=np.float32)
    img_array = preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

# =====================================================
# HOME
# =====================================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# =====================================================
# PREDICTION API
# =====================================================
@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    img_tensor = preprocess_image(image)

    preds = model.predict(img_tensor, verbose=0)[0]
    confidence = float(np.max(preds))
    class_idx = int(np.argmax(preds))
    class_name = class_names[class_idx]

    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "status": "low_confidence",
            "confidence": round(confidence * 100, 2)
        }

    advice = advice_data.get(class_name, {})

    return {
        "status": "success",
        "prediction": class_name,
        "confidence": round(confidence * 100, 2),
        "advice": advice
    }

# =====================================================
# GRAD-CAM XAI API (USING YOUR LOGIC)
# =====================================================
@app.post("/api/gradcam")
async def gradcam(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image_resized = image.resize(IMG_SIZE)

    img_array = np.array(image_resized, dtype=np.float32)
    img_tensor = preprocess_input(img_array)
    img_tensor = np.expand_dims(img_tensor, axis=0)

    # Generate Grad-CAM heatmap
    heatmap = get_gradcam(
        model=model,
        img_tensor=img_tensor,
        last_conv_layer_name="top_conv"
    )

    # Overlay heatmap
    cam_image = overlay_gradcam(
        img=np.array(image_resized),
        heatmap=heatmap
    )

    _, buffer = cv2.imencode(".png", cam_image)
    encoded_img = base64.b64encode(buffer).decode("utf-8")

    return {
        "status": "success",
        "gradcam": encoded_img
    }



# =====================================================
# HEALTH CHECK (Render)
# =====================================================
@app.get("/health")
def health():
    return {"status": "ok"}
