import requests
from flask import Flask, render_template, request
from scrapper import get_data, get_data_by_id

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
def index():
  order_param = request.args.get("order_by")
  db_check = db.get(order_param)
  button = """<div><b>Popular</b></div><div><a href="/?order_by=new">New</a></div>"""
  if order_param: # query args가 있다면
    if order_param == "new":
      button = """<div><a href="/?order_by=popular">Popular</a></div>
      <div><b>New</b></div>"""
    if db_check: # db에 저장되어 있다면 => db 데이터 사용
      result = db_check
    else: # db에 저장 x => 수집 및 db 저장
      if order_param == "popular":
        result = get_data(popular)
      else:
        result = get_data(new)  
      db[order_param] = result
  else: # query args가 없다면 => popular 기준 수집 및 db 저장
    result = get_data(popular)
    db[order_param] = result
  return render_template("index.html", result=result, button=button)

@app.route("/?order_by=<select>")
def index_order_by(select):
  result = get_data(select)
  return render_template("index.html", result=result)

@app.route("/<id>")
def get_news_info(id):
  url = make_detail_url(id)
  result = get_data_by_id(url)
  return render_template("detail.html", result=result)


app.run(host="0.0.0.0")