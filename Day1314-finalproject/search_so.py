import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  html = requests.get(url)
  soup = BeautifulSoup(html.text, "html.parser")
  pagination = soup.find("div",{"class":"s-pagination"})
  if pagination:
    last_page = pagination.find_all("a")
    last_page = int(last_page[-2].find("span").string)
  else:
    last_page = -1
  return last_page


def get_job_info(html):
  title = html.find("a",{"class","s-link stretched-link"})["title"]
  region = html.find("h3",{"class","fc-black-700"}).find_all("span")
  company = region[0].get_text(strip=True)
  region = region[1]
  if region:
    region = region.get_text(strip=True)
  else:
    region = None
  job_id = html["data-jobid"]
  detail_link = f"https://stackoverflow.com/jobs/{job_id}"
  apply_link = f"https://stackoverflow.com/jobs/apply/{job_id}"
  return {"title":title, "company":company, "region":region, "detail_link":detail_link, "apply_link":apply_link}
  

def collect_job_info(url, last_page):
  print("Scrapping stackoverflow")
  jobs = []
  for page in range(last_page):
    print(f"page {page+1}")
    html = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(html.text, "html.parser")
    boxes = soup.find_all("div",{"class":"-job"})
    for box in boxes:
      job = get_job_info(box)
      jobs.append(job)
  return jobs


def get_jobs_so(word):
  URL= f"https://stackoverflow.com/jobs?r=true&q={word}"
  last_page = get_last_page(URL)
  if last_page != -1:
    jobs = collect_job_info(URL, last_page)
  else:
    jobs = []
  return jobs
