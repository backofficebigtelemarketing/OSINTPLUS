from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_links(query):
    query = query.strip().replace(" ", "+")
    return {
        "Motori di Ricerca Generali": {
            "Google": f"https://www.google.com/search?q={query}",
            "Bing": f"https://www.bing.com/search?q={query}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={query}",
            "Yandex": f"https://yandex.com/search/?text={query}",
            "Yahoo": f"https://search.yahoo.com/search?p={query}",
            "StartPage": f"https://www.startpage.com/do/dsearch?query={query}",
            "Mojeek": f"https://www.mojeek.com/search?q={query}",
            "Qwant": f"https://www.qwant.com/?q={query}"
        },
        "Motori di Ricerca Social": {
            "Namechk": f"https://namechk.com/{query}",
            "WhatsMyName": "https://whatsmyname.app",
            "Social-Searcher": f"https://www.social-searcher.com/search-users/?q={query}",
            "Hashatit": f"https://www.hashatit.com/search?q={query}",
            "OSINT Industries": f"https://www.osint.industries/post/social-media-lookup-how-to-find-hidden-profiles-and-accounts-with-osint",
            "Sherlock": f"https://github.com/sherlock-project/sherlock",
            "Holehe": f"https://github.com/megadose/holehe"
        },
        "Strumenti Investigativi": {
            "Epieos": f"https://epieos.com/?q={query}",
            "IntelX": f"https://intelx.io/?s={query}",
            "Whois": f"https://who.is/whois/{query}",
            "Hunter.io": f"https://hunter.io/search/{query}",
            "Shodan": f"https://shodan.io/search?query={query}",
            "ZoomEye": f"https://www.zoomeye.org/searchResult?q={query}"
        },
        "Reverse Image": {
            "Google Images": f"https://images.google.com/searchbyimage?image_url={query}",
            "Yandex Images": f"https://yandex.com/images/search?rpt=imageview&url={query}",
            "TinEye": f"https://tineye.com/search?url={query}"
        }
    }

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/results", response_class=HTMLResponse)
def search(request: Request, query: str = Form(...)):
    results = []
    data = generate_links(query)
    for category, links in data.items():
        for name, link in links.items():
            results.append((f"{category} - {name}", link))
    return templates.TemplateResponse("results.html", {"request": request, "query": query, "results": results})
