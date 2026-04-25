import numpy as np

def calculate_histogram(img_gray):
    return np.bincount(img_gray.ravel(), minlength=256)

def histogram_stretching(img_gray):
    min_val = np.min(img_gray)
    max_val = np.max(img_gray)
    if max_val == min_val:
        return img_gray.copy()
    stretched = ((img_gray.astype(np.float32) - min_val) / (max_val - min_val)) * 255.0
    return np.clip(stretched, 0, 255).astype(np.uint8)

def enhance_contrast(img_gray, alpha, beta):
    """
    Modül 9: Kontrast Artırma
    yeni_piksel = clip(alpha * eski_piksel + beta, 0, 255)
    """
    enhanced = img_gray.astype(np.float32) * alpha + beta
    return np.clip(enhanced, 0, 255).astype(np.uint8)
