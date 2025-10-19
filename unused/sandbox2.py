#!/usr/bin/env python


import re

cleaned_file = """
Mm

[Chorus: Jack Harlow &
Fergie
]
I been a G, throw up the L, sex in the A.M., uh-huh
O-R-O-U-S, yeah
And I can put you in First class, up in the sky
I can put you in First class, up in the s—, up-up in the s—
I been a G, throw up the L, sex in the A.M., uh-huh
O-R-O-U-S, yeah
And I can put you in First class, up in the sky, mm, mm
I can put you in First class, up in
 the s—, up-up in the s—


I can see the whole city from this balcony
Back in 2019, I was outside freely, but now they got it out for me
I don't care what frat that you was in, you can't alpha me, keep dreamin'
Pineapple juice, I give her sweet, sweet, sweet semen\n
I know what they like so I just keep cheesin'\n
Hard drive full of heat seekin'\n
Tryna come the same day as Jack? Rethink it\n
You don't need Givenchy, you need Jesus\n
Why do y'all sleep on me? I need reasons
Uh, I got plaques in thе mail, peak season
Shout out to my UPS workers makin' surе I receive 'em
You can do it too, believe it

[Chorus: Jack Harlow &
Fergie
]
I been a G, throw up the L, sex in the A.M., uh-huh
O-R-O-U-S, yeah
And I can put you in First class, up in the sky, mm, mm
I can put you in First class, up in the s—, up-up in the s—


Are you ready? Ha, yes, I am
They say, "You a superstar now," damn, I guess I am
You might be the man, well, that's unless I am
Okay, I'll confess I am
Go ahead and get undressed, I am
Okay, cool, you on Sunset?
I'm 'bout to slide, okay, I'm outside, okay
This lifestyle don't got many downsides
'Cept for the lack of time I get 'round my
Family, makin' sure they never downsize
I got visions of my mom sayin', "Wait, this house mine?"
Can't lie, I'm on Angus, Cloud 9
I got 'em on the bandwagon now, 'bout time
I ain't even got no downtime
Every time I speak, she say, "Yeah, that sounds fine"

[Chorus: Jack Harlow &
Fergie
]
I been a G, throw up the L, sex in the A.M., uh-huh
O-R-O-U-S, yeah
And I can put you in First class, up in the sky
I can put you in First class, up in the s—, up-up in the s—
I been a G, throw up the L, sex in the A.M., uh-huh
O-R-O-U-S, yeah
And I can put you in First class, up in the sky, mm, mm
I can put you in First class
"""


def format_quotes(title):
    # created a sorted by values version of the dictionary
    counted_words = {
        "I": 35,
        "In": 31,
        "The": 28,
        "You": 18,
        "Up": 14,
        "Can": 12,
        "A": 11,
        "Put": 10,
        "First": 10,
        "Class": 10,
        "S—": 8,
        "Mm": 7,
        "And": 6,
        "Got": 6,
        "Been": 5,
        "G": 5,
        "Throw": 5,
        "L": 5,
        "Sex": 5,
        "M": 5,
        "Uh-huh": 5,
        "O-r-o-u-s": 5,
        "Yeah": 5,
        "Sky": 5,
        "Am": 5,
        "Jack": 4,
        "Up-up": 4,
        "They": 4,
        "It": 4,
        "On": 4,
        "Okay": 4,
        "[chorus": 3,
        # "Harlow": 3,
        # "&": 3,
        # "Fergie": 3,
        # "]": 3,
        # "This": 3,
        # "Now": 3,
        # "Me": 3,
        # "Don't": 3,
        # "Sweet": 3,
        # "Of": 3,
        # "Need": 3,
        # "My": 3,
        # "I'm": 3,
        # "Time": 3,
        # "Was": 2,
        # "Outside": 2,
        # "Out": 2,
        # "For": 2,
        # "What": 2,
        # "That": 2,
        # "Can't": 2,
        # "Keep": 2,
        # "Do": 2,
        # "To": 2,
        # "Makin'": 2,
        # "'em": 2,
        # "Say": 2,
        # '"': 2,
        # "Get": 2,
        # "'bout": 2,
        # "See": 1,
        # "Whole": 1,
        # "City": 1,
        # "From": 1,
        # "Balcony": 1,
        # "Back": 1,
        # "2019": 1,
        # "Freely": 1,
        # "But": 1,
        # "Care": 1,
        # "Frat": 1,
        # "Alpha": 1,
        # "Dreamin'": 1,
        # "Pineapple": 1,
        # "Juice": 1,
        # "Give": 1,
        # "Her": 1,
        # "Semen": 1,
        # "Know": 1,
        # "Like": 1,
        # "So": 1,
        # "Just": 1,
        # "Cheesin'": 1,
        # "Hard": 1,
        # "Drive": 1,
        # "Full": 1,
        # "Heat": 1,
        # "Seekin'": 1,
        # "Tryna": 1,
        # "Come": 1,
        # "Same": 1,
        # "Day": 1,
        # "As": 1,
        # "Rethink": 1,
        # "Givenchy": 1,
        # "Jesus": 1,
        # "Why": 1,
        # "Y'all": 1,
        # "Sleep": 1,
        # "Reasons": 1,
        # "Uh": 1,
        # "Plaques": 1,
        # "Thе": 1,
        # "Mail": 1,
        # "Peak": 1,
        # "Season": 1,
        # "Shout": 1,
        # "Ups": 1,
        # "Workers": 1,
        # "Surе": 1,
        # "Receive": 1,
        # "Too": 1,
        # "Believe": 1,
        # "Are": 1,
        # "Ready": 1,
        # "Ha": 1,
        # "Yes": 1,
        # '"you': 1,
        # "Superstar": 1,
        # "Damn": 1,
        # "Guess": 1,
        # "Might": 1,
        # "Be": 1,
        # "Man": 1,
        # "Well": 1,
        # "That's": 1,
        # "Unless": 1,
        # "I'll": 1,
        # "Confess": 1,
        # "Go": 1,
        # "Ahead": 1,
        # "Undressed": 1,
        # "Cool": 1,
        # "Sunset": 1,
        # "Slide": 1,
        # "Lifestyle": 1,
        # "Many": 1,
        # "Downsides": 1,
        # "'cept": 1,
        # "Lack": 1,
        # "'round": 1,
        # "Family": 1,
        # "Sure": 1,
        # "Never": 1,
        # "Downsize": 1,
        # "Visions": 1,
        # "Mom": 1,
        # "Sayin'": 1,
        # '"wait': 1,
        # "House": 1,
        # "Mine": 1,
        # "Lie": 1,
        # "Angus": 1,
        # "Cloud": 1,
        # "9": 1,
        # "Bandwagon": 1,
        # "Ain't": 1,
        # "Even": 1,
        # "No": 1,
        # "Downtime": 1,
        # "Every": 1,
        # "Speak": 1,
        # "She": 1,
        # '"yeah': 1,
        # "Sounds": 1,
        # 'Fine"': 1,
    }
    # create quotes list with the ones containing the most repeated words
    quotes = []
    for word in counted_words:
        if counted_words[word] > 1 and len(word) > 3:
            quotes.extend(re.findall(r"\n.*" + word + r".*\n", cleaned_file, re.I))
            # quotes.extend(re.findall(r"\n.*" + word + r".*\n", cleaned_file, re.I))
    # sort quotes by length
    quotes.sort(key=lambda s: len(s))
    # create a list of the quotes containing the longest word of the title
    longest_title_word = max(title.split(" "), key=len)
    longest_title_word_quotes = re.findall(
        r"\n.*" + longest_title_word + r".*\n", cleaned_file, re.I
    )
    # sort longest_title_word_quotes by length
    longest_title_word_quotes.sort(key=lambda s: len(s))
    print(longest_title_word_quotes)
    # insert the shortest of the longest_title_word_quotes at first index
    # of quotes to ensure it will be included in the final selection
    # for q in longest_title_word_quotes:
    if len(longest_title_word_quotes) > 0:
        quotes.insert(0, longest_title_word_quotes[0])
    # clean the quotes
    print(quotes)
    cleaned_quotes = map(
        str.strip,
        [s.replace('"', "").replace(" ,", " ").replace("  ", " ") for s in quotes],
    )
    # remove duplicates preserving the order
    unique_quotes = list(dict.fromkeys(cleaned_quotes))
    print(unique_quotes)
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


print_quotes(format_quotes("First Class"))
