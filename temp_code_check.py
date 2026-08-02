
def convert_time_to_sec(str_time):
     minutes, seconds = str_time.split(":")
     total = int(minutes) * 60 + int(seconds)
     return total

time = convert_time_to_sec("1:00")
print(time)
