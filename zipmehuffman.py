import time


class MYNODE(): # Creates root and nodes for the Huffman tree

    coder = dict() 
    
    def __init__(self, text = None, priority = -1, left = None, right = None): # Creates new node
        self.pr = priority
        self.text = text
        self.left = left
        self.right = right
        self.code = ''

    def reader(self): # Fills in the dictionary with coded symbols
        if self.text != None:
            self.coder[self.text] = self.code
            return
        if self.left != None:
            self.left.code = self.code + '1'
            self.left.reader()
        if self.right != None:
            self.right.code = self.code + '0'
            self.right.reader()


def EncoderDict(mas): # Reads the file and creates nodes
    len_mas = len(mas)
    mas2 = [MYNODE('', 2 ** 32)] * len_mas
    i, j, curr_ind = 0, 0, 0
    while i < len_mas - 1:
        minn = min(mas[i].pr + mas[i + 1].pr, mas[i].pr + mas2[j].pr, mas2[j].pr + mas2[j + 1].pr)
        if mas[i].pr + mas[i + 1].pr <= minn:
            mas2[curr_ind] = MYNODE(None, mas[i].pr + mas[i + 1].pr, mas[i], mas[i + 1])
            i += 2
        elif mas[i].pr + mas2[j].pr <= minn:
            mas2[curr_ind] = MYNODE(None, mas[i].pr + mas2[j].pr, mas[i], mas2[j])
            i += 1
            j += 1
        else:
            mas2[curr_ind] = MYNODE(None, mas2[j].pr + mas2[j + 1].pr, mas2[j], mas2[j + 1])
            j += 2
        curr_ind += 1
    while j < curr_ind:
        if i < len_mas and mas[i].pr + mas2[j].pr <= mas2[j].pr + mas2[j + 1].pr:
            mas2[curr_ind] = MYNODE(None, mas[i].pr + mas2[j].pr, mas[i], mas2[j])
            i += 1
            j += 1
        else:
            mas2[curr_ind] = MYNODE(None, mas[j].pr + mas2[j + 1].pr, mas2[j], mas2[j + 1])
            j += 2
        curr_ind += 1
    mas2[-2].reader()
    return mas2[-2].coder


def MyEncoder(filez): # Creates zipped file
    with open(filez, 'rb') as f: a = f.read()
    wordz = dict()
    for i in a:
        if i not in wordz: wordz[i] = 1
        else: wordz[i] += 1
    wordz = sorted(list(wordz.items()), key = lambda x: x[1])
    for i in range(len(wordz)): wordz[i] = MYNODE(wordz[i][0], wordz[i][1])
    encoded = EncoderDict(wordz)
    with open(filez, 'rb') as f: a = f.read()
    s = ''
    for i in a: s += encoded[i]
    i, len_s, rez = 0, len(s), bytearray()
    while i + 8 < len_s:
        rez.append(int(s[i:i + 8], 2))
        i += 8
    rez.append(int(s[i:], 2))
    f = open(filez + '.zmh', 'wb')
    flag, byte_key = 1, bytearray()
    for j in encoded.keys(): byte_key.append(j)
    f.write(byte_key)
    f.write(bytes('--', encoding = 'utf-8'))
    for j in encoded.values(): f.write(bytes('|' + str(j), encoding = 'utf-8'))
    f.write((len_s - i).to_bytes(1, byteorder = 'big'))
    f.write(bytes('____', encoding = 'utf-8'))
    f.write(rez)
    f.close()
    print('Done. Your zipped file is in the same directory called: ' + filez + '.zmh')
    return True


def MyDecoder(filez): # Creates unzipped file
    with open(filez, 'rb') as f: a = f.read()
    skipz, bytearr = a.split(bytes('____', encoding = 'utf-8'))
    new_str, decoder, len_bytearr = '', dict(), len(bytearr)
    keyz, valz = skipz.split(bytes('--', encoding = 'utf-8'))
    valz = valz.split(bytes('|', encoding = 'utf-8'))
    for i in range(1, len(valz) - 1): decoder[str(valz[i])[2:-1]] = keyz[i - 1]
    decoder[str(valz[-1])[2:-5]] = keyz[i]
    len_last_block = int(str(valz[-1])[-2:-1]) % 8
    for i in range(len_bytearr - 1): new_str += '0' * (8 - len(str(bin(bytearr[i]))[2:])) + str(bin(bytearr[i]))[2:]
    new_str += '0' * (len_last_block - len(str(bin(bytearr[-1]))[2:])) + str(bin(bytearr[-1]))[2:]
    rez, i, j, len_new_str = bytearray(), 0, 1, len(new_str)
    while j < len_new_str:
        while new_str[i:j] not in decoder: j += 1
        rez.append(decoder[new_str[i:j]])
        i, j = j, j + 1
    with open('new_' + filez[:-4], 'wb') as f: f.write(rez)
    print('Done. Your unzipped file is in the same directory called: ' + 'new_' + filez[:-4])
    return True


inp = input('Welcome!\nMenu:\nType "zip" to zip your file.\nType "unzip" to unzip your file.\nType here:')
filez = input('Enter PATH to the file.\nType here:')
try: f = open(filez, 'rb')
except Exception: print('Something is wrong with your file. Fix the error and try again.')
else:
    st = time.time()
    f.close()
    if inp == 'zip': MyEncoder(filez)
    elif inp == 'unzip' and filez[-4:] == '.zmh': MyDecoder(filez)
    else: print('Something went wrong. Try again.')
finally: print('Have a good day!')
print("--- %s seconds ---" % (time.time() - st))
