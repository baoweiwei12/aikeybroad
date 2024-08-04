from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from typing import Tuple
# 固定的16字节密钥（128位）
key = b'imm6sco23gx97qml'

# AES 解密
def decrypt(ciphertext:str, key:bytes) -> Tuple[int, str]:
    # 使用冒号分隔 IV 和 密文
    iv_str, encrypted_text_str = ciphertext.split(':')
    # base64 解码
    iv = base64.b64decode(iv_str)
    encrypted_text = base64.b64decode(encrypted_text_str)
    # 创建AES解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并去填充
    decrypted_data = unpad(cipher.decrypt(encrypted_text), AES.block_size)
    # 提取时间戳和明文
    timestamp, plaintext = decrypted_data.split(b"||", 1)
    return int(timestamp.decode('utf-8')), plaintext.decode('utf-8')

# 使用示例
ciphertext = "nZ6WIu+Up6P5E4dwkzM4Rw==:foMh64oeHAj0K8YrgiI/lvZ7mDxku0V2UK/quMM5TYA="  
timestamp, decrypted_text = decrypt(ciphertext, key)
print("解密后的时间戳:", timestamp)
print("解密后的明文:", decrypted_text)
