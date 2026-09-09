from pydantic import BaseModel, Field

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
    name: str = Field(min_length = 1, max_length = 64)
    content: str = Field(min_length = 1, max_length = 10000)

