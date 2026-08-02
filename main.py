import csv

def main():

    songs = []

# Create python database - list of dictionaries
    with open("songs.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append({"number": row["number"], "title": row["title"], "duration": row["duration"]})


    num_setlist = get_setlist_from_user()

    setlist = []
    setlist_duration = 0

    for song_number in num_setlist:
        
        for row in songs:
            if row["number"] == str(song_number):
                  setlist.append({"number": row["number"], "title": row["title"]})
                  setlist_duration += int(convert_time_to_sec(row["duration"]))

    print(setlist)
    print(setlist_duration)

    duration = convert_sec_to_time(setlist_duration)
    print(f"Duration: {duration}")



def get_setlist_from_user():
    setlist = []
    x = int(input("Choose first song: "))

    while x != 0:
        setlist.append(x)
        x = int(input("Choose next song: "))

    return setlist

def convert_time_to_sec(str_time):
     minutes, seconds = str_time.split(":")
     total = int(minutes) * 60 + int(seconds)
     return total

def convert_sec_to_time(sec_time):
    minutes = sec_time // 60
    seconds = sec_time % 60

    return f"{minutes}min {seconds}sec"

    

if __name__ == "__main__":
    main()
