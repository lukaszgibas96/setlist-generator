import csv

def main():

    songs = []

# Create python database - list of dictionaries
    with open("songs.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append({"number": row["number"], "title": row["title"], "duration": row["duration"]})

    for row in songs:
            if row["number"] == "2":
                print(row["title"])
    
    setlist = input_setlist()
    print(setlist)


def input_setlist():
    input_setlist = []
    input_setlist.append(int(input("Choose first song: ")))
    x = 1
    while x != 0:
        if not x == 0:
            x = int(input("Choose next song: "))
            input_setlist.append(x)

    return input_setlist

        
    print(f"setlista to {input_setlist}")







    

if __name__ == "__main__":
    main()
