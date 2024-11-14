import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from main import *
import numpy as np

def calculate_psnr(original, modified):
    mse = np.mean((original - modified) ** 2)
    if mse == 0:
        return float('inf')  # Perfect match
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr

# def psnr_section():
#     original_path = open_file("Open Original Image")
#     if not original_path:
#         return
#     modified_path = open_file("Open Modified Image")
#     if not modified_path:
#         return
#
#     # Загрузка изображений
#     original = cv2.imread(original_path)
#     modified = cv2.imread(modified_path)
#
#     # Проверка на совпадение размеров
#     if original.shape != modified.shape:
#         messagebox.showerror("Error", "Images must have the same dimensions!")
#         return
#
#     # Вычисление PSNR
#     psnr_value = calculate_psnr(original, modified)
#     messagebox.showinfo("PSNR Result", f"PSNR: {psnr_value:.2f} dB")
#
# psnr_button = tk.Button(window, text="Calculate PSNR", command=psnr_section)
# psnr_button.pack(pady=10)




class SteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Steganography Application")

        # Frame for images
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.top_image_label = tk.Label(self.image_frame,
                                        text="Original Image")
        self.top_image_label.pack()
        self.top_image_canvas = tk.Canvas(self.image_frame, width=550,
                                          height=350, bg='grey')
        self.top_image_canvas.pack()

        self.bottom_image_label = tk.Label(self.image_frame,
                                           text="Modified Image")
        self.bottom_image_label.pack()
        self.bottom_image_canvas = tk.Canvas(self.image_frame, width=550,
                                             height=350, bg='grey')
        self.bottom_image_canvas.pack()

        # Frame for controls
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.load_button = tk.Button(self.control_frame, text="Load BMP Image",
                                     command=self.load_image)
        self.load_button.pack(pady=5)

        self.load_message_button = tk.Button(self.control_frame,
                                             text="Load Secret Message File",
                                             command=self.load_message_file)
        self.load_message_button.pack(pady=5)

        self.secret_message_label = tk.Label(self.control_frame,
                                             text="Secret Message:")
        self.secret_message_label.pack(pady=5)

        self.secret_message_entry = tk.Entry(self.control_frame, width=40)
        self.secret_message_entry.pack(pady=5)

        self.len_interval_label = tk.Label(self.control_frame,
                                             text="Len interval:")
        self.len_interval_label.pack(pady=5)

        self.len_interval_entry = tk.Entry(self.control_frame, width=40)
        self.len_interval_entry.pack(pady=5)

        self.encode_button = tk.Button(self.control_frame,
                                       text="Encode Message",
                                       command=self.encode_message)
        self.encode_button.pack(pady=5)

        self.decode_button = tk.Button(self.control_frame,
                                       text="Decode Message",
                                       command=self.decode_message)
        self.decode_button.pack(pady=5)

        self.psnr_button = tk.Button(self.control_frame,
                                       text="Calculate PSNR",
                                       command=self.psnr)
        self.psnr_button.pack(pady=5)

        self.psnr_button = tk.Button(self.control_frame,
                                     text="Load pixels",
                                     command=self.load_pixels)
        self.psnr_button.pack(pady=5)

        self.result_message_label = tk.Label(self.control_frame, text="")
        self.result_message_label.pack(pady=5)

        self.original_image = None
        self.modified_image = None
        self.random_pixels = []

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.modified_image = Image.open(file_path)
            self.original_image_for_display = self.original_image.copy()
            self.modified_image_for_display = self.modified_image.copy()
            print(f'size of original_image = {self.original_image.size}')
            print(f'size of modified_image = {self.modified_image.size}')
            print(f"original_image = {self.original_image} Original Image Loaded")
            self.display_image(self.top_image_canvas, self.original_image)

    def load_message_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                message = file.read()
                self.secret_message_entry.delete(0, tk.END)
                self.secret_message_entry.insert(0, message)

    def encode_message(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please load an image first.")
            return
        secret_message = self.secret_message_entry.get()

        num_secret_mes_pixels = len(secret_message) * 8  # Общее количество бит
        print(f'In encode size of original_image = {self.original_image.size}')
        print(f'in encode size of modified_image = {self.modified_image.size}')
        self.modified_image = self.original_image
        # Получаем пиксели изображения
        pixels_img = self.modified_image.load()
        # print(len(pixels))
        len_interval = int(self.len_interval_entry.get())

        # Сохраняем ширину и высоту
        width_img, height_img = self.modified_image.size

        try:
            self.random_pixels = select_random_pixels(num_secret_mes_pixels,
                                                 width_img,
                                                 height_img,
                                                 len_interval)
            print(f'random pixels = {self.random_pixels}')
            save_pixels_to_file(self.random_pixels, 'pixels.txt')
        except IntervalLengthError as e:
            print(e)
            self.result_message_label.config(
                text="Ошибка в кодировании!")
            messagebox.showinfo("Ошибка", f"{e}.")



        embed_data(pixels_img, secret_message.encode('utf-8'),
                   width_img, height_img, self.random_pixels)


        self.modified_image.save("output.bmp")
        file_path = "output.bmp"
        if file_path:
            self.modified_image = Image.open(file_path)
            image_for_display = self.modified_image.copy()
            # print(f"original_image = {self.original_image} Original Image Loaded")
            image_for_display.thumbnail((550, 350))
            self.photo2 = ImageTk.PhotoImage(image_for_display)
            self.bottom_image_canvas.create_image(275, 175, image=self.photo2)
            # self.display_image(self.bottom_image_canvas, self.original_image)

        # self.display_image(self.bottom_image_canvas, self.modified_image)
        # self.display_image(self.top_image_canvas, self.original_image)
        # image.thumbnail((550, 350))
        # self.photo = ImageTk.PhotoImage(image)
        # canvas.create_image(275, 175, image=self.photo)
        self.result_message_label.config(text="Message encoded successfully!")
        messagebox.showinfo("Успешно", f"Вставлено бит: {len(self.random_pixels)}.")

        # Here you would implement the encoding functionality
        # For demonstration, simply show a success message

        # self.modified_image = self.original_image  # Placeholder for the actual modified image



    def decode_message(self):
        # if self.modified_image is None:
        #     messagebox.showerror("Error", "Please encode an image first.")
        #     return

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.bmp")])

        # Here you would implement the decoding functionality
        # For demonstration, simply show a success message
        decoded_message = decode_data(file_path, 10, self.random_pixels)
        print("Decoded message:", decoded_message)
        self.result_message_label.config(text="Message decoded successfully!")
        messagebox.showinfo("Декодированное сообщение", decoded_message)

    def display_image(self, canvas, image):
        image_for_display = image.copy()
        # Resize image to fit canvas
        image_for_display.thumbnail((550, 350))
        self.photo = ImageTk.PhotoImage(image_for_display)
        canvas.create_image(275, 175, image=self.photo)

    def psnr(self):
        orig_image = None
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.bmp")])
        if file_path:
            orig_image = Image.open(file_path)

        modif_img = Image.open('output.bmp')

        # Преобразование в массивы NumPy
        original_array = np.array(orig_image)
        modified_array = np.array(modif_img)


        # Вычисление PSNR
        psnr_value = calculate_psnr(original_array, modified_array)
        messagebox.showinfo("PSNR:", psnr_value)
        print(f'PSNR: {psnr_value} dB')

    def load_pixels(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.txt")])

        self.random_pixels = load_pixels_from_file(file_path)
        messagebox.showinfo("Успех", 'Пиксели были загружены')




if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()