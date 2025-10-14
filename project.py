#!/usr/bin/env python

import sys
import os
import platform
import re
import wikipedia
import requests
import lyricsgenius
from bs4 import BeautifulSoup


def main():
    try:
        interface()
    except EOFError:
        sys.exit(0)


def interface():
    screen_clean()
    year = input(
        """
==================== TIME MACHINE ====================

Please type a year between 1946 and 2024:

=> """
    )
    try:
        if 1945 < int(year) < 2025:
            print("\nRetrieving data...\n")
            year_charts = get_charts(year)

            screen_clean()
            print(
                f"""
================= {year} TOP SINGLES =================

Pop charts:
        {year_charts['song_1']}
        by {year_charts['artist_1']}

R&B/Soul/Hip-Hop charts:
        {year_charts['song_3']}
        by {year_charts['artist_3']}

Country charts:
        {year_charts['song_5']}
        by {year_charts['artist_5']}


    ====    Here are some characteristic    ====
    ====     quotes from these 3 songs:     ====

"""
            )

            i = 1
            while i < 7:
                if (
                    i in (1, 3, 5)
                    and year_charts[f"artist_{i}"] != "Not found 🙃"
                    and year_charts[f"song_{i}"] != "Not found 🙃"
                ):
                    try:
                        lyrics, title = get_lyrics(
                            artist=year_charts[f"artist_{i}"],
                            song=year_charts[f"song_{i}"],
                        )
                        print_quotes(format_quotes(lyrics, title))
                    except KeyError:
                        print(f"\nCouldn't retrieve that song's lyrics 🙃\n")
                i += 1

        else:
            interface()

    except ValueError:
        interface()


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
    # create the dictionary
    years = {}
    # iterate over each table row to extract the <td> tag
    for col in table_row:
        html_col = col.find_all("td")
        if len(html_col) == 7:
            # create the year key/value(list) pair
            year = html_col[0].text.strip()[0:5]
            years[year] = {}
            i = 1
            while i < 7:
                if i in (1, 3, 5):
                    # select only the songs (and not the albums) to feed the dictionary
                    if matches := re.search(
                        r'(?:"?(.+)"\[\d.*\](.+)\n)?(.+)\[\d.*\](.+)',
                        html_col[i].text.strip(),
                    ):
                        years[year][f"song_{i}"] = matches.group(3)
                        years[year][f"artist_{i}"] = matches.group(4)

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
    # create a list of the quotes containing the longest word of the title
    longest_title_word = max(title.split(" "), key=len)
    quotes = re.findall(r"\n.*" + longest_title_word + r".*\n", cleaned_file, re.I)
    # extend quotes list to the ones containing the most repeated words
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


def screen_clean():
    os_name = platform.system()
    if os_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")  # for Mac and Linux


if __name__ == "__main__":
    main()
