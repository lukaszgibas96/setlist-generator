
def check_duration_format(duration):

    try:
        minutes,seconds = duration.split(":")
        print(minutes)
        print(seconds)
        if int(minutes) > 0 and not minutes.startswith("0"):
            if 0 < int(seconds) < 60:
                return True
            return False
        return False
    except ValueError:
        return False


test = check_duration_format(" 1:223 ")
print(test)