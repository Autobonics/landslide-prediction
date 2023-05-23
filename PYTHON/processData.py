from writeCsv import writeData
import pandas as pd


def processData(count, calCount):
    try:
        data = pd.read_csv("incoming.csv")
        Rain = getRainOrMositureAvg(data, count, "Rain")
        Moisture = getRainOrMositureAvg(data, count, "Moisture")
        X = getGyroscopeAvg(data, calCount, count, "X")
        Y = getGyroscopeAvg(data, calCount, count, "Y")
        Z = getGyroscopeAvg(data, calCount, count, "Z")
        writeData(
            [Rain, Moisture, X, Y, Z],
            "processedData.csv",
        )
        return [Rain, Moisture, X, Y, Z]
    except:
        pass


def getGyroscopeAvg(
    data,
    count,
    calCount,
    name,
):
    return abs(
        data[calCount - 20 : calCount][name].mean()
        - data[count - 5 : count][name].mean()
    )


def getRainOrMositureAvg(data, count, name):
    return abs(data[count - 20 : count][name].mean())


def isValidData(Input):
    try:
        if (
            Input[0] == 0
            and Input[1] == 0
            and Input[2] == 0
            and Input[3] == 0
            and Input[4] == 0
        ):
            print("No nodes connected")
            return False
        else:
            return True
    except IndexError:
        return False
