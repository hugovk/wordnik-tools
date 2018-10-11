#!/usr/bin/env python
# encoding: utf-8
"""
Download a Wordnik list to a text file.
Note: API only allows access to your own lists,
so use wordnik_list_scraper.py for others' lists.
"""
from __future__ import print_function
import argparse
import sys
import yaml
from wordnik import swagger, AccountApi, WordListApi

# from pprint import pprint


def get_wordnik_token(username, password):
    account_api = AccountApi.AccountApi(wordnik_client)
    result = account_api.authenticate(username, password)
    token = result.token
    # print("Your Wordnik token is: " + token)
    return token


def load_yaml(filename):
    """
    File should contain:
    wordnik_username: TODO_ENTER_YOURS
    wordnik_password: TODO_ENTER_YOURS
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
        "wordnik_username",
        "wordnik_password",
        "wordnik_api_key",
    }:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def download_list(permalink, token):
    """Download a Wordnik list and return a list of words"""
    results = wordlist_api.getWordListWords(permalink, token)
    words = []
    for result in results:
        words.append(result.word)
        # print(dir(result))
        # print("word:\t", result.word)
        # print("createdAt:\t", result.createdAt)
        # print("numberCommentsOnWord:\t", result.numberCommentsOnWord)
        # print("numberLists:\t", result.numberLists)
        # print("userId:\t", result.userId)
        # print("username:\t", result.username)
    return words


def sort_words(word_list):
    """Case-insensitive sort"""
    return sorted(words, key=lambda s: s.lower())


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
        "-y",
        "--yaml",
        default="M:\\bin\\data\\wordnik.yaml",
        help="YAML file location containing Wordnik API key",
    )
    parser.add_argument(
        "-o", "--outfile", help="Save to this file. Default: <permalink>.txt"
    )
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)
    wordnik_client = swagger.ApiClient(
        credentials["wordnik_api_key"], "http://api.wordnik.com/v4"
    )
    wordlist_api = WordListApi.WordListApi(wordnik_client)
    token = get_wordnik_token(
        credentials["wordnik_username"], credentials["wordnik_password"]
    )

    words = download_list(args.permalink, token)
    words = sort_words(words)
    word_string = "\n".join(words)
    print(word_string)
    if not args.outfile:
        args.outfile = args.permalink + ".txt"
    with open(args.outfile, "w") as f:
        f.write(word_string.encode("utf-8"))

# End of file
