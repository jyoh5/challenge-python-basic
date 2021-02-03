import requests, json

def get_data(url):
  html = requests.get(url)
  html_to_json = json.loads(html.text)
  return html_to_json["hits"]


def get_data_by_id(url):
  html = requests.get(url)
  return json.loads(html.text)