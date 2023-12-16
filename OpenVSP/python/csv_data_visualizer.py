filename = input("type csv filename without extension\n>")

with open(f"{filename}.csv") as file:
    data = file.read()


data_dict = {}
for block in data.split("#"):
    content = block.split("\n")
    titles = content[0].split(",")
    if len(titles) > 1:
        lines = content[1:]
        for title, line in zip(titles, lines):
            data_dict[title.strip()] = line
            print(f"{title}: {line}")
        continue
    data_dict[titles[0].strip()] = [[element for element in line.split(",")] for line in content[1:]]
    # print(data_dict[content[0]])

# input()

def gather_data():
    print("Type an key from the list:")
    print("... Ooor type 'exit' to exit\n")
    for key in data_dict.keys():
        print(key)
    response = input()
    if response.lower() == "exit":
        return
    else:
        try:
            print(data_dict[response])
        except KeyError:
            print("Digita direito animal")
            return


while True:
    gather_data()
    challenge = input("type 'S.O.S' to break the loop\n>")
    if challenge == 'S.O.S':
        break
