from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_links(query):
    query = query.strip().replace(" ", "+")
    return {
        "Google": f"https://www.google.com/search?q={query}",
        "Epieos": f"https://epieos.com/?q={query}",
        "Namechk": f"https://namechk.com/{query}",
        "Hunter.io": f"https://hunter.io/search/{query}",
        "IntelX": f"https://intelx.io/?s={query}",
        "SocialSearcher": f"https://www.social-searcher.com/search-users/?q={query}",
        "Whois": f"https://who.is/whois/{query}",
        "Shodan": f"https://www.shodan.io/search?query={query}"
        "facebook": f"https://www.facebook.com/search?query={query}"
    }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/results", response_class=HTMLResponse)
async def results(request: Request, query: str = Form(...)):
    links = generate_links(query)
    return templates.TemplateResponse("results.html", {"request": request, "query": query, "links": links})
