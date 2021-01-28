import requests, os, re

quit_flag = True

while(quit_flag):
  os.system("clear")
  print("Welcome to IsItDown.py!")
  print("Please write a URL or URLs you want to check. (separated by comma)")
  urls = input()
  urls = urls.split(",")

  for url in urls:
    url = re.sub(" +","",url)

    p = re.compile("^https?",re.I)
    m = p.match(url)

    if(m == None):
      url = "http://" + url

    try:
      rq_result = requests.get(url)
      status = ""
      if rq_result.status_code == requests.codes.ok:
        status = "up"
      else:
        status = "down"
      print(f"{rq_result.url} is {status}")
    except requests.exceptions.ConnectionError:
      print(f"{url} is not a valid URL.")
      

  question_flag = True
  while(question_flag):
    quit_input = input("Do you want to start over? y/n ")
    if quit_input in ["n","N"]:
      quit_flag = False
      question_flag = False
    elif quit_input in ["y","Y"]:
      quit_flag = True
      question_flag = False
    else:
      print("That's not a valid answer.")
      question_flag = True
