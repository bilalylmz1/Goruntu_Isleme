import numpy as np
from algorithms.filters import apply_convolution

def prewitt_edge_detection(img_gray):
    """
    Modül 12: Kenar Bulma (Prewitt)
    """
    Kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    Ky = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    
    # Konvolüsyon işlemi (apply_convolution fonksiyonumuzdan)
    Gx = apply_convolution(img_gray, Kx).astype(np.float32)
    Gy = apply_convolution(img_gray, Ky).astype(np.float32)
    
    # Gradyan büyüklüğü
    G = np.sqrt(Gx**2 + Gy**2)
    return np.clip(G, 0, 255).astype(np.uint8)
