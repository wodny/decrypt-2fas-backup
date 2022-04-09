# decrypt-2fas-backup

[2FAS app][1] encrypted export decryption tool.

## Usage

Run first to get the dependency:
```sh
$ pip3 install cryptography
```

Run the tool:
```sh
$ ./decrypt-2fas-backup.py passphrase 2fas-backup-20220408234614.2fas
```

## Purpose of the script

Usage of 2FA secrets on a PC using tools like [oathtool][2],
especially in case of a smartphone failure.


[1]: https://2fas.com/
[2]: http://www.nongnu.org/oath-toolkit/
