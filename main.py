import secrets
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

DB_PATH = "links.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS links (code TEXT PRIMARY KEY, url TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()


init_db()


class LinkRequest(BaseModel):
    url: str


@app.get("/")
def read_root():
    return {"message": "URL Shortener API is running"}


@app.post("/shorten")
def shorten_url(link: LinkRequest):
    code = secrets.token_urlsafe(4)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO links (code, url) VALUES (?, ?)", (code, link.url))
    conn.commit()
    conn.close()
    return {"code": code, "short_url": f"/{code}"}


@app.get("/{code}")
def redirect_to_url(code: str):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Short link not found")
    return RedirectResponse(url=row[0])
