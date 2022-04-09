#!/usr/bin/env python3

# 2FAS app[1] encrypted export decryption tool
#
# Script by Marcin Szewczyk <mszewczyk@wodny.org>, 2022
# Completely not associated with the 2FAS company
#
# Purpose of the script:
# Usage of 2FA secrets on a PC using tools like oathtool[2],
# especially in case of a smartphone failure.
#
# [1]: https://2fas.com/
# [2]: http://www.nongnu.org/oath-toolkit/

# Run first to get the dependency:
# $ pip3 install cryptography

import argparse
import json
import base64
import pprint

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

__version__ = "0.1"

def main():
    p = argparse.ArgumentParser(
        description="2FAS app encrypted export decryption tool",
        fromfile_prefix_chars="@",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("passphrase", help="passphrase used during export from the app (use @FILENAME to read from file)")
    p.add_argument("backup", help="backup file")
    options = p.parse_args()

    with open(options.backup) as f:
        data = json.load(f)
    services_enc = data["servicesEncrypted"]
    credentials_enc, pbkdf2_salt, nonce = map(base64.b64decode, services_enc.split(":"))
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=pbkdf2_salt, iterations=10000)
    key = kdf.derive(options.passphrase.encode("utf8"))
    aesgcm = AESGCM(key)
    credentials_dec = aesgcm.decrypt(nonce, credentials_enc, None)
    credentials_dec = json.loads(credentials_dec)
    pprint.pprint(credentials_dec)

if __name__ == "__main__":
    main()
