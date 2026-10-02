import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

# Short code -> original URL. Lives only in memory: resets whenever the
# server restarts. Replacing this with a real database is the next milestone.
links: dict[str, str] = {}


class LinkRequest(BaseModel):
    url: str


@app.get("/")
def read_root():
    return {"message": "URL Shortener API is running"}


@app.post("/shorten")
def shorten_url(link: LinkRequest):
    code = secrets.token_urlsafe(4)
    links[code] = link.url
    return {"code": code, "short_url": f"/{code}"}


@app.get("/{code}")
def redirect_to_url(code: str):
    if code not in links:
        raise HTTPException(status_code=404, detail="Short link not found")
    return RedirectResponse(url=links[code])
