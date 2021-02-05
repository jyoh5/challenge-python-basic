import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def get_data(url, subreddit):
  html = requests.get(url, headers=headers)
  soup = BeautifulSoup(html.text, "html.parser")
  post_list = soup.find_all("div",{"class":"_1oQyIsiPHYt6nx7VOmd1sz"})

  result = []
  print(url)

  for idx, post in enumerate(post_list):
    bote_count = post.find("div",{"class":"_1rZYMD_4xY3gRcSS3p8ODO"})
    # promoted = post.find("span",{"class":"_2oEYZXchPfHwcf9mTMGMg8"})
    title = post.find("h3",{"class":"_eYtD2XCVieq6emjKBH3m"})
    link = post.find("a",{"class":"_13svhQIUZqD9PVzFcLwOKT"})
    
    try:
      tmp = {}
      tmp["subreddit"] = subreddit
      if bote_count:
        bc = bote_count.text
        if bc[-1] == "k":
          bc = float(bc[:-1])*1000
        tmp["bote_count"] = int(bc)
      else:
        tmp["bote_count"] = 0
      # if promoted:
      #   tmp["promoted"] = promoted
      if title:
        tmp["title"] = title.text
      if link:
        tmp["link"] = link["href"]
      result.append(tmp)
    except TypeError:
      pass
    except ValueError:
      pass
  return result