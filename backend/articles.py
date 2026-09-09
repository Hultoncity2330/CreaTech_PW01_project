from pathlib import Path
from models import ArticleInfo, NewArticle
import markdown2

ARTICLES_FOLDER = Path(__file__).parent.parent / "articles"
TRASH_FOLDER = Path(__file__).parent.parent / "trash"


#--------------------------------------------------#


def get_list_articles() -> list[ArticleInfo]:
    articles: list[ArticleInfo] = []

    for file in ARTICLES_FOLDER.glob("*.md"):
        articles.append(ArticleInfo(
            name = file.stem,
            articleUrl = file.stem
        ))
    
    return articles


def get_article_content(article_name: str) -> tuple[str, str]:
    article_path = ARTICLES_FOLDER / f"{article_name}.md"

    if not article_path.exists():
        raise FileNotFoundError(article_name)

    markdown_content = article_path.read_text(encoding="utf-8")
    html_content = markdown2.markdown(markdown_content)

    return markdown_content, html_content


def post_new_article(new_article: NewArticle) -> ArticleInfo:
    name = new_article.name
    content = new_article.content

    if not all(char.isalnum() or char in " _-" for char in name):
        raise ValueError("The name is invalid")

    new_article_file = ARTICLES_FOLDER / (name + ".md")

    if new_article_file.exists():
        raise FileExistsError(name)

    new_article_file.write_text(content, encoding="utf-8")

    return ArticleInfo(
        name = name,
        articleUrl = name
    )


def edit_article(article_name: str, content: str) -> ArticleInfo:
    article_path = ARTICLES_FOLDER / f"{article_name}.md"
    
    if not article_path.exists():
        raise FileNotFoundError(article_name)

    article_path.write_text(content, encoding="utf-8")

    return ArticleInfo(
        name = article_name,
        articleUrl = article_name
    )


def delete_article(article_name):
    article_path = ARTICLES_FOLDER / f"{article_name}.md"
    trash_path = TRASH_FOLDER / f"{article_name}.md"

    if not article_path.exists():
        raise FileNotFoundError(article_name)

    TRASH_FOLDER.mkdir(exist_ok = True)

    if trash_path.exists():
        trash_path.unlink()

    article_path.rename(trash_path)



