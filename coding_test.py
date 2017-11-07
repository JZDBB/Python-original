# from Crypto.Cipher import AES
#
# import sys
# from Crypto.Cipher import AES
# from binascii import b2a_hex, a2b_hex
#
#
# class prpcrypt():
#     def __init__(self, key):
#         self.key = key
#         self.mode = AES.MODE_CBC
#
#     # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
#     def encrypt(self, text):
#         cryptor = AES.new(self.key, self.mode, self.key)
#         # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
#         length = 16
#         count = len(text)
#         add = length - (count % length)
#         text = text + ('\0' * add)
#         self.ciphertext = cryptor.encrypt(text)
#         # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
#         # 所以这里统一把加密后的字符串转化为16进制字符串
#         return b2a_hex(self.ciphertext)
#
#     # 解密后，去掉补足的空格用strip() 去掉
#     def decrypt(self, text):
#         cryptor = AES.new(self.key, self.mode, self.key)
#         plain_text = cryptor.decrypt(a2b_hex(text))
#         return plain_text.rstrip('\0')
#
#
# pc = prpcrypt('key123')
# data = open('./coding.txt', 'w')
# message = "123456"
# ciphertext = pc.encrypt(message)
# print(ciphertext)
# data.write(ciphertext)
# data.close()
# message1 = pc.decrypt(ciphertext)



from Crypto.Cipher import AES
from Crypto import Random
import binascii

def AES_File(fs):
    key = b'1234567890!@#$%^' #16-bytes password
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print('if fs is a multiple of 16...')
    #if fs is a multiple of 16
    x = len(fs) % 16
    print('fs的长度是： ', len(fs))
    print('The num to padded is : ', x)
    if x != 0:
        fs_pad = fs + '0'*(16 - x) #It shoud be 16-x not
        print('fs_pad is : ', fs_pad)
        print(len(fs_pad))
        print(len(fs_pad)%16)
    msg = iv + cipher.encrypt(fs_pad)
    print('File after AES is like...', binascii.b2a_hex(msg[:10]))
    return msg

#Create a Test Src File and Get FileSteam
fs = open('test', 'w+')
fs.write('啊，我爱你，我的祖国！')
fs.write('凌晨三时开始进攻！')
fs.seek(0,0)
fs_msg = fs.read()
print(fs_msg)
fs.close()

#Crypt Src FileStream
fc = open('fc', 'wb')
fc_msg = AES_File(fs_msg)
fc.writelines(fc_msg)
fc.close()