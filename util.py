import pandas as pd
import uuid
import os
import time
import classifier

clf = classifier.classifier()


def createDirs() -> None:
    try:
        if not os.path.exists("data"):
            print(f"[INFO] Creating data directory")
            os.mkdir("data")

        if not os.path.exists("data/raw"):
            print(f"[INFO] Creating data/raw directory")
            os.mkdir("data/raw")

        if not os.path.exists("data/processed"):
            print(f"[INFO] Creating data/processed directory")
            os.mkdir("data/processed")

        return None

    except Exception as e:
        print(f"Error creating directories: {e}")
        return str(e)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"Attribute {name} not found")

    def __setattr__(self, name, value):
        self[name] = value

    def __str__(self) -> str:
        return super().__str__()


def genUUID() -> str:
    return uuid.uuid4().hex


def formatTime(response_time: float):
    milliseconds = round(response_time * 1000, 2)
    response_time_formatted = f"{milliseconds} ms"
    return response_time_formatted


def parseCSV(job: AttrDict, csv: str) -> (pd.DataFrame, str):
    try:
        err = saveCSV(job, csv)
        if (err != None):
            return None, err

        df = pd.read_csv(f"./data/raw/job-{job.id}.csv")

        headers = df.columns.values.tolist()
        print(headers)

        pred = clf.predict(headers)
        print(pred)

        return (df, pred), None

    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return None, str(e)


def saveCSV(job: AttrDict, df: pd.DataFrame) -> str:
    try:

        if isinstance(df, pd.DataFrame):
            df.to_csv(f"./data/processed/job-{job.id}.csv")
            return None

        if isinstance(df, str):
            with open(f"./data/raw/job-{job.id}.csv", "w") as f:
                f.write(df)
            return None

        return "Invalid data type"

    except Exception as e:
        print(f"Error saving CSV: {e}")
        return str(e)


def dfToJson(df: pd.DataFrame) -> (list, str):
    try:
        return df.to_dict(orient="records"), None

    except Exception as e:
        print(f"Error converting dataframe to json: {e}")
        return None, str(e)
