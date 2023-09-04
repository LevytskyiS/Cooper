import requests


url = "https://www.linkedin.com/search/results/people/?geoUrn=%5B'103973174'%5D&keywords=it%20recruiter&origin=FACETED_SEARCH&sid=oZa"

response = requests.get(url)

text_file = "linkedin.txt"

with open(text_file, "w", encoding="utf-8") as fh:
    fh.write(response.text)
