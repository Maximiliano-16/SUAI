import tkinter as tk
from tkinter import filedialog, messagebox
from main import *



class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")

        # Большое окно для отображения текста
        self.text_display = tk.Text(root, wrap='word', height=40, width=100)
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Фреймы для Encode и Decode
        self.encode_frame = self.create_encode_frame()
        self.decode_frame = self.create_decode_frame()

        # Поле для вывода ошибок
        self.error_display = tk.Text(root, height=5, wrap='word', fg='red')
        self.error_display.pack(side=tk.BOTTOM, fill=tk.X)

    def create_encode_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, padx=10, pady=10)

        # Кнопка для загрузки текста
        load_btn = tk.Button(frame, text="Загрузить текст", command=self.load_text, width=20, height=2)
        load_btn.pack(pady=5)

        # Поле для ввода секретного сообщения
        self.secret_msg = tk.Entry(frame, width=40, font=('Arial', 14))
        self.secret_msg.pack(pady=5)

        # Кнопка для кодирования сообщения
        encode_btn = tk.Button(frame, text="Спрятать сообщение", command=self.encode_message)
        encode_btn.pack(pady=5)

        return frame

    def create_decode_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, padx=10, pady=10)

        # Кнопка для декодирования сообщения
        decode_btn = tk.Button(frame, text="Декодировать сообщение", command=self.decode_message, width=20, height=2)
        decode_btn.pack(pady=5)

        # Кнопка для загрузки закодированного текста
        load_encoded_btn = tk.Button(frame, text="Загрузить закодированный текст", command=self.load_encoded_text, width=25, height=3)
        load_encoded_btn.pack(pady=5)

        # Кнопка для сохранения текста
        save_btn = tk.Button(frame, text="Сохранить текст",
                             command=self.save_text, width=25, height=4)
        save_btn.pack(pady=5)

        return frame

    def load_text(self):
        file_path = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                text = '\n'.join(
                    line.rstrip() for line in text.splitlines())
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, text)

    def encode_message(self):

        secret_message = self.secret_msg.get()
        text = self.text_display.get(1.0, tk.END)
        text = '\n'.join(
            line.rstrip() for line in text.splitlines())
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        print(f'text: {text}')
        encoded_text = text
        # encoded_text, input_bits = embed_message(secret_message, output_file, text)

        try:
            encoded_text, input_bits = embed_message(secret_message,
                                                       output_file,
                                                       text)  # Передаем данные, которые недостаточно длинные
            messagebox.showinfo("Успешно", f"Вставлено бит: {input_bits}.")
            self.error_display.delete(1.0, tk.END)
        except DataLengthError as e:
            print(e)
            self.show_error(e)
            # Сообщаем об ошибке пользователю
        # text = self.text_display.get(1.0, tk.END).strip()
        # secret_msg = self.secret_msg.get().strip()
        # if not text or not secret_msg:
        #     self.show_error("Текст или секретное сообщение не может быть пустым.")
        #     return
        # Простейший алгоритм встраивания сообщения
        # if len(secret_msg) + 1 > len(text):
        #     self.show_error("Секретное сообщение слишком длинное для текста.")
        #     return

        # encoded_text = text + "\n" + secret_msg
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, encoded_text)

    def decode_message(self):
        text = self.text_display.get(1.0, tk.END)
        secret_msg = text_steganography_decode(text, 2)

        if len(text) > 1:
            # secret_msg = text[-1]
            messagebox.showinfo("Декодированное сообщение", secret_msg)
            self.error_display.delete(1.0, tk.END)
        else:
            self.show_error("Нет закодированного сообщения.")

    def load_encoded_text(self):
        file_path = filedialog.askopenfilename(title="Выберите закодированный файл", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, text)

    def show_error(self, message):
        self.error_display.delete(1.0, tk.END)
        self.error_display.insert(tk.END, message)

    def save_text(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить текстовый файл", defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")])
        if file_path:
            text = self.text_display.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)

input_file = 'text.txt'
output_file = 'output.txt'

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()