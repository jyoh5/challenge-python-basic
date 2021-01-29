import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

rq_result = requests.get(url)
parsed_result = BeautifulSoup(rq_result.text, "html.parser")

table = parsed_result.find("table", {"class":"tablesorter"})
tbody = table.find("tbody")
trs = tbody.find_all("tr")

code_arr = []
for tr in trs:
  skip_flag = True
  country, code = "", ""
  for idx, td in enumerate(tr.find_all("td")):
    if idx == 1 and td.string == "No universal currency":
      skip_flag = False
      break
    elif idx == 0:
      country = td.string
    elif idx == 2:
      code = td.string
  if skip_flag:
    code_arr.append([country, code])

code_sorted_arr = sorted(code_arr, key=(lambda x: x[0]))


print("Hi! Please select a country by number.")
for idx, code in enumerate(code_sorted_arr):
  print(f"# {idx}: {code[0]}")

input_flag = True
while(input_flag):
  user_input = input("\nselect a number: ")
  try:
    user_idx = int(user_input)
    if user_idx < len(code_sorted_arr):
      print(f"contry: \t\t{code_sorted_arr[user_idx][0]}")
      print(f"currency code: \t{code_sorted_arr[user_idx][1]}")
      input_flag = False
    else:
      print("Choose a number from the list.")
  except:
    print("That wasn't a number.")