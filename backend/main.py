from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import markdown2


articles_folder = Path(__file__).parent.parent / "articles"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Article(BaseModel):
    """Article including its content"""
    name: str = Field(description = "The name of the article", examples = ["Alphabet"])
    content: str = Field(description = "Content in HTML of the article")
    articleUrl: str
    source: str = Field(description = "Content in Markdown of the article")


class ArticleInfo(BaseModel):
    name: str
    articleUrl: str


class NewArticle(BaseModel):
    name: str
    content: str


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
    article_path = articles_folder / f"{article_name}.md"

    if not article_path.exists():
        raise HTTPException(404, "This article doesn't exist.")

    markdown_content = article_path.read_text(encoding="utf-8")
    html_content = markdown2.markdown(markdown_content)
    return {"name": article_name,
            "articleUrl": f"/article/{article_name}",
            "content": html_content,
            "source": markdown_content}


@app.post("/create")
def create_article(new_article: NewArticle):
    name = new_article.name
    content = new_article.content

    if len(name) > 50:
        raise HTTPException(401, "Too long title")
    
    new_article_file = articles_folder / (name + ".md")
    new_article_file.write_text(content, encoding="utf-8")

    return {
        "name": name,
        "articleUrl": f"/article/{name}",
        "content": content
    }
