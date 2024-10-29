import re

def count_spaces_and_translate_to_binary(text, splitmess = 2):
    matches = re.findall(r'[.!?]( +)', text)

    spaces_between_sentences = [len(match) - 1 for match in matches]

    binary_spaces = [bin(spaces)[2:].zfill(splitmess) for spaces in spaces_between_sentences]

    return ''.join(binary_spaces)


def text_steganography_encode(text, secret, splitmess = 2):
    # Переводим секретное сообщение в двоичную строку
    binary_secret = ''.join(format(ord(char), '08b') for char in secret)
    # Разбиение на пары
    binary_pairs = [binary_secret[i:i + splitmess] for i in range(0, len(binary_secret), splitmess)]
    sentences = text.split('.')
    encoded_text = ''

    for i, sentence in enumerate(sentences[:-1]):
        if i < len(binary_pairs):
            space = '.'
            for j in range(len(binary_pairs[0])):
                if binary_pairs[i][j] == '1': space += ' ' * 2 ** ((splitmess - j) - 1)

            encoded_text += sentence + space
        else:
            encoded_text += sentence + '.'

    encoded_text += sentences[-1]
    return encoded_text, len(binary_secret)


def text_steganography_decode(encoded_text, splitmess):
    binary_secret = count_spaces_and_translate_to_binary(encoded_text, splitmess)

    result = ""
    for i in range(0, len(binary_secret), 8):
        byte = binary_secret[i:i + 8]
        character = chr(int(byte, 2))
        result += character

    return result