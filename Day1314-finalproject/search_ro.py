import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def get_job_info(html):
  title = html.find("h2",{"itemprop":"title"}).get_text(strip=True)
  company = html.find("h3",{"itemprop":"name"}).get_text(strip=True)
  region = html.find("div",{"class":"location"})
  if region:
    region = region.get_text(strip=True)
  else:
    region = None
  detail_link = html["data-id"]
  detail_link = f"https://remoteok.io/remote-jobs/{detail_link}"
  r = requests.get(detail_link, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")
  apply_link = soup.find("a",{"class":"action-apply"})
  if apply_link:
    apply_link = apply_link["href"]
  else:
    apply_link = None
  return {"title":title, "company":company, "region":region, "detail_link":detail_link,"apply_link":apply_link}

def collect_job_info(url):
  print("Scrapping remoteok")
  jobs = []
  html = requests.get(url, headers=headers)
  soup = BeautifulSoup(html.text, "html.parser")
  tr_list = soup.select("tr.job:not(.closed)")
  for tr in tr_list:
    job = get_job_info(tr)
    jobs.append(job)
  return jobs


def get_jobs_ro(word):
  URL= f"https://remoteok.io/remote-dev+{word}-jobs"
  jobs = collect_job_info(URL)
  return jobs
