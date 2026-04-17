'''

This program will encrypt and decrypt a given .txt file

'''

#Define the encrypt function
def encrypt(text, shift_1, shift_2):
    result = ''
    for char in text:
        if char.isalpha():
            if char.islower():
                base_a_lower = ord('a')
                base_n_lower = ord('n')
                if ord(char) >= 97 and ord(char) <= 109:
                    result += chr((ord(char) - base_a_lower + shift_1 * shift_2) % 13 + base_a_lower)
                else: result += chr((ord(char) - base_n_lower - shift_1 - shift_2) % 13 + base_n_lower)
            elif char.isupper():
                base_a_upper = ord('A')
                base_n_upper = ord('N')
                if ord(char) >= 65 and ord(char) <= 77:
                    result += chr((ord(char) - base_a_upper - shift_1) % 13 + base_a_upper)
                else: result += chr((ord(char) - base_n_upper + shift_2 ** 2) % 13 + base_n_upper)
        else:
            result += char
    return result

#Define the decrypt function
def decrypt(text_encrypt, shift_1, shift_2):
    result_decrypt = ''
    for char in text_encrypt:
        if char.isalpha():
            if char.islower():
                base_a_lower = ord('a')
                base_n_lower = ord('n')
                if ord(char) >= 97 and ord(char) <= 109:
                    result_decrypt += chr((ord(char) - base_a_lower - shift_1 * shift_2) % 13 + base_a_lower)
                else: result_decrypt += chr((ord(char) - base_n_lower + shift_1 + shift_2) % 13 + base_n_lower)
            elif char.isupper():
                base_a_upper = ord('A')
                base_n_upper = ord('N')
                if ord(char) >= 65 and ord(char) <= 77:
                    result_decrypt += chr((ord(char) - base_a_upper + shift_1) % 13 + base_a_upper)
                else: result_decrypt += chr((ord(char) - base_n_upper - shift_2 ** 2) % 13 + base_n_upper)
        else:
            result_decrypt += char
    return result_decrypt

#Define the read function

def read_file(file_name: str) -> str:
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

#Define the write function

def write_file(file_name: str, content: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as file:
        return file.write(content)

#Main program body (run 'encrypt' then write the txt file or run 'decrypt' then write the text file and verify)

text = read_file('raw_text.txt')
shift_1 = int(input('Choose a number from 1 to 12 > '))
shift_2 = int(input('Choose another number from 1 to 12 > '))
# Check that the number is between 1 and 12 and run the encrypt function
if 0 < shift_1 < 13 and 0 < shift_2 < 13:
    text_encrypt = (encrypt(text,shift_1,shift_2))
    write_file('encrypted_text.txt',text_encrypt)
    text_decrypt = decrypt(read_file('encrypted_text.txt'),shift_1,shift_2)
    write_file('decrypted_text.txt',text_decrypt)
else: print('Error')

if read_file('decrypted_text.txt') == read_file('raw_text.txt'):
    print('Your decryption was successful!')
else: print('Your decryption was unsuccessful :/')
