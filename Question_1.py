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

#Main program body (run 'encrypt' then write the txt file or run 'decrypt' then write the text file and verify)

text = ('''The quick brown fox jumps over the lazy dog beneath the shady willows. The dog, startled from his peaceful afternoon nap, quickly rises and chases after the mischievous fox. 

<<<Through vibrant meadows and past buzzing beehives they race, disturbing a flock of quails that scatter into the crisp autumn sky.>>> The fox, quite pleased with his clever prank, dashes into his cozy underground den while the dog, now exhausted from the zealous pursuit, returns to his favorite spot under the whispering branches to resume his quiet slumber.''')
shift_1 = int(input('Choose a number from 1 to 12 > '))
shift_2 = int(input('Choose another number from 1 to 12 > '))
text_encrypt = (encrypt(text,shift_1,shift_2))
print(encrypt(text,shift_1,shift_2))
print(decrypt(text_encrypt,shift_1,shift_2))