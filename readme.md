# PushBullet Sender

Push something to your phone from the command line with pushbullet

# Usage

```bash
usage: pushbullet [-h] [-d DESCRIPTION] [-t TYPE] (-l LINK | -u URL | -p PATH | -n NOTE | --TESTS)

Send a note, a link or a file to your phone

optional arguments:
  -h, --help            show this help message and exit
  -d DESCRIPTION, --description DESCRIPTION
                        -d My message Description of what you send
  -t TYPE, --type TYPE  -t image/jpeg - The filetype of uploaded_file
  -l LINK, --link LINK  -l https://qkzk.xyz. - The link you want to send
  -u URL, --url URL     -u https://i.imgur.com/IAYZ20i.jpg - The url of the file you want to send
  -p PATH, --path PATH  -p /home/bob/hello.txt - The path of the file to send
  -n NOTE, --note NOTE  -n blablabla... - The body of your note
  --TESTS               Tests the functions
```

```bash
# help message
$ python pushb.py -h 
# push a note
$ python pushb.py -d title -n body
# push a link
$ python pushb.py -d title -l https://qkzk.xyz
# push an uploaded file
$ python pushb.py -d title -u https://i.imgur.com/IAYZ20i.jpg -t image/jpeg
# push a file
$ python pushb.py -d title -p /home/bob/hello.txt
# run all the tests and exit. WARNING : will spam you !
$ python pushb.py --TESTS
```


# Installation

You need `pushbullet` : "A simple python client for pushbullet.com"

```bash
$ pip install pushbullet.py
```

# Tokens

1. Create an API key from [pushbullet](https://www.pushbullet.com/#settings/account)
2. click "Access Tokens"
3. create the file "tokens.py" right next to the script and paste it there

    file content :

    ```python
    APIKEY = "your_secret_api_key"
    PHONENAME = "the nickname of your phone"
    ```

