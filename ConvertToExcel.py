import pandas as pd
import sys

filename = sys.argv[1]
out = sys.argv[2]

df = pd.read_csv(filename)

df.to_excel(out)