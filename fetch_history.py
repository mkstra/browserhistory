#!/usr/bin/env python
import sqlite3
import pandas as pd
import sys, getopt
import datetime
import os


#IF you get "database is locked" -> close Chrome / Brave browser
def convertChromeTime(ms):
    """Convert the amount of microsends into a datetime object. 
    Google chrome doesn't use Unix epoch.
    """
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ms)


def main(user, browser="chrome", os="mac"):
    browser_data = "BraveSoftware/Brave-Browser" if browser == "brave" else "Google/Chrome"
    # TODO avoid hardcoded path
    path = "/Users/{user}/Library/Application Support/{browser_data}/Default/History".format(user=user, browser_data=browser_data)
    
    if (os=="windows"):
        browser_data = "BraveSoftware\Brave-Browser" if browser == "brave" else "Google\Chrome"
        path = r'C:\Users\{user}\AppData\Local\{browser_data}\User Data\Default\History'.format(user=user, browser_data=browser_data)

    #path = "/home/{user}/.config/chromium/Default/History".format(user=user, data=browser_data)
    print("...getting history data from ", path)
    conn = sqlite3.connect(path)

    query = "SELECT urls.url, urls.title, visit_time, visit_duration, transition, visit_count FROM visits INNER JOIN urls on urls.id = visits.url"
    visitAndURLs = pd.read_sql_query(query, conn)
    df = visitAndURLs


    df['visit_duration'] = df['visit_duration'].apply(lambda x: x/1000000.) # convert into seconds
    df['visit_time'] = df['visit_time'].apply(convertChromeTime)
    
    df["name"] = user 
    print(df[:5])
    outname = 'data.csv'
    outdir = './out'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)
    df.to_csv (fullname, index = False, header=True)

#df = pd.read_sql_query("select * from urls", conn)
if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2], sys.argv[3] if 3 < len(sys.argv) else None)
