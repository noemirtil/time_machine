
# TIME MACHINE

#### Video Demo:  [https://youtu.be/udcpzr9RI_Y](https://youtu.be/udcpzr9RI_Y)

#### Description:

##### _Caution_: This project can't run from Codespace (would run into an access_token AssertionError)

The "Time machine" application will rescape some characteristic quotes from forgotten top songs of the past, to let the user a glimpse into the era of their choice, spanning the last 78 years of pop music. Beyond the nostalgic appeal, "Time machine" also reveals how, for example, pop culture in a year like 1959 was influenced by war feats, whereas, as soon as the next year, popular interests were more focused towards emotional feelings.

On opening `project.py`, the terminal interface will automatically clear, and the user will be asked to select a year. If the year entered is not between 1946 and 2024 (as prompted), or in any format that isn't a numerical integer year, the user will be prompted again. The user can also type `^d` to exit Time machine without displaying an error.

Time machine will then pass the selected year to the `get_charts(year_of_interest)` function, which uses [Wikipedia API](https://pypi.org/project/wikipedia/) in order to connect with a [Wikipedia page](https://en.wikipedia.org/wiki/List_of_Billboard_Year-End_number-one_singles_and_albums) in which the top charts are referenced by year. The `get_charts(year_of_interest)` function then uses the [BeautifulSoup API](https://pypi.org/project/beautifulsoup4/) in order to parse through the "top charts" html table rows, find the rows beginning by a year number, and creates a `years` dictionary in which every key is a year. The value for each year is also a dictionary containing six keys, refering to three song names and three corresponding artist names in this example format:


	1985: {
		'song_1': '"Careless Whisper"',
		'artist_1': 'Wham! featuring George Michael',
		'song_3': '"Rock Me Tonight (For Old Times Sake)"',
		'artist_3': 'Freddie Jackson',
		'song_5': '"Lost in the Fifties Tonight"',
		'artist_5': 'Ronnie Milsap'
		}


In this project I purposely decided to focus only on the singles, leaving the albums options open to some future developing. Therefore, `get_charts(year_of_interest)` only collects odd-numbered data, even-numbered data being reserved for the albums.
Consistently using various regexes throughout the whole application process to clean and extract data, the `get_charts(year_of_interest)` function then populates the `years` dictionary with the data collected from the [Wikipedia page](https://en.wikipedia.org/wiki/List_of_Billboard_Year-End_number-one_singles_and_albums), and the `interface()` function then displays on screen basic information about the prompted year's three top singles.

Once for each of the three top singles, Time machine will then automatically pass the artist name and the song name to the `get_lyrics(artist, song)` function, which relies on the [lyricsgenius API](https://pypi.org/project/lyricsgenius/) to collect the lyrics for each song from the [genius website](https://genius.com/). Not every song is available on Genius, some of the oldest ones won't be found, and the retrieving also fluctuates upon [genius website](https://genius.com/) servers, however, most of the top singles are available. Also, [the requests API](https://pypi.org/project/requests/) is used to catch exceptions and print a friendly message until next intent, otherwise, `get_lyrics(artist, song)` will return a tuple of two strings: one long lyrics string and another string for the song title.

This tuple is then passed to the `format_quotes(lyrics, title)` function, whose main purpose is to select the most characteristic phrases out of the whole lyrics string, basing its choice on several parameters:

- Does the phrase contain some significant word from the song title?
- Does the phrase contain a word that appears at least twice in the song?
- Are these words longer than three characters?
- Is the phrase shorter than 67 characters?
- Does the phrase appear frequently throughout the song?
- Is the phrase among the longest already selected?

To do so, once again, regexes are used to clean the lyrics long string, split it into a list, and populate a dictionary in which every word is a key whose value is the number of its occurences in the song, in this example format:


	{'The': 16,
	'I': 13,
	'To': 12,
	'Never': 9,
	'A': 9,
	'Have': 9,
	'Dance': 9,
	'And': 8,
	'So': 8,
	'Gonna': 7,
	"I'm": 6,
	'Again': 6,
	'That': 6,
	'Friend': 5,
	'No': 5,
	'Better': 5,
	'Oh': 5,
	'You': 5,
	'With': 5,
	'Is': 4, AND SO ON...}


Once all the quotes of interest are listed, `format_quotes(lyrics, title)` keeps on doing a bit of cleaning to avoid near-duplicates before sorting them by number of occurences with the help of `Counter` function from `collections` module. Then the list is passe through the `remove_subsets(list)` function before `format_quotes(lyrics, title)` returns it.

The purpose of `remove_subsets(list)` is to find subsets of other quotes. Thus, if almost all (all, or all but one) of the words in a quote belong to another quote, it will be removed from the list, to prevent the user from feeling they're reading the same quote twice when only one word differs.

The `interface()` function will then pass the list returned by `format_quotes(lyrics, title)` to `print_quotes(quotes)` in order to display the five most characteristic quotes from everyone of the three top singles of the selected year, after some additional final cleaning in order to catch some special cases.


#### Hope you'll enjoy using "Time machine" as much as I enjoyed writing it!





