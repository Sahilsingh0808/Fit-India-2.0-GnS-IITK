from flask import Flask, render_template
import pandas as pd
import operator


app = Flask(__name__)


@app.route('/')
def table():

    data = pd.read_csv("cycle.csv")
    name = data["Name"]
    distance = data["Distance"]
    date = data["Date"]
    duration = data["Duration"]
    nameList = {}
    distList = {}
    print(type(nameList))

    for index, row in data.iterrows():
        dateTime = str(row["Date"])
        date = ''
        for i in dateTime:
            if i == ',':
                break
            date += i
        date = date.split(' ')
        date = int(date[1])
        if ((date < 23) and (date > 29)):
            data.drop(data.index[(data["Date"] == dateTime)],
                      axis=0, inplace=True)

    print(type(nameList))
    for i in range(len(name)):
        if name[i] in nameList:
            nameList[name[i]] += 1
            distList[name[i]] += distance[i]
        else:
            nameList[name[i]] = 1
            distList[name[i]] = distance[i]

    distList = sorted(distList.items(), key=operator.itemgetter(0))
    nameList = sorted(nameList.items(), key=operator.itemgetter(0))

    print((nameList))
    print()
    print((distList))

    print(type(nameList))

    nameL = []
    distL = []
    roundsL = []

    for i in range(len(nameList)):
        nameL.append(nameList[i][0])
        distL.append(distList[i][1])
        roundsL.append(nameList[i][1])

    dataDict = {'Name': nameL, 'Distance': distL, 'Rounds': roundsL}

    df = pd.DataFrame(dataDict)

    df = df.sort_values(by=['Distance'], ascending=False)

    print(type(df.to_html()))

    htmlTable = df.to_html()
    htmlTable = htmlTable[200:]
    htmlTable = htmlTable[:-17]
    # htmlTable.replace("</th>", "</td>")
    # htmlTable.replace("<th>", "<td>")
    print(df.to_html())

    return render_template('index.html', data=htmlTable, heading="FIT INDIA 2.0 Cycling")
