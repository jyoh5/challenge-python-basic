import csv

def save_to_csv(jobs, word):
  file = open(f"jobs_{word}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title","company","location","detail_link","apply_link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return

  