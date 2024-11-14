from PIL import Image
import random

class IntervalLengthError(Exception):
    """Исключение для ошибок длины данных."""
    pass

# Необходимо задать размер окна в в этом окне рандомно вставлять пиксели, определить можно ли вставить всё сообщение, если нет, то предложить уменьшить интервал
def select_random_pixels(num_pixels, width, height, interval):

    selected_pixels = set()
    max_num_pixels = width * height
    counter = 1
    start_idx = 0
    end_idx = 1

    if num_pixels > max_num_pixels // interval:
        print('Слишком мало строк')
        raise IntervalLengthError(f"Невозможно закодировать сообщение с такой длиной интервала")

    for i in range(0, max_num_pixels, interval):
        random.seed(i)
        # print(f'i = {i}')
        start_idx = end_idx
        end_idx = counter*interval

        selected_num = random.randint(start_idx, end_idx)
        # print(f'start_idx = {start_idx}, end_idx = {end_idx}, selected_num = {selected_num}')

        selected_pixels.add((selected_num % width-1, selected_num // width-1))
        # print(f'(selected_num % width-1, selected_num // height-1) = {(selected_num % width-1, selected_num // width-1)}')
        # print(f'selected_pixels = {selected_pixels}')
        counter += 1

        if len(selected_pixels) >= num_pixels:
            break

    print(selected_pixels)
    # print(f'max_num_pixels = ', max_num_pixels)
    # while len(selected_pixels) < num_pixels:
    #     selected_pixels.add((random.randint(0, width - 1), random.randint(0, height - 1)))
    return list(selected_pixels)

def embed_data(pixels, message, width, height, random_pixels):
    data_index = 0
    for x, y in random_pixels:
        if data_index < len(message) * 8:  # 8 бит на символ
            r, g, b = pixels[x, y]
            if message[data_index // 8] & (1 << (7 - (data_index % 8))):  # Получаем бит
                r |= 1  # Установка младшего бита
            else:
                r &= ~1  # Сброс младшего бита
            pixels[x, y] = (r, g, b)
            data_index += 1


def decode_data(image_path, num_pixels, random_pixels):
    # Открываем изображение
    image = Image.open(image_path)
    pixels = image.load()

    # Сначала подготовим массив для хранения извлеченных битов
    bits = []

    # Извлекаем биты из указанных рандомных пикселей
    for x, y in random_pixels:
        r, g, b = pixels[x, y]
        bits.append(r & 1)  # Получаем младший бит красного канала

    # Теперь нужно собрать биты в байты
    byte_array = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= (bits[i + j] << (7 - j))  # Ставим бит на нужное место
        byte_array.append(byte)

    # Конвертируем байты в строку
    message = byte_array.decode('utf-8', errors='ignore')
    return message

def save_pixels_to_file(pixels, filename):
    with open(filename, 'w') as file:

        file.write(str(pixels))  # Записываем список пикселей как строку


def load_pixels_from_file(filename):
    with open(filename, 'r') as file:
        data = file.read()  # Читаем всю строку
        pixels = eval(data)  # Преобразуем строку обратно в список
    return pixels

if __name__ == '__main__':

    # Открываем изображение
    imagee = Image.open("skyimage.bmp")
    pixels = None

    message = "Hello"
    num_pixels = len(message) * 8  # Общее количество бит

    # Получаем пиксели изображения
    pixels = imagee.load()
    # print(len(pixels))

    # Сохраняем ширину и высоту
    width, height = imagee.size

    rand_pixels = select_random_pixels(num_pixels, width, height, 1000)
    print(rand_pixels)

    embed_data(pixels, message.encode('utf-8'), width, height, rand_pixels)

    imagee.save("output.bmp")

    imagee.show()

    decoded_message = decode_data("output.bmp", num_pixels, rand_pixels)
    print("Decoded message:", decoded_message)



