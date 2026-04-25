import numpy as np

def rgb_to_gray(img_rgb):
    """Gri dönüşüm formülü: 0.299R + 0.587G + 0.114B"""
    R = img_rgb[:, :, 0].astype(np.float32)
    G = img_rgb[:, :, 1].astype(np.float32)
    B = img_rgb[:, :, 2].astype(np.float32)
    gray = 0.299 * R + 0.587 * G + 0.114 * B
    return np.clip(gray, 0, 255).astype(np.uint8)

def rgb_to_hsv(img_rgb):
    """RGB'den HSV'ye manuel dönüşüm."""
    R_norm = img_rgb[:, :, 0] / 255.0
    G_norm = img_rgb[:, :, 1] / 255.0
    B_norm = img_rgb[:, :, 2] / 255.0

    Cmax = np.max(img_rgb / 255.0, axis=2)
    Cmin = np.min(img_rgb / 255.0, axis=2)
    delta = Cmax - Cmin

    H = np.zeros_like(Cmax)
    mask_r = (Cmax == R_norm) & (delta != 0)
    H[mask_r] = 60 * (((G_norm[mask_r] - B_norm[mask_r]) / delta[mask_r]) % 6)
    
    mask_g = (Cmax == G_norm) & (delta != 0)
    H[mask_g] = 60 * (((B_norm[mask_g] - R_norm[mask_g]) / delta[mask_g]) + 2)
    
    mask_b = (Cmax == B_norm) & (delta != 0)
    H[mask_b] = 60 * (((R_norm[mask_b] - G_norm[mask_b]) / delta[mask_b]) + 4)

    S = np.zeros_like(Cmax)
    mask_cmax = Cmax != 0
    S[mask_cmax] = delta[mask_cmax] / Cmax[mask_cmax]

    V = Cmax

    H = (H / 2).astype(np.uint8)
    S = (S * 255).astype(np.uint8)
    V = (V * 255).astype(np.uint8)

    hsv_img = np.zeros_like(img_rgb)
    hsv_img[:, :, 0] = H
    hsv_img[:, :, 1] = S
    hsv_img[:, :, 2] = V
    return hsv_img

def rgb_to_ycbcr(img_rgb):
    """RGB'den YCbCr'ye manuel dönüşüm."""
    R = img_rgb[:, :, 0].astype(np.float32)
    G = img_rgb[:, :, 1].astype(np.float32)
    B = img_rgb[:, :, 2].astype(np.float32)

    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = 128 - 0.168736 * R - 0.331264 * G + 0.5 * B
    Cr = 128 + 0.5 * R - 0.418688 * G - 0.081312 * B

    ycbcr_img = np.zeros_like(img_rgb)
    ycbcr_img[:, :, 0] = np.clip(Y, 0, 255).astype(np.uint8)
    ycbcr_img[:, :, 1] = np.clip(Cb, 0, 255).astype(np.uint8)
    ycbcr_img[:, :, 2] = np.clip(Cr, 0, 255).astype(np.uint8)
    return ycbcr_img
