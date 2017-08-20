# Collection of frequent use UNIX commands

## SCP (Secure Copy)
```sh
scp source_file_name username@destination_host:destination_folder
# example
scp test.zip pi@192.168.43.1:Downloads/.
```

## Unzipping

### zip

```sh
unzip test.zip
```

### gzip

```sh
gzip -d test.gz
gzip -d test.gzip
```

### tar.gz

```sh
tar -xvzf test.tar.gz
```