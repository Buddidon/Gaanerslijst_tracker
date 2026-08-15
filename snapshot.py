import os
import pandas as pd
from datetime import date

SPREADSHEET_ID = "10824RIUe1LPg4vZX3_RSObw300wskd8FpCONvGOB9_U"
GID = 1974762863
URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID}"

DATA_FILE = "data.csv"
HISTORY_FILE = "history_file.csv"


def get_data():
    today = date.today().isoformat()
    try:
        data_today = pd.read_csv(URL)
        data_today["Day"] = today

        data_today.to_csv(DATA_FILE, index=False)

        write_header = not os.path.exists(HISTORY_FILE)
        if os.path.exists(HISTORY_FILE):
            history = pd.read_csv(HISTORY_FILE)
            if today in history["Day"].values:
                print(f"Data for {today} already recorded.")
                return

        data_today.to_csv(HISTORY_FILE, mode="a", header=write_header, index=False)
        print(f"Recorded Gaanerslijst snapshot for {today}.")
    except Exception as exc:
        print(f"ERROR: {exc}")
        raise


def main():
    get_data()


if __name__ == "__main__":
    main()
