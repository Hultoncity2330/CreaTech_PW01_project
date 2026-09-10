from pydantic import BaseModel, Field


#--------------------------< Articles >------------------------#


class ArticleInfo(BaseModel):
    """Represent basic information used to identify and access an article."""
    name: str
    articleUrl: str


class Article(BaseModel):
    """Represent a complete article returned by the API."""
    name: str = Field(description = "The name of the article", examples = ["Alphabet"])
    content: str = Field(description = "Content in HTML of the article")
    articleUrl: str
    source: str = Field(description = "Content in Markdown of the article")
    author: str | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory = list)


class NewArticle(BaseModel):
    """Represent the data required to create a new article."""
    name: str = Field(min_length = 1, max_length = 64)
    content: str = Field(min_length = 1, max_length = 10000)
    author: str | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory = list)


class EditArticle(BaseModel):
    """Represent the optional data used to update an existing article."""
    content: str | None = Field(default = None, min_length = 1, max_length = 10000)
    author: str | None = None
    category: str | None = None
    tags: list[str] | None = None


class DeleteArticle(BaseModel):
    """Represent the response returned after deleting an article."""
    message: str


class RestoreArticle(BaseModel):
    """Represent the response returned after restoring an article."""
    message: str


#--------------------------< Comments >------------------------#


class Comment(BaseModel):
    """Represent a complete stored comment returned by the API."""
    id: str
    author: str | None = None
    content: str = Field(min_length = 1, max_length = 1000)


class NewComment(BaseModel):
    """Represent the data required to create a new comment."""
    author: str | None = None
    content: str = Field(min_length = 1, max_length = 1000)


class EditComment(BaseModel):
    """Represent the optional data used to update an existing comment."""
    author: str | None = None
    content: str | None = Field(default = None, min_length = 1, max_length = 1000)


class DeleteComment(BaseModel):
    """Represent the response returned after deleting a comment."""
    message: str


