
file_path = 'text.txt'



# Файл Texts.py содержит графический интерфейс для взаимодействия пользователя и алгоритма.
import tkinter as tk
from tkinter import filedialog, Toplevel, StringVar, LabelFrame, Entry, Button, messagebox, ttk
from ciphers import text_steganography_decode
from ciphers import text_steganography_encode


def open_text_steg(root):
    def browse_file(entry_var):
        file_path = filedialog.askopenfilename(
            title="Select a Text File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, encoding='cp866') as file:
                    content = file.read()
                    entry_var.set(content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read the file: {str(e)}")

    def run_encode():
        text_data = encode_text_file_content.get()
        secret_message = secret_message_entry.get()  #.encode('cp866')
        max_spaces = selected_spaces.get()

        if not text_data:
            messagebox.showwarning("Input Required", "Please select a text file for encoding.")
            return

        if not secret_message:
            messagebox.showwarning("Input Required", "Please enter a secret message.")
            return

        encoded_content, input_bit = text_steganography_encode(text_data, secret_message, max_spaces)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
            title="Save Encoded File"
        )
        if save_path:
            try:
                with open(save_path, 'w', encoding='cp866') as file:
                    file.write(encoded_content)
                messagebox.showinfo("Success", f"Bits: {input_bit}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {str(e)}")

    def run_decode():
        encoded_data = decode_file_content.get()
        max_spaces = selected_spaces.get()
        if not encoded_data:
            messagebox.showwarning("Input Required", "Please select a text file for decoding.")
            return

        secret_message = text_steganography_decode(encoded_data, max_spaces)
        messagebox.showinfo("Decoding Result", f"Secret Message: {secret_message}")

    window = Toplevel(root)
    window.title("Textual Steganography")
    window.geometry("400x500")
    window.grab_set()

    # ----- Выбор пробелов -----
    tk.Label(window, text="Выберите максимальное количество пробелов:").pack(pady=(10, 0))

    selected_spaces = tk.IntVar(value=2)  # Значение по умолчанию

    # Создаем рамку для радиокнопок
    button_frame = tk.Frame(window)
    button_frame.pack(pady=(5, 10))

    # Радиокнопки для выбора количества пробелов
    tk.Radiobutton(button_frame, text="2", variable=selected_spaces, value=1).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(button_frame, text="4", variable=selected_spaces, value=2).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(button_frame, text="16", variable=selected_spaces, value=4).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(button_frame, text="64", variable=selected_spaces, value=8).pack(side=tk.LEFT, padx=5)

    # Encoding Frame
    encode_frame = LabelFrame(window, text="Encode", padx=10, pady=10)
    encode_frame.pack(padx=10, pady=10, fill="both")

    encode_text_file_content = StringVar()

    browse_encode_button = Button(encode_frame, text="Select Text File",
                                  command=lambda: browse_file(encode_text_file_content))
    browse_encode_button.pack(pady=5)

    tk.Label(encode_frame, text="Secret Message:").pack()
    secret_message_entry = Entry(encode_frame, width=50)
    secret_message_entry.pack(pady=5)

    encode_button = Button(encode_frame, text="Encode and Save", command=run_encode)
    encode_button.pack(pady=5)

    # Decoding Frame
    decode_frame = LabelFrame(window, text="Decode", padx=10, pady=10)
    decode_frame.pack(padx=10, pady=10, fill="both")

    decode_file_content = StringVar()

    browse_decode_button = Button(decode_frame, text="Select Encoded File",
                                  command=lambda: browse_file(decode_file_content))
    browse_decode_button.pack(pady=5)

    decode_button = Button(decode_frame, text="Decode", command=run_decode)
    decode_button.pack(pady=5)
