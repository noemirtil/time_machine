
# TIME MACHINE

#### Video Demo:  <URL HERE>

#### Description:

The 'Time machine' application will rescape some characteristic quotes from forgotten top songs of the past, to let the user catch a glimpse of the musical pop era of their choice.

On opening project.py, the terminal interface will clean and the user will be prompted for a year. If the year entered is not between 1946 and 2024 as prompted, or in any format that isn't a numerical year, the user will be prompted again. At every moment, the user can enter ^d to exit Time machine without displaying an error.

Once received a compatible year, Time machine will pass it to the get_charts() function, which uses the [Wikipedia API](https://pypi.org/project/wikipedia/) in order to connect with [a Wikipedia page](https://en.wikipedia.org/wiki/List_of_Billboard_Year-End_number-one_singles_and_albums) in which the top charts of the pop era are referenced. The get_charts() function then uses the [BeautifulSoup API](https://pypi.org/project/beautifulsoup4/) in order to parse through the "top charts" html table rows, find the rows beginning by a year number, and creates a 'years' dictionary in which every key is a year. The value for each year is also a dictionary containing six keys, refering to three song names and three corresponding artist names in this example format:


	1985: {
		'song_1': '"Careless Whisper"',
		'artist_1': 'Wham! featuring George Michael',
		'song_3': '"Rock Me Tonight (For Old Times Sake)"',
		'artist_3': 'Freddie Jackson',
		'song_5': '"Lost in the Fifties Tonight"',
		'artist_5': 'Ronnie Milsap'
		}


In this project I purposely decided to focus on the singles, letting the albums option open to some future developing, that's why get_charts() only collects odd-numbered data, even-numbered data being reserved for the albums.
Always relying on the use of various regexes throughout the whole application process to clean and extract data, the get_charts() function then seeds the 'years' dictionary with the data collected from the wikipedia page, and the interface() function then displays on screen the basic information about the prompted year's three top singles.

Once for each of the three top singles, Time machine will then automatically pass the artist name and the song name to the get_lyrics() function, which relies on the [lyricsgenius API](https://pypi.org/project/lyricsgenius/) to collect each song's lyrics from [genius website](https://genius.com/). [The requests API](https://pypi.org/project/requests/) is used to raise an exception if any, otherwise will return a tuple of two strings: one long lyrics string and another string for the title of the song.

This tuple is then passed to the format_quotes(lyrics, title) function which main purpose is to select the most characteristic phrases from the whole lyrics string, basing its choice on three parameters:
- Does the phrase contain the longest word of the song's title?
- Does the phrase contain one of the song's most repeated words?
- Are these words longer than four characters?

To do so, 















