from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "URL Shortener API is running"}


def test_shorten_and_redirect():
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    code = response.json()["code"]

    redirect_response = client.get(f"/{code}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com"


def test_unknown_code_returns_404():
    response = client.get("/this-code-does-not-exist")
    assert response.status_code == 404
