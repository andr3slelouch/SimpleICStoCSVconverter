import wget
import os
import csv

def addEvent(header, filename):
    f = open("mycalendar.ics", "r")
    f2 = open("calendar.csv", "w+")
    f1 = f.readlines()
    header = ["BEGIN", "UID", "SUMMARY", "DESCRIPTION", "CLASS",
               "LAST-MODIFIED", "DTSTAMP", "DTSTART", "DTEND", "CATEGORIES"]
    for x in header:
        f2.write(x + ";")
    f2.write("\n")
    wrBegin = False
    wrNormal = False
    wrDescription = False
    for x in f1:
        # print(x)
        # print(str(x.count('\t'))+"---"+x)
        list = x.split(":", 1)
        if list[0] == "BEGIN" and list[1] == "VEVENT\n":
            wrNormal = True
            wrBegin = True
            list[1] = "VEVENT"
            # print(list[1])
        elif list[0] == "DESCRIPTION":
            wrDescription = True
            f2.write("\"")
            # print(list[0])
        elif list[0] == "CLASS":
            wrDescription = False
            f2.write("\"" + ";")
            # print(list[0])
        elif list[0] == "END" and list[1] == "VEVENT\n":
            wrNormal = False
            # print(list[0])
        else:
            ""
        if wrNormal and wrDescription == False:
            removebsn = list[1].split("\n", 1)
            f2.write(removebsn[0] + ";")
        elif wrNormal and wrDescription:
            for y in list:
                new_list = {x.replace('\n', '').replace('\t', '')
                            for x in list}
                for x in new_list:
                    f2.write(x)
        elif wrNormal == False and wrBegin:
            f2.write("\n")


def convertICStoCSV():
    print("Empezando:")
    print("Eliminando si existe")
    filename = "mycalendar.ics"
    if os.path.exists(filename):
        os.remove(filename)
    url = ""
    wget.download(url, "mycalendar.ics")


def findHeader(icsCal):
    f = open(icsCal, "r")
    print("Looking for headers in this file....")
    f2 = open("calendar.csv", "w+")
    checker = 0
    f1 = f.readlines()
    wrBegin = False # Flag to detect the line BEGIN:VEVENT
                    # , and start saving the parameters of the event
                    # in this case is for getting the headers for the CSV
    wrNormal = False
    wrDescription = False # Saving a description that could be large
    for x in f1:
        # print(x)
        # print(str(x.count('\t'))+"---"+x)
        #headers = []
        list = x.split(":", 1)
        chars = [c for c in list[0]]
        if list[0] == "BEGIN" and list[1] == "VEVENT\n": # Looking for the line that begins an event
            wrNormal = True
            wrBegin = True
        elif list[0] == "DESCRIPTION": # Looking for the line where the description begins to activate its flag
            wrDescription = True
        elif chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n': # If the lines are not beginning  with an space or an "\t", means that is another tag and not currently a decription, but it can change
            wrDescription = False


        if list[0] == "END": # If the event comes to its end the flag deactivates
            wrNormal = False
        else:
            ""


        if wrNormal == False and wrBegin == True: # If all of the headers are reached it only writes and \n and stops the for loop
            f2.write("END\n")
        elif wrNormal and wrDescription == False: # Everything that can be and tag inside an event is appended to the list, but if the events are irregulars this can cause errors
            f2.write(list[0] + ";")
        elif wrNormal and wrDescription:
            if list[0] == "DESCRIPTION":
                f2.write(list[0] + ";")

    f2.close()
    listHeaders = []

    with open("calendar.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            listHeaders.append(row)

    filename="calendar.csv"
    if os.path.exists(filename):
        os.remove(filename)
    return max(listHeaders,key=len)

def main():
    print(findHeader("icsExamples/US_Holidays.ics"))
    #addEvent(findHeader("icsExamples/US_Holidays.ics"), "icsExamples/US_Holidays.ics")

if __name__== "__main__":
  main()
