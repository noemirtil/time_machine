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

Please enter a year between 1946 and 2024:

=> """
    )
    # get that year's top charts from Wikipedia
    try:
        if 1945 < int(year) < 2025:
            print("\nRetrieving data...\n")
            year_charts = get_charts(year)

            screen_clean()
            # display only the singles, not the albums, that's why the numbers are even:
            print(
                f"""
================== {year} TOP SINGLES =================

Nº1 of the Pop charts in {year}:
        {year_charts['song_1']}
        by {year_charts['artist_1']}

Nº1 of the R&B/Soul/Hip-Hop charts in {year}:
        {year_charts['song_3']}
        by {year_charts['artist_3']}

Nº1 of the Country charts in {year}:
        {year_charts['song_5']}
        by {year_charts['artist_5']}


    ====     Here are some significant      ====
    ====     quotes from these 3 songs:     ====

"""
            )
            # for each song, retrieve the lyrics from Genius, extract the best quotes and display them:
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
                        print(
                            f"\nCouldn't retrieve that song's lyrics 🙃\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                        )
                    except TypeError:
                        print(
                            f"\nCouldn't retrieve that song's lyrics 🙃\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                        )
                i += 1
            # resetting 'year' variable to avoid query confusion
            del year
        else:
            interface()

    except ValueError:
        interface()


def get_charts(year_of_interest):
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
                    # feed the years[year] dictionary in that format:
                    # 1985: {'song_1': '"Careless Whisper"', 'artist_1': 'Wham! featuring George Michael',
                    # 'song_3': '"Rock Me Tonight (For Old Times Sake)"', 'artist_3': 'Freddie Jackson',
                    # 'song_5': '"Lost in the Fifties Tonight"', 'artist_5': 'Ronnie Milsap'}
                    if years[year][f"song_{i}"][0] != '"':
                        years[year][f"song_{i}"] = '"' + years[year][f"song_{i}"]
                    if years[year][f"song_{i}"][-1] != '"':
                        years[year][f"song_{i}"] = years[year][f"song_{i}"] + '"'

                i += 1
    return years[year_of_interest]


def get_lyrics(artist, song):
    # clean inputs for the API
    cleaned_artist = re.sub(r"\s\(.*\)|/.*", "", artist).strip()
    cleaned_title = re.sub(r"\"|\s\(.*\)|[\(\)]|/.*", "", song).strip()

    # my personal token
    tokenized = lyricsgenius.Genius(
        "w7Y1kofFOGXkztFMC5gC4SaRzxm24pxZraUU8n902tbu9opjgdkQlh8WHP5BDylB"
    )
    # retrieve the song's lyrics
    try:
        file = tokenized.search_song(cleaned_title, cleaned_artist)
        if file != None:
            return file.lyrics, cleaned_title
        else:
            print("Sorry, this song was not found 🙃")
            return ("", "")

    except requests.exceptions.RequestException:
        print("Sorry, this song was not found 🙃\n")
        return ("", "")


def remove_subsets(list):
    # iterate through the quotes to find subsets of other quotes
    i = 0
    while i < len(list):
        # create a list with the words of the quote
        # split_quote = list[i].split(" ")
        split_quote = [word.lower().replace(",", "") for word in list[i].split(" ")]
        # set default value for is_substring variable
        is_substring = False
        # sub-iteration
        for quote in list:
            # list all quote's words
            words = [word.lower().replace(",", "") for word in quote.split(" ")]
            # pass if sub-iterated quote matches iterated quote
            if quote == list[i]:
                pass
            # if all words of sub-iterated quote match the iterated quote
            elif all([ele in words for ele in split_quote]):
                # then change value for is_substring variable
                is_substring = True
                break
        # remove quote from the list if is_substring variable is True
        if is_substring:
            list.remove(list[i])
            # decrement the index to account for the removed element
            i -= 1
        # increment the index to trigger next iteration
        i += 1
    return list


def format_quotes(lyrics, title):
    # print(lyrics)
    # remove the [...] notes
    cleaned_file = re.sub(
        r"\[.*\n?.*\n?.*\n?\]|\(.*?\n?.*?\n?.*?\n?\)|\(\n|\n\)",
        "",
        lyrics,
    )
    # print("\n" + cleaned_file)
    # create a list of words
    split_file = re.split(r"[\s.,;:?()]", cleaned_file)
    # print(split_file)
    # capitalize each word to solve case problems
    capitalized = list(map(str.capitalize, split_file))
    # create a dictionary of counted words
    counted_words = {word: capitalized.count(word) for word in capitalized}
    # print(counted_words)
    del counted_words[""]
    # created a sorted by values version of the dictionary
    # sorted_words = dict(
    #     sorted(counted_words.items(), key=lambda key_val: key_val[1], reverse=True)
    # )
    # print(sorted_words)
    # create quotes list with the ones containing the most repeated words
    quotes = []
    for word in counted_words:
        if counted_words[word] > 1 and len(word) > 3:
            quotes.extend(re.findall(r"\n.*" + word + r".*\n", cleaned_file, re.I))
    # sort quotes by length
    quotes.sort(key=lambda s: len(s), reverse=True)
    # create a list of the quotes containing the longest word of the title
    longest_title_word = max(title.split(" "), key=len)
    longest_title_word_quotes = re.findall(
        r"\n.*" + longest_title_word + r".*\n", cleaned_file, re.I
    )
    # sort longest_title_word_quotes by length
    longest_title_word_quotes.sort(key=lambda s: len(s), reverse=True)
    # print(longest_title_word_quotes)
    # append the longest of the longest_title_word_quotes to quotes list
    if len(longest_title_word_quotes) > 0:
        quotes.append(longest_title_word_quotes[0])
    # print(quotes)
    # clean the quotes
    cleaned_quotes = list(
        map(
            str.strip,
            [s.replace('"', "").replace(" ,", " ").replace("  ", " ") for s in quotes],
        )
    )
    # create a dictionary of counted quotes
    counted_quotes = {quote: cleaned_quotes.count(quote) for quote in cleaned_quotes}
    # print(counted_quotes)
    # created a sorted by values list from the dictionary
    sorted_quotes = []
    for quote, n in sorted(
        counted_quotes.items(), key=lambda key_val: key_val[1], reverse=True
    ):
        sorted_quotes.append(quote)
    # print(remove_subsets(sorted_quotes))
    return remove_subsets(sorted_quotes)


def print_quotes(quotes):
    print("")
    if len(quotes) > 0:
        # create a list of the best quotes
        selected_quotes = []
        for quote in quotes:
            quote[0].upper()
            quote_format = quote.replace("\n", "")
            if quote_format[0] != "(" and len(quote_format.split(" ")) > 1:
                selected_quotes.append(quote_format)
        # print the top best quotes of the list (max 5)
        for quote in selected_quotes[:5]:
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
