from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import subprocess
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/results", response_class=HTMLResponse)
def search(request: Request, query: str = Form(...)):
    results = []

    # 1. Sherlock (per username)
    sherlock_output = f"sherlock_results_{query}.txt"
    subprocess.run(["python3", "sherlock/sherlock.py", query, "--print-found", "--timeout", "10", "--output", sherlock_output])

    if os.path.exists(sherlock_output):
        with open(sherlock_output, "r") as file:
            links = file.readlines()
            results += [("Sherlock", link.strip()) for link in links]
        os.remove(sherlock_output)

    # 2. Epieos (email o telefono)
    epieos_url = f"https://epieos.com/?q={query}"
    results.append(("Epieos", epieos_url))

    return templates.TemplateResponse("results.html", {
        "request": request,
        "query": query,
        "results": results
    })
