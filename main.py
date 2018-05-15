import argparse

import collections
import requests
import time
import os
import sys


SEARCH_BASE_URL = 'http://www.tekstowo.pl/wyszukaj.html'
SEARCH_FMT_STR = SEARCH_BASE_URL + '?search-title={title}&search-artist={artist}'

Song = collections.namedtuple('Song', ['artist', 'title', 'url'])


class Fetcher:
    def fetch_page(self, url):
        with requests.Session() as session:
            response = session.get(url)
            return response.content

    def search_song(self, artist, title):
        destination_url = SEARCH_FMT_STR.format(title=title, artist=artist)
        return self.fetch_page(destination_url)

    def fetch_lyrics(self, song):
        return self.fetch_page(song.url)


class Parser:
    def parse_search_results(self, results):
        songs_list = []
        results = results.decode('utf-8')
        if 'Znalezieni artyści' in results:
            results = results.split('Znalezieni artyści:')[0]
        operation_array = results.split('<div class="box-przeboje">')[1:]
        for item in operation_array:
            temp_artist_title = item.split('title="')[1].split('">')[0]
            temp_artist = temp_artist_title.split(' - ')[0]
            temp_title = temp_artist_title.split(' - ')[1]
            temp_url = 'http://www.tekstowo.pl'
            temp_url += item.split('a href="')[1].split('.html')[0]
            temp_url += '.html'
            songs_list.append(Song(temp_artist, temp_title, temp_url))

        return songs_list

    def parse_song_lyrics(self, html):
        return html.decode('utf-8')\
            .split('<h2>Tekst piosenki:</h2><br />')[1]\
            .split('<p>&nbsp;</p>')[0]\
            .replace('<br />', '\n')\
            .replace('\n\n', '\n')\
            .strip()  # remove leading and trailing spaces

class Main:
        def get_lyrics(self, song, n=0):
            song = '. '.join(song.split('. ')[1:])[:-9].split(' - ')
            artist = song[0]
            title = song[1]
            temp_txt = self._fetcher.search_song(artist, title)
            temp_results = self._parser.parse_search_results(temp_txt)
            try:
                temp_txt = self._fetcher.fetch_lyrics(temp_results[n])  # 1st song
            except IndexError:
                return "Song not found on tekstowo.pl!"
            temp_txt = self._parser.parse_song_lyrics(temp_txt)
            return temp_txt


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
        artist, title = retrieve_artist_and_title(args.song)
    except InvalidSongFormat as e:
        print(e)
        sys.exit(1)

    print(Parser().parse_song_lyrics(Fetcher().fetch_lyrics(Parser().parse_search_results(Fetcher().search_song(artist, title))[0])))
