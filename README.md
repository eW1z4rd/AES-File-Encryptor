# FileEncryptor
使用AES-CBC模式对一个文件或者对当前文件目录进行加解密操作。

## Quick start

### Installation

- `pip install pycryptodome`

### Usage

#### CLI

> FileEncryptor.py -p <password> [-e/-d/-E/-D] <filename>

#### Options

```
-p, --pwd: enter your password.
-e, --encrypt <filename>: encrypt the file
-d, --decrypt <filename>: decrypt the file
-E: encrypt all files in the current directory.
-D: decrypt all files in the current directory.
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/eW1z4rd/AES-FileEncryptor/blob/master/LICENSE) file for details.
