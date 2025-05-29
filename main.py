from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_links(query):
    return {
        "Motori di Ricerca": {
            "Google": f"https://www.google.com/search?q={query}",
            "Bing": f"https://www.bing.com/search?q={query}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={query}",
            "Yandex": f"https://yandex.com/search/?text={query}",
            "Yahoo": f"https://search.yahoo.com/search?p={query}",
            "StartPage": f"https://www.startpage.com/do/dsearch?query={query}",
            "Mojeek": f"https://www.mojeek.com/search?q={query}",
            "Qwant": f"https://www.qwant.com/?q={query}"
        },
        "Motori Social (Username)": {
            "Namechk": f"https://namechk.com/{query}",
            "WhatsMyName": "https://whatsmyname.app",
            "CheckUsernames": f"https://checkusernames.com/{query}",
            "UserSearch": f"https://usersearch.org/results/?q={query}",
            "KnowEm": f"https://knowem.com/checkusername/{query}",
            "SocialSearcher": f"https://www.social-searcher.com/search-users/?q={query}"
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
