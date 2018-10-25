
import os
import csv

inputfilepath = os.path.join("Resources/election_data.csv")
outfilepath = os.path.join("Resources/output.txt")

with open(inputfilepath,"r") as inputfile :

    records = csv.reader(inputfile, delimiter=',')
    next(records)
    #allRows = list(records)
    electionDict = {}
    count = 0
    for row in records:
        count +=1

        if electionDict.get(row[2]) is not None:
            i = int(electionDict.get(row[2]))
            i +=1
            electionDict[row[2]] = i
        else:
            electionDict[row[2]] = 1

    print(electionDict)
    row1 = "Election Results"
    row2 = "-------------------------------"
    row3 = f"Total Votes : {count}"
    row4 = ""
    winner = ""
    for k,v in electionDict.items():
        winPercent = (v * 100)/count
        row4 += f"{k} : {round(winPercent,4)}% ({v})\n"
        if v == max(list(electionDict.values())):
            winner = k

    row5 = f"Winner: {winner}" 

    print(row1 + "\n" + row2 + "\n" + row3 + "\n" + row2 + "\n" + row4 + row2 + "\n" + row5 + "\n" + row2)

    with open(outfilepath,"w") as outfile :

        outfile.write(row1 + "\n" + row2 + "\n" + row3 + "\n" + row2 + "\n" + row4 + row2 + "\n" + row5 + "\n" + row2)


   

