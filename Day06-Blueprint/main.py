import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

code_arr = []

def print_codes():
  # os.system("clear")
  url = "https://www.iban.com/currency-codes"

  rq_result = requests.get(url)
  parsed_result = BeautifulSoup(rq_result.text, "html.parser")

  table = parsed_result.find("table", {"class":"tablesorter"})
  tbody = table.find("tbody")
  trs = tbody.find_all("tr")

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
      code_arr.append({"country":country, "code":code})

  # code_sorted_arr = sorted(code_arr, key=(lambda x: x[0]))

  # print("Hi! Please select a country by number.")
  for idx, code in enumerate(code_arr):
    print(f"# {idx}: {code['country']}")

  
def ask(is_country="True"):
  """
  is_country : True -> return country code
               False -> return amount
  """

  input_flag = True
  while(input_flag):
    user_input = input("\tnumber: ")
    try:
      user_idx = int(user_input)
      if(is_country):
        if user_idx < len(code_arr):
          print(f"\tcontry: {code_arr[user_idx]['country']}")
          # print(f"currency code: \t{code_arr[user_idx]['code']}")
          # input_flag = False
          return code_arr[user_idx]['code']
        else:
          print("Choose a number from the list.")
      else:
        return user_idx
    except ValueError:
      print("That wasn't a number.")


def money_change(from_code, to_code, amount):
  url = f"https://transferwise.com/gb/currency-converter/{from_code}-to-{to_code}-rate?amount={amount}"
  html = requests.get(url)
  data = BeautifulSoup(html.text, "html.parser")
  exchange = float(data.find("span",{"class":"text-success"}).string)
  from_value = format_currency(amount, from_code, u'#,##0 ¤')
  to_value = format_currency(amount*exchange, to_code, u'#,##0 ¤')
  print(f"\n{from_value} = {to_value}")


def run():
  print_codes()
  print("\nSelect a country's number")
  from_code = ask()
  print("\nSelect another country's number")
  to_code = ask()
  print(f"\nHow Many {from_code} do you want to convert to {to_code}")
  amount = ask(is_country=False)
  money_change(from_code, to_code,amount)

print("Welcome to CurrencyConvert Ver2.0")
run()