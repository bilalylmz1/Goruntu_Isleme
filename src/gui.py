import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

# Sprint 1
from algorithms.color import rgb_to_gray, rgb_to_hsv, rgb_to_ycbcr
from algorithms.threshold import apply_threshold
# Sprint 2
from algorithms.geometry import rotate_image, crop_image, zoom_image
from algorithms.arithmetic import image_add, image_divide
# Sprint 3
from algorithms.contrast import histogram_stretching, enhance_contrast, calculate_histogram
from algorithms.filters import mean_filter, median_filter, add_salt_and_pepper_noise, unsharp_masking
# Sprint 4
from algorithms.edge import prewitt_edge_detection
from algorithms.morphology import erosion, dilation, opening, closing

# Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Görüntü İşleme Eğitim Aracı - Final")
        self.root.geometry("1400x850")
        
        self.original_img_rgb = None
        self.processed_img = None
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Sol Panel
        self.left_frame = tk.Frame(self.root, width=280, bg="#2c3e50")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.left_frame, text="İŞLEM MENÜSÜ", fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=10)
        self.create_menu_button("Resim Yükle", self.load_image, bg="#27ae60")
        
        # Sprint 1
        tk.Label(self.left_frame, text="-- Sprint 1 --", fg="#95a5a6", bg="#2c3e50").pack(pady=(5,0))
        self.create_menu_button("1. Gri Dönüşüm", self.show_gray_panel)
        self.create_menu_button("2. Binary / Eşikleme", self.show_threshold_panel)
        self.create_menu_button("6. Renk Uzayı", self.show_color_space_panel)
        
        # Sprint 2
        tk.Label(self.left_frame, text="-- Sprint 2 --", fg="#95a5a6", bg="#2c3e50").pack(pady=(5,0))
        self.create_menu_button("3. Döndürme", self.show_rotate_panel)
        self.create_menu_button("4. Kırpma", self.show_crop_panel)
        self.create_menu_button("5. Yakınlaştırma", self.show_zoom_panel)
        self.create_menu_button("8. Aritmetik İşlemler", self.show_arithmetic_panel)
        
        # Sprint 3
        tk.Label(self.left_frame, text="-- Sprint 3 --", fg="#f1c40f", bg="#2c3e50").pack(pady=(5,0))
        self.create_menu_button("7. Histogram Germe", self.show_histogram_panel)
        self.create_menu_button("9. Kontrast Artırma", self.show_contrast_panel)
        self.create_menu_button("10. Konvolüsyon (Mean)", self.show_mean_filter_panel)
        self.create_menu_button("13. Gürültü ve Filtreleme", self.show_noise_panel)
        
        # Sprint 4
        tk.Label(self.left_frame, text="-- Sprint 4 --", fg="#e74c3c", bg="#2c3e50").pack(pady=(5,0))
        self.create_menu_button("12. Kenar Bulma", self.show_edge_panel)
        self.create_menu_button("14. Unsharp Maskeleme", self.show_unsharp_panel)
        self.create_menu_button("15. Morfolojik İşlemler", self.show_morphology_panel)
        
        # 2. Sağ Panel
        self.right_frame = tk.Frame(self.root, width=280, bg="#ecf0f1")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)
        
        tk.Label(self.right_frame, text="PARAMETRELER", bg="#ecf0f1", font=("Arial", 12, "bold")).pack(pady=20)
        self.param_container = tk.Frame(self.right_frame, bg="#ecf0f1")
        self.param_container.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # 3. Orta Panel
        self.center_frame = tk.Frame(self.root, bg="#bdc3c7")
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.image_display_frame = tk.Frame(self.center_frame, bg="#bdc3c7")
        self.image_display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label_orig_title = tk.Label(self.image_display_frame, text="Orijinal Görüntü", bg="#bdc3c7", font=("Arial", 12))
        self.label_orig_title.place(relx=0.25, rely=0.05, anchor=tk.CENTER)
        self.canvas_orig = tk.Canvas(self.image_display_frame, bg="white", width=400, height=400)
        self.canvas_orig.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
        
        self.label_proc_title = tk.Label(self.image_display_frame, text="İşlenmiş Görüntü", bg="#bdc3c7", font=("Arial", 12))
        self.label_proc_title.place(relx=0.75, rely=0.05, anchor=tk.CENTER)
        self.canvas_proc = tk.Canvas(self.image_display_frame, bg="white", width=400, height=400)
        self.canvas_proc.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
        
        self.hist_frame = tk.Frame(self.center_frame, bg="#bdc3c7", height=200)

    def create_menu_button(self, text, command, bg="#34495e"):
        btn = tk.Button(self.left_frame, text=text, command=command, bg=bg, fg="white", 
                        font=("Arial", 10), relief=tk.FLAT, pady=2)
        btn.pack(fill=tk.X, padx=10, pady=1)

    def clear_parameters(self):
        for widget in self.param_container.winfo_children(): widget.destroy()
        self.hist_frame.pack_forget()
        for widget in self.hist_frame.winfo_children(): widget.destroy()

    def update_canvas(self, canvas, img_matrix):
        if img_matrix is None: return
        h, w = img_matrix.shape[:2]
        scale = min(400/w, 400/h)
        new_w, new_h = int(w * scale), int(h * scale)
        if new_w <= 0 or new_h <= 0: return
        resized = cv2.resize(img_matrix, (new_w, new_h))
        img_pil = Image.fromarray(resized).convert("L") if len(resized.shape) == 2 else Image.fromarray(resized)
        img_tk = ImageTk.PhotoImage(img_pil)
        canvas.image = img_tk 
        canvas.create_image(400//2, 400//2, anchor=tk.CENTER, image=img_tk)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
        if not file_path: return
        bgr = cv2.imread(file_path)
        if bgr is None: return
        self.original_img_rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        self.processed_img = self.original_img_rgb.copy()
        self.update_canvas(self.canvas_orig, self.original_img_rgb)
        self.update_canvas(self.canvas_proc, self.processed_img)
        self.clear_parameters()

    def check_image(self):
        if self.original_img_rgb is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return False
        return True

    def _apply_and_draw(self, func, *args):
        try:
            self.processed_img = func(*args)
            self.update_canvas(self.canvas_proc, self.processed_img)
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem hatası:\n{str(e)}")

    # SPRINT 1, 2, 3 ARAYÜZLERİ
    def show_gray_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        tk.Button(self.param_container, text="Uygula", command=lambda: self._apply_and_draw(rgb_to_gray, self.original_img_rgb), bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_threshold_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        val = tk.IntVar(value=127)
        tk.Scale(self.param_container, from_=0, to=255, orient=tk.HORIZONTAL, variable=val, bg="#ecf0f1").pack(fill=tk.X)
        tk.Button(self.param_container, text="Uygula", command=lambda: self._apply_and_draw(apply_threshold, rgb_to_gray(self.original_img_rgb), val.get()), bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_color_space_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        tk.Button(self.param_container, text="RGB -> HSV", command=lambda: self._apply_and_draw(rgb_to_hsv, self.original_img_rgb), bg="#e67e22", fg="white").pack(fill=tk.X, pady=5)
        tk.Button(self.param_container, text="RGB -> YCbCr", command=lambda: self._apply_and_draw(rgb_to_ycbcr, self.original_img_rgb), bg="#9b59b6", fg="white").pack(fill=tk.X, pady=5)

    def show_rotate_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        angle = tk.IntVar(value=0)
        tk.Scale(self.param_container, from_=-180, to=180, orient=tk.HORIZONTAL, variable=angle, bg="#ecf0f1").pack(fill=tk.X)
        tk.Button(self.param_container, text="Uygula", command=lambda: self._apply_and_draw(rotate_image, self.original_img_rgb, angle.get()), bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_crop_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        h, w = self.original_img_rgb.shape[:2]
        inputs = {}
        for label, max_val in [("Y Start", h), ("Y End", h), ("X Start", w), ("X End", w)]:
            tk.Label(self.param_container, text=label, bg="#ecf0f1").pack()
            var = tk.IntVar(value=0 if "Start" in label else max_val)
            tk.Entry(self.param_container, textvariable=var).pack()
            inputs[label] = var
        def apply():
            y1, y2, x1, x2 = inputs["Y Start"].get(), inputs["Y End"].get(), inputs["X Start"].get(), inputs["X End"].get()
            self._apply_and_draw(crop_image, self.original_img_rgb, y1, y2, x1, x2)
        tk.Button(self.param_container, text="Kırp", command=apply, bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_zoom_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        scale = tk.DoubleVar(value=1.5)
        tk.Scale(self.param_container, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, variable=scale, bg="#ecf0f1").pack(fill=tk.X)
        tk.Button(self.param_container, text="Uygula", command=lambda: self._apply_and_draw(zoom_image, self.original_img_rgb, scale.get()), bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_arithmetic_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        ratio = tk.DoubleVar(value=0.5)
        tk.Scale(self.param_container, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=ratio, bg="#ecf0f1").pack(fill=tk.X)
        def apply_add():
            path = filedialog.askopenfilename()
            if path: self._apply_and_draw(image_add, self.original_img_rgb, cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB), ratio.get())
        tk.Button(self.param_container, text="Harmanla", command=apply_add, bg="#3498db", fg="white").pack(fill=tk.X)
        div = tk.DoubleVar(value=2.0)
        tk.Scale(self.param_container, from_=1.0, to=10.0, resolution=0.5, orient=tk.HORIZONTAL, variable=div, bg="#ecf0f1").pack(fill=tk.X)
        tk.Button(self.param_container, text="Böl", command=lambda: self._apply_and_draw(image_divide, self.original_img_rgb, div.get()), bg="#e67e22", fg="white").pack(fill=tk.X)

    def show_contrast_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        alpha = tk.DoubleVar(value=1.5)
        tk.Scale(self.param_container, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, variable=alpha, bg="#ecf0f1").pack(fill=tk.X)
        beta = tk.IntVar(value=10)
        tk.Scale(self.param_container, from_=-100, to=100, orient=tk.HORIZONTAL, variable=beta, bg="#ecf0f1").pack(fill=tk.X)
        tk.Button(self.param_container, text="Uygula", command=lambda: self._apply_and_draw(enhance_contrast, rgb_to_gray(self.original_img_rgb), alpha.get(), beta.get()), bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_mean_filter_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        k_size = tk.IntVar(value=3)
        tk.Scale(self.param_container, from_=3, to=11, resolution=2, orient=tk.HORIZONTAL, variable=k_size, bg="#ecf0f1").pack(fill=tk.X)
        tk.Button(self.param_container, text="Başlat", command=lambda: [messagebox.showinfo("Bilgi","Bekleyiniz.."), self._apply_and_draw(mean_filter, rgb_to_gray(self.original_img_rgb), k_size.get())], bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_noise_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        prob = tk.DoubleVar(value=0.05)
        tk.Scale(self.param_container, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, variable=prob, bg="#ecf0f1").pack(fill=tk.X)
        self.noisy_cache = None
        def apply_noise():
            self.noisy_cache = add_salt_and_pepper_noise(rgb_to_gray(self.original_img_rgb), prob.get())
            self.update_canvas(self.canvas_proc, self.noisy_cache)
        tk.Button(self.param_container, text="Gürültü Ekle", command=apply_noise, bg="#e74c3c", fg="white").pack(fill=tk.X, pady=5)
        tk.Button(self.param_container, text="Ortalama ile Temizle", command=lambda: self._apply_and_draw(mean_filter, self.noisy_cache, 3) if self.noisy_cache is not None else messagebox.showerror("Hata","Gürültü yok"), bg="#f39c12", fg="white").pack(fill=tk.X, pady=5)
        tk.Button(self.param_container, text="Medyan ile Temizle", command=lambda: self._apply_and_draw(median_filter, self.noisy_cache, 3) if self.noisy_cache is not None else messagebox.showerror("Hata","Gürültü yok"), bg="#27ae60", fg="white").pack(fill=tk.X, pady=5)

    def show_histogram_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        def apply():
            gray = rgb_to_gray(self.original_img_rgb)
            stretched = histogram_stretching(gray)
            self.update_canvas(self.canvas_proc, stretched)
            self.hist_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
            for w in self.hist_frame.winfo_children(): w.destroy()
            fig = Figure(figsize=(8, 2.5), dpi=100)
            ax1 = fig.add_subplot(121); ax1.plot(calculate_histogram(gray), color='black'); ax1.set_title("Orijinal Histogram"); ax1.set_xlim([0, 256])
            ax2 = fig.add_subplot(122); ax2.plot(calculate_histogram(stretched), color='black'); ax2.set_title("Gerilmiş Histogram"); ax2.set_xlim([0, 256])
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.hist_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tk.Button(self.param_container, text="Uygula", command=apply, bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    # ==========================================
    # SPRINT 4 ARAYÜZLERİ
    # ==========================================
    def show_edge_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        tk.Label(self.param_container, text="Prewitt Operatörü Gx ve Gy", bg="#ecf0f1").pack(pady=10)
        def apply():
            messagebox.showinfo("Bilgi", "Kenar tespiti konvolüsyon barındırır. İşlem 5-10 saniye sürebilir.")
            gray = rgb_to_gray(self.original_img_rgb)
            self._apply_and_draw(prewitt_edge_detection, gray)
        tk.Button(self.param_container, text="Kenarları Çıkar", command=apply, bg="#3498db", fg="white").pack(fill=tk.X)

    def show_unsharp_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        tk.Label(self.param_container, text="Keskinlik Katsayısı (k)", bg="#ecf0f1").pack(pady=5)
        k_val = tk.DoubleVar(value=1.5)
        tk.Scale(self.param_container, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, variable=k_val, bg="#ecf0f1").pack(fill=tk.X)
        def apply():
            messagebox.showinfo("Bilgi", "İşlem 5-10 saniye sürebilir.")
            gray = rgb_to_gray(self.original_img_rgb)
            self._apply_and_draw(unsharp_masking, gray, k_val.get())
        tk.Button(self.param_container, text="Uygula", command=apply, bg="#3498db", fg="white").pack(fill=tk.X, pady=10)

    def show_morphology_panel(self):
        self.clear_parameters()
        if not self.check_image(): return
        
        tk.Label(self.param_container, text="Önce Binary'e Çevriliyor", bg="#ecf0f1").pack(pady=5)
        
        # Binary eşik slider'ı
        thresh = tk.IntVar(value=127)
        tk.Scale(self.param_container, from_=0, to=255, orient=tk.HORIZONTAL, variable=thresh, bg="#ecf0f1").pack(fill=tk.X)
        
        def do_morph(func):
            messagebox.showinfo("Bilgi", "İşlem sürebilir.")
            gray = rgb_to_gray(self.original_img_rgb)
            binary = apply_threshold(gray, thresh.get())
            self._apply_and_draw(func, binary, 3)
            
        tk.Button(self.param_container, text="Genişleme (Dilation)", command=lambda: do_morph(dilation), bg="#e74c3c", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(self.param_container, text="Aşınma (Erosion)", command=lambda: do_morph(erosion), bg="#e67e22", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(self.param_container, text="Açma (Opening)", command=lambda: do_morph(opening), bg="#f1c40f", fg="black").pack(fill=tk.X, pady=2)
        tk.Button(self.param_container, text="Kapama (Closing)", command=lambda: do_morph(closing), bg="#2ecc71", fg="white").pack(fill=tk.X, pady=2)
