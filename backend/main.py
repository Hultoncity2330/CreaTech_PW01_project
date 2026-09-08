from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import markdown2


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Article(BaseModel):
    name: str
    content: str
    articleUrl: str
    source: str

class ArticleInfo(BaseModel):
    name: str
    articleUrl: str


articles_folder = Path(__file__).parent.parent / "articles"


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
def get_article(article_name: str) -> dict[str, str]:
    file_path = articles_folder / f"{article_name}.md"
    markdown_content = file_path.read_text(encoding="utf-8")
    html_content = markdown2.markdown(markdown_content)
    return {"name": article_name,
            "articleUrl": f"/article/{article_name}",
            "content": html_content,
            "source": markdown_content}
