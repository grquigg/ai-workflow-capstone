import json
import glob
import pandas as pd
def load_data(pathname):
#load data
    data = []
    for filename in glob.glob(f"{pathname}/*.json"):
        with open(filename, "r") as file:
            for line in file:
                entry = json.loads(line)
                data += entry
    df = pd.DataFrame(data)
    return df
