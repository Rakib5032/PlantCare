# 🌿 PlantCare AI - Disease Detection System

A comprehensive web application for detecting plant diseases using deep learning and explainable AI techniques.

![PlantCare AI](https://img.shields.io/badge/AI-Powered-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)

---

## ✨ Features

- 🌿 **29 Disease Detection** — Detects 29 different plant diseases across 6 plant types  
- 📸 **Dual Input** — Upload images or capture directly from camera  
- 🎯 **High Accuracy** — Predictions with confidence scores (90%+ accuracy)  
- 💡 **Treatment Recommendations** — Expert advice for each disease  
- 🔬 **Explainable AI** — Grad-CAM visualization showing model attention  
- 📱 **Responsive Design** — Works on desktop, tablet, and mobile  
- 🎨 **Modern UI** — Gradient design with smooth animations  

---

## 🌱 Supported Plants

Our AI can detect diseases in these 6 plant types:

1. **Eggplant** 🍆 — 7 conditions  
2. **Guava** 🥭 — 8 conditions  
3. **Luffa** 🥒 — 2 conditions  
4. **Rose** 🌹 — 4 conditions  
5. **Sweet Orange** 🍊 — 3 conditions  
6. **Tea** 🍵 — 5 conditions  

---

## 📁 Project Structure


```
project_root/
├─ app.py                     # Main Streamlit application
├─ requirements.txt           # Python dependencies
├─ README.md                  # Project documentation
├─ .gitignore                 # Git ignore file
│
├─ model/                     # Saved model files
│   └─ final_model.h5        # Trained EfficientNetV2B3 model
│
├─ static/                    # Static assets
│   ├─ css/                  # CSS files (embedded in app)
│   └─ js/                   # JavaScript files
│
├─ uploads/                   # Temporarily store uploaded images
│   └─ .gitkeep
│
├─ xai_outputs/               # Grad-CAM / SHAP / LIME results
│   └─ .gitkeep
│
├─ suggestions/               # Disease information database
│   └─ disease_suggestions.json
│
└─ utils/                     # Helper modules
    ├─ __init__.py
    ├─ preprocessing.py      # Image preprocessing functions
    ├─ gradcam.py           # Grad-CAM implementation
    └─ xai.py               # XAI utilities (SHAP, LIME)


---

## 🖼️ Image Requirements

- **Format**: JPG, JPEG, or PNG  
- **Size**: Maximum 10MB  
- **Quality**: Clear, well-lit images work best  
- **Content**: Single leaf or fruit with visible symptoms  

---

## 🔬 Model Information

- **Architecture**: EfficientNetV2B3  
- **Input Size**: 224 × 224 × 3 (RGB)  
- **Output Classes**: 29 plant diseases  
- **Last Conv Layer**: `top_conv` (used for Grad-CAM)  
- **Training Dataset**: Custom dataset with 6 plant types  

---

## 🛠️ Technical Details

### Dependencies

- **FastAPI** — Web application framework  
- **TensorFlow** — Deep learning model inference  
- **OpenCV** — Image processing and Grad-CAM overlay  
- **Pillow** — Image handling  
- **NumPy** — Numerical operations  
- **Pandas** — Data manipulation (optional)  

---

## 🧠 XAI Methods

### Current

- ✅ **Grad-CAM** — Implemented and working  

### Coming Soon

- ⏳ **SHAP** — Shapley Additive Explanations  
- ⏳ **LIME** — Local Interpretable Model-agnostic Explanations  

---

## 📊 Performance

- **Accuracy**: 97%+ on test dataset  
- **Inference Time**: < 2 seconds per image  

---

## 📝 Future Enhancements

- [ ] SHAP integration  
- [ ] LIME integration  
- [ ] Mobile app version (React Native)  
- [ ] Multi-language support  
- [ ] Disease progression tracking  
- [ ] Community forum for farmers  
- [ ] Expert consultation booking  
- [ ] Batch image processing  
- [ ] Public API for integrations  
- [ ] Historical data analytics  

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Rakib5032** — *Initial work*

---

## 🙏 Acknowledgments

- Dataset contributors  
- TensorFlow team  
- FastAPI team  
- All farmers and gardeners who helped test the application  

---

## 📧 Contact

For questions, suggestions, or support:

- **GitHub**: https://github.com/Rakib5032  

---

## 📸 App Screenshots

![Home Page](images/image.png)  
![Upload Image](images/image-1.png)  
![Prediction Result](images/image-2.png)  
![Grad-CAM Visualization](images/image-3.png)  

---

**Built with ❤️ for farmers and gardeners worldwide**

🌿 Happy Farming! 🌿
