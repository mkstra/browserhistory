import pandas as pd
import numpy as np
# Include standard modules
import argparse
import sys
# Initiate the parser
from params import blacklist

# Read arguments from the command line

# stop_urls = ["chrome.google", "github.com", "tiktok.", "facebook.com", "roamresearch.com", ".pdf", 
# "amazon.", "airbnb.", "/video", "linkedin.", "libgen.", "google.com", 
# "file:///", "google.com", "duckduckgo.com", "twitter.com", "jitsi.", 
# "slack.com", "youtube.com", "reddit.com", "meet.", "/accounts", "/billing", "stackoverflow.com"]

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="csv location")
parser.add_argument("--visit_duration", help=" minimum seconds a url was -visited-?")

parser.add_argument("--hard", help=" thorough cleaning that uses web scraping information?")


def main():

    args = parser.parse_args()

    history = pd.read_csv(args.path or "out/data.csv")

    min_visit_duration = 200 or args.visit_duration
    print(len(history)," initial entries")

    url_mask = [np.sum([u in v for u in blacklist]) == 0 for v in history.url]
    len(history[url_mask])

    c = history[url_mask]
    not_homepage_mask = [True if len([_ for _ in url.split("/") if _]) > 2 else False for url in c.url ]

    cleaned = c[not_homepage_mask]
    cleaned = cleaned.drop_duplicates(subset=["url"])

    print(len(cleaned)," entries after removing stop urls and duplicates")
    
    cleaned = cleaned[cleaned.visit_duration > min_visit_duration]
    print(len(cleaned)," entries after removing sites with < ", min_visit_duration, " seconds visit_duration")

    cleaned.to_csv("out/cleaned.csv", index = False, header=True)



if __name__ == "__main__":
   main()
