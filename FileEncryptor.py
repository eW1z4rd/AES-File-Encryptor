#!/usr/bin/python3

import os
import getopt
import sys

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

import time


class FileEncryptor(object):
    def __init__(self):
        self.key = bytes()  # 32 bytes

    def get_key(self, str_pwd):
        byte_pwd = str_pwd.encode()
        hash_pwd = SHA256.new(byte_pwd).digest()
        self.key = hash_pwd

    @staticmethod
    def encrypt(plain_text, key):
        def pad(s):
            return s + b'\0' * (AES.block_size - len(s) % AES.block_size)

        pad_text = pad(plain_text)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(pad_text)

    @staticmethod
    def decrypt(cipher_text, key):
        iv = cipher_text[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pad_text = cipher.decrypt(cipher_text[AES.block_size:])
        return pad_text.rstrip(b'\0')

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            plain_text = f.read()
        enc = self.encrypt(plain_text, self.key)
        with open(file_name + ".enc", 'wb') as f:
            f.write(enc)
        os.remove(file_name)
        fn = os.path.basename(file_name)

        print("[+] Encrypted " + fn + " --> " + fn + ".enc success.")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            cipher_text = f.read()
        dec = self.decrypt(cipher_text, self.key)
        with open(file_name[:-4], 'wb') as f:
            f.write(dec)
        os.remove(file_name)
        fn = os.path.basename(file_name)

        print("[+] Decrypted " + fn + " --> " + fn[:-4] + " success.")

    def encrypt_all_files(self):
        def walk_dir(d):
            dir_path = os.path.dirname(d)
            dirs = []
            for dirName, subdirList, fileList in os.walk(dir_path):
                for file_name in fileList:
                    if file_name != os.path.basename(__file__):  # Exclude this file
                        dirs.append(os.path.join(dirName, file_name))
            return dirs

        dir_list = walk_dir(os.path.realpath(__file__))  # Begin with the current path
        content = bytes()

        for f_dir in dir_list:
            with open(f_dir, 'rb') as f:
                s = f.read()
            content += s + self.key[:8] + f_dir.encode() + self.key[-8:]  # Add flag

            os.remove(f_dir)
            f_path = os.path.split(f_dir)[0]
            try:
                os.removedirs(f_path)  # Delete all empty directories, from the rightmost
            except OSError:
                pass

            print("[+] Encrypted " + f_dir + " success.")
            time.sleep(0.05)  # Delay print

        if content:
            enc = self.encrypt(content, self.key)
            with open('lockFile.enc', 'wb') as f:
                f.write(enc)

            print("[+] Generated the lockFile.enc file.")

    def decrypt_all_files(self):
        with open('lockFile.enc', 'rb') as f:
            dec = f.read()
            content = self.decrypt(dec, self.key)
        os.remove('lockFile.enc')

        print("[+] Decrypted the lockFile.enc success.")

        content_dir_list = content.split(self.key[-8:])[:-1]  # Deal with Flag
        for content_dir in content_dir_list:
            f_content, f_dir = content_dir.split(self.key[:8])
            f_path, f_name = os.path.split(f_dir.decode())
            if not os.path.exists(f_path):
                os.mkdir(f_path)
            rebuild_dir = os.path.join(f_path, f_name)
            with open(rebuild_dir, 'wb') as f:
                f.write(f_content)

            print("[+] Generated " + rebuild_dir + " success.")
            time.sleep(0.05)

    @staticmethod
    def usage():
        print("[*] Usage: FileEncryptor.py -p <password> [-e/-d/-E/-D] <filename>")
        print("  -h, --help                show Usage.")
        print("  -p, --pwd <password>      enter your password.")
        print("  -e, --encrypt <filename>  encrypt the file.")
        print("  -d, --decrypt <filename>  decrypt the file.")
        print("  -E                        encrypt all files in the current directory.")
        print("  -D                        decrypt all files in the current directory.")

    def handle(self):
        opts, args = getopt.getopt(sys.argv[1:], '-h-p:-e:-d:-E-D', ['help', 'pwd=', 'encrypt=', 'decrypt='])

        if not opts or '-h' in opts[0] or '--help' in opts[0]:
            self.usage()
        elif '-p' not in opts[0] and '--pwd' not in opts[0]:
            print("[-] The '-p' parameter must be specified first!")
            sys.exit(0)

        try:
            for opt_name, opt_value in opts:
                if opt_name in ('-p', '--pwd'):
                    pwd = opt_value
                    self.get_key(pwd)
                if opt_name in ('-e', '--encrypt'):
                    filename = opt_value
                    self.encrypt_file(filename)
                if opt_name in ('-d', '--decrypt'):
                    filename = opt_value
                    self.decrypt_file(filename)
                if opt_name == '-E':
                    self.encrypt_all_files()
                if opt_name == '-D':
                    self.decrypt_all_files()
        except IOError:
            print("[-] Error, No such file or directory!")


if __name__ == '__main__':
    FE = FileEncryptor()
    FE.handle()
