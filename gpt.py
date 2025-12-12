import csv
import time

# ============================================================
# ACTION CLASS
# ============================================================

class Action:
    """ Class representing an action """
    def __init__(self, name, cost, benefits_pourcent):
        self.name = name
        self.cost = float(cost)
        self.benefits_pourcent = float(benefits_pourcent.replace("%", ""))

    @property
    def benefits_euros(self):
        """
        Represent cost in units of 0.1€ to reduce DP size
        Example:
            12.3€ -> 123 units
        """
        return self.benefits_pourcent * self.cost / 100

    @property
    def cost_units(self):
        """
        Represent cost in units of 0.1€ to reduce DP size
        Example:
            12.3€ -> 123 units
        """
        return int(round(self.cost * 10))

    @property
    def benefits_units(self):
        """
        Benefits in same units (0.1€)
        """
        return int(self.benefits_pourcent * self.cost_units / 100)


# ============================================================
# LOAD DATA
# ============================================================

def get_all_actions():
    all_actions = []
    with open('dataset1.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip header
        for row in csv_reader:
            name, cost, benefits = row
            if float(cost) > 0:
                all_actions.append(Action(name, cost, benefits))
    return all_actions


# ============================================================
# OPTIMIZED KNAPSACK (1D DP + BACKTRACK)
# ============================================================

def get_best_combo(budget_euros, all_actions):

    # Budget converted to 0.1€ units:
    # 500€ -> 5000 units
    budget_units = int(budget_euros * 10)

    dp = [0] * (budget_units + 1)
    choice = [[False] * (budget_units + 1) for _ in range(len(all_actions))]

    # ---------------- DP FILL ----------------
    for i, action in enumerate(all_actions):
        cost_u = action.cost_units
        benefit_u = action.benefits_units

        for b in range(budget_units, cost_u - 1, -1):
            if dp[b] < dp[b - cost_u] + benefit_u:
                dp[b] = dp[b - cost_u] + benefit_u
                choice[i][b] = True

    # ---------------- BACKTRACK ----------------
    best_combo = {
        "actions_list": [],
        "total_cost": 0,
        "total_benefits": 0 #dp[budget_units] / 10  # convert back to euros
    }

    b = budget_units
    for i in range(len(all_actions) - 1, -1, -1):
        if choice[i][b]:
            action = all_actions[i]
            best_combo["actions_list"].append(action)
            best_combo["total_cost"] += action.cost
            b -= action.cost_units

    for penis in best_combo["actions_list"] :
        best_combo["total_benefits"] += penis.benefits_euros

    return best_combo


# ============================================================
# DISPLAY
# ============================================================

def view_best_combo(best_combo):
    print("\nList of actions to buy:")

    for action in best_combo["actions_list"]:
        print(
            f"\n> {action.name}:"
            f"\n  Cost: {action.cost}€"
            f"\n  Benefits after 2 years: {action.benefits_euros}€ ({action.benefits_pourcent}%)"
        )

    print(f"\nTotal cost: {round(best_combo['total_cost'], 2)}€")
    print(f"Total benefits (after 2 years): {round(best_combo['total_benefits'], 2)}€")


# ============================================================
# TIMER DECORATOR
# ============================================================

def timer(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time() - start
        print(f"\nTime: {round(end, 4)} seconds")
        return result
    return wrapper


# ============================================================
# MAIN
# ============================================================

@timer
def run():
    actions = get_all_actions()
    best_combo = get_best_combo(500, actions)
    view_best_combo(best_combo)

run()
