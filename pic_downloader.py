#!/usr/bin/env python3

__author__ = "Jay Castleberry - jcastleberry31@gatech.edu"
__version__ = "1.0.0"
__license__ = "MIT"

import requests
import shutil
import pprint
import os
import platform
from time import sleep


def nasa_pic_downloader():
    terminal_size = shutil.get_terminal_size(fallback=(80, 20))
    term_col_size = terminal_size.columns
    pp = pprint.PrettyPrinter(indent=4, depth=2, width=term_col_size)
    term_middle = (term_col_size - 34) / 2
    try:
        spacer = " " * int(term_middle)
    except Exception:
        spacer = "          "

    def clear_screen():
        found_os = platform.system()
        win_os = 'Windows'
        if found_os is win_os:
            os.system('cls')
        else:
            os.system('clear')

    clear_screen()

    print('\n')
    print("X" * term_col_size)
    print(f"{spacer}NASA PICTURE OF THE DAY DOWNLOADER{spacer}")
    print("X" * term_col_size)
    print('\n')

    def get_request(url):
        sleep(1)
        r = requests.get(url)
        pp.pprint(f"""Status Code: {r.status_code}""")
        pp.pprint(f"""Request Headers: {r.headers}""")
        pp.pprint(f"""Request JSON: {r.json()}""")
        return r.json()

    def get_pic(d):
        print('\n')
        date_object = d
        pp.pprint("***************************************")
        pp.pprint(f"""Sending NASA API Request for {str(date_object)}""")
        pp.pprint("***************************************")
        print('\n')
        api_url = f"""https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={date_object}"""
        try:
            pic = get_request(api_url)
            print('\n')
            pp.pprint(f"""DATE: {pic["date"]}""")
            pp.pprint(f"""TITLE: {pic["title"]}""")
            pp.pprint("EXPLANATION:")
            pp.pprint(pic["explanation"])
        except (requests.exceptions.RequestException, KeyError, Exception) as e:
            pp.pprint(f"""ERROR: {e}""")
            pp.pprint("EXITING PROGRAM")
            raise SystemExit()

        def downloader(url, date):
            resp = requests.get(url, stream=True)
            file = f"""nasa_apod_{date}.jpg"""
            local_file = open(file, 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)
            del resp

        # determine link for pic, get HD if available
        if "hdurl" in pic:
            download_url = pic["hdurl"]
            pp.pprint(f"""HD URL: {pic["hdurl"]}""")
            downloader(download_url, date_object)
        elif "url" in pic:
            download_url = pic["url"]
            pp.pprint(f"""URL: {pic["url"]}""")
            downloader(download_url, date_object)
        else:
            pp.pprint("!!! NO DOWNLOAD URL FOR THIS DATE !!!")

    # Dates to download
    dates = ["2020-08-13",
             "2020-08-12"]

    # Generator loops through list of dates and downloads the pic for each
    [get_pic(d) for d in dates]
    print('\n' * 2)
    pp.pprint("ALL PICTURES SUCCESSFULLY DOWNLOADED - EXITING")
    print('\n' * 2)


if __name__ == "__main__":
    nasa_pic_downloader()
    SystemExit()
