from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Article, ArticleInfo, DeleteComment, NewArticle, EditArticle, DeleteArticle, RestoreArticle, Comment, NewComment, EditComment, DeleteComment
from articles import get_article_content, get_list_articles, post_new_article, edit_article, delete_article, restore_article
from comments import get_comments, add_comment, edit_comment, delete_comment


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#--------------------------< Articles >------------------------#


@app.get("/")
def root() -> dict[str, str]:
    """Return a simple message confirming that the API is running."""
    return {"message": "It works !"}


@app.get("/add10/{number}")
def add10(number: int) -> int:
    """Return the given number increased by ten."""
    return int(number) + 10


@app.get("/list")
def list_articles() -> list[ArticleInfo]:
    """Return the list of all available articles."""
    return get_list_articles()


@app.get("/article/{article_name}")
def read_article(article_name: str) -> Article:
    """Return an article with its metadata, Markdown source and HTML content."""

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
    """Create a new article from validated request data."""

    try:
        return post_new_article(new_article)

    except FileExistsError:
        raise HTTPException(400, "An article with this name already exists")

    except ValueError:
        raise HTTPException(400, "This name is invalid")


@app.post("/article/{article_name}/edit")
def update_article(article_name: str, article: EditArticle) -> ArticleInfo:
    """Update the content or metadata of an existing article."""

    try:
        return edit_article(article_name, article)
    
    except FileNotFoundError:
            raise HTTPException(404, "This article doesn't exist.")


@app.delete("/article/{article_name}/delete")
def remove_article(article_name: str) -> DeleteArticle:
    """Move an existing article to the trash directory."""

    try:
        delete_article(article_name)
        return DeleteArticle(message = "Article moved to trash successfully.")

    except FileNotFoundError:
        raise HTTPException(404, "This article doesn't exist.")


@app.post("/article/{article_name}/restore")
def restore_article_route(article_name: str) -> RestoreArticle:
    """Restore an article from the trash directory."""

    try:
        restore_article(article_name)
        return RestoreArticle(message = "Article restored succesfully.")

    except FileNotFoundError:
        raise HTTPException(404, "This article doesn't exist in trash.")

    except FileExistsError:
        raise HTTPException(400, "An article with this name already exists.")


#--------------------------< Comments >------------------------#


@app.get("/comments")
def list_comments() -> list[Comment]:
    """Return all the comments stored by the application."""
    return get_comments()


@app.post("/comments")
def create_comment(new_comment: NewComment) -> Comment:
    """Create and return a new comment."""

    try:
        return add_comment(new_comment)

    except ValueError:
        raise HTTPException(400, "The comment cannot be empty.")


@app.post("/comments/{comment_id}/edit")
def update_comment(comment_id: str, edit: EditComment) -> Comment:
    """Update and return an existing comment identified by its ID."""

    try:
        return edit_comment(comment_id, edit)

    except FileNotFoundError:
        raise HTTPException(404, "This comment doesn't exist.")

    except ValueError:
        raise HTTPException(400, "The comment cannot be empty.")


@app.delete("/comments/{comment_id}")
def remove_comment(comment_id: str) -> DeleteComment:
    """Delete a comment identified by its ID."""

    try:
        delete_comment(comment_id)

        return DeleteComment(message = "Comment deleted successfully.")

    except FileNotFoundError:
        raise HTTPException(404, "This comment doesn't exist.")


