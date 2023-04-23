import pandas as pd


def load():
    airport_data = pd.read_csv("data/Airports.csv")
    airport_data.to_pickle("data/flights.pkl")


if __name__ == '__main__':
    load()
    flights = pd.read_pickle("data/flights.pkl")
    print(flights.head())
