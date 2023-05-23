import csv

fieldnames = [
    "Rain",
    "Moisture",
    "X",
    "Y",
    "Z",
]

fieldnamesForTrainignAI = [*fieldnames, "Target"]


def makeFile(file_name="incoming.csv", isTrainingData=False):
    with open(file_name, "w") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnamesForTrainignAI if isTrainingData else fieldnames,
        )
        csv_writer.writeheader()


def writeData(Input, file_name="incoming.csv"):
    with open(file_name, "a+", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        try:
            info = {
                "Rain": Input[0],
                "Moisture": Input[1],
                "X": Input[2],
                "Y": Input[3],
                "Z": Input[4],
            }
            csv_writer.writerow(info)
        except IndexError:
            print("No suficcient elemets")
        except TypeError:
            print("None type object cannot be saved")


def writeTrainingData(Input, Color, file_name="trainingData.csv"):
    with open(file_name, "a+", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesForTrainignAI)
        infoWithTarget = {
            "Rain": Input[0],
            "Moisture": Input[1],
            "X": Input[2],
            "Y": Input[3],
            "Z": Input[4],
            "Target": Color,
        }
        try:
            csv_writer.writerow(infoWithTarget)
        except IndexError:
            print("No suficcient elemets")
        except TypeError:
            print("None type object cannot be saved")
