import base64
import os
import io
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class dbinterface():
    def __init__(self, fullpath, password, salt=None, salt_file=None):
        self.fullpath = fullpath
        self.path, self.name = os.path.split(fullpath)
        self.salt = False
        if salt and not salt_file:
            self.set_salt(salt=salt)
        elif salt_file and not salt:
            self.set_salt(salt_file=salt_file)
        self.password = bytes(password, 'utf-8')
    # GENERATE A NEW SALT AND SAVE IT TO FILE IF REQUESTED

    def generate_salt(self, salt_file=None):
        try:
            self.salt = os.urandom(16)
            if salt_file:
                with open(salt_file, "wb") as file:
                    file.write(self.salt)
        except Exception as error:
            return error
        return True
    # GET SALT FROM USER OR FROM FILE

    def set_salt(self, salt=None, salt_file=None):
        try:
            if salt and not salt_file:
                self.salt = salt
                return True
            if salt_file and not salt:
                with open(salt_file, "rb") as file:
                    self.salt = file.read()
                return True
        except Exception as error:
            return error
        return False
    # READ DB AND RETURN IT

    def read(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        f = Fernet(key)
        with open(self.fullpath, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        try:
            decrypted_data = io.StringIO(
                f.decrypt(encrypted_data).decode("utf-8"))
        except Exception as error:
            return error
        return decrypted_data
    # WRITE DB

    def write(self, data):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        f = Fernet(key)
        try:
            encrypted_data = f.encrypt(data.encode())
            # write the encrypted file
            with open(self.fullpath, "wb") as file:
                file.write(encrypted_data)
        except Exception as error:
            return error
        return True
    # READ FILE, APPEND STRING AND THEN REWRITE FILE WITH ENCRYPTION

    def append(self, data):
        filedata = self.read().read()
        filedata += data
        return self.write(filedata)
