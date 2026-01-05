let selectedFile = null;

// ===============================
// IMAGE INPUT & PREVIEW
// ===============================
document.getElementById("imageInput").addEventListener("change", (event) => {
    selectedFile = event.target.files[0];

    if (!selectedFile) return;

    const preview = document.getElementById("previewImg");
    preview.src = URL.createObjectURL(selectedFile);
    preview.style.display = "block";

    // Reset outputs
    document.getElementById("result").innerHTML = "";
    document.getElementById("xaiOutput").innerHTML = "";
    document.getElementById("xaiBtn").classList.add("hidden");
});

// ===============================
// CLEAR EVERYTHING
// ===============================
function clearAll() {
    selectedFile = null;

    document.getElementById("imageInput").value = "";
    document.getElementById("previewImg").src = "/static/images/placeholder.jpg";
    document.getElementById("result").innerHTML = "";
    document.getElementById("xaiOutput").innerHTML = "";
    document.getElementById("xaiBtn").classList.add("hidden");
}

// ===============================
// ANALYZE IMAGE
// ===============================
async function analyze() {
    if (!selectedFile) {
        alert("Please select or capture an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<p>⏳ Analyzing image...</p>";

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // LOW CONFIDENCE CASE
        if (data.status === "low_confidence") {
            resultDiv.innerHTML = `
                <p style="color:#d32f2f;">
                    ⚠️ Low confidence (${data.confidence}%).
                    Please try another image.
                </p>
            `;
            return;
        }

        // SUCCESS
        document.getElementById("xaiBtn").classList.remove("hidden");

        resultDiv.innerHTML = `
            <h3>🌱 ${data.prediction}</h3>
            <p><b>Confidence:</b> ${data.confidence}%</p>
            <p><b>Suggestion:</b> ${data.advice.suggestion}</p>
            <p><b>Treatment:</b> ${data.advice.treatment}</p>
            <p><b>Prevention:</b> ${data.advice.prevention}</p>
        `;

    } catch (error) {
        resultDiv.innerHTML = "<p style='color:red;'>❌ Prediction failed.</p>";
        console.error(error);
    }
}

// ===============================
// SHOW GRAD-CAM XAI
// ===============================
async function showXAI() {
    if (!selectedFile) return;

    const xaiBtn = document.getElementById("xaiBtn");
    xaiBtn.innerText = "⏳ Generating XAI...";

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("/api/gradcam", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const img = document.createElement("img");
        img.src = "data:image/png;base64," + data.gradcam;
        img.style.width = "100%";
        img.style.borderRadius = "12px";
        img.style.marginTop = "10px";

        const xaiOutput = document.getElementById("xaiOutput");
        xaiOutput.innerHTML = "";
        xaiOutput.appendChild(img);

        xaiBtn.innerText = "🔍 XAI Result (Grad-CAM)";

    } catch (error) {
        console.error(error);
        xaiBtn.innerText = "❌ XAI Failed";
    }
}
