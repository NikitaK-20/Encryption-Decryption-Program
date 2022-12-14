import os
import random
import sys

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(key, filename):
    chunk_size = 64 * 1024
    out_File = os.path.join(os.path.dirname(filename), "(encrypted)" + os.path.basename(filename))
    file_size = str(os.path.getsize(filename)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, "rb") as infile:
        with open(out_File, "wb") as outfile:
            outfile.write(file_size)
            outfile.write(IV)
            while True:
                chunk = infile.read(chunk_size)

                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    out_File = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
    chunk_size = 64 * 1024
    with open(filename, "rb") as infile:
        file_size = infile.read(16)
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(out_File, "wb") as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(int(file_size))


def all_files():
    all_Files = []
    for root, subfiles, files in os.walk(os.getcwd()):
        for names in files:
            all_Files.append(os.path.join(root, names))

    return all_Files


choice = input("Do you want to (E)ncrypt or (D)ecrypt? ")
password = input("Enter the password: ")

encFiles = all_files()

if choice == "E":
    for Tfiles in encFiles:
        if os.path.basename(Tfiles).startswith("(encrypted)"):
            print("%s is already encrypted", str(Tfiles))
            pass

        elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
            pass
        else:
            encrypt(SHA256.new(password).digest(), str(Tfiles))
            print("Done encrypting %s", str(Tfiles))
            os.remove(Tfiles)

elif choice == "D":
    filename = input("Enter the filename to decrypt: ")
    if not os.path.exists(filename):
        print("The file does not exist")
        sys.exit(0)
    elif not filename.startswith("(encrypted)"):
        print("%s is already not encrypted", filename)
        sys.exit()
    else:
        decrypt(SHA256.new(password).digest(), filename)
        print("Done decrypting %s", filename)
        os.remove(filename)

else:
    print("Please choose a valid command.")
    sys.exit()
