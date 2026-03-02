import pandas as pd

# =========================
# Paramètres
# =========================
BUDGET = 500

# =========================
# Chargement
# =========================
data = pd.read_csv("dataset2.csv")

# Nettoyage
data = data[(data["price"] > 0) & (data["profit"] > 0)].copy()

# Médianes
median_price = data["price"].median()
median_profit = data["profit"].median()

print(f"Médiane des coûts : {median_price:.2f} €")
print(f"Médiane des bénéfices : {median_profit:.2f} €")
print()

# =========================
# Conversion pour DP
# =========================
data["price_int"] = (data["price"] * 100).astype(int)
data["profit_int"] = (data["profit"] * 100).astype(int)

budget_int = BUDGET * 100
n = len(data)

# =========================
# Programmation dynamique
# =========================
dp = [[0] * (budget_int + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    cost = data.iloc[i-1]["price_int"]
    value = data.iloc[i-1]["profit_int"]
    
    for w in range(budget_int + 1):
        if cost <= w:
            dp[i][w] = max(dp[i-1][w],
                           dp[i-1][w - cost] + value)
        else:
            dp[i][w] = dp[i-1][w]

# =========================
# Reconstruction
# =========================
w = budget_int
selected = []

for i in range(n, 0, -1):
    if dp[i][w] != dp[i-1][w]:
        selected.append(data.iloc[i-1])
        w -= data.iloc[i-1]["price_int"]

selected.reverse()

# =========================
# Affichage détaillé
# =========================
print("Actions optimales :\n")

total_cost = 0
total_profit = 0

for row in selected:
    print(f"{row['name']} | Profit: {row['profit']}€ | Cost: {row['price']}€")
    total_cost += row["price"]
    total_profit += row["profit"]

print("\n===== Résumé =====")
print(f"Nombre d'actions : {len(selected)}")
print(f"Coût total : {total_cost:.2f} €")
print(f"Bénéfice total : {total_profit:.2f} €")