
# TIME MACHINE

#### Video Demo:  <URL HERE>

#### Description:

The "Time machine" application will rescape some characteristic quotes from forgotten top songs of the past, to let the user catch a glimpse of the musical pop era of their choice.

On opening `project.py`, the terminal interface will automatically clean up and the user will be asked to select a year. If the year entered is not between 1946 and 2024 as prompted, or in any format that isn't a numerical integer year, the user will be prompted again. At every moment, the user can type `^ d` to exit Time machine without displaying an error.

Time machine will pass the selected year to the `get_charts()` function, which uses the [Wikipedia API](https://pypi.org/project/wikipedia/) in order to connect with [a Wikipedia page](https://en.wikipedia.org/wiki/List_of_Billboard_Year-End_number-one_singles_and_albums) in which the top charts of the pop era are referenced. The `get_charts()` function then uses the [BeautifulSoup API](https://pypi.org/project/beautifulsoup4/) in order to parse through the "top charts" html table rows, find the rows beginning by a year number, and creates a `years` dictionary in which every key is a year. The value for each year is also a dictionary containing six keys, refering to three song names and three corresponding artist names in this example format:


	1985: {
		'song_1': '"Careless Whisper"',
		'artist_1': 'Wham! featuring George Michael',
		'song_3': '"Rock Me Tonight (For Old Times Sake)"',
		'artist_3': 'Freddie Jackson',
		'song_5': '"Lost in the Fifties Tonight"',
		'artist_5': 'Ronnie Milsap'
		}


In this project I purposely decided to focus only on the singles, letting the albums options open to some future developing, that's why `get_charts()` only collects odd-numbered data, even-numbered data being reserved for the albums.
Always relying on the use of various regexes throughout the whole application process to clean and extract data, the `get_charts()` function then seeds the `years` dictionary with the data collected from the wikipedia page, and the `interface()` function then displays on screen the basic information about the prompted year's three top singles.

Once for each of the three top singles, Time machine will then automatically pass the artist name and the song name to the `get_lyrics()` function, which relies on the [lyricsgenius API](https://pypi.org/project/lyricsgenius/) to collect each song's lyrics from [genius website](https://genius.com/). [The requests API](https://pypi.org/project/requests/) is used to raise an exception if any, otherwise will return a tuple of two strings: one long lyrics string and another string for the title of the song.

This tuple is then passed to the `format_quotes(lyrics, title)` function, whose main purpose is to select the most characteristic phrases out of the whole lyrics string, basing its choice on three parameters:

- Does the phrase contain the longest word of the song's title?
- Does the phrase contain one of the song's most repeated words?
- Are these words longer than four characters?

To do so, once again, regexes are used to clean the lyrics long string, split it into a list, feed a dictionary in which every word occurence is a key whose value is the number of its occurences in the song, in this example format:


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
	'Is': 4, 
	'Should': 4, 
	'Known': 4, 
	"It's": 4, 
	"You're": 4, 
	'Been': 4, 
	'Way': 4, 
	'We': 4, 
	'Good': 3, 
	'Mind': 3, 
	'In': 3, 
	'All': 3, 
	'Your': 3, 
	'Guilty': 3, 
	'Feet': 3, 
	'Got': 3, 
	'Rhythm': 3, 
	'Though': 3, 
	'Easy': 3, 
	'Pretend': 3, 
	'Know': 3, 
	'Not': 3, 
	'Fool': 3, 
	'Than': 3, 
	'Waste': 3, 
	"I'd": 3, 
	'Given': 3, 
	'Danced': 3, 
	'Could': 3, 
	'This': 3, 
	'Time': 2, 
	'Can': 2, 
	'Mend': 2, 
	'Careless': 2, 
	'Whispers': 2, 
	'Of': 2, 'Heart': 2, 'Ignorance': 2, 'Kind': 2, "There's": 2, 'Comfort': 2, 'Truth': 2, 'Pain': 2, "You'll": 2, 'Find': 2, 'Woah': 2, 'As': 2, 'Music': 2, 'Cheat': 2, 'Chance': 2, 'Now': 2, 'Me': 2, 'Wrong': 2, 'Yeah': 1, 'Mm': 1, 'Feel': 1, 'Unsure': 1, 'Take': 1, 'Hand': 1, 'Lead': 1, 'Floor': 1, 'Dies': 1, 'Something': 1, 'Eyes': 1, 'Calls': 1, 'Silver': 1, 'Screen': 1, 'Its': 1, 'Sad': 1, 'Goodbyes': 1, 'Chеat': 1, 'Chancе': 1, 'Without': 1, 'Love': 1, 'Tonight': 1, 'Seems': 1, 'Loud': 1, 'Wish': 1, 'Lose': 1, 'Crowd': 1, 'Maybe': 1, "We'd": 1, 'Hurt': 1, 'Each': 1, 'Other': 1, 'Things': 1, 'Want': 1, 'Say': 1, 'Together': 1, 'Lived': 1, 'Forever': 1, 'But': 1, "Who's": 1, 'Please': 1, 'Stay': 1, 'Gone': 1, 'Was': 1, 'What': 1, 'Did': 1, 'Had': 1, 'Leave': 1, 'Alone': 1}



In this example one can appreciate the complex questions rising at the time of chosing the right balance between most repeated words, which tend to be very short in  a pop song, and between longest words, obviously more interesting but also 










