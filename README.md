# FileEncryptor
使用AES-CBC模式对一个文件进行加解密操作，或者对当前文件目录进行加解密操作。

## Quick start

### Installation

- `pip install pycryptodome`

### Usage

### CLI

> FileEncryptor.py -p [password] [options]

### Options

```shell
-p, --pwd
			enter your password.
-e, --encrypt
			encrypt the file
-d, --decrypt
			decrypt the file
-E
			encrypt all files in the current directory.
-D
			decrypt all files in the current directory.
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/eW1z4rd/AES-FileEncryptor/blob/master/LICENSE) file for details.
