'''

This program will encrypt and decrypt a given .txt file

'''

#Define the encrypt function
def encrypt(text, shift1, shift2):
    result = ''
    for char in text:
        if char.isalpha():
            if char.islower():
                base = ord('a')
                if ord(char) >= 97 and ord(char) <= 109:
                    #need to change this to %13 so that letters stay in their half of thhe alphabet
                    result += chr((ord(char) - base + shift1 * shift2) % 26 + base)
                else: result += chr((ord(char) - base - shift1 - shift2) % 26 + base)
            elif char.isupper():
                base = ord('A')
                if ord(char) >= 65 and ord(char) <= 77:
                    #same here, change this to %13
                    result += chr((ord(char) - base - shift1) % 26 + base)
                else: result += chr((ord(char) - base + shift2 * shift2) % 26 + base)
        else:
            result += char
    return result

#Define the decrypt function
def decrypt(text_encrypt, shift1, shift2):
    result = ''
    return result

#Main program body (run 'encrypt' then write the txt file or run 'decrypt' then write the text file and verify)

text = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
shift1 = 2
shift2 = 3
print(encrypt(text,shift1,shift2))