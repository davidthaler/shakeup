'''
Script computes the Kaggle leaderboard shakeup metric as given by BreakfastPirate at:
https://www.kaggle.com/c/liberty-mutual-fire-peril/forums/t/10187/quantifying-leaderboard-shake-up
It returns values for the whole leaderboard and for the top 10% of finishers.

To run this, go to Kaggle and bring up the leaderboard you want. 
The URL will look like:
https://www.kaggle.com/c/challenges-in-representation-learning-the-black-box-learning-challenge/leaderboard

Use that (as a string) as the url_root argument to shakeup(). 
author: David Thaler
'''
import math
import argparse
from collections import namedtuple
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

Result = namedtuple('Result', 'shakeup_all shakeup_top10pct')

def get_data(url):
    '''
    Scrapes Kaggle to get data from leaderboards

    Params:
      url: the whole url to the LB

    Returns:
      a Pandas data frame with the places, team ids and team names taken from the LB.
    '''
    raw_html = requests.get(url)
    parsed_html = bs(raw_html.content)
    data = [(int(tag.select('td.leader-number')[0].text), 
             tag.attrs['id']) 
             for tag in parsed_html.find_all('tr', id=True)]
    out = pd.DataFrame(data, columns=['place', 'id'])
    return out

def shakeup(url_root):
    '''
    Computes the shakeup between the final public and private leaderboards 
    for Kaggle competitions. Data is scraped from Kaggle.

    Params:
      url_root: the LB url not including the trailing /public or /private part 

    Returns:
      a namedtuple with the shakeup for the whole LB and the top 10% 
    '''
    pvt_url = url_root + '/private'
    pub_url = url_root + '/public'

    pvt_data = get_data(pvt_url)
    pub_data = get_data(pub_url)

    all_data = pvt_data.merge(pub_data, on='id', suffixes=('_pvt', '_pub'))
    shake = all_data.place_pvt - all_data.place_pub
    shake_all = shake.abs().mean() / len(shake)
    cut = math.floor(0.1 * len(shake))
    shake_top = shake[:cut].abs().mean() / len(shake)
    return Result(shake_all, shake_top)


def load_all(urls):
    '''
    Takes an iterable of Kaggle LB URLs and computes the shakeup for each one.

    Params:
      urls: iterable of LB URLs, without the final /public or /private part

    Returns:
      a Pandas data frame with the competition name and LB shakeup
    '''
    # TODO: should be a for-loop so that we can handle exceptions per-item
    # TODO: we need the competition names...they are in the url
    return pd.DataFrame([shakeup(url.strip()) for url in urls], 
                columns=['shakeup_all', 'shakeup_top_10%'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates the shakeup metric for Kaggle leaderboards.')
    arg_group = parser.add_mutually_exclusive_group(required=True)
    arg_group.add_argument('-u', '--url', 
            help='URL for a Kaggle LB, w/o the final /public or /private')
    arg_group.add_argument('-f', '--file',
            help='A file with a list of Kaggle LB URLs, with one URL per line')
    args = parser.parse_args()

    # TODO: add exception handling
    if args.url is not None:
        print(shakeup(args.url))
    else:
        with open(args.file) as fp:
            print(load_all(fp))