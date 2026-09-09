def choose_from(list_of_valid: list[str], question):
    user_input = input(question)
    if user_input in list_of_valid:
        return user_input
    else:
        return ValueError("Invalid user input")

colors = ["red", "green", "blue"]
try:
    picked = choose_from(colors, "Choose a color : ")
except ValueError:
    print("There was an error")
else: # If everything went well
    print("You picked", picked)
