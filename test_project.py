import pytest

from project import format_quotes
from project import print_quotes
from project import get_lyrics
from project import get_charts


def test_format_quotes():
    with pytest.raises(TypeError):
        format_quotes(1, 2)
    with pytest.raises(TypeError):
        format_quotes("Vogue")
    assert format_quotes(
        "[Produced by Shep Pettibone and Madonna]\n\n[Intro]\nStrike a pose\nStrike a pose\nVogue (Vogue, vogue)\nVogue (Vogue, vogue)\n\n[Verse 1]\nLook around, everywhere you turn is heartache\nIt's everywhere that you go (Look around)\nYou try everything you can to escape\nThe pain of life that you know (Life that you know)\nWhen all else fails and you long to be\nSomething better than you are today\nI know a place where you can get away\nIt's called a dance floor\nAnd here's what it's for, so\n\n[Chorus]\nCome on, vogue (Vogue)\nLet your body move to the music (Move to the music)\nHey, hey, hey\nCome on, vogue (Vogue)\nLet your body go with the flow (Go with the flow)\nYou know you can do it\n\n[Verse 2]\nAll you need is your own imagination\nSo use it, that's what it's for (That's what it's for)\nGo inside for your finest inspiration\nYour dreams will open the door (Open up the door)\nIt makes no difference if you're black or white\nIf you're a boy or a girl\nIf the music's pumping, it will give you new life\nYou're a superstar\nYes, that's what you are, you know it\n\n[Chorus]\nCome on, vogue (Vogue, vogue)\nLet your body groove to the music (Groove to the music)\nHey, hey, hey\nCome on, vogue (Vogue, vogue)\nLet your body go with the flow (Go with the flow)\nYou know you can do it\n\n[Bridge]\nBeauty's where you find it\nNot just where you bump and grind it\nSoul is in the musical\nThat's where I feel so beautiful\nMagical, life's a ball, so\nGet up on the dance floor\n\n[Chorus]\nVogue (Vogue)\nLet your body move to the music (Move to the music)\nHey, hey, hey\nCome on, vogue (Vogue, vogue)\nLet your body go with the flow (Go with the flow)\nYou know you can do it\n\n[Refrain]\nVogue (Vogue)\nBeauty's where you find it (Move to the music)\nVogue (Vogue)\nBeauty's where you find it (Go with the flow)\n\n[Verse 3]\nGreta Garbo, and Monroe\nDietrich and DiMaggio\nMarlon Brando, Jimmy Dean\nOn the cover of a magazine\nGrace Kelly, Harlow, Jean\nPicture of a beauty queen\nGene Kelly, Fred Astaire\nGinger Rogers dance on air\nThey had style, they had grace\nRita Hayworth gave good face\nLauren, Katharine, Lana too\nBette Davis, we love you\nLadies with an attitude\nFellas that were in the mood\nDon't just stand there, let's get to it\nStrike a pose, there's nothing to it\nVogue\nVogue\n\n[Outro]\nOoh, you've got to\nLet your body move to the music\nOoh, you've got to just\nLet your body go with the flow\nOoh, you've got to\nVogue (Vogue, vogue, vogue)",
        "Vogue",
    ) == [
        "Vogue",
        "Come on, vogue",
        "Soul is in the musical",
        "Beauty's where you find it",
        "Let your body move to the music",
        "That's where I feel so beautiful",
        "Let your body groove to the music",
        "I know a place where you can get away",
        "Look around, everywhere you turn is heartache",
        "If the music's pumping, it will give you new life",
    ]


def test_print_quotes():
    with pytest.raises(TypeError):
        print_quotes()
    with pytest.raises(TypeError):
        print_quotes(1989)


def test_get_lyrics():
    with pytest.raises(TypeError):
        get_lyrics(1989, "madonna")
    with pytest.raises(TypeError):
        get_lyrics("madonna", 1989)
    with pytest.raises(NameError):
        get_lyrics(q, w)


def test_get_charts():
    with pytest.raises(KeyError):
        get_charts("1945")
    with pytest.raises(KeyError):
        get_charts("2026")
    with pytest.raises(KeyError):
        get_charts("year")
    with pytest.raises(TypeError):
        get_charts()
