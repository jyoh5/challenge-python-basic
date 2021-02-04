# import requests
from flask import Flask, render_template, request
# from bs4 import BeautifulSoup
from scrapper import get_data

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

db = {}

app = Flask("DayEleven")

@app.route("/")
def home():
  return render_template("home.html", subreddits=subreddits)

@app.route("/read")
def read():
  result = []
  sub_arr = []
  for subreddit in subreddits:
    if request.args.get(subreddit):
      sub_arr.append(subreddit)
      if db.get(subreddit) == None:
        url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
        db[subreddit] = get_data(url, subreddit)
      result.extend(db.get(subreddit))
      
  result = sorted(result, key=(lambda x: x['bote_count']), reverse=True)    

  return render_template("read.html", reddit_data={'data': result, 'sub_arr':sub_arr})


app.run(host="0.0.0.0")