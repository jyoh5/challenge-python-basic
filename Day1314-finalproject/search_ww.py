import requests
from bs4 import BeautifulSoup

def get_job_info(html):
  title = html.find("span",{"class","title"}).string
  company = html.find("span",{"class","company"}).string
  region = html.find("span",{"class","region"})
  if region:
      region = region.get_text(strip=True)
  else:
    region = None
  detail_link = html.find("a", recursive=False)["href"]
  detail_link = f"https://weworkremotely.com{detail_link}"
  r = requests.get(detail_link)
  soup = BeautifulSoup(r.text, "html.parser")
  apply_link = soup.find("a",{"id":"job-cta-alt-2"})
  if apply_link:
    apply_link = apply_link["href"]
  else:
    apply_link = None
  return {"title":title, "company":company, "region":region, "detail_link":detail_link, "apply_link":apply_link}

def collect_job_info(url):
  print("Scrapping weworkremotely")
  jobs = []
  html = requests.get(url)
  soup = BeautifulSoup(html.text, "html.parser")
  boxes = soup.find_all("li",{"class":"feature"})
  for idx, box in enumerate(boxes):
    job = get_job_info(box)
    jobs.append(job)
  return jobs


def get_jobs_ww(word):
  URL= f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = collect_job_info(URL)
  return jobs
