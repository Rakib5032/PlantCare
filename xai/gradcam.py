import tensorflow as tf
import numpy as np
import cv2

def get_gradcam(model, img_tensor, last_conv_layer_name, pred_index=None):
    """
    Robust Grad-CAM implementation compatible with:
    - EfficientNetV2
    - Frozen models
    - Mixed precision
    - List/Tensor outputs
    """

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(last_conv_layer_name).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_tensor)

        # 🔥 CRITICAL FIX: unwrap predictions safely
        if isinstance(predictions, (list, tuple)):
            predictions = predictions[0]

        # Determine predicted class
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])

        class_channel = predictions[:, pred_index]

    # Compute gradients
    grads = tape.gradient(class_channel, conv_outputs)

    # Safety check
    if grads is None:
        return np.ones(conv_outputs.shape[1:3], dtype=np.float32)

    # Global average pooling
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Weight feature maps
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)

    # Normalize
    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap) + tf.keras.backend.epsilon()

    return heatmap.numpy().astype(np.float32)


def overlay_gradcam(img, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay Grad-CAM heatmap on original image
    """
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, colormap)

    return cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)
