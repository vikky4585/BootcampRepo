
import os
import csv

inputfilepath = os.path.join("Resources/budget_data.csv")
outfilepath = os.path.join("Resources/output.txt")

with open(inputfilepath,"r") as inputfile :

    records = csv.reader(inputfile, delimiter=',')
    next(records)
    allRows = list(records)
    monthset = set()
    total = 0
    previous = 0
    difference = 0
    totaldiff = 0
    diffList = []
    for row in allRows:
        monthset.add(row[0])
        total += float(row[1])
        current = float(row[1])
        if previous !=  0:
            difference = current - previous
            totaldiff += difference
            diffList.append(difference)
        
        previous = float(row[1])
    
    #minRow = [row for x,row in enumerate(records) if x == (diffList.index(min(diffList)))]
    row1 = "Financial Analysis"
    row2 = "-------------------------------------"
    row3 = f"Total Months: {len(monthset)}" 
    row4 = f"Total : {total}"
    row5 = f"Average  Change :$ {totaldiff/(len(monthset) -1)}"
    row6 = f"Greatest Increase in Profits: {allRows[diffList.index(max(diffList)) +1 ][0]} (${max(diffList)})"
    row7 = f"Greatest Decrease in Profits: {allRows[diffList.index(min(diffList)) +1 ][0]} (${min(diffList)})"

    print(row1 + "\n" + row2+ "\n" + row3+ "\n" + row4+ "\n" + row5+ "\n" + row6+ "\n" + row7)

with open(outfilepath,"w") as outfile :

    outfile.write(row1 + "\n" + row2+ "\n" + row3+ "\n" + row4+ "\n" + row5+ "\n" + row6+ "\n" + row7)
