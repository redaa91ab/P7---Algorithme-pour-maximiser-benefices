import pandas as pandas

data = pandas.read_csv("dataset2.csv")
#print(data)

data_clean = data[(data["price"] > 0) & (data["profit"] > 0)]

data_trash =  data[data["price"] <= 0]
#print(data_trash, "\n", len(data_trash), " rows")

price_data_sorted = data_clean.sort_values(by="price", ascending=False)
#print(price_data_sorted)

moyenne_price = data_clean["price"].mean()
#print(moyenne_price)

mediane_price = data_clean["price"].median()
#print(mediane_price)

ecart_type_price = data_clean["price"].std()
#print(ecart_type_price)

profit_data_sorted = data_clean.sort_values(by="profit", ascending=False)
#print(profit_data_sorted)

moyenne_profit = data_clean["profit"].mean()
#print(moyenne_profit)

mediane_price = data_clean["profit"].median()
#print(mediane_price)

ecart_type_profit = data_clean["profit"].std()
print(ecart_type_profit)