from flask import Flask, render_template, request, redirect, send_file
from search_ww import get_jobs_ww
from search_so import get_jobs_so
from search_ro import get_jobs_ro
from export import save_to_csv

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

db = {}
app = Flask("remote jobs")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/search")
def search():
  word = request.args.get("word")
  existingJobs = db.get(word)
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      ww = get_jobs_ww(word)
      so = get_jobs_so(word)
      ro = get_jobs_ro(word)
      jobs = ww + so + ro
      db[word] = jobs
  else:
    return redirect("/")
  
  return render_template("search.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)

@app.route("/export")
def export():
  word = request.args.get("word")
  try:
    if word:
      word = word.lower()
      existingJobs = db.get(word)
      if existingJobs:
        save_to_csv(existingJobs, word)
      else:
        raise Exception()
    else:
      raise Exception()
  except:
    return redirect("/")
  return send_file(f"jobs_{word}.csv", attachment_filename=f"jobs_{word}.csv",as_attachment=True)

app.run(host="0.0.0.0")