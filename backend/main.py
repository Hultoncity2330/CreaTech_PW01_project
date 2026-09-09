from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Article, ArticleInfo, NewArticle
from articles import get_article_content, get_list_articles, post_article


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
    articles = get_list_articles()
    return articles


@app.get("/article/{article_name}")
def get_article(article_name: str) -> Article:
    try:
        markdown_content, html_content = get_article_content(article_name)
    except FileNotFoundError:
        raise HTTPException(404, "This article doesn't exist.")
    
    return Article(
        name = article_name,
        articleUrl = f"/article/{article_name}",
        content = html_content,
        source = markdown_content
    )


@app.post("/create")
def create_article(new_article: NewArticle):
    try:
        return post_article(new_article)
    except FileNotFoundError:
        raise HTTPException(404, "This article doesn't exist.")

