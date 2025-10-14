#!/usr/bin/env python

import sys
import os
import platform
import re
import wikipedia
import requests
import lyricsgenius
from bs4 import BeautifulSoup


def get_lyrics(artist, song):
    cleaned_artist = re.sub(r"\s\(.*\)|/.*", "", artist).strip()
    cleaned_title = re.sub(r"\"|\s\(.*\)|[\(\)]|/.*", "", song).strip()

    # my personal token
    tokenized = lyricsgenius.Genius(
        "w7Y1kofFOGXkztFMC5gC4SaRzxm24pxZraUU8n902tbu9opjgdkQlh8WHP5BDylB"
    )
    # retrieving the song's lyrics
    try:
        file = tokenized.search_song(cleaned_title, cleaned_artist)
        if file != None:
            return file.lyrics, cleaned_title
        else:
            print("Sorry 🙃\n")

    except requests.exceptions.RequestException:
        print("Sorry, this song was not found 🙃\n")


def format_quotes(lyrics, title):
    # remove the [...] notes
    cleaned_file = re.sub(r"\[.*\]|\(.*\)|\(\n|\n\)", "", lyrics)
    # create a list of words
    split_file = re.split(r"[\s.,;:?()]", cleaned_file)
    # capitalize each word to solve case problems
    capitalized = list(map(str.capitalize, split_file))
    # create a dictionary of counted words
    counted_words = {word: capitalized.count(word) for word in capitalized}
    del counted_words[""]
    # created a sorted by values version of the dictionary
    sorted_words = dict(
        sorted(counted_words.items(), key=lambda key_val: key_val[1], reverse=True)
    )
    # create a list of the quotes containing the longest word in the title
    longest_title_word = max(title.split(" "), key=len)
    quotes = re.findall(r"\n.*" + longest_title_word + r".*\n", cleaned_file, re.I)
    # extend quotes list to the most repeated words
    for word in sorted_words:
        if sorted_words[word] > 3 and len(word) > 4:
            quotes.extend(re.findall(r"\n.*" + word + r".*\n", cleaned_file, re.I))
    # remove duplicates
    unique_quotes = list(
        set(
            map(
                str.strip,
                [
                    s.replace('"', "").replace(" ,", " ").replace("  ", " ")
                    for s in quotes
                ],
            )
        )
    )
    unique_quotes.sort(key=lambda s: len(s))
    return unique_quotes


def print_quotes(quotes):
    print("")
    if len(quotes) > 0:
        selected_quotes = []
        for quote in quotes:
            quote[0].upper()
            quote_format = quote.replace("\n", "")
            if quote_format[0] != "(" and len(quote_format.split(" ")) > 2:
                selected_quotes.append(quote_format)
        for quote in selected_quotes[:4]:
            print(quote)
    else:
        print("Sorry, this song lacks lyrics 🙃")
    print(
        f"""
~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
            """
    )


lyrics, title = get_lyrics("Madonna", "Vogue")
print_quotes(format_quotes(lyrics, title))
