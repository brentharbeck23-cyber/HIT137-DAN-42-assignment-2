'''

This program will encrypt and decrypt a given .txt file

'''

def encrypt(text, shift1, shift2):
    result = ''
    for char in text:
        if char.isalpha():
            if char.islower():
                base = ord('a')
                if ord(char) >= 97 and ord(char) <= 109:
                    result += chr((ord(char) - base + shift1 * shift2) % 26 + base)
                else: result += chr((ord(char) - base - shift1 - shift2) % 26 + base)
            elif char.isupper():
                base = ord('A')
                if ord(char) >= 65 and ord(char) <= 77:
                    result += chr((ord(char) - base - shift1) % 26 + base)
                else: result += chr((ord(char) - base + shift2 * shift2) % 26 + base)
        else:
            result += char
    return result

text = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
shift1 = 2
shift2 = 3
print(encrypt(text,shift1,shift2))