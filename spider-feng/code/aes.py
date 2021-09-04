import base64
import math
import time
from Crypto.Cipher import AES


class AESCipherCBC:
    """
    AES 加密方式，CBC模式
    pip3 install pycryptodome
    """

    def __init__(self, key, iv):
        # 可以自定义key和iv
        self.__key = key
        self.__iv = iv

    @staticmethod
    def pad(padding_data):
        length = 16 - (len(padding_data) % 16)
        return padding_data.encode() + (chr(length) * length).encode()

    def encrypt(self, un_encrypt_data):
        cipher = AES.new(self.__key, AES.MODE_CBC, self.__iv)
        encrypt_data = base64.b64encode(cipher.encrypt(self.pad(un_encrypt_data)))
        return encrypt_data


if __name__ == '__main__':
    # key AES 秘钥
    # iv  AES-128-CBC偏移量
    e = AESCipherCBC(b'2b7e151628aed2a6', b'2b7e151628aed2a6')
    url2 = "/v1/content/list"
    data = "url=" + url2 + "$time=" + str(int(math.floor(time.time() * 1000))) + "000000"
    enc_str = e.encrypt(data)
    print('enc_str: ' + enc_str.decode())
