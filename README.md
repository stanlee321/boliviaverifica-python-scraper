# WebScraper BoliviaVerifica

This bot downloads the blog post from the page  `https://boliviaverifica.bo` .

It works following the pipeline:

* Download the links to the posts
* With the links to the posts, dowloads the info from each blog posts (Title, sub title, body texts and images)
  

## Setup 
It works using python 3.7+ `pip install -r requirements.txt`

## Run 

`python main.py`

## Results

There are files `3_links.csv` `4_links.csv` `5_links.csv` which are files created the the step one in the pipeline.

You can follow the second step in the pipeline in a video created by me in my facebook page here:

`https://www.facebook.com/stanley.salvatierra/videos/10225308030829819`

Where I downloaded the rest of the information.


## TODOS

* Create DB connection and schema for the downloaded data.
* Merge the pipeline procedures
* Create Docker container 