# Backend tutorials

Extend the article API with optional metadata and a site-wide comments page.
The frontend is already prepared for both features. Implement the routes and
storage in FastAPI, then use the interface to check the result.

## Working with JSON in Python

JSON is a text format for structured data. Python's built-in `json` module
converts between JSON text and Python values.

### Convert between text and Python objects

```python
import json

metadata = {
    "author": "Alex",
    "tags": ["Python", "Web"],
    "category": "Programming",
}

text = json.dumps(metadata, ensure_ascii=False)
restored_metadata = json.loads(text)

print(restored_metadata["author"])  # Alex
```

- `json.dumps(value)` returns a string.
- `json.loads(text)` parses a string and returns a Python value.
- JSON objects become dictionaries; arrays become lists.
- `ensure_ascii=False` keeps accented characters readable.

JSON uses double quotes and the values `true`, `false`, and `null`.
Python uses `True`, `False`, and `None`. Let the JSON module handle the
conversion rather than constructing JSON with string concatenation.

### Read and write a complete JSON file

```python
import json
from pathlib import Path

path = Path("comments.json")
comments = [
    {"id": 1, "author": "Alex", "content": "Great articles!"},
]

with path.open("w", encoding="utf-8") as file:
    json.dump(comments, file, ensure_ascii=False, indent=2)

with path.open("r", encoding="utf-8") as file:
    saved_comments = json.load(file)
```

`dump` and `load` work with open files; `dumps` and `loads` work with
strings. Use a complete JSON file for comments. Article files use a different
format: one JSON line followed by Markdown.

## Reading the first line, then the rest of a file

An article file such as `My_article.md` has this structure:

```text
{"author": "Alex", "tags": ["Python", "Web"], "category": "Programming"}

# My article

Article content.
```

Read the two parts with the same open file:

```python
from pathlib import Path

path = Path("My_article.md")

with path.open("r", encoding="utf-8") as file:
    first_line = file.readline()
    markdown_body = file.read()
```

`readline()` reads one line, including its newline when present. The file
position then sits at the start of the next line. `read()` continues from
that position to the end; it does not start over.

The `with` block closes the file automatically. An empty file returns
`""` from both calls.

### Parse the metadata

For a file with a JSON header:

```python
import json

metadata = json.loads(first_line)
author = metadata.get("author", "")
tags = metadata.get("tags", [])
category = metadata.get("category", "")
```

Only parse the first line with `json.loads`. Calling `json.load` on the whole
article would also try to parse the Markdown as JSON.

Older articles may not have a metadata line. This helper preserves their first
line instead of accidentally removing the heading:

```python
import json


def read_article_file(path):
    """Return metadata and Markdown, including support for older files."""
    with path.open("r", encoding="utf-8") as file:
        first_line = file.readline()
        remainder = file.read()

    try:
        metadata = json.loads(first_line)
    except json.JSONDecodeError:
        return {}, first_line + remainder

    if not isinstance(metadata, dict):
        return {}, first_line + remainder

    return metadata, remainder
```

This convention treats a first line that is not a JSON object as ordinary
Markdown. When editing headers manually, check the JSON syntax: an invalid
header will be treated as part of the article.

## Writing a line and the Markdown body

```python
import json


def write_article_file(path, metadata, markdown_body):
    """Write one JSON header line followed by the Markdown body."""
    with path.open("w", encoding="utf-8") as file:
        file.write(json.dumps(metadata, ensure_ascii=False))
        file.write("\n")
        file.write(markdown_body)
```

`write()` writes exactly the supplied text; it does not add a newline.
Do not use `indent` for the metadata header: the JSON must fit on one line.

Opening with `"w"` replaces the entire file. To change only the metadata,
first read the existing body, then write it back with the updated header:

```python
metadata, markdown_body = read_article_file(path)
metadata["author"] = "Sam"
write_article_file(path, metadata, markdown_body)
```

Appending with `"a"` writes at the end of the file, so it cannot replace the
first line. Rewriting the header and body is the straightforward approach here.

## Exercise: article metadata

### Define the fields

Add these optional fields to the article request and response models:

- `author`: a string, empty by default.
- `category`: a string, empty by default.
- `tags`: a list of strings, empty by default. In Pydantic, use
  `Field(default_factory=list)` for its default.

The frontend converts comma-separated tags into a JSON array before sending
them. Keep this array format in storage and responses.

### Connect the routes to storage

1. In `POST /create`, accept the name, Markdown content, and optional metadata.
   Generate the filename from the name by replacing spaces with underscores:
   `My article` becomes `My_article.md`.
2. Write the metadata as the first line and the Markdown as the remaining body.
3. In `GET /article/{article_url}`, read the two parts separately. Convert only
   the Markdown body to HTML.
4. In `POST /article/{article_url}/edit`, update the body and supplied metadata,
   then rewrite the file.

An empty author or category string, or an empty tags array, clears that value.
If a field is omitted from an editing request, preserve its saved value.
Pydantic's `model_dump(exclude_unset=True)` helps distinguish omitted fields
from explicitly supplied empty values.

The reading route returns:

```json
{
  "name": "My article",
  "articleUrl": "My_article",
  "author": "Alex",
  "tags": ["Python", "Web"],
  "category": "Programming",
  "content": "<h1>My article</h1><p>Article content.</p>",
  "source": "# My article\n\nArticle content."
}
```

`content` contains rendered HTML; `source` contains the Markdown body used by
the editor. Neither includes the JSON header.

The creation route returns the created article, including `articleUrl`.
The frontend uses that response to refresh the list and open the new article.
Metadata stays optional: older files must still work.

### Check the result

Create an article with metadata, read it back, edit its author and tags, then
reload it. Also check that clearing a field removes its saved value and that
an older file without a header still displays its first line.

The frontend's metadata exercise disappears for each author or tags field once
that field has a value.

## Exercise: site-wide comments

Comments belong to the whole site, not to individual articles. They have no
article identifier and are displayed as plain text.

### Define the data

Use a Pydantic request model with a required, non-blank `content` string and an
optional `author` string. Reject content containing only whitespace.
Generate a unique `id` on the backend; do not ask the frontend to supply it.

### List comments

`GET /comments` returns an array, oldest first:

```json
[
  {"id": 1, "author": "Alex", "content": "Great articles!"}
]
```

Return `[]` when there are no comments.

### Create a comment

`POST /comments` accepts:

```json
{"author": "Alex", "content": "Great articles!"}
```

Validate the input, store the comment, and return the stored object:

```json
{"id": 1, "author": "Alex", "content": "Great articles!"}
```

The frontend adds this response to the list and clears the form. An empty author
displays as “Anonymous”.

### Add persistence

Start with a Python list to check the routes. It resets when the server restarts.
Then use a `comments.json` file with the `json.load` and `json.dump` operations
shown above:

1. Read the saved list, or use an empty list if the file does not exist yet.
2. Add the new comment with its generated ID.
3. Write the complete list back to the JSON file.
4. Return the newly stored comment.

Keep identifiers unique across restarts. A UUID string is one option.
Simple file storage is sufficient for this exercise; simultaneous writes would
need coordination or database storage.

### Check the complete flow

Use `/docs` to create a comment and check that it appears in the GET response.
Then repeat through the frontend. Once persistence is implemented, restart
FastAPI and verify that previously saved comments are still returned.
