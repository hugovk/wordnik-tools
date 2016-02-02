#!/usr/bin/env python
# encoding: utf-8
"""
Make a citation for Wordnik.

1. Formats the citation input into a comment marked up with HTML
2. Asks to add to Wordnik
3. If you do, automatically adds it to the list
4. Wordnik has no API to add comments, so copies the citation to the clipboard
   and opens the word's page so you can manually paste it into the comment box
5. Asks to save the cited URL to the Internet Archive because linkrot
"""
from __future__ import print_function, unicode_literals
import argparse
from sys import platform as _platform
from dateutil.parser import parse  # pip install python-dateutil
from dateutil.relativedelta import relativedelta

import datetime
import re
import subprocess
import sys
import webbrowser


# https://github.com/hugovk/word-tools/blob/master/word_tools.py
import word_tools

# from pprint import pprint


# Windows cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def write_to_clipboard(text):

    if _platform == "darwin":
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
    elif _platform == "win32":
        from Tkinter import Tk
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.destroy()
        print("Copied to clipboard")
    else:
        print(_platform + " not yet supported for clipboard")


# http://stackoverflow.com/a/3041990/724176
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def today_timestamp():
    """Return a string like 14 December 2015"""
    import time
    return time.strftime('%d %B %Y')


def parse_now_or_past(timestr):
    """Parse a timestring. If no year given, return a date that's today or in
    the past"""
    indate = parse(timestr, dayfirst=True, yearfirst=False)
    indate = indate.date()
    now = datetime.datetime.now().date()
    # In the future?
    if indate > now:
        # Subtract a year
        indate += relativedelta(years=-1)
    return indate


def validate_date(timestr):
    """Take an input date string, validate and perhaps add year,
    and return a string like 14 December 2015"""
    date = parse_now_or_past(timestr)
    return date.strftime('%d %B %Y')


def embolden(word, quote):
    """Make word bold in quote, regardless of but maintaining case"""
    return re.sub(r"(" + word + r")", r"<b>\1</b>", quote, flags=re.I)


def source_from_url(url):
    """Get the source form the URL"""
    if "theguardian.com" in url:
        return "The Guardian"
    elif "washingtonpost.com" in url:
        return "Washington Post"
    elif "bikeradar.com" in url:
        return "BikeRadar"
    elif url.startswith("https://twitter.com"):
        username = url.lstrip("https://twitter.com")
        first_slash = username.index("/")
        username = username[:first_slash]
        return "@" + username
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make a citation for Wordnik.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'word',
        help="Word to cite, will be bolded if found in quote")

#     parser.add_argument('url', nargs='+', help="Quotation link")

    parser.add_argument(
        '-p', '--pos', default="n.",
        help="Part-of-speech, e.g. n. adj.")
    parser.add_argument(
        '--defn',
        help="A definition")
    parser.add_argument(
        '-q', '--quote', type=lambda s: unicode(s, 'utf8'),
        help="Quotation snippet")
    parser.add_argument(
        '-s', '--source',
        help="Quotation source")
    parser.add_argument(
        '-sr', '--source_roman', action='store_true',
        help="Quotation source in roman (i.e. not italic)?")
    parser.add_argument(
        '-d', '--date',
        help="Quotation date. Default: today.")
    parser.add_argument(
        '-u', '--url',
        help="Quotation link")
    parser.add_argument(
        '-l', '--list', default="new-to-me--2016",
        help="Permalink of the Wordnik list to post to")
    args = parser.parse_args()

    # Format a little something like this:

    # <b>spinning rust</b>, <i>n.</i> A computer hard disk, specifically one
    # using magnetic storage, as opposed to a solid-state drive (SSD).

    # <a href="https://twitter.com/wiredfool/status/577541476214706176">erics,
    # 16 March 2015</a>:

    # <blockquote>Apparently it wrote those 11gigs _after_ I moved 10 gigs of
    # email archives to <b>spinning rust</b> this morning.</blockquote>

    print()

    if args.url and not args.source:
        args.source = source_from_url(args.url)

    # Line 1
    text = ''
    line = ''
    if args.word:
        line += '<b>' + args.word + '</b>'
    if args.pos:
        if len(line) > 0:
            line += ', '
        line += '<i>' + args.pos + '</i>'
    if args.defn:
        if len(line) > 0:
            line += ' '
        line += args.defn
    if len(line) > 0:
        print(line)
        print()
        text += line + "\n\n"

    # Line 2
    line = ''
    if args.url:
        line += '<a href="' + args.url + '">'
    if args.source:
        if args.source_roman:
            line += args.source
        else:
            line += '<i>' + args.source + '</i>'
    if args.date:
        line += ', ' + validate_date(args.date)
    else:
        line += ', ' + today_timestamp()
    if args.url:
        line += '</a>'
    if len(line) > 0:
        line += ':'
        print(line)
        print()
        text += line + "\n\n"

    # Line 3
    line = ''
    if args.quote:
        quote = args.quote
        if args.word:
            quote = embolden(args.word, quote)
        line = '<blockquote>' + quote + '</blockquote>'
        print(line)
        print()
        text += line + "\n\n"

    write_to_clipboard(text)

    if args.list:
        answer = query_yes_no(
            "Add '" + args.word + "' to " + args.list + " on Wordnik?",
            default="no")
        if not answer:
            sys.exit("Not posting")
        else:
            print("Post to Wordnik")
            word_tools.add_to_wordnik([args.word], args.list)

            url = "https://www.wordnik.com/words/" + args.word  # + "#discuss"
            print(url)
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible

    if args.url:
        answer = query_yes_no(
            "Save '" + args.url + "' to Internet Archive?",
            default="no")
        if not answer:
            sys.exit("Not saving")
        else:
            print("Save to Internet Archive")
            url = "http://web.archive.org/save/" + args.url
            print(url)
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


# End of file
