from crew_assembler.assembler import Assembler


def main():
    print("\n\nwelcome to Crew Assembler, by hex benjamin!\n")
    print("+ + + ⬡ + + +\n")
    crew = Assembler(config_path="./tomltests/example.toml")
    result = crew.run()
    print("\n+ + + ⬡ + + +")
    print("RUN RESULTS :")
    print("+ + + ⬡ + + +\n")
    print(result + "\n\n")


if __name__ == "__main__":
    main()
