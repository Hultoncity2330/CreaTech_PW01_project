# Article Frontend

A small Vue 3 client for the article API built during the course. It provides a
visual interface for listing, reading, creating, and editing articles while the
backend remains the main focus of the project.

Vue is included locally and runs directly in the browser. There is no package
manager, build step, or frontend server to configure.

## Running the project

1. Start the FastAPI backend at `http://127.0.0.1:8000`.
2. Open `index.html` in a browser.

If your browser restricts local files, serve the directory instead:

```bash
python3 -m http.server 5173
```

Then open <http://127.0.0.1:5173>.

## Configuration

Edit `config.js` to change the API address or enable features:

```js
window.APP_CONFIG = {
  apiUrl: 'http://127.0.0.1:8000',

  features: {
    create: true,
    edit: true,
  },
}
```

The `create` and `edit` flags can be enabled when the corresponding backend
routes are implemented.

## API contract

Request and response bodies use JSON when present. Article URLs follow the
Wikipedia convention: the URL is the article name with whitespace replaced by
underscores.

```text
My article → My_article
```

### List articles

```http
GET /list
```

```json
[
  {
    "name": "My article",
    "articleUrl": "My_article"
  },
  {
    "name": "Symmetric cryptography",
    "articleUrl": "Symmetric_cryptography"
  }
]
```

The **Refresh list** button calls this endpoint again.

### Read an article

```http
GET /article/{article_url}
```

```json
{
  "name": "My article",
  "articleUrl": "My_article",
  "content": "<h1>My article</h1><p>Rendered HTML.</p>",
  "source": "# My article\n\nMarkdown source."
}
```

- `content` is the HTML rendered by the backend and displayed on the article
  page.
- `source` is the original Markdown used by the edit form. It is only required
  when editing is enabled.

### Create an article

```http
POST /create
Content-Type: application/json
```

Request body:

```json
{
  "name": "My article",
  "content": "# My article\n\nMarkdown source."
}
```

The backend creates the file, generates the article URL, and returns the created
article:

```json
{
  "name": "My article",
  "articleUrl": "My_article",
  "content": "<h1>My article</h1><p>Markdown source.</p>",
  "source": "# My article\n\nMarkdown source."
}
```

The frontend refreshes the article list and redirects using `articleUrl` from
this response. The creation request does not send a URL.

### Edit an article

```http
POST /article/{article_url}/edit
Content-Type: application/json
```

Request body:

```json
{
  "content": "# Updated title\n\nUpdated Markdown source."
}
```

The frontend derives `article_url` from the article name. Any successful `2xx`
response redirects the user back to the article page.

## CORS

An HTML file opened directly has a `null` origin. The following FastAPI setup is
suitable for this local project:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For a deployed application, replace `"*"` with the actual frontend origin.

## Project structure

```text
simplefront/
├── index.html      # Interface and Vue directives
├── app.js          # Vue state, actions, and navigation
├── api.js          # Requests to the FastAPI backend
├── config.js       # API address and feature flags
├── style.css       # Interface styles
└── vendor/         # Local Vue 3 distribution
```

`api.js` exposes four operations to the Vue application: `list`, `get`, `create`,
and `update`. The application uses hash-based URLs such as
`#/article/My_article`, so direct navigation and browser refreshes work without
server-side routing.

## Troubleshooting

- Open the browser console to inspect every API request and response status.
- If FastAPI logs `200` but the frontend reports a network error, check the CORS
  middleware and reload the page.
- If Markdown appears as plain text, ensure the backend returns rendered HTML in
  `content`, not the Markdown source.
