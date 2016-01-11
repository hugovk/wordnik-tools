#!/usr/bin/env python
# encoding: utf-8
"""
Download comments (from a user) on a word (or list thereof).
Scrapes because no comment fetching via API.
"""
from __future__ import print_function
import argparse
import urllib2
import sys
from bs4 import BeautifulSoup, Comment  # pip install BeautifulSoup4
from urlparse import urljoin  # Python 2
from urllib import quote


def fix_relative_links(soup, base_url):
    """ Change all relative links to absolute links """
    a_tags = soup.find_all("a", href=True)
    for a in a_tags:
        if a['href'].startswith("/"):
            a['href'] = urljoin(base_url, a['href'])
    return soup


def scrape_word_comments(slug, user=None):
    # """Scrape a Wordnik word and return a list of comments"""
    found = []

    url = "https://wordnik.com/words/" + quote(slug.encode('utf8'), safe="")
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")

    ul_comments = soup.find(id="commentsOnWord")
    li_comments = ul_comments.find_all("li", class_="comment")

    for comment in li_comments:
        if user:
            span_author = comment.find_all("span", class_="author")[0]
            a = span_author.find_all("a", href=True)[0]
            if not "/users/" + user == a['href'].lower():
                continue

        body = comment.find_all("div", class_="body")[0]
        # Remove some bits
        for a in body.findAll("a", "report_comment"):
            a.extract()
        # Remove HTML comments:
        # <!-- you won't flag your own comments as spam -->
        for html_comment in body.findAll(text=lambda text: isinstance(
                text, Comment)):
            html_comment.extract()

        body = fix_relative_links(body, "https://www.wordnik.com")

        found.append(body)
    return found


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download comments (from a user) on a word (or list).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-w', '--word',
        help="Word slug, eg. spinning%%20rust for "
             "https://wordnik.com/words/spinning%%20rust")
    parser.add_argument(
        '-l', '--list',
        help="List slug, eg. new-to-me--2015 for "
             "https://wordnik.com/lists/new-to-me--2015")
    parser.add_argument(
        '-u', '--user',
        help="Restrict to this user",
        default="hugovk")
    parser.add_argument(
        '-o', '--outfile',
        help="Save to this file. Default: <slug>.txt")
    args = parser.parse_args()

    if args.word and args.list:
        sys.exit("Please give just a word or list, not both")
    elif not args.word and not args.list:
        sys.exit("Please give a word or list")

    if args.word:
        words = [args.word]

    if args.list:
        from wordnik_list_scraper import scrape_list, sort_words
        words = scrape_list(args.list)
        words = sort_words(words)

    comments = []
    for word in words:
        new_comments = scrape_word_comments(word, args.user)
        comments.extend(new_comments)
        for comment in new_comments:
            print(comment)

    # word_string = '\n'.join(words)
    # print(word_string)
    # if not args.outfile:
        # args.outfile = args.permalink + ".txt"
    # with open(args.outfile, 'w') as f:
        # f.write(word_string)

# End of file
