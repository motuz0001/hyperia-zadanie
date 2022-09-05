import requests
from bs4 import BeautifulSoup
import json

url = "https://www.hyperia.sk/kariera/"

results = []

s = requests.Session()
r = s.get(url)
soup = BeautifulSoup(r.text, features="html.parser")

classes = soup.findAll(class_="arrow-link")
for i in range(len(classes) - 1):
    r = s.get("https://www.hyperia.sk" + classes[i]["href"])
    soup = BeautifulSoup(r.content, features="html.parser", )

    title = soup.find(class_="hero-text col-lg-12").find("h1").text.strip()

    # class for place, salary and contract_type
    info_classes = soup.findAll(class_="col-md-4 icon")

    place = info_classes[0].text.split(":")[1]
    salary = info_classes[1].get_text("<?>").split("<?>")[2]
    contract_type = info_classes[2].text.split("pomeru")[1]

    contact_email = soup.find(class_="position-button")["href"].split(":")[1]

    results.append({
        "title": title,
        "place": place,
        "salary": salary,
        "contract_type": contract_type,
        "contact_email": contact_email
    })

with open("results.json", "w") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("DONE")
s.close()
