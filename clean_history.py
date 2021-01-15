import pandas as pd
import numpy as np
# Include standard modules
import argparse
import sys
# Initiate the parser
from params import blacklist

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="csv location")
parser.add_argument("--visit_duration", help=" minimum seconds a url was -visited-?")

parser.add_argument("--hard", help=" thorough cleaning that uses web scraping information?")


def main(path, visit_duration):


    history = pd.read_csv(path or "out/data.csv")

    min_visit_duration = 120 or visit_duration
    print(len(history)," initial entries")

    legit_url = [np.sum([u in v for u in blacklist]) == 0 for v in history.url]

    c = history[legit_url]
    not_homepage_mask = [True if len([_ for _ in url.split("/") if _]) > 2 else False for url in c.url ]

    cleaned = c[not_homepage_mask]
    cleaned = cleaned.drop_duplicates(subset=["url"])

    print(len(cleaned)," entries after removing stop urls and duplicates")
    
    cleaned = cleaned[cleaned.visit_duration > min_visit_duration]
    print(len(cleaned)," entries after removing sites with < ", min_visit_duration, " seconds visit_duration")

    cleaned.to_csv("out/cleaned.csv", index = False, header=True)



if __name__ == "__main__":
    args = parser.parse_args()
    main(args.path, args.visit_duration)
