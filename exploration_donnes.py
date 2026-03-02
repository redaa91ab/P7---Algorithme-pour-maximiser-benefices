import pandas as pandas

data = pandas.read_csv("dataset1.csv")

data_sorted = data.sort_values(by="price", ascending=False)

data_trash =  data[data["price"] <= 0]

print(data_trash, , "\n", len(data_trash), " rows")
