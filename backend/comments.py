from pathlib import Path
import json
import uuid

from models import Comment, NewComment

COMMENTS_FILE = Path(__file__).parent.parent / "comments.json"


#--------------------------------------------------#


def get_comments() -> list[Comment]:
    """Return all comments stored in `comments.json`."""

    try:
        with COMMENTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        return []

    return [
        Comment(**comment)
        for comment in data
    ]


def save_comments(comments: list[Comment]) -> None:
    """Save all comments to comments.json."""

    data = [
        comment.model_dump()
        for comment in comments
    ]

    with COMMENTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent = 4
        )



def add_comment(new_comment: NewComment) -> Comment:
    """Create and save a new comment."""

    if not new_comment.content.strip():
        raise ValueError("The comment cannot be empty")

    comments = get_comments()

    comment = Comment(
        id = str(uuid.uuid4()),
        author = new_comment.author,
        content = new_comment.content
    )

    comments.append(comment)
    save_comments(comments)

    return comment
