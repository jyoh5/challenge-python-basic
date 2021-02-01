import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

html = requests.get(alba_url)
soup = BeautifulSoup(html.text, "html.parser")
super_brand = soup.find("div", {"id":"MainSuperBrand"})
goods_box = super_brand.find("ul", {"class":"goodsBox"})
goods_box_info_arr = goods_box.findAll("li")

company_info = {}

for goods_box_info in goods_box_info_arr:
  brands = goods_box_info.findAll("a",{"class":"brandHover"})
  for brand in brands:
    company = brand.find("span",{"class":"company"}).find("strong").string
    company_info[company] = brand["href"]


for company_name, company_url in company_info.items():
  if "/" in company_name:
    company_name = company_name.replace("/","_")
  if " " in company_name:
    company_name = company_name.replace(" ","_")
  print(f"now: {company_name} → {company_url}")

  html = requests.get(company_url)
  soup = BeautifulSoup(html.text, "html.parser")
  normal_info = soup.find("div",{"id":"NormalInfo"})
  tbody = normal_info.find("tbody")
  tr_arr = tbody.select("tr:not(.summaryView)")
  
  # paging = normal_info.find("a",{"class":"prev"})
  # print(paging)
  # print(normal_info)
  # location = paging.find("span",{"class":"location"}).text
  # print(location)
  
  try:
    with open(f"{company_name}.csv", "w") as f:
      writer = csv.writer(f)
      writer.writerow(["local","company","work_time","pay_icon","pay_number","reg_date"])

      for tr in tr_arr:
        local = tr.find("td",{"class":"local"}).text
        company = tr.find("td",{"class":"title"}).find("span",{"class":"company"}).string
        # tmp_dict["title"] = tr.find("td",{"class":"title"}).find("span",{"class":"title"}).string
        work_time = tr.find("td",{"class":"data"}).find("span").string
        pay_icon = tr.find("td",{"class":"pay"}).find("span",{"class":"payIcon"}).string
        pay_number = tr.find("td",{"class":"pay"}).find("span",{"class":"number"}).string
        reg_date = tr.find("td",{"class":"regDate"}).string
        
        writer.writerow([local,company,work_time,pay_icon,pay_number,reg_date])
  except AttributeError:
    print(f"\t→ 데이터 없음")

  
  
