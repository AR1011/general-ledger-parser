from typing import List, Tuple, Dict


class Prediction:
    def __init__(self, predictions: List[Dict]):
        # self.predictions =
        self.predictions = predictions

    def __str__(self):
        return str(self.predictions)


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
