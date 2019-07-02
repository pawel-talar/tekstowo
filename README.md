# tekstowo

Retrieve lyrics (without translation for now) of a given song from
[tekstowo.pl](http://www.tekstowo.pl/).

### Help

```shell
python tekstowo.py -h
usage: tekstowo.py [-h] [-t] [--lt] song

Find lyrics and translation for a song using tekstowo.pl

positional arguments:
  song        Song to find lyrics for in format (with quotes):
                     "<ARTIST> - <TITLE>"

optional arguments:
  -h, --help         show this help message and exit
  -t, --translation  Flag to clarify we want download just translation,
                     default lirycs
  --lt               Flag to clarify we want download lirycs and translation,
                     default only lirycs

```

### Example

```
$ python tekstowo.py "Nirvana - About a girl"
I need an easy friend
I do, with an ear to lend
...
```

### Credits

Most of the code has been copied from
[winamp-tekstowo](https://github.com/asdfMaciej/winamp-tekstowo)
project by [Maciej Kaszkowiak](https://github.com/asdfMaciej). If you like it,
take a look at his projects :smiley:.
