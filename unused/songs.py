#!/usr/bin/env python

import json
import requests
import sys
import unused.albums as albums


def main():

    print(albums.name)

    # response = requests.get(
    #     "https://itunes.apple.com/search?entity=song&limit=201&term=" + sys.argv[1]
    # )
    # data = response.json()
    # i = 1
    # for result in data["results"]:
    #     print(f"{i} {result["trackName"]}")
    #     i += 1


if __name__ == "__main__":
    main()
