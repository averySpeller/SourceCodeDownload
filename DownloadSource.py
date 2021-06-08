import requests
import subprocess
import os

jwt = subprocess.run(["state", "export", "jwt"], stdout=subprocess.PIPE,text=True).stdout.rstrip()

url = "https://platform.activestate.com/sv/mediator/api"
json_query  = { "query": """{
    project(org: "ActiveStateee", name: "ActivePythonEnterprise-3.8") {
      __typename
      ... on Project {
        name
        description
        commit {
          commit_id
          sources(limit: 4) {
            name
            version
            url
          }
        }
      }
      ... on NotFound {
        message
      }
    }
  }
""" }
headers = {"Authorization": "Bearer %s" % jwt}

r = requests.post(url=url, json=json_query, headers=headers)

sources = r.json()["data"]["project"]["commit"]["sources"]
project = r.json()["data"]["project"]["name"]
print("project: ", project)

for s in sources:
  r = requests.get(url=s["url"],headers=headers)
  print("downloading...", )
# download zip files
  with open(os.path.basename(s["url"]), "wb") as f:
      f.write(r.content)
      print(f.name)

