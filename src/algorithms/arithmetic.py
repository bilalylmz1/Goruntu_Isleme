import numpy as np
import cv2 # Sadece resize için gerekirse (ama manuelde numpy olmalı)

def image_add(img1, img2, ratio=0.5):
    """
    ratio: img1'in ağırlığıdır (alpha).
    Boyutlar uyuşmazsa OpenCV ile eşitliyoruz ki arayüz çökmesin.
    """
    if img1.shape != img2.shape:
        # Arayüz deneyimi için uyumsuzlukta 2. resmi 1'e uyduruyoruz
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
    mat1 = img1.astype(np.float32)
    mat2 = img2.astype(np.float32)
    
    blended = (mat1 * ratio) + (mat2 * (1.0 - ratio))
    return np.clip(blended, 0, 255).astype(np.uint8)

def image_divide(img, scalar):
    if scalar == 0:
        scalar = 1.0
    mat = img.astype(np.float32)
    divided = mat / scalar
    return np.clip(divided, 0, 255).astype(np.uint8)
