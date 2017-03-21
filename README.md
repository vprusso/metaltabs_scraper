# metaltabs_scraper

Python script to determine guitar tunings of songs from <a href="http://metaltabs.com/index.html">metaltabs.com</a>.

## Overview

In the command line, run:

`python metal_tabs_scrapy.py` 

The script will then go to metaltabs.com and process each guitar tab file and attempt to determine the guitar tuning. The band name, song name, and attempted tuning type will be saved in a text file. 

A previously scraped and cleaned CSV file is included in the repo under the name `metal_tunings_cleaned.csv`. 

For more information, consult the blog post <a href="http://vprusso.github.io/blog/2017/the-most-metal-guitar-tuning/">here.</a>

## Dependencies

1. Python 3.
2. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).
