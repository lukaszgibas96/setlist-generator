import csv

def main():

    songs = load_songs_from_csv()

    num_setlist = get_setlist_from_user()



    setlist , setlist_duration = create_setlist(num_setlist, songs)
    

    print(setlist)
    print(setlist_duration)

    duration = convert_sec_to_time(setlist_duration)
    print(f"Duration: {duration}")




# ---------------------- function definitions


def load_songs_from_csv():

    songs = []
    
    with open("songs.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                songs.append({"number": row["number"], "title": row["title"], "duration": row["duration"]})
    return songs

def get_setlist_from_user():
    setlist = []
    x = int(input("Choose first song: "))

    while x != 0:
        setlist.append(x)
        x = int(input("Choose next song: "))

    return setlist

def create_setlist(user_setlist, dataset):
    setlist = []
    setlist_duration = 0
     
    for song_number in user_setlist:
             
        for row in dataset:
            if row["number"] == str(song_number):
                setlist.append({"number": row["number"], "title": row["title"]})
                setlist_duration += int(convert_time_to_sec(row["duration"]))
    return setlist, setlist_duration

     
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
