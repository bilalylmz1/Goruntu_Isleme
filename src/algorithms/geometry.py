import numpy as np
import math

def rotate_image(img, angle_degrees):
    angle_rad = math.radians(angle_degrees)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)
    
    h, w = img.shape[:2]
    c_y, c_x = h / 2.0, w / 2.0
    
    new_img = np.zeros_like(img)
    y_indices, x_indices = np.indices((h, w))
    
    y_shifted = y_indices - c_y
    x_shifted = x_indices - c_x
    
    x_old = (x_shifted * cos_theta + y_shifted * sin_theta) + c_x
    y_old = (-x_shifted * sin_theta + y_shifted * cos_theta) + c_y
    
    x_old = np.round(x_old).astype(int)
    y_old = np.round(y_old).astype(int)
    
    valid_mask = (x_old >= 0) & (x_old < w) & (y_old >= 0) & (y_old < h)
    
    if len(img.shape) == 3:
        new_img[y_indices[valid_mask], x_indices[valid_mask], :] = img[y_old[valid_mask], x_old[valid_mask], :]
    else:
        new_img[y_indices[valid_mask], x_indices[valid_mask]] = img[y_old[valid_mask], x_old[valid_mask]]
        
    return new_img

def crop_image(img, y_start, y_end, x_start, x_end):
    h, w = img.shape[:2]
    y_start = max(0, min(y_start, h))
    y_end = max(0, min(y_end, h))
    x_start = max(0, min(x_start, w))
    x_end = max(0, min(x_end, w))
    
    if y_start >= y_end or x_start >= x_end:
        return img.copy()
        
    return img[y_start:y_end, x_start:x_end].copy()

def zoom_image(img, scale_factor):
    if scale_factor <= 0:
        return img.copy()
        
    h, w = img.shape[:2]
    new_h = int(h * scale_factor)
    new_w = int(w * scale_factor)
    
    if len(img.shape) == 3:
        new_img = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
    else:
        new_img = np.zeros((new_h, new_w), dtype=img.dtype)
        
    y_indices = (np.arange(new_h) / scale_factor).astype(int)
    x_indices = (np.arange(new_w) / scale_factor).astype(int)
    
    y_indices = np.clip(y_indices, 0, h - 1)
    x_indices = np.clip(x_indices, 0, w - 1)
    
    xx, yy = np.meshgrid(x_indices, y_indices)
    
    if len(img.shape) == 3:
        new_img = img[yy, xx, :]
    else:
        new_img = img[yy, xx]
        
    return new_img
