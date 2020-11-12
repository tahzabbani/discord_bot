import requests
import json
from urllib import request, response, error, parse
from urllib.request import urlopen

def get_build(champion, lane):
    x = requests.get("http://lol.lukegreen.xyz/build/" + lane + "/" + champion)
    build = x.json()

    build_array = []

    for i in build:
        build_array.append(i + ": " + ', '.join(build.get(str(i))))
    
    return "\n".join(build_array)

def get_skills(champion, lane):
    x = requests.get("http://lol.lukegreen.xyz/skillorder/" + lane + "/" + champion)
    skills = x.json()
    return " -> ".join(skills)
