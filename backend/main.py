from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import markdown2

from models import Article, ArticleInfo, NewArticle
from articles import article_func


articles_folder = Path(__file__).parent.parent / "articles"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "It works !"}

@app.get("/add10/{number}")
def add10(number):
    return int(number) + 10

@app.get("/list")
def list_articles() -> list[dict[str, str]]:
    articles = []

    for file in articles_folder.glob("*.md"):
        articles.append({
            "name": file.stem,
            "articleUrl": file.stem
        })
    
    return articles

@app.get("/article/{article_name}")
def get_article(article_name: str) -> Article:
    markdown_content, html_content = article_func(article_name)
    return Article (
        name = article_name,
        articleUrl = f"/article/{article_name}",
        content = html_content,
        source = markdown_content
    )


@app.post("/create")
def create_article(new_article: NewArticle):
    name = new_article.name
    content = new_article.content

    if len(name) > 50:
        raise HTTPException(400, "Too long title")
    if len(name) < 1:
        raise HTTPException(400, "Too short title")
    if not all(char.isalnum() or char in " _-" for char in name):
        raise HTTPException(400, "The name is invalid")

    new_article_file = articles_folder / (name + ".md")
    if new_article_file.exists():
        raise HTTPException(400, "An article with this name already exists")

    new_article_file.write_text(content, encoding="utf-8")

    return {
        "name": name,
        "articleUrl": f"/article/{name}",
        "content": content
    }
