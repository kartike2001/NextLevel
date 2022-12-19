import string
from random import random


def getOrElse(dict, key):
    if key in dict:
        return str(dict[key])
    else:
        return "0"


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def stringTomap(s):
    d = {}
    for item in s.split(b';'):
        k, v = item.split(b'=')
        d[k.strip()] = v.strip()
    return d


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def requestParser(data):
    header = data.split(b'\r\n\r\n')[0]
    lines = header.split(b'\r\n')
    method = lines[0].split(b'/')[0]
    dic = {}
    for everyHeader in lines[1:]:
        key = everyHeader.split(b':')[0].strip().lower()
        value = everyHeader.split(b':')[1].strip()
        dic[key] = value
        dic[b"method"] = method
    return dic


def generate_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))


def keyval(string):
    dictionary = {}
    for i in string.split(','):
        key, value = i.split(':')
        key = key.replace('\"', '').replace(' ', '')
        value = value.replace('\"', '').replace(' ', '')
        dictionary[key] = value
    return dictionary


def bytetobinary(byte):
    bitstring = ''
    for i in range(8):
        bitstring = str(byte % 2) + bitstring
        byte = byte >> 1
    return bitstring