from pathlib import Path
from models import ArticleInfo, NewArticle
import markdown2
import json

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


def get_article_content(article_name: str) -> tuple[dict, str, str]:
    article_path = ARTICLES_FOLDER / f"{article_name}.md"

    if not article_path.exists():
        raise FileNotFoundError(article_name)

    metadata, markdown_content = read_article_file(article_path)
    html_content = markdown2.markdown(markdown_content)

    return metadata, markdown_content, html_content


def read_article_file(article_path: Path) -> tuple[dict, str]:
    file_content = article_path.read_text(encoding="utf-8")
    first_line, separator, remaining_content = file_content.partition("\n")

    try:
        metadata = json.loads(first_line)
        if not isinstance(metadata, dict):
            raise ValueError
        markdown_content = remaining_content

    except (json.JSONDecodeError, ValueError):
        metadata = {}
        markdown_content = file_content

    return metadata, markdown_content


def write_article_file(
        article_path: Path,
        content: str,
        author: str | None,
        category: str | None,
        tags: list[str],
    ) -> None:

    metadata = {
        "author": author,
        "category": category,
        "tags": tags,
    }

    metadata_json = json.dumps(metadata)

    article_path.write_text(
        metadata_json + "\n" + content,
        encoding="utf-8",
    )


#--------------------------------------------------#


def post_new_article(new_article: NewArticle) -> ArticleInfo:
    name = new_article.name
    content = new_article.content

    if not all(char.isalnum() or char in " _-" for char in name):
        raise ValueError("The name is invalid")

    new_article_file = ARTICLES_FOLDER / (name + ".md")

    if new_article_file.exists():
        raise FileExistsError(name)

    write_article_file(
        new_article_file,
        new_article.content,
        new_article.author,
        new_article.category,
        new_article.tags,
    )

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


