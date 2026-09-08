from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import markdown2


def article_func(article_name):
    articles_folder = Path(__file__).parent.parent / "articles"
    article_path = articles_folder / f"{article_name}.md"

    if not article_path.exists():
        raise HTTPException(404, "This article doesn't exist.")

    markdown_content = article_path.read_text(encoding="utf-8")
    html_content = markdown2.markdown(markdown_content)
    return markdown_content,html_content
