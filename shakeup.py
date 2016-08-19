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
import sys
import re
import math
import argparse
from collections import namedtuple
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

NAME_PATTERN = re.compile(r'c/(.*)/leaderboard')

Result = namedtuple('Result', 'competition_name shakeup_all shakeup_top10pct spearman_corr')

class LBParseError(Exception):
    '''Class indicates that no Kaggle Leaderboard was found at given URL'''
    pass

class LBNameError(Exception):
    '''Class indicates that given URL does not have correct format'''
    pass

def get_data(url):
    '''
    Scrapes Kaggle to get data from leaderboards

    Params:
      url: the whole url to the LB

    Returns:
      a Pandas data frame with the places, team ids and team names taken from the LB.
    '''
    response = requests.get(url)
    response.raise_for_status()
    # In Python 2, BeautifulSoup needs html5lib to parse long LBs correctly
    if sys.version_info.major == 2:
        try:
            parsed_html = bs(response.content, 'html5lib')
        except ImportError:
            raise ImportError('In Py2.7, html5lib is needed. See readme/module doc.')
    else:
        parsed_html = bs(response.content)
    data = [(int(tag.select('td.leader-number')[0].text), 
             tag.attrs['id']) 
             for tag in parsed_html.find_all('tr', id=True)]
    if len(data) == 0:
        raise LBParseError('Cannot find Kaggle LB at URL: %s' % url)
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
    cut = int(math.floor(0.1 * len(shake)))
    shake_top = shake[:cut].abs().mean() / len(shake)
    spearman = all_data.place_pvt.corr(all_data.place_pub, method='spearman')
    comp_name = get_name(url_root)
    return Result(comp_name, shake_all, shake_top, spearman)

def get_name(url):
    '''
    Gets the competition name from a full url.

    Params:
      url: a full url or base url
    
    Returns:
      the url part after /c/ and before /leaderboard
    '''
    names = re.findall(NAME_PATTERN, url)
    if len(names) == 0:
        raise LBNameError('Cannot extract name from URL: %s' % url)
    else:
        return names[0]

def load_all(urls):
    '''
    Takes an iterable of Kaggle LB URLs and computes the shakeup for each one.

    Params:
      urls: iterable of LB URLs, without the final /public or /private part

    Returns:
      a Pandas data frame with the competition name and LB shakeup
    '''
    results = []
    for url in urls:
        name = get_name(url)
        print('Loading %s' % name)
        try:
            results.append(shakeup(url.strip()))
        except LBParseError:
            print('Skipping %s. Cannot parse Kaggle LB at URL: %s' % (name, url))
        except requests.HTTPError:
            print('Skipping %s. Cannot load resource at URL: %s' % (name, url))
    return pd.DataFrame(results, columns=['competition_name', 
                'shakeup_all', 'shakeup_top_10%', 'spearman_corr'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates the shakeup metric for Kaggle leaderboards.')
    arg_group = parser.add_mutually_exclusive_group(required=True)
    arg_group.add_argument('-u', '--url', 
            help='URL for a Kaggle LB, w/o the final /public or /private')
    arg_group.add_argument('-f', '--file',
            help='A file with a list of Kaggle LB URLs, with one URL per line')
    args = parser.parse_args()
    if args.url is not None:
        out = shakeup(args.url)
        print(pd.DataFrame([out], 
            columns=['comp name', 'shakeup', 'top 10% shakeup', 'Spearman corr']))
    else:
        with open(args.file) as fp:
            print(load_all(fp))
