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
    
    setlist = get_setlist_from_user()
    print(setlist)


def get_setlist_from_user():
    setlist = []
    x = int(input("Choose first song: "))

    while x != 0:
        setlist.append(x)
        x = int(input("Choose next song: "))

    return setlist

        
    print(f"setlista to {input_setlist}")







    

if __name__ == "__main__":
    main()
