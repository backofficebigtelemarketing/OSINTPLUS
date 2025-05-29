from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_osint_links(query):
    return {
        "Motori di Ricerca": {
            "Google": f"https://www.google.com/search?q={query}",
            "Bing": f"https://www.bing.com/search?q={query}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={query}",
            "Yandex": f"https://yandex.com/search/?text={query}"
        },
        "Social Network": {
            "Instagram": f"https://www.instagram.com/{query}",
            "TikTok": f"https://www.tiktok.com/@{query}",
            "Telegram": f"https://t.me/{query}",
            "Facebook": f"https://www.facebook.com/{query}",
            "X (Twitter)": f"https://x.com/{query}",
            "YouTube": f"https://www.youtube.com/@{query}",
            "LinkedIn": f"https://www.linkedin.com/in/{query}",
            "Pinterest": f"https://www.pinterest.com/{query}",
            "Reddit": f"https://www.reddit.com/user/{query}",
            "GitHub": f"https://github.com/{query}",
            "Snapchat": f"https://www.snapchat.com/add/{query}",
            "Discord": f"https://discord.com/users/{query}",
            "Twitch": f"https://www.twitch.tv/{query}",
            "Tumblr": f"https://{query}.tumblr.com",
            "Medium": f"https://medium.com/@{query}",
            "VK": f"https://vk.com/{query}",
            "Ask.fm": f"https://ask.fm/{query}"
        },
        "Strumenti OSINT": {
            "Namechk": f"https://namechk.com/{query}",
            "WhatsMyName": "https://whatsmyname.app",
            "Epieos": f"https://epieos.com/?q={query}",
            "Whois": f"https://who.is/whois/{query}",
            "Hunter.io": f"https://hunter.io/search/{query}",
            "Shodan": f"https://shodan.io/search?query={query}",
            "IntelX": f"https://intelx.io/?s={query}"
        },
        "Reverse Image": {
            "Google Images": f"https://images.google.com/searchbyimage?image_url={query}",
            "Yandex Images": f"https://yandex.com/images/search?rpt=imageview&url={query}"
        }
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/results", response_class=HTMLResponse)
def results(request: Request, query: str = Form(...)):
    categories = generate_osint_links(query)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "query": query,
        "categories": categories
    })
