import abcdefg


def caesar(key, letter):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    if letter == ' ' or letter == '.':
        return letter
    for i in range(26):
        if alphabet[i] == letter:
            return alphabet[(i + key) % 26]
# Key 11


def caesar_brutforce(cipher):
    text = cipher.lower()
    text = split(text)
    plain = []
    firstTime = True

    for key in range(1, 26):
        for i in range(len(text)):
            if firstTime:
                plain.append(caesar(key, text[i]))
            else:
                plain[i] = caesar(key, text[i])
        print('Key = ' + str(key))
        print(list_to_string(plain))
        firstTime = False
    return


def vigenére(key, plaintext):
    cipher = []
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    print(alphabet)
    if type(key) == str:
        key = key.lower()
        key = split(key)
    if type(key) != list:
        print('Falscher Key wurde angegeben!')
        return

    for i in range(len(plaintext) // 3):
        print(alphabet.index([key[0]]))
        print(caesar(alphabet.index(key[0]), plaintext[i]))
        cipher.append(caesar(alphabet.index(key[0]), plaintext[i]))
        if i + 1 < len(plaintext):
            print(alphabet.index([key[1]]))
            print(caesar(alphabet.index(key[1]), plaintext[i+1]))
            cipher.append(caesar(alphabet.index(key[1]), plaintext[i+1]))
        if i +2 < len(plaintext):
            print(alphabet.index(key[2]))
            print(caesar(alphabet.index(key[2]), plaintext[i+2]))
            cipher.append(caesar(alphabet.index(key[2]), plaintext[i+2]))
    return cipher



def conv(letter):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    return alphabet[letter]

def list_to_string(list):
    string = ''
    for i in range(len(list)):
        string = string + list[i]
    return string


def split(word):
    return [char for char in word]


'''alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
text = 'DBUITV   EJPTFZTEGRNKTWKGFPIFTEWGRTEHMWETUEMVWVTDF'
text = text.lower()
text = split(text)
plain = []
empty = []

FirstTime = True
for a in range(26):
    for b in range(26):
        for c in range(26):
            for i in range(len(text)):
                if FirstTime:
                    plain.append(caesar(conv(a), text[i]))
                else:
                    plain[i] = caesar(conv(a), text[i])
                if i+1 < len(text) and FirstTime:
                    plain.append(caesar(conv(b), text[i+1]))
                elif i+1 < len(text):
                    plain[i+1] = caesar(conv(b), text[i+1])
                if i + 2 < len(text) and FirstTime:
                    plain.append(caesar(conv(c), text[i+2]))
                elif i+2 < len(text):
                    print(i)
                    plain[i + 2] = caesar(conv(c), text[i + 2])
                i += 2
            FirstTime = False
            print(plain)
            print('-------------------------------------------------')
            plain = empty'''

print(vigenére('abc', 'AAA'))