# CreaTech — Computer Science Workshop 1

Backend for the **Development Tools & Web Server** workshop. The project implements a small wiki-style application with a provided Vue frontend and a FastAPI backend written in Python.

The backend supports article listing, reading, creation, editing, metadata, soft deletion and restoration, as well as persistent site-wide comments.

## Features

- List Markdown articles stored on disk.
- Read an article and convert Markdown to HTML with `markdown2`.
- Create and edit articles.
- Store optional article metadata: `author`, `category`, and `tags`.
- Preserve compatibility with older Markdown files without metadata.
- Soft-delete articles by moving them to `trash/`.
- Restore deleted articles from `trash/` through the backend API.
- List and create site-wide comments.
- Edit and delete comments by unique ID.
- Persist comments in `comments.json`.
- Validate API inputs and outputs with Pydantic.
- Translate Python exceptions into appropriate HTTP errors in FastAPI.
- Enable CORS for the provided local frontend.

## Project structure

```text
CreaTech_PW01_project/
├── articles/               # Active Markdown articles
├── backend/
│   ├── articles.py         # Article business logic and file operations
│   ├── comments.py         # Comment business logic and JSON persistence
│   ├── main.py             # FastAPI routes and HTTP error handling
│   ├── models.py           # Pydantic API models
│   ├── pyproject.toml      # Python project configuration
│   └── uv.lock             # Locked Python dependencies
├── simplefront_v3/         # Provided Vue 3 frontend
├── trash/                  # Soft-deleted articles
├── comments.json           # Persistent comments
├── .gitignore
└── README.md
```

The backend follows a layered architecture:

```text
Frontend
   ↓ HTTP / JSON
main.py
   ↓ Python calls
articles.py / comments.py
   ↓
Filesystem
```

`main.py` handles FastAPI routes and converts business-layer exceptions into `HTTPException`. `articles.py` and `comments.py` contain no FastAPI dependency and are responsible for file operations. `models.py` defines the Pydantic schemas exchanged through the API.

## Requirements

- Python **3.14 or newer**
- [`uv`](https://docs.astral.sh/uv/)

The Python dependencies are declared in `backend/pyproject.toml`:

- `fastapi[standard]`
- `markdown2`

## Installation

Clone the repository and enter the backend directory:

```bash
git clone <repository-url>
cd CreaTech_PW01_project/backend
```

Install the locked dependencies with `uv`:

```bash
uv sync
```

## Running the backend

From the `backend/` directory, run:

```bash
uv run fastapi dev main.py
```

The API is then available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Running the frontend

Start the backend first, then open:

```text
simplefront_v3/index.html
```

If the browser restricts local files, serve the frontend directory with a local HTTP server:

```bash
cd simplefront_v3
python -m http.server 5173
```

Then open:

```text
http://127.0.0.1:5173
```

The frontend expects the backend at `http://127.0.0.1:8000` by default.

## Article storage

Articles are stored as `.md` files inside `articles/`.

Metadata uses the **first-line JSON format**. A file can therefore look like this:

```text
{"author": "Alex", "category": "Programming", "tags": ["Python", "Web"]}
# FastAPI

Article content written in Markdown.
```

The first line is parsed as metadata only when it contains a valid JSON object. The remaining text is treated as Markdown.

Older files remain compatible. If the first line is not a JSON object, the entire file is treated as Markdown and empty/default metadata is returned.

When an article is read:

- `source` contains the Markdown body without the metadata line;
- `content` contains the HTML generated from that Markdown body;
- `author`, `category`, and `tags` are returned separately.

## Article API

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/list` | Return all active articles |
| `GET` | `/article/{article_name}` | Return one article, its HTML, source and metadata |
| `POST` | `/create` | Create a new article |
| `POST` | `/article/{article_name}/edit` | Edit article content and/or metadata |
| `GET` | `/article/{article_name}/delete` | Move an article to `trash/` |
| `POST` | `/article/{article_name}/restore` | Restore an article from `trash/` |

### Create an article

Example request:

```http
POST /create
Content-Type: application/json
```

```json
{
  "name": "FastAPI",
  "content": "# FastAPI\n\nA Python web framework.",
  "author": "Alex",
  "category": "Programming",
  "tags": ["Python", "Web"]
}
```

### Read an article

Example response:

```json
{
  "name": "FastAPI",
  "content": "<h1>FastAPI</h1>\n<p>A Python web framework.</p>\n",
  "articleUrl": "FastAPI",
  "source": "# FastAPI\n\nA Python web framework.",
  "author": "Alex",
  "category": "Programming",
  "tags": ["Python", "Web"]
}
```

### Edit an article

Only fields supplied by the client are applied. This allows metadata fields that are omitted from the request to keep their existing values.

Example:

```json
{
  "category": "Computer Science",
  "tags": ["Python", "API"]
}
```

### Delete and restore articles

Deletion is implemented as a **soft delete**. The `.md` file is moved from `articles/` to `trash/` rather than being permanently removed.

```text
articles/FastAPI.md
        ↓ delete
trash/FastAPI.md
        ↓ restore
articles/FastAPI.md
```

If an older copy already exists in `trash/`, it is replaced when the active article is deleted.

The restore endpoint is currently a backend feature and can be tested from `/docs`; the provided frontend does not expose a Restore button.

> Note: the provided frontend v3 expects article deletion through `GET /article/{article_name}/delete`, so the backend follows that project-specific contract.

## Comments

Comments are global to the website rather than attached to individual articles. They are stored as JSON in `comments.json`.

Each stored comment contains:

```json
{
  "id": "7db8931d-97d0-43b2-8830-bd4372604382",
  "author": "Alex",
  "content": "Thanks for the articles!"
}
```

IDs are generated by the backend using `uuid.uuid4()` and stored as strings.

An author is optional. Comment content must contain at least one non-whitespace character.

## Comment API

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/comments` | Return all comments |
| `POST` | `/comments` | Create a new comment |
| `POST` | `/comments/{comment_id}/edit` | Edit an existing comment |
| `DELETE` | `/comments/{comment_id}` | Delete an existing comment |

### Create a comment

```json
{
  "author": "Alex",
  "content": "Thanks for the articles!"
}
```

The backend returns the stored comment with its generated ID.

### Edit a comment

Example:

```json
{
  "content": "Updated comment"
}
```

### Delete a comment

Deletion removes the selected comment from the list and rewrites `comments.json`.

If `comments.json` does not exist yet, `GET /comments` returns an empty list:

```json
[]
```

## Validation and error handling

Pydantic models define the API contract and validate incoming data. Examples of validation rules include:

- article names: 1–64 characters;
- article content: maximum 10,000 characters;
- comment content: maximum 1,000 characters;
- optional article metadata;
- optional comment author.

The business layer raises standard Python exceptions such as:

```text
FileNotFoundError
FileExistsError
ValueError
```

`main.py` catches these exceptions and translates them into HTTP responses such as `404 Not Found` or `400 Bad Request`.

## CORS

CORS is enabled for the local workshop environment:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This configuration is convenient for local development. A deployed application should restrict allowed origins instead of using `"*"`.

## Development principles

The project follows the practices introduced during Workshop 1:

- clear separation of responsibilities;
- type annotations;
- Pydantic validation;
- short functions with one main responsibility;
- docstrings for functions and API models;
- defensive error handling;
- persistent storage through files;
- small and descriptive Git commits;
- dependency management with `uv`.

## Useful commands

```bash
# Install/synchronize dependencies
uv sync

# Run the FastAPI development server
uv run fastapi dev main.py

# Open the API documentation
# http://127.0.0.1:8000/docs

# Check Git status
git status

# Create a commit
git add .
git commit -m "Describe the change"

# Push commits
git push
```

## Workshop

**Computer Science — Workshop 1: Development Tools & Web Server**  
September 7–9, 2026

The frontend is provided as part of the workshop. The main implementation work in this repository focuses on the Python/FastAPI backend.
