import pickle
import pandas as pd


def main():
    with open('knc_model.pkl', 'rb') as mod_file:
        knc = pickle.load(mod_file)
    # Enter the 18 features as input
    input_title = [
        "Aspect",
        "Curvature",
        "Earthquake",
        "Elevation",
        "Flow",
        "Lithology",
        "NDVI",
        "NDWI",
        "Plan",
        "Precipitation",
        "Profile",
        "Slope",
        "temperature",
        "humidity",
        "rain",
        "moisture",
        "pressure"
    ]
    landslide_input = [
        2, 3.333333333, 1.666666667, 4, 2.666666667, 2.333333333, 3, 2.666666667, 3, 2.666666667, 2.666666667, 2.333333333, 18.21255, 84.33422333, 26668.91667, 31.24853333, 1017.904157
    ]
    df = pd.DataFrame(data=[landslide_input], columns=input_title)
    res = knc.predict(df)[0]
    if (res == 0):
        print("Landslide didn't occur")
    else:
        print("Landslide occured ")


if (__name__ == "__main__"):
    main()
