from communicate import Communicate, get_value
from writeCsv import writeData, makeFile, writeTrainingData
from processData import processData, isValidData
import time
import keyboard
from firebase import CloudData

port = "COM9"
connected = False
gateway = Communicate(port, 9600)
time.sleep(1)

if gateway.handshake():
    connected = True
    print("Connected")
else:
    print(" Not Connected")


def conditionAlert(data):
    magenta = 35
    red = 10
    Rain, Moisture, X, Y, Z = data
    if X > magenta or Y > magenta or Z > magenta:
        gateway.magenta()
        print("Magenta")
        return "magenta"
    elif X > red or Y > red or Z > red:
        gateway.red()
        print("Red")
        return "red"
    elif Rain > 25 or Moisture > 100:
        gateway.orange()
        print("Orange")
        return "orange"
    elif Rain > 10 or Moisture > 70:
        gateway.yellow()
        print("Yellow")
        return "yellow"
    elif Rain > 10 or Moisture > 66:
        gateway.green()
        print("Green")
        return "green"
    else:
        gateway.white()
        print("White")
        return "white"


cloud = CloudData("/")

if connected:
    makeFile()
    valdiDataCount = 0  # count of valid data
    calDataCount = 20  # for calibration
    while True:
        try:
            Input = get_value(gateway)
            # print(Input)
            if isValidData(Input):
                writeData(Input)
                valdiDataCount += 1
                if valdiDataCount == 20:
                    makeFile("processedData.csv")
                    pass
                if valdiDataCount > 25:
                    processedData = processData(valdiDataCount - 1, calDataCount)
                    print(processedData)
                    Color = conditionAlert(processedData)
                    # for re-calibration (gyroscope data)
                    cTime = round(time.time())
                    print("Uploading to firebase")
                    cloud.upload(processedData, Color, cTime)
                    print("Uploaded!")
                    try:
                        if keyboard.is_pressed("c"):
                            print("Re-Callibrating...")
                            calDataCount = valdiDataCount - 1
                    except:
                        pass
                else:
                    gateway.loading()
                    print("Callibrating...")

            time.sleep(0.2)
        except IndexError:
            print("No suficcient elemets")
        except KeyboardInterrupt:
            gateway.close()
            break
        except:
            print("Error")
            break
