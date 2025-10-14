#!/usr/bin/env python

import pytest

# from project import interface
from project import get_lyrics
from project import get_charts


# def test_interface():
#     pass


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
