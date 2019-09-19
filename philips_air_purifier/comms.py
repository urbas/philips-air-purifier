import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import json
import random
import requests

DH_PUBLIC_BASE = int(
    "A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B88"
    "6A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D0"
    "8BC8858F4DCEF97C2A24855E6EEB22B3B2E5",
    16,
)
DH_PUBLIC_MODULUS = int(
    "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA90611"
    "2324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C"
    "1A65E68CFDA76D4DA708DF1FB2BC2E4A4371",
    16,
)


def get_api_url(host, resource):
    return f"http://{host}/di/v1/products/{resource}"


def create_dh_keypair():
    private_key = random.getrandbits(256)
    public_key = pow(DH_PUBLIC_BASE, private_key, DH_PUBLIC_MODULUS)
    return private_key, public_key


def get_shared_secret_key(other_public_key, my_private_key):
    shared_secret_key = pow(other_public_key, my_private_key, DH_PUBLIC_MODULUS)
    return shared_secret_key.to_bytes(128, byteorder="big")[:16]


def get_key(host):
    def philips_key_exchanger(client_public_key):
        url = get_api_url(host, "0/security")
        data = json.dumps({"diffie": format(client_public_key, "x")})
        security_info = requests.put(url=url, data=data.encode("ascii")).json()
        encrypted_session_key = bytes.fromhex(security_info["key"])
        philips_public_key = int(security_info["hellman"], 16)
        return encrypted_session_key, philips_public_key

    return exchange_keys(philips_key_exchanger)


def exchange_keys(server_callback):
    private_key, public_key = create_dh_keypair()
    encrypted_session_key, server_public_key = server_callback(public_key)
    shared_secret_key = get_shared_secret_key(server_public_key, private_key)
    session_key = aes_decrypt(encrypted_session_key, shared_secret_key)
    return session_key[:16]


def dh_decrypt(data, key):
    decrypted_data = aes_decrypt(base64.b64decode(data), key)
    return unpad(decrypted_data, 16, style="pkcs7")[2:].decode("ascii")


def dh_encrypt(str_data, key):
    # NB: adding two bytes in front of the string data because the air purifier
    # seems to do that too
    padded_data = pad(("  " + str_data).encode("ascii"), 16, style="pkcs7")
    return base64.b64encode(aes_encrypt(padded_data, key))


def aes_decrypt(data, key):
    return AES.new(key, AES.MODE_CBC, bytes(16)).decrypt(data)


def aes_encrypt(data, key):
    return AES.new(key, AES.MODE_CBC, bytes(16)).encrypt(data)
