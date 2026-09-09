from multiprocessing import Value
from pathlib import Path


if False:
    def choose_from(list_of_valid: list[str], question):
        user_input = input(question)
        if user_input in list_of_valid:
            return user_input
        else:
            raise ValueError("Invalid user input")

    colors = ["red", "green", "blue"]
    try:
        picked = choose_from(colors, "Choose a color: ")
    except ValueError:
        # NEVER write except: or except Exception:
        # Except must targets specific exception types. 
        print("There was an error")
    else:  # If everything went well
        print("You picked", picked)


"""
Pseudo code of fastapi engine error management:

def fastapi_engine(user_url):
    apifunction = get_api_function(user_url)
    # user_url is '/list, so i get list_articles()
    try:
        response = apifunction()
    except HTTPException:
        response = "Error 404"
    return response
"""

######

valid_int: bool = False
user_input: str = ""
user_int: int = 0

while not valid_int:
    user_input = input("Entrez un nombre: ")
    try:
        user_int = int(user_input)
    except ValueError:
        print("invalid value")
    else:
        valid_int = True

print("Vous avez entré", user_int)

### Ask the User the choose a filename in articles/
### And then print its content
### If the file does not exist, ask the user again.
### Using try and except.

def show_article():
    ask_again = True
    content = ""
    while ask_again:
        fname = input("Enter article name: ")
        file_path = Path("../../../1_blog/articles") / (fname + ".md")
        try:
            content = file_path.read_text()
        except FileNotFoundError:
            print("invalid filename")
        else:
            ask_again = False
    print(content)
