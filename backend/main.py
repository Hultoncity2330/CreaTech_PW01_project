from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Article, ArticleInfo, NewArticle, EditArticle, DeleteArticle
from articles import get_article_content, get_list_articles, post_new_article, edit_article, delete_article


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#--------------------------------------------------#


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "It works !"}


@app.get("/add10/{number}")
def add10(number):
    return int(number) + 10


@app.get("/list")
def list_articles() -> list[ArticleInfo]:
    return get_list_articles()


@app.get("/article/{article_name}")
def read_article(article_name: str) -> Article:
    try:
        metadata, markdown_content, html_content = get_article_content(article_name)
    
    except FileNotFoundError:
        raise HTTPException(404, "This article doesn't exist.")
    
    return Article(
        name = article_name,
        articleUrl = f"{article_name}",
        content = html_content,
        source = markdown_content,
        author = metadata.get("author"),
        category = metadata.get("category"),
        tags = metadata.get("tags", [])
    )


@app.post("/create")
def create_article(new_article: NewArticle) -> ArticleInfo:
    try:
        return post_new_article(new_article)

    except FileExistsError:
        raise HTTPException(400, "An article with this name already exists")

    except ValueError:
        raise HTTPException(400, "This name is invalid")


@app.post("/article/{article_name}/edit")
def update_article(article_name: str, article: EditArticle) -> ArticleInfo:
    try:
        return edit_article(article_name, article)
    
    except FileNotFoundError:
            raise HTTPException(404, "This article doesn't exist.")


@app.get("/article/{article_name}/delete")
def delete_article_route(article_name: str) -> DeleteArticle:
    try:
        delete_article(article_name)
        return DeleteArticle(message = "Article moved to trash successfully.")

    except FileNotFoundError:
        raise HTTPException(404, "This article doesn't exist.")

