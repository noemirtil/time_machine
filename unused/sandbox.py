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
            # print(file.lyrics)
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
    # print(sorted_words)
    # create a list of the quotes containing the longest word in the title
    longest_title_word = max(title.split(" "), key=len)
    print(longest_title_word)
    # quotes = re.findall(r"\n.*" + longest_title_word + r".*\n", cleaned_file, re.I)
    quotes = []
    # extend quotes list to the most repeated words
    for word in sorted_words:
        if sorted_words[word] > 3 and len(word) > 4:
            quotes.append(re.findall(r"\n.*" + word + r".*\n", cleaned_file, re.I))
    # remove duplicates
    print(quotes)
    unique_quotes = list(
        set(
            map(
                str.strip,
                [
                    s.replace('"', "").replace(" ,", " ").replace("  ", " ")
                    for s in quotes
                    if isinstance(s, str)  # Check if s is a string
                ],
            )
        )
    )
    unique_quotes.sort(key=lambda s: len(s))
    unique_quotes.insert(
        0, re.findall(r"\n.*" + longest_title_word + r".*\n", cleaned_file, re.I)
    )
    print(unique_quotes)
    return unique_quotes


# lyrics, title = get_lyrics("Madonna", "Vogue")
# print_quotes(format_quotes(lyrics, title))
# print(get_lyrics("Madonna", "Vogue"))
# print(format_quotes(1, 2))


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


# print_quotes(3)


def get_charts(y):
    page = wikipedia.page("List_of_Billboard_Year-End_number-one_singles_and_albums")
    # create a BeautifulSoup Object
    soup = BeautifulSoup(
        page.html(),
        "html.parser",
    )
    # find the table we are looking for
    charts_table = soup.find("table", {"class": "wikitable"})
    # find all `tr` tags
    table_row = charts_table.find_all("tr")
    # create the dictionary of years
    years = {}
    # iterate over each table row to extract the <td> tag
    for col in table_row:
        html_col = col.find_all("td")
        if len(html_col) == 7:
            # create the year key/value(dict) pair like {1985: {}}
            year = html_col[0].text.strip()[0:5]
            years[year] = {}
            i = 1
            while i < 7:
                if i in (1, 3, 5):
                    # select only the songs (and not the albums) to feed the dictionary values
                    if matches := re.search(
                        r'(?:"?(.+)"\[\d.*\](.+)\n)?(.+)\[\d.*\](.+)',
                        html_col[i].text.strip(),
                    ):
                        years[year][f"song_{i}"] = matches.group(3)
                        years[year][f"artist_{i}"] = matches.group(4)
                    # manage key errors:
                    if not f"song_{i}" in years[year].keys():
                        years[year][f"song_{i}"] = "Not found 🙃"
                    if not f"artist_{i}" in years[year].keys():
                        years[year][f"artist_{i}"] = "Not found 🙃"
                    years[year][f"song_{i}"] = re.sub(
                        r"\[\d+\]", "", years[year][f"song_{i}"]
                    )
                    if years[year][f"song_{i}"][0] != '"':
                        years[year][f"song_{i}"] = '"' + years[year][f"song_{i}"]
                    if years[year][f"song_{i}"][-1] != '"':
                        years[year][f"song_{i}"] = years[year][f"song_{i}"] + '"'

                i += 1
    return years[y]


# print(get_charts("1985"))
# print(get_lyrics("Wham! featuring George Michael", '"Careless Whisper"'))
format_quotes(
    "[Intro]\nTime can never mend\nThe careless whispers of a good friend\nTo the heart and mind, ignorance is kind\nThere's no comfort in the truth, pain is all you'll find\nShould have known better, yeah\n\n[Instrumental Break]\n\n[Bridge]\nOh, woah, woah, oh\nMm\n\n[Verse 1]\nI feel so unsure\nAs I take your hand and lead you to the dance floor\nAs the music dies, something in your eyes\nCalls to mind a silver screen and all its sad goodbyes\n\n[Chorus]\nI'm never gonna dance again\nGuilty feet have got no rhythm\nThough it's easy to pretend\nI know you're not a fool\nI should have known better than to chеat a friend\nAnd waste the chancе that I'd been given\nSo I'm never gonna dance again\nThe way I danced with you, oh\n\n[Verse 2]\nTime can never mend\nThe careless whispers of a good friend\nTo the heart and mind, ignorance is kind\nThere's no comfort in the truth, pain is all you'll find\n\n[Chorus]\nI'm never gonna dance again\nGuilty feet have got no rhythm\nThough it's easy to pretend\nI know you're not a fool\nI should have known better than to cheat a friend (Shoulda known better, yeah)\nAnd waste the chance that I'd been given\nSo I'm never gonna dance again\nThe way I danced with you, oh\n\n[Post-Chorus]\nNever without your love\n\n[Instrumental Break]\n\n[Verse 3]\nTonight, the music seems so loud\nI wish that we could lose this crowd\nMaybe it's better this way\nWe'd hurt each other with the things we want to say\nWe could have been so good together\nWe could have lived this dance forever\nBut now, who's gonna dance with me?\nPlease stay\n\n[Chorus]\nAnd I'm never gonna dance again\nGuilty feet have got no rhythm\nThough it's easy to pretend\nI know you're not a fool\nI should have known better than to cheat a friend\nAnd waste the chance that I'd been given\nSo I'm never gonna dance again\nThe way I danced with you, oh\n\n[Instrumental Break]\n\n[Outro]\n(Now that you're gone) Now that you're gone\n(Now that you're gone) Was what I did so wrong, so wrong\nThat you had to leave me alone?",
    "Careless Whisper",
)
