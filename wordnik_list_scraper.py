#!/usr/bin/env python3
# encoding: utf-8
"""
Download a Wordnik list to a text file.
Scrapes because API only allows access to your own lists.
"""
import argparse

from bs4 import BeautifulSoup  # pip install BeautifulSoup4
from urllib.request import urlopen

from pprint import pprint


def scrape_list(permalink):
    # """Scrape a Wordnik list and return a list of words"""
    url = "https://wordnik.com/lists/" + permalink
    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")
    wordlist = soup.find(id="sortable_wordlist")
    words = wordlist.find_all("li", class_="word")

    # <h1 id="headword">Words new to me (2018) <span class="heart_quotes right loveOnly"></span></h1>

    title = soup.find("h1", id="headword").text.strip()

    # <li class="word"><a href="/words/thinhead">thinhead</a>
    #   <span class="popular" style="display:none">and appears on
    #       <a href="/words/thinhead#lists">2</a> lists</span>
    #   <span class="details">was added by
    #       <a href="/users/hernesheir">hernesheir</a> and appears on
    #       <a href="/words/thinhead#lists">2</a> lists</span>
    # </li>

    # pprint(words)
    found = []
    for word in words:
        if "hidden" not in word["class"]:
            found.append(word.find(text=True))

    return title, found


def sort_words(word_list):
    """Case-insensitive sort"""
    return sorted(word_list, key=lambda s: s.lower())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a Wordnik list to a text file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "permalink",
        help="Wordnik permalink, eg. cutthroats for "
        "http://wordnik.com/lists/cutthroats",
    )
    parser.add_argument(
        "-o", "--outfile", help="Save to this file. Default: <permalink>.txt"
    )
    args = parser.parse_args()

    title, words = scrape_list(args.permalink)
    print("# " + title + "\n\n")
    words = sort_words(words)
    word_string = "\n".join(words)
    print(word_string)
    if not args.outfile:
        args.outfile = args.permalink + ".txt"
    with open(args.outfile, "w") as f:
        f.write("# " + title + "\n\n")
        f.write(word_string)

# End of file
