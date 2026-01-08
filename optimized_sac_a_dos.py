import csv
import time


class Action:
    """ Class that represents an action """
    def __init__(self, name, cost_euros, benefits_pourcent):
        """
        Args :
            name : Name of the action
            cost_euros : Cost of the action, in euros
            benefits_pourcent : Benefits of the action, in pourcent
            benefits_euros : Benefits of the action, in euros
        """
        self.name = name
        self.cost_euros = float(cost_euros)
        self.benefits_pourcent = float(benefits_pourcent.replace("%", ""))

    @property
    def benefits_euros(self):
        """ Benefits of the action, in euros """
        return self.benefits_pourcent*self.cost_euros / 100

    @property
    def cost_centimes(self):
        """ Cost of the action, in centimes """
        return int(self.cost_euros * 100)

    @property
    def benefits_centimes(self):
        """ Benefits of the action, in centimes """
        return self.benefits_pourcent*self.cost_centimes / 100

    @classmethod
    def format_number(self, number):
        """ Return number without .0 if it's integer, or round to 2 if it's a float"""
        return int(number) if number.is_integer() else round(number, 2)


def get_all_actions():
    """
    Return a list of all the CSV actions as instances of the Action class
    Process : Open a csv file, create an instance of Action class for each line that represent an action,
    and add it to the "all_actions" list
    """
    all_actions = []
    with open('dataset1.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            name = row[0]
            cost_euros = row[1]
            benefits_pourcent = row[2]
            if float(cost_euros) > 0:
                all_actions.append(Action(name, cost_euros, benefits_pourcent))

    return all_actions


def get_best_combo(budget_euros, all_actions):
    """
    Determines the optimal combination of actions maximizing benefits without exceeding budget by using
    the knapsack algorithm trough a matrice.

    Args:
        budget_euros (int): Available budget in euros.
        all_actions (list): List of instances of the Action class

    Returns:
        dict: {
            "actions_list": list of selected actions
            "total_cost_euros": total cost of selected actions,
            "total_benefits_euros": total benefits of selected actions
        }
    """

    budget_centimes = budget_euros * 100
    matrice = [[0 for x in range(budget_centimes + 1)] for x in range(len(all_actions) + 1)]

    for action_index in range(1, len(all_actions) + 1):
        action_cost_centimes = all_actions[action_index - 1].cost_centimes
        action_benefits_centimes = all_actions[action_index - 1].benefits_centimes
        for actual_budget in range(1, budget_centimes + 1):
            if action_cost_centimes <= actual_budget:
                matrice[action_index][actual_budget] = max(
                                                matrice[action_index-1][actual_budget],
                                                action_benefits_centimes
                                                + matrice[action_index - 1][actual_budget - action_cost_centimes]
                                                )
            else:
                matrice[action_index][actual_budget] = matrice[action_index - 1][actual_budget]

    actual_budget = budget_centimes
    action_index = len(all_actions)
    best_combo = {
        "actions_list": [],
        "total_cost_euros": 0,
        "total_benefits_euros": 0
        }

    while actual_budget >= 0 and action_index >= 0:
        action = all_actions[action_index - 1]
        if matrice[action_index][actual_budget] == (
            action.benefits_centimes
            + matrice[action_index - 1][actual_budget - action.cost_centimes]
        ):
            best_combo["actions_list"].append(action)
            best_combo["total_cost_euros"] += action.cost_euros
            actual_budget -= action.cost_centimes
        action_index -= 1

    for action in best_combo["actions_list"]:
        best_combo["total_benefits_euros"] += action.benefits_euros

    return best_combo


def view_best_combo(best_combo):
    """ Print all the necessary information of the best combo """
    print("\nList of actions to buy :")
    for action in best_combo["actions_list"]:
        print(
            f"\n> {action.name} :"
            f"\n  Cost : {Action.format_number(action.cost_euros)}€"
            f"\n  Benefits after 2 years : {Action.format_number(action.benefits_euros)}€"
            f"({Action.format_number(action.benefits_pourcent)}%)"
              )
    print(f"\nTotal cost : {Action.format_number(best_combo["total_cost_euros"])}€")
    print(f"Total benefits (after 2 years) : {Action.format_number(best_combo["total_benefits_euros"])}€")


def timer(func):
    """ Record the process time of a function """
    def wrapper():
        start_time = time.time()
        result = func()
        end_time = time.time() - start_time
        print(f"\nTime : {end_time} seconds")
        return result
    return wrapper


@timer
def run():
    """
    Main entry
    """
    all_actions = get_all_actions()
    best_combo = get_best_combo(500, all_actions)
    view_best_combo(best_combo)


run()
