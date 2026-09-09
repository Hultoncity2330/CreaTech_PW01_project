from pathlib import Path
from fastapi import HTTPException
import markdown2

ARTICLES_FOLDER = Path(__file__).parent.parent / "articles"


def get_article_content(article_name):
    article_path = ARTICLES_FOLDER / f"{article_name}.md"

    if not article_path.exists():
        raise FileNotFoundError(article_name)

    markdown_content = article_path.read_text(encoding="utf-8")
    html_content = markdown2.markdown(markdown_content)

    return markdown_content, html_content


def get_list_articles():
    articles = []

    for file in ARTICLES_FOLDER.glob("*.md"):
        articles.append({
            "name": file.stem,
            "articleUrl": file.stem
        })
    return articles


def post_article(new_article):
    name = new_article.name
    content = new_article.content

    if len(name) > 50:
        raise HTTPException(400, "Too long title")
    if len(name) < 1:
        raise HTTPException(400, "Too short title")
    if not all(char.isalnum() or char in " _-" for char in name):
        raise HTTPException(400, "The name is invalid")

    new_article_file = ARTICLES_FOLDER / (name + ".md")
    if new_article_file.exists():
        raise HTTPException(400, "An article with this name already exists")

    new_article_file.write_text(content, encoding="utf-8")

    return {
        "name": name,
        "articleUrl": f"/article/{name}",
        "content": content
    }

