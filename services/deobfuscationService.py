import base64
import os
import sys

"""
from tkinter import filedialog
from cryptography.fernet import Fernet
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
"""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def decode_base64(file_path):
    try:
        f_origin = open(file_path, 'r')
        f_decoding = open(resource_path("psParser1.txt"), 'w')
        while True:
            line = f_origin.readline()
            if not line: break
            context = base64.b64decode(line)
            f_decoding.write(context.decode("ascii", errors="strict"))
            f_decoding.write("\n")

        f_origin.close()
        f_decoding.close()
    except:
        f_decoding = open(resource_path("psParser1.txt"), 'w')
        f_decoding.write("비난독화가 올바르게 진행되지 않았습니다.\n비난독화를 다시 진행해주세요.")
        f_decoding.close()

def decode_hex(file_path):
    try:
        f_origin = open(file_path, 'r')
        f_decoding = open(resource_path("psParser1.txt"), 'w')
        while True:
            line = f_origin.readline()
            if not line: break
            context = bytearray.fromhex(line)
            context.decode()
            f_decoding.write(context.decode("ascii", errors="strict"))
            f_decoding.write("\n")

        f_origin.close()
        f_decoding.close()
    except:
        f_decoding = open(resource_path("psParser1.txt"), 'w')
        f_decoding.write("비난독화가 올바르게 진행되지 않았습니다.\n\n비난독화를 다시 진행해주세요.")
        f_decoding.close()

"""
아래의 encode, decode는 키를 필요로 하는 방식들입니다.
해당 프로젝트의 주제와 맞지 않다는 판단하에 일단은 사용하지 않았습니다.
"""
"""
def xor_encode_decode(file_path): #테스트 # ;기준으로 날라가는거 같은데 그거 나중에 확인 # 완전 정확하게 encode가 안되는거 같은데 왜 그런거지?
    d = open(file_path, 'r').read()
    data = d
    d.close()

    key = "12345"

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    f = open("test.txt", 'w')
    f.write(ret)
    f.close()

    f = open("test.txt", 'r')
    line = f.readline()
    data = line

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

def xor_encode(file_path):
    d = open(file_path, 'r').read()

    data = d
    key = '4'

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

def xor_decode(file_path):
    f = open(file_path, 'r')
    line = f.readline()
    data = line

    f = open(open_key(), 'r')
    key = f.readline()

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    f_decoding = open("psParser1.txt", 'w')
    f_decoding.write(ret)
    f.close()

def xor(file_path):
    d = open(file_path, 'r').read()

    data = d
    key = '4'

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    data = ret
    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

def symmetricKey(file_path):
    d = open(file_path, 'r').read()

    key = Fernet.generate_key()
    f = open("key.txt", 'w')
    f.write(key.decode())
    f.close()

    fernet = Fernet(key)
    encrypt_str = fernet.encrypt(d.encode())

    f = open("test.txt", 'w')
    f.write(encrypt_str.decode())
    f.close()

    decrypt_str = fernet.decrypt(encrypt_str)

def decode_symmetric(file_path):
    d = open(file_path, 'r').read()
    print(d.encode())

    f = open(open_key(), 'r')
    key = f.readline()

    fernet = Fernet(key)
    decrypt_str = fernet.decrypt(d)

    f_decoding = open("psParser1.txt", 'w')
    f_decoding.write(decrypt_str.decode())
    f.close()


def rsaEncode(file_path):
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)
    private_pem = rsa.exportKey()
    with open("private.pem", "wb") as f:
        f.write(private_pem)
        f.close()
    public_pem = rsa.publickey().exportKey()
    with open("public.pem", "wb") as f:
        f.write(public_pem)
        f.close()

    message = "Hello,This is RSA"
    rsakey = RSA.importKey(open("public.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # pkcs1_v1_5
    cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))

def rsaDecode():
    cipher_text = "V62K8w2L4xAZ0wrMlzh+cGn7AY3Anp4P01KWk75hlDx6Zqe2MbRXdpfdO4eOtDqdgiS2V8nQhNTIjnYMtN1FTisOwGictzgzfsfAcNTTuVcHoOLmfSXtokhUSO+44ydCeDMs/VCs+AcFZZAk8J+R9pXtlUx8aNnhVQIby2K8WVU="
    encrypt_text = cipher_text.encode('utf-8')
    rsakey = RSA.importKey(open("private.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # pkcs1_v1_5
    text = cipher.decrypt(base64.b64decode(encrypt_text), "    ")

def open_key():
    key_path = filedialog.askopenfilename(filetypes=[('Key File','.txt')])
    key_path = key_path.replace('\\', '/')
    if key_path == '':
        print("키 경로를 찾을 수 없습니다.")
        exit()
    else:
        print("키 업로드 완료")
        print("\n")

    return key_path
"""
