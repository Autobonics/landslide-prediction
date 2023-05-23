from communicate import Communicate, get_value
from writeCsv import writeData, makeFile
from processData import processData, isValidData
# from onnxRun import predict
import time
import keyboard
from predict import predict

port = "COM8"
connected = False
gateway = Communicate(port, 9600)
time.sleep(1)

if gateway.handshake():
    connected = True
    print("Connected")
else:
    print(" Not Connected")


def predictColor(processedData):
    # colros in the order of the index of ml model (can be obtained by running the model using training data)
    # colors = ["green", "magenta", "orange", "red", "white", "yellow"]
    # index = predict(processedData)
    # return colors[index]
    landSlideData = [ 2, 3.333333333, 1.666666667, 4, 2.666666667, 2.333333333, 3, 2.666666667, 3, 2.666666667, 2.666666667, 2.333333333, 18.21255, 84.33422333, processedData[0], processedData[1], 1017.904157]
    isLandslide = predict(landSlideData) 
    if(isLandslide):
        return "red"
    else:
        return "white"


def setGatewayColor(gateway, color="white"):
    if color == "white":
        gateway.white()
    elif color == "green":
        gateway.green()
    elif color == "yellow":
        gateway.blue()
    elif color == "orange":
        gateway.orange()
    elif color == "red":
        gateway.red()
    elif color == "magenta":
        gateway.magenta()
    else:
        gateway.white()


if connected:
    makeFile()
    valdiDataCount = 0  # count of valid data
    calDataCount = 20  # for calibration
    processedDataCount = 0
    while True:
        try:
            Input = get_value(gateway)
            # print(valdiDataCount)
            if isValidData(Input):
                writeData(Input)
                valdiDataCount += 1
                if valdiDataCount == 20:
                    makeFile("processedData.csv")
                    pass
                if valdiDataCount > 25:
                    processedData = processData(valdiDataCount - 1, calDataCount)
                    print(processedData)
                    # Prediction
                    color = predictColor(processedData)
                    # Alerting
                    setGatewayColor(gateway, color)

                    try:
                        # for re-calibration (gyroscope data)
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
