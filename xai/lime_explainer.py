import numpy as np
import tensorflow as tf
from lime import lime_image
from skimage.segmentation import mark_boundaries

IMG_SIZE = (224, 224)

def predict_fn(images, model):
    """
    LIME expects a batch prediction function
    """
    images = images.astype(np.float32)
    preds = model.predict(images, verbose=0)
    return preds


def generate_lime(model, image_np, class_idx):
    """
    Generate LIME explanation for a single image
    """

    explainer = lime_image.LimeImageExplainer()

    explanation = explainer.explain_instance(
        image_np,
        classifier_fn=lambda x: predict_fn(x, model),
        top_labels=1,
        hide_color=0,
        num_samples=1000
    )

    temp, mask = explanation.get_image_and_mask(
        label=class_idx,
        positive_only=True,
        hide_rest=False,
        num_features=10
    )

    lime_img = mark_boundaries(temp / 255.0, mask)
    lime_img = (lime_img * 255).astype(np.uint8)

    return lime_img
