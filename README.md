## shakeup
This script computes the Kaggle leaderboard shakeup metric as given by BreakfastPirate in a [forum post](
https://www.kaggle.com/c/liberty-mutual-fire-peril/forums/t/10187/quantifying-leaderboard-shake-up).
The metric is essentially the mean absolute percentage change in rank for all entrants.
This script scrapes the data from the Kaggle website.
It returns values for the whole leaderboard and for the top 10% of finishers, either for a single leaderboard, of for a whole set of them.

### Usage
You can use this script with a single URL to get the shakeup for one competition or with a list of URLs in a file, 
one URL per line, to get results for a set of competitions. 
In either case, go the the leaderboard of the competition you want and copy the URL.
It will look something like this:    

    https://www.kaggle.com/c/liberty-mutual-fire-peril/leaderboard 

Note that it should not include any final /public or /private part.
The file urls.txt has a sample of three leaderboard urls in it.

    >>> python shakeup.py -h
    usage: shakeup.py [-h] (-u URL | -f FILE)
    
    Generates the shakeup metric for Kaggle leaderboards.
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     URL for a Kaggle LB, w/o the final /public or /private
      -f FILE, --file FILE  A file with a list of Kaggle LB URLs, with one URL per
                        line


