from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/results", response_class=HTMLResponse)
def results(request: Request, query: str = Form(...)):
    query_links = [
        f"https://www.google.com/search?q={query}",
        f"https://www.bing.com/search?q={query}",
        f"https://yandex.com/search/?text={query}",
        f"https://duckduckgo.com/?q={query}",
        f"https://namechk.com/{query}",
        f"https://whatsmyname.app/",
        f"https://epieos.com/?q={query}",
        f"https://who.is/whois/{query}",
        f"https://hunter.io/search/{query}",
        f"https://shodan.io/search?query={query}",
        f"https://intelx.io/?s={query}",
        f"https://images.google.com/searchbyimage?image_url={query}",
        f"https://yandex.com/images/search?rpt=imageview&url={query}"
    ]
    return templates.TemplateResponse("results.html", {
        "request": request, "query": query, "links": query_links
    })
