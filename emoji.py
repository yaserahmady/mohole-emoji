#!/usr/bin/env python3

import json
import random
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
def index(input):
    return emojify(input)


def main():
    i = " ".join(sys.argv[1:])
    o = emojify(i)
    print(o)


def emojify(string):
    # Open the emoji→text mapping json
    with open("mappings.json") as json_file:
        data = json.load(json_file)
        alphabet = data["alphabet"]
        compounds = data["compounds"]

    # # Print mappings for debug purposes
    # for mapping in [compounds, alphabet]:
    # 	for text, emoji in mapping.items():
    # 		print(f'{text} = {"".join(emoji)}')

    # Convert the input string to UPPERCASE
    string = string.upper()

    # Replace compounds first
    for text, emoji in compounds.items():
        string = string.replace(text, emoji)

    # Replace single letters
    for text, emoji in alphabet.items():

        for letter in list(string):
            if type(emoji) is list:
                string = string.replace(
                    text, random.choice(emoji), 1
                )  # 3rd arg is `count` (optional) - the number of times you want to replace the old substring with the new substring

            elif type(emoji) is str:
                string = string.replace(text, emoji)

    # Make spaces more visible
    string = string.replace(" ", "   ")

    return string


if __name__ == "__main__":
    main()
