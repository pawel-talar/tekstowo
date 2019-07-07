# tekstowo

Retrieve lyrics (without translation for now) of a given song from
[tekstowo.pl](http://www.tekstowo.pl/).

### Help

```shell
python tekstowo.py -h
usage: tekstowo.py [-h] [-t] [-l] song

Find lyrics and translation for a song using tekstowo.pl

positional arguments:
  song      Song to find lyrics for in format (with quotes):
            "<ARTIST> - <TITLE>"

optional arguments:
  -h, --help         show this help message and exit
  -t, --translation  Download translation
  -l, --lyrics       Download lyrics

```

### Examples

```
$ python tekstowo.py "Nirvana - About a girl"
I need an easy friend
I do, with an ear to lend
...
```

```
$ python tekstowo.py "Rammstein - Rammlied" -t
Kto czeka z rozwagą,
ten zostanie nagrodzony w odpowiednim czasie,
Teraz oczekiwanie ma koniec,
nadstawcie uszu, posłuchajcie legendy.
...
```

### Credits

Most of the code has been copied from
[winamp-tekstowo](https://github.com/asdfMaciej/winamp-tekstowo)
project by [Maciej Kaszkowiak](https://github.com/asdfMaciej). If you like it,
take a look at his projects :smiley:.
