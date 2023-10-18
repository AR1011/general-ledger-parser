import pandas as pd
import uuid
import os
import time
import classifier
import classes
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


def genUUID() -> str:
    return uuid.uuid4().hex


def formatTime(response_time: float):
    milliseconds = round(response_time * 1000, 2)
    response_time_formatted = f"{milliseconds} ms"
    return response_time_formatted


def parseCSV(job: classes.AttrDict, csv: str) -> (pd.DataFrame, str):
    try:
        err = saveCSV(job, csv)
        if (err != None):
            return None, err

        df = pd.read_csv(f"./data/raw/job-{job.id}.csv")
        df.fillna("", inplace=True)

        headers = df.columns.values.tolist()

        pred, err = clf.predict(headers)
        if (err != None):
            return None, err

        mappings, err = createMappings(df, pred)
        if (err != None):
            return None, err

        df = df.rename(columns=mappings)

        return (df, pred), None

    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return None, str(e)


def saveCSV(job: classes.AttrDict, df: pd.DataFrame) -> str:
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


def createMappings(df: pd.DataFrame, prediction: classes.Prediction) -> (dict, str):
    print(type(prediction.predictions))
    try:
        mappings = {}
        for pred in prediction.predictions:
            mappings[pred.col_name] = pred.prediction
        return mappings, None

    except Exception as e:
        print(f"Error creating mappings: {e}")
        return None, str(e)
