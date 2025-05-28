from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_302_FOUND
import sqlite3
from datetime import datetime

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
templates = Jinja2Templates(directory="templates")

def db_connection():
    conn = sqlite3.connect("osint.db")
    return conn

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        request.session["user"] = username
        return RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenziali errate"})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT query, timestamp FROM history WHERE username=? ORDER BY timestamp DESC", (user,))
    history = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "history": history})

@app.post("/search")
def search(request: Request, input_data: str = Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (username, query, timestamp) VALUES (?, ?, ?)", (user, input_data, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    links = [
        f"https://www.google.com/search?q={input_data}",
        f"https://www.bing.com/search?q={input_data}",
        f"https://yandex.com/search/?text={input_data}",
        f"https://duckduckgo.com/?q={input_data}",
        f"https://namechk.com/{input_data}",
        f"https://whatsmyname.app/",
        f"https://epieos.com/?q={input_data}",
        f"https://who.is/whois/{input_data}",
        f"https://hunter.io/search/{input_data}",
        f"https://shodan.io/search?query={input_data}",
        f"https://intelx.io/?s={input_data}"
    ]
    return templates.TemplateResponse("results.html", {"request": request, "results": links, "query": input_data})
