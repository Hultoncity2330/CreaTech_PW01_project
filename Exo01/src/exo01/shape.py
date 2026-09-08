success = 0
shape = ""
valid_shapes = ["triangle", "square", "circle", "ellipse"]

while not success:
    shape = input("Enter a shape : ")
    if shape in valid_shapes:
        success = 1
    else:
        print("Invalid shape")
        print("The valid shapes are :")
        for elt in valid_shapes:
            print(f"- {elt}")


print(f"You chose {shape}.")