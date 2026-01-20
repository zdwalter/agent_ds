import os
from pathlib import Path
from typing import Optional

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("crypto", log_level="ERROR")


def _read_file_or_string(input_str: str) -> bytes:
    """If input_str is a valid file path, read its contents; otherwise treat as string."""
    path = Path(input_str)
    if path.exists():
        return path.read_bytes()
    # If it's hex-encoded?
    if len(input_str) % 2 == 0 and all(
        c in "0123456789abcdefABCDEF" for c in input_str
    ):
        # Possibly hex, but we'll treat as plain string for simplicity
        pass
    return input_str.encode("utf-8")


def _write_file(output_file: Optional[str], data: bytes) -> Optional[str]:
    if output_file:
        Path(output_file).write_bytes(data)
        return f" Written to {output_file}."
    return None


@mcp.tool()
def generate_symmetric_key(
    key_size: int = 256, output_file: Optional[str] = None
) -> str:
    """
    Generate a random symmetric key for AES encryption.
    """
    try:
        if key_size not in (128, 192, 256):
            return "Error: key_size must be 128, 192, or 256."
        key = os.urandom(key_size // 8)
        if output_file:
            Path(output_file).write_bytes(key)
            return f"Generated {key_size}-bit key and saved to {output_file}."
        else:
            return f"Generated {key_size}-bit key (hex): {key.hex()}"
    except Exception as e:
        return f"Error generating symmetric key: {str(e)}"


@mcp.tool()
def encrypt_symmetric(
    plaintext: str,
    key: str,
    output_file: Optional[str] = None,
) -> str:
    """
    Encrypt data with AES (CBC mode) using a symmetric key.
    """
    try:
        # Load key (either hex string or file)
        key_path = Path(key)
        if key_path.exists():
            key_bytes = key_path.read_bytes()
        else:
            # Assume hex
            key_bytes = bytes.fromhex(key)
        # Generate a random IV
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
        encryptor = cipher.encryptor()
        # Pad plaintext to multiple of block size
        plain_bytes = plaintext.encode("utf-8")
        pad_len = 16 - (len(plain_bytes) % 16)
        plain_bytes += bytes([pad_len] * pad_len)
        ciphertext = encryptor.update(plain_bytes) + encryptor.finalize()
        # Combine IV + ciphertext
        result = iv + ciphertext
        saved = _write_file(output_file, result)
        saved_msg = saved if saved else ""
        return f"Encryption successful. Ciphertext (hex): {result.hex()}{saved_msg}"
    except Exception as e:
        return f"Error encrypting: {str(e)}"


@mcp.tool()
def decrypt_symmetric(ciphertext: str, key: str) -> str:
    """
    Decrypt data encrypted with AES.
    """
    try:
        # Load key
        key_path = Path(key)
        if key_path.exists():
            key_bytes = key_path.read_bytes()
        else:
            key_bytes = bytes.fromhex(key)
        # Load ciphertext (either file or hex)
        ct_path = Path(ciphertext)
        if ct_path.exists():
            data = ct_path.read_bytes()
        else:
            data = bytes.fromhex(ciphertext)
        iv = data[:16]
        ciphertext_bytes = data[16:]
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ciphertext_bytes) + decryptor.finalize()
        # Remove padding
        pad_len = padded_plain[-1]
        if pad_len > 16 or pad_len < 1:
            raise ValueError("Invalid padding")
        plain_bytes = padded_plain[:-pad_len]
        return f"Decryption successful. Plaintext: {plain_bytes.decode('utf-8')}"
    except Exception as e:
        return f"Error decrypting: {str(e)}"


@mcp.tool()
def generate_key_pair(
    key_size: int = 2048,
    output_public: Optional[str] = None,
    output_private: Optional[str] = None,
) -> str:
    """
    Generate an RSA public/private key pair.
    """
    try:
        if key_size not in (2048, 3072, 4096):
            return "Error: key_size must be 2048, 3072, or 4096."
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        saved = ""
        if output_private:
            Path(output_private).write_bytes(private_pem)
            saved += f" Private key saved to {output_private}."
        if output_public:
            Path(output_public).write_bytes(public_pem)
            saved += f" Public key saved to {output_public}."
        return f"Generated {key_size}-bit RSA key pair.{saved}"
    except Exception as e:
        return f"Error generating key pair: {str(e)}"


@mcp.tool()
def encrypt_asymmetric(
    plaintext: str,
    public_key: str,
    output_file: Optional[str] = None,
) -> str:
    """
    Encrypt data with RSA public key.
    """
    try:
        # Load public key
        pub_path = Path(public_key)
        if pub_path.exists():
            pub_pem = pub_path.read_bytes()
        else:
            pub_pem = public_key.encode("utf-8")
        pub_key = serialization.load_pem_public_key(pub_pem)
        # RSA encryption
        ciphertext = pub_key.encrypt(
            plaintext.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        saved = _write_file(output_file, ciphertext)
        saved_msg = saved if saved else ""
        return f"Encryption successful. Ciphertext (hex): {ciphertext.hex()}{saved_msg}"
    except Exception as e:
        return f"Error encrypting: {str(e)}"


@mcp.tool()
def decrypt_asymmetric(ciphertext: str, private_key: str) -> str:
    """
    Decrypt data with RSA private key.
    """
    try:
        # Load private key
        priv_path = Path(private_key)
        if priv_path.exists():
            priv_pem = priv_path.read_bytes()
        else:
            priv_pem = private_key.encode("utf-8")
        priv_key = serialization.load_pem_private_key(priv_pem, password=None)
        # Load ciphertext
        ct_path = Path(ciphertext)
        if ct_path.exists():
            ct_bytes = ct_path.read_bytes()
        else:
            ct_bytes = bytes.fromhex(ciphertext)
        plaintext = priv_key.decrypt(
            ct_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return f"Decryption successful. Plaintext: {plaintext.decode('utf-8')}"
    except Exception as e:
        return f"Error decrypting: {str(e)}"


@mcp.tool()
def sign_data(
    message: str,
    private_key: str,
    output_file: Optional[str] = None,
) -> str:
    """
    Sign a message with a private key (RSA).
    """
    try:
        # Load private key
        priv_path = Path(private_key)
        if priv_path.exists():
            priv_pem = priv_path.read_bytes()
        else:
            priv_pem = private_key.encode("utf-8")
        priv_key = serialization.load_pem_private_key(priv_pem, password=None)
        # Sign
        signature = priv_key.sign(
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        saved = _write_file(output_file, signature)
        saved_msg = saved if saved else ""
        return f"Signature created (hex): {signature.hex()}{saved_msg}"
    except Exception as e:
        return f"Error signing: {str(e)}"


@mcp.tool()
def verify_signature(message: str, signature: str, public_key: str) -> str:
    """
    Verify a signature with a public key.
    """
    try:
        # Load public key
        pub_path = Path(public_key)
        if pub_path.exists():
            pub_pem = pub_path.read_bytes()
        else:
            pub_pem = public_key.encode("utf-8")
        pub_key = serialization.load_pem_public_key(pub_pem)
        # Load signature
        sig_path = Path(signature)
        if sig_path.exists():
            sig_bytes = sig_path.read_bytes()
        else:
            sig_bytes = bytes.fromhex(signature)
        pub_key.verify(
            sig_bytes,
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return "Signature is valid."
    except InvalidSignature:
        return "Signature is invalid."
    except Exception as e:
        return f"Error verifying signature: {str(e)}"


@mcp.tool()
def hash_data(data: str, output_file: Optional[str] = None) -> str:
    """
    Compute a cryptographic hash (SHA‑256) of data.
    """
    try:
        data_bytes = _read_file_or_string(data)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data_bytes)
        hash_result = digest.finalize()
        saved = _write_file(output_file, hash_result)
        saved_msg = saved if saved else ""
        return f"SHA‑256 hash (hex): {hash_result.hex()}{saved_msg}"
    except Exception as e:
        return f"Error hashing data: {str(e)}"


if __name__ == "__main__":
    mcp.run()
