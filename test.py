roman_number = [ 
        {"n": 1, "rn": "I"},
        {"n": 2, "rn": "II"},
        {"n": 3, "rn": "III"},
        {"n": 4, "rn": "IV"},
        {"n": 5, "rn": "V"},
        {"n": 6, "rn": "VI"},
        {"n": 7, "rn": "VII"},
        {"n": 8, "rn": "VIII"},
        {"n": 9, "rn": "IX"},
        {"n": 10, "rn": "X"}
            ]

def main():

    number = input("Number to convert: ").strip()
    if int(number) <=39:
        if 0 < int(number) <= 10:
            convert_number = find_number_of_unit(number)
            print(convert_number)

        else:
            tens = int(number[0])
            ones = int(number[1])

            convert_number = tens * "X" + find_number_of_unit(ones)
            print(convert_number)


def find_number_of_unit(number):
    if int(number) == 0:
        return ""
    
    for row in roman_number:
        if row["n"] == int(number):
            return row["rn"]
        


main()