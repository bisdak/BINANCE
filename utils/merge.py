import pandas as pd
import sys

csv1 = sys.argv[1]
csv2 = sys.argv[2]
id = sys.argv[3]


df1 = pd.read_csv(csv1, encoding='utf8')
df2 = pd.read_csv(csv2, encoding='utf8')

final = pd.merge(df1, df2, on=id, how='left') 

final.to_csv('final.csv', sep="\t")

