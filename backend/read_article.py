from pathlib import Path

ARTICLES_FOLDER = Path(__file__).parent.parent / "articles"

def read_article() -> str:
    """Demande un article jusqu'à ce qu'un fichier existant soit choisi."""

    

    while True:
        filename = input("Nom de l'article : ")

        try:
            article_path = ARTICLES_FOLDER / f"{filename}.md"
            content = article_path.read_text(encoding="utf-8")
            return content

        except FileNotFoundError:
            print("Cet article n'existe pas. Réessaie.")


print(read_article())
