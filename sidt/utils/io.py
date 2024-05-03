import csv
import inspect
import os
from dataclasses import asdict, fields


def dump(data, filename):
    # data must be a dataclass object or list of the same dataclass objects

    origin = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    os.makedirs(os.path.join("out", origin), exist_ok=True)
    path = os.path.join("out", origin, filename + ".csv")

    field_names = [f.name for f in fields(data[0])]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for item in data:
            writer.writerow(asdict(item))
