import numpy as np

def apply_convolution(img_gray, kernel):
    k_h, k_w = kernel.shape
    pad_h = k_h // 2
    pad_w = k_w // 2
    h, w = img_gray.shape
    padded_img = np.pad(img_gray, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    output = np.zeros_like(img_gray, dtype=np.float32)
    
    # Python döngüleri ile matris çarpımı yavaş olacağı için NumPy dilimleme kullanabiliriz,
    # Ama projenin kuralı "Matematiksel altyapıyı sıfırdan uygulamak" olduğu için döngü kullanılıyor.
    for i in range(h):
        for j in range(w):
            region = padded_img[i:i+k_h, j:j+k_w]
            output[i, j] = np.sum(region * kernel)
    return np.clip(output, 0, 255).astype(np.uint8)

def mean_filter(img_gray, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size * kernel_size)
    return apply_convolution(img_gray, kernel)

def add_salt_and_pepper_noise(img_gray, prob=0.05):
    noisy_img = np.copy(img_gray)
    h, w = noisy_img.shape
    r = np.random.rand(h, w)
    noisy_img[r < prob/2] = 255
    noisy_img[(r >= prob/2) & (r < prob)] = 0
    return noisy_img

def median_filter(img_gray, kernel_size=3):
    h, w = img_gray.shape
    pad = kernel_size // 2
    padded_img = np.pad(img_gray, pad, mode='constant', constant_values=0)
    output = np.zeros_like(img_gray)
    for i in range(h):
        for j in range(w):
            region = padded_img[i:i+kernel_size, j:j+kernel_size]
            output[i, j] = np.median(region)
    return output

def unsharp_masking(img_gray, k=1.0):
    """
    Modül 14: Unsharp Maskeleme
    """
    blurred = mean_filter(img_gray, kernel_size=3)
    mask = img_gray.astype(np.float32) - blurred.astype(np.float32)
    sharpened = img_gray.astype(np.float32) + (k * mask)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
