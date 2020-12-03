# News Crawler
This repo provides a utility for parsing [CommonCrawl News](https://commoncrawl.org/2016/10/news-dataset-available/) (a.k.a. CC-NEWS) files into a state ready for text analysis using Docker. 

This repo is mostly taken from the [RealNews](https://github.com/rowanz/grover/tree/master/realnews) repo part of [Grover repo](https://github.com/rowanz/grover) and adapted to use Docker. 

## Understanding CC-NEWS
CC-NEWS is the 'live' news version of the CommonCrawl (CC-MAIN). CC-MAIN provides a monthly slice of the internet, which is great, but monthly. CC-NEWS produces a file with news every 1-2 hours with a typical size of 1.2GB

Some issues (apart from size) arise from the warc format and the raw html format of the crawl. This repo helps to extract purely the text part of it. Results are stored directly into your s3 bucket of choice

For a sample result, consider the included `realnews_tiny.jsonl` file (also totally taken from the [Grover repo](https://github.com/rowanz/grover) btw.)



## Usage with Docker

Clone this repo, move to real_news folder, build the image
```
cd real_news
docker build --tag real_news .
```

Run on a selected file
```python
docker run news_crawl     
    -e AWS_ACCESS_KEY=[YOUR_ACCESS_KEY]     
    -e AWS_SECRET_KEY=[YOUR_SECRET_KEY]    
    python real_news.py 
    --path crawl-data/CC-NEWS/YYYY/MM/FILE_NAME 
    --bucket_name [YOUR_S3_TARGET_BUCKET]
```

For example for the file `CC-NEWS-20201015155253-00179.warc.gz`
```python
docker run real_news
     -e AWS_ACCESS_KEY=my_super_access_key
     -e AWS_SECRET_KEY=my_super_secret_key
    python real_news.py
     --path crawl-data/CC-NEWS/2020/10/CC-NEWS-20201015155253-00179.warc.gz
     --bucket_name real-news
```

## Finding news files
Find a news file to parse. To find all the files on a given day, use

`aws s3 ls s3://commoncrawl/crawl-data/CC-NEWS/YYYY/MM/CC-NEWS-YYYYMMDD --no-sign-request`

Where DD, MM & YYYY are to be replaced with the desired days accordingly. For instance, the following call

`aws s3 ls s3://commoncrawl/crawl-data/CC-NEWS/2020/10/CC-NEWS-20201015 --no-sign-request` yields a list of 18 files, for the day:
```python
[DATE]     [TIME]   [FILE_ID]  [FILE_NAME]
2020-10-15 05:05:03 1072702920 CC-NEWS-20201015011026-00168.warc.gz
2020-10-15 07:05:03 1072729221 CC-NEWS-20201015032129-00169.warc.gz
[...]
2020-10-16 02:05:03 1072726498 CC-NEWS-20201015225649-00185.warc.gz
```