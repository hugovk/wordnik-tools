#!/usr/bin/env python
# encoding: utf-8
"""
Download comments (from a user) on a word.
Scrapes because no comment fetching via API.
"""
from __future__ import print_function
import argparse
import urllib2
from urlparse import urljoin  # Python 2
from bs4 import BeautifulSoup, Comment  # pip install BeautifulSoup4


def fix_relative_links(soup, base_url):
    """ Change all relative links to absolute links """
    a_tags = soup.find_all("a", href=True)
    for a in a_tags:
        if a['href'].startswith("/"):
            a['href'] = urljoin(base_url, a['href'])
    return soup


def scrape_word_comments(slug, user=None):
    # """Scrape a Wordnik word and return a list of comments"""
    url = "https://wordnik.com/words/" + slug
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")

    ul_comments = soup.find(id="commentsOnWord")
    li_comments = ul_comments.find_all("li", class_="comment")

    found = []

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
        description="Download a Wordnik list to a text file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'slug',
        help="Word slug, eg. spinning%%20rust for "
             "https://www.wordnik.com/words/spinning%%20rust")
    parser.add_argument(
        '-u', '--user',
        help="Restrict to this user")
    parser.add_argument(
        '-o', '--outfile',
        help="Save to this file. Default: <slug>.txt")
    args = parser.parse_args()

    comments = scrape_word_comments(args.slug, args.user)

    for comment in comments:
        print(comment)

    # word_string = '\n'.join(words)
    # print(word_string)
    # if not args.outfile:
        # args.outfile = args.permalink + ".txt"
    # with open(args.outfile, 'w') as f:
        # f.write(word_string)

# End of file
