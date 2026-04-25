import numpy as np

def apply_threshold(img_gray, threshold_val):
    """
    Modül 2 & 11: Binary Dönüşüm ve Tek Eşikleme
    Verilen eşik (threshold_val) değerinin üzerini beyaz (255),
    altını siyah (0) yapar.
    """
    binary_img = np.zeros_like(img_gray)
    binary_img[img_gray > threshold_val] = 255
    return binary_img
