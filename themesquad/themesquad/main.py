def hello():
    name = input(" >  What your name is? | ")
    print(f"\n >  Hello, {name or 'Jeff'}!\n\t-- themesquad")


if __name__ == "__main__":
    hello("Jeff")
