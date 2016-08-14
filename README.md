## shakeup
This script computes the Kaggle leaderboard shakeup metric as given by BreakfastPirate in a [forum post](
https://www.kaggle.com/c/liberty-mutual-fire-peril/forums/t/10187/quantifying-leaderboard-shake-up).
The metric is essentially the mean absolute percentage change in rank.
This script scrapes the data from the Kaggle website.
It returns values for the whole leaderboard and for the top 10% of finishers, either for a single leaderboard, of for a whole set of them.

### Usage
    >>> python shakeup.py -h
    usage: shakeup.py [-h] (-u URL | -f FILE)
    
    Generates the shakeup metric for Kaggle leaderboards.
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     URL for a Kaggle LB, w/o the final /public or /private
      -f FILE, --file FILE  A file with a list of Kaggle LB URLs, with one URL per
                        line


