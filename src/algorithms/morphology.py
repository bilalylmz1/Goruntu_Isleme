import numpy as np

def erosion(binary_img, kernel_size=3):
    h, w = binary_img.shape
    pad = kernel_size // 2
    padded = np.pad(binary_img, pad, mode='constant', constant_values=0) # Aşınmada aslında 255 (beyaz) pad daha iyidir, ancak basitlik için 0
    output = np.zeros_like(binary_img)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kernel_size, j:j+kernel_size]
            # Tüm komşular 255 ise merkez 255 kalır
            if np.all(region == 255):
                output[i, j] = 255
            else:
                output[i, j] = 0
    return output

def dilation(binary_img, kernel_size=3):
    h, w = binary_img.shape
    pad = kernel_size // 2
    padded = np.pad(binary_img, pad, mode='constant', constant_values=0)
    output = np.zeros_like(binary_img)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kernel_size, j:j+kernel_size]
            # Komşularda en az bir 255 varsa merkez 255 olur
            if np.any(region == 255):
                output[i, j] = 255
            else:
                output[i, j] = 0
    return output

def opening(binary_img, kernel_size=3):
    # Önce aşınma, sonra genişleme (gürültü siler)
    eroded = erosion(binary_img, kernel_size)
    return dilation(eroded, kernel_size)

def closing(binary_img, kernel_size=3):
    # Önce genişleme, sonra aşınma (kırıkları kapatır)
    dilated = dilation(binary_img, kernel_size)
    return erosion(dilated, kernel_size)
