import argparse

import collections
import requests
import sys


SEARCH_BASE_URL = 'http://www.tekstowo.pl/wyszukaj.html'
SEARCH_FMT_STR = SEARCH_BASE_URL + '?search-title={title}&search-artist={artist}'

Song = collections.namedtuple('Song', ['artist', 'title', 'url'])


def fetch_page(url):
    with requests.Session() as session:
        response = session.get(url)
        return response.content


def search_song(song):
    destination_url = SEARCH_FMT_STR.format(title=song.title, artist=song.artist)
    return fetch_page(destination_url)


def fetch_lyrics(song):
    return fetch_page(song.url)


def extract_song(item):
    artist_title = item.split('title="')[1].split('">')[0]
    artist, title = map(str.strip, artist_title.split(' - ')[:2])
    url = 'http://www.tekstowo.pl{}.html' \
        .format(item.split('a href="')[1].split('.html')[0])
    return Song(artist, title, url)


def parse_search_results(results):
    results = results.decode('utf-8')
    if 'Znalezieni artyści' in results:
        results = results.split('Znalezieni artyści:')[0]
    return [extract_song(item) for item in results.split('<div class="box-przeboje">')[1:]]


def parse_song_lyrics(html):
    return html.decode('utf-8') \
        .split('<h2>Tekst piosenki:</h2><br />')[1] \
        .split('<p>&nbsp;</p>')[0] \
        .replace('<br />', '\n') \
        .replace('\n\n', '\n') \
        .strip()


class InvalidSongFormat(Exception):
    pass


def retrieve_artist_and_title(song):
    if song.count('-') != 1:
        raise InvalidSongFormat('Passed song string must contain only one "-"')
    artist, title = map(str.strip, song.split('-'))
    if len(artist) == 0:
        raise InvalidSongFormat("Artist part cannot be empty")
    if len(title) == 0:
        raise InvalidSongFormat("Title part cannot be empty")

    return artist, title


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find lyrics for a song using tekstowo.pl')
    parser.add_argument('song', help='Song to find lyrics for in format (with quotes): '
                                     '"<ARTIST> - <TITLE>"')
    args = parser.parse_args()
    try:
        song = Song(*retrieve_artist_and_title(args.song), None)
    except InvalidSongFormat as e:
        print(e)
        sys.exit(1)

    ss = search_song(song)
    psr = parse_search_results(ss)[0]
    fl = fetch_lyrics(psr)
    psl = parse_song_lyrics(fl)
    print(psl)
