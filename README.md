## shakeup
During Kaggle competitions, a public leaderboard is available for competitors to see about how they doing.
It is computed from a subset of the test data.
To prevent overfitting to this data, the final competition results are based on a disjoint subset of the test data.
Consequently, the final standings are somewhat different than the last standings shown on the 
leaderboard during the competition.
This difference is called the 'shakeup' and it gives an indication of the stability of the models entered 
in the competition, and whether they have overfitted the public leaderboard. 

### shakeup.py
This script computes the Kaggle leaderboard shakeup metric as given by BreakfastPirate in a [forum post](
https://www.kaggle.com/c/liberty-mutual-fire-peril/forums/t/10187/quantifying-leaderboard-shake-up).
The metric is essentially the mean absolute percentage change in rank for all entrants.
This script scrapes the data from the Kaggle website.
It returns values for the whole leaderboard, for the top 10% of finishers and the Spearman Rank Correlation, 
either for a single leaderboard, of for a whole set of them.


### Dependencies
This script requires Requests, BeautifulSoup and Pandas.
Due to a parsing problem in BeautifulSoup under Python 2.x, 
you will need html5lib if you are using Python 2.x.

### Usage
You can use this script with a single URL to get the shakeup for one competition or with a 
list of URLs in a file, one URL per line, to get results for a set of competitions. 
In either case, go the the leaderboard of the competition you want and copy the URL.
It will look something like this:    

    https://www.kaggle.com/c/liberty-mutual-fire-peril/leaderboard 

Note that it should not include any final /public or /private part.

#### File example
The file urls.txt has a sample of three leaderboard urls in it.

    >>> python shakeup.py -f urls.txt
    Loading liberty-mutual-fire-peril
    Loading walmart-recruiting-store-sales-forecasting 
    Loading challenges-in-representation-learning-the-black-box-learning-challenge
                                    competition_name  shakeup_all  \
    0                          liberty-mutual-fire-peril     0.072486   
    1         walmart-recruiting-store-sales-forecasting     0.007158   
    2  challenges-in-representation-learning-the-blac...     0.010332   

       shakeup_top_10%  spearman_corr  
    0         0.066972       0.938846  
    1         0.005831       0.998428  
    2         0.008576       0.998771  
    
#### Single URL example
Note that the URL should not include any final /public or /private part.

    >>> python shakeup.py -u https://www.kaggle.com/c/liberty-mutual-fire-peril/leaderboard
                       comp name   shakeup  top 10% shakeup  Spearman corr
    0  liberty-mutual-fire-peril  0.072486         0.066972       0.938846


