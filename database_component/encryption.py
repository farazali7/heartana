from cryptography.fernet import Fernet
import numpy as np


def generate_key():
    key = Fernet.generate_key()
    with open("database_key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("database_key.key", "rb").read()


def encrypt_heart_recording(heart_recording):
    key = load_key()
    heart_recording_bytes = heart_recording.tobytes()
    fernet = Fernet(key)
    encrypted_sound = fernet.encrypt(heart_recording_bytes)

    return encrypted_sound


def decrypt_heart_recording(encrypted_heart_recording):
    key = load_key()
    fernet = Fernet(key)
    bytes_of_original_data = fernet.decrypt(encrypted_heart_recording)
    heart_sound_data = np.frombuffer(bytes_of_original_data)
    return heart_sound_data