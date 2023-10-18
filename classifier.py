from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import time
import classes


class classifier:
    def __init__(self):
        self.load()

    def load(self):
        st = time.time()
        date = ["date", "Date", "DATE", "dates", "Dates", "DATES"]

        accountName = ["accountName", "AccountName", "ACCOUNTNAME", "accountname", "Accountname", "ACCOUNTNAME"]

        accountType = ["accountType", "AccountType", "ACCOUNTTYPE"]

        accountNumber = ["accountNumber", "AccountNumber", "ACCOUNTNUMBER", "accountnumber", "Accountnumber", "ACCOUNTNUMBER"]

        credit = ["credit", "Credit", "CREDIT"]

        debit = ["debit", "Debit", "DEBIT"]

        amount = ["amount", "Amount", "AMOUNT"]

        description = ["description", "Description", "DESCRIPTION"]

        balance = ["balance", "Balance", "BALANCE"]

        columns = [
            ('date', date),
            ('accountName', accountName),
            ('accountType', accountType),
            ('accountNumber', accountNumber),
            ('credit', credit),
            ('debit', debit),
            ('amount', amount),
            ('description', description),
            ('balance', balance)
        ]

        column_name = [item for col, sublist in columns for item in sublist]
        label = [col for col, sublist in columns for _ in sublist]

        data = pd.DataFrame({
            'column_name': column_name,
            'label': label
        })

        self.model = Pipeline([
            ('vectorizer', CountVectorizer(analyzer='char', ngram_range=(1, 3))),
            ('classifier', LogisticRegression())
        ])

        self.model.fit(data['column_name'], data['label'])
        delta = time.time() - st
        print(f"[INFO] Model loaded successfully in {round(delta, 3)} seconds")

    def predict(self, column_names: List[str]) -> Tuple[Dict, str]:
        try:
            inputs = column_names.copy()
            map = {col_name: orig for col_name, orig in zip(column_names, inputs)}

            column_names = [col_name.lower()for col_name in column_names]

            results = {"success": True, "predictions": []}

            if len(column_names) > 0:
                predictions = self.model.predict(column_names)
                probabilities = self.model.predict_proba(column_names)

                for i, col_name in enumerate(column_names):
                    realName = map[col_name]
                    result = classes.AttrDict(
                        {"col_name": realName, "prediction": predictions[i],
                         "confidence": round(np.max(probabilities[i]) * 100, 3),
                         "probabilities": classes.AttrDict({})})

                    for j, label in enumerate(self.model.classes_):
                        result["probabilities"][label] = round(probabilities[i][j] * 100, 3)

                    results["predictions"].append(result)

            return classes.Prediction(results["predictions"]), None

        except Exception as e:
            return None, str(e)
