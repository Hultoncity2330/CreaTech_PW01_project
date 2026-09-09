from pydantic import BaseModel, Field


#--------------------------< Articles >------------------------#


class ArticleInfo(BaseModel):
    name: str
    articleUrl: str


class Article(BaseModel):
    """Article including its content"""
    name: str = Field(description = "The name of the article", examples = ["Alphabet"])
    content: str = Field(description = "Content in HTML of the article")
    articleUrl: str
    source: str = Field(description = "Content in Markdown of the article")
    author: str | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory = list)


class NewArticle(BaseModel):
    name: str = Field(min_length = 1, max_length = 64)
    content: str = Field(min_length = 1, max_length = 10000)
    author: str | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory = list)


class EditArticle(BaseModel):
    content: str | None = Field(min_length = 1, max_length = 10000)
    author: str | None = None
    category: str | None = None
    tags: list[str] | None = None


class DeleteArticle(BaseModel):
    message: str


#--------------------------< Comments >------------------------#


class Comment(BaseModel):
    id: str
    author: str | None = None
    content: str = Field(min_length = 1, max_length = 1000)


class NewComment(BaseModel):
    author: str | None = None
    content: str = Field(min_length = 1, max_length = 1000)


