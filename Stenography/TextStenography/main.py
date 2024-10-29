import re

class DataLengthError(Exception):
    """Исключение для ошибок длины данных."""
    pass

def embed_message(secret_message, output_file, content):
    # Преобразуем сообщение в двоичный формат
    binary_message = ''.join(format(ord(char), '08b') for char in
                             secret_message) + '00000000'  # Завершаем нулем

    print(f'binary_message = {binary_message}')
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_message)
    print(f'binary_secret = {binary_secret}')

    inserted_bits = 0

    # with open(container_file, 'r') as f:
    #     lines = f.readlines()

    splitmess = 2
    binary_pairs = [binary_secret[i:i + splitmess] for i in
                    range(0, len(binary_secret), splitmess)]
    strings = content.split('\n')

    if len(strings) < len(binary_secret):
        print('Слишком мало строк')
        raise DataLengthError(f"Количество строк должно быть не менее {len(binary_secret)}, Сейчас {len(strings)} строки")
    print(f'strings = {strings}')
    # print(f'lines = {lines}')
    print(f'binary_pairs = {binary_pairs}')
    encoded_text = '' #

    for i, string in enumerate(strings[:-1]):
        if i < len(binary_secret):
            if binary_secret[i] == '0':
                space = ' \n'
            else:
                space = '  \n'
            encoded_text += string + space
        else:
            encoded_text += string + '\n'


    encoded_text += strings[-1]

    print(f'encoded_text = {encoded_text}')

    return encoded_text, len(binary_secret)


def count_spaces_and_translate_to_binary(text, splitmess = 2):
    # matches = re.findall(r'[.!?]( +)', text)
    matches = re.findall(r'( +)[\n]', text)
    print(f'matches = {matches}')
    spaces_between_sentences = [len(match) - 1 for match in matches]
    print(f'spaces_between_sentences = {spaces_between_sentences}')
    binarystr = ''
    for spaces in spaces_between_sentences:
        binarystr+=str(spaces)
    binary_spaces = [bin(spaces)[2:].zfill(splitmess) for spaces in spaces_between_sentences]
    print(f'binary_spaces = {binary_spaces}')
    return binarystr


def text_steganography_decode(encoded_text, splitmess):
    binary_secret = count_spaces_and_translate_to_binary(encoded_text, splitmess)

    result = ""
    for i in range(0, len(binary_secret), 8):
        print(f'binary_secret[i : i+8] = {binary_secret[i : i+8]}')
        byte = binary_secret[i : i+8]
        character = chr(int(byte, 2))
        result += character

    return result


def extract_message(container_file):
    binary_message = ''

    with open(container_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Считаем количество пробелов в конце строки
        count_spaces = 0
        while line.endswith(' '):
            count_spaces += 1
            line = line[:-1]  # Убираем пробелы

        # Генерируем двоичное сообщение на основе количества пробелов
        if count_spaces == 1:
            binary_message += '0'
        elif count_spaces == 2:
            binary_message += '1'

    # Делим двоичное сообщение на байты
    message_bytes = [binary_message[i:i + 8] for i in
                     range(0, len(binary_message), 8)]
    secret_message = ''

    for byte in message_bytes:
        if byte == '00000000':
            break  # Конец сообщения
        secret_message += chr(int(byte, 2))

    return secret_message


# Пример использования
container_file = 'text.txt'
secret_message = 'Hell'
output_file = 'output.txt'
# file_path = filedialog.askopenfilename(
#     title="Select a Text File",
#     filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
# )
file_path = 'text2.txt'
if file_path:
    try:
        with open(file_path, encoding='cp866') as file:
            content = file.read()
        content = '\n'.join(line.rstrip() for line in content.splitlines())

    except Exception as e:
        print("Error", f"Failed to read the file: {str(e)}")

# Внедрение сообщения
encoded_content = content
try:
    encoded_content, input_bit = embed_message(secret_message, output_file, content)  # Передаем данные, которые недостаточно длинные
except DataLengthError as e:
    print(e)  # Сообщаем об ошибке пользователю

print(f'Encoded_content: {encoded_content}')

# Извлечение сообщения
decoded_message = text_steganography_decode(encoded_content, 2)
extracted_message = extract_message(output_file)
print(f'Decoded message: {decoded_message}')