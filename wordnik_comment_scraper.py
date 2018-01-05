#!/usr/bin/env python
# encoding: utf-8
"""
Download comments (from a user) on a word (or list thereof).
Scrapes because no comment fetching via API.
"""
from __future__ import print_function, unicode_literals

import argparse
import sys

from bs4 import BeautifulSoup, Comment  # pip install BeautifulSoup4

try:
    # Python 3
    from urllib.parse import quote, urljoin
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib import quote
    from urllib2 import urlopen
    from urlparse import urljoin


def print_html_header(user, slug, title, subtitle):
    print("""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">""")
    if title:
        print("    <title>{}</title>".format(title))
    print("""    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
""")
    if title:
        print("<h1>{}</h1>".format(title))
        print("")
    if subtitle:
        print("<h2>{}</h2>".format(subtitle))
        print("")
    if user and slug:
        print("""<h3>Compiled<br>by<br><a
        href="https://www.wordnik.com/users/{user}">{user}</a><br>on
        <br><a href="https://www.wordnik.com/lists/{slug}"><img
        alt="Wordnik" src="wordnik.png" width="100"></h3>
""".format(user=user, slug=slug, title=title, subtitle=subtitle))


def print_html_footer():
    print("""
  </body>
</html>""")


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
    page = urlopen(url)
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
        help="List slug, eg. new-to-me--2017 for "
             "https://wordnik.com/lists/new-to-me--2017")
    parser.add_argument(
        '-u', '--user',
        help="Restrict to this user",
        default="hugovk")
    parser.add_argument(
        '-t', '--title',
        help="Title for HTML output",
        default="New to me (2017)")
    parser.add_argument(
        '-s', '--subtitle',
        help="Subtitle for HTML output",
        default="A Lexicon<br>of Newish Words<br>"
                "That Caught My Eye<br>in 2017")
#     parser.add_argument(
#         '-o', '--outfile',
#         help="Save to this file. Default: <slug>.txt")
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

    print_html_header(args.user, args.list, args.title, args.subtitle)

    print('<ul class="index">')
    for word in words:
        w = word.encode("utf-8")
        print('<li><a href="#{}">{}</a>'.format(w, w))
    print('</ul>')

    for word in words:
        w = word.encode("utf-8")
        print('<div id="{}">'.format(w))
        new_comments = scrape_word_comments(word, args.user)
        comments.extend(new_comments)
        for comment in new_comments:
            print(comment)
        print('</div>')

    print_html_footer()

#     word_string = '\n'.join(words)
#     print(word_string)
#     if not args.outfile:
#         args.outfile = args.permalink + ".txt"
#     with open(args.outfile, 'w') as f:
#         f.write(word_string)

# End of file
