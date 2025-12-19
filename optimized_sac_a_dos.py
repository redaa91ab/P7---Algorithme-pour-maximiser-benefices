import csv 
import time

class Action:
    """ Class that represents an action """
    def __init__(self, name, cost, benefits_pourcent):
        """ 
        Args :
            name : Name of the action (Action-1, etc...) 
            cost : Cost of the action in euros
            benefits_pourcent : Pourcent of benefits after 2 years
            benefits_euros : Benefits in euros after 2 years
        """
        self.name = name
        self.cost = float(cost)
        self.benefits_pourcent = float(benefits_pourcent.replace("%", ""))
        self.benefits_euros = self.benefits_pourcent * self.cost / 100


    @property
    def units(self):
        return int(self.cost*100)

    @property
    def benefits_units(self):
        return self.benefits_pourcent * self.units / 100
    
    @classmethod
    def format_number(self, number):
        """Return number without .0 if it's integer"""
        return int(number) if number.is_integer() else round(number, 2)


def get_all_actions():
    """
    Return a list of Action objects
    Process : Open a csv file, then create an instance of Action class for each line that represent an action, and add it to the list "all_actions" 
    """
    all_actions = []
    with open('dataset1.csv', mode='r') as csv_file :
        csv_reader = csv.reader(csv_file) 
        next(csv_reader)
        for row in csv_reader :
            name = row[0]
            cost = row[1]
            benefits_pourcent = row[2]
            if float(cost) > 0 :
                all_actions.append(Action(name, cost, benefits_pourcent))

    return all_actions

def get_best_combo(budget_euros, all_actions) :
    budget_units = budget_euros * 100
    matrice = [[0 for x in range(budget_units + 1)] for x in range(len(all_actions) + 1)]

    for action_index in range(1, len(all_actions) + 1):
        action_unit = all_actions[action_index-1].units
        action_benefits_units = all_actions[action_index-1].benefits_units
    
        for actual_budget in range(1, budget_units + 1) :
            if action_unit <= actual_budget :
                matrice[action_index][actual_budget] = max(
                                                            matrice[action_index-1][actual_budget],
                                                            action_benefits_units + matrice[action_index-1][actual_budget - action_unit]
                                                            )
            else :
                matrice[action_index][actual_budget] = matrice[action_index-1][actual_budget]

    actual_budget = budget_units
    action_index = len(all_actions)
    best_combo = {
        "actions_list" : [],
        "total_cost" : 0,
        "total_benefits" : 0
        }

    while actual_budget >= 0 and action_index >= 0 :
        action = all_actions[action_index-1]
        if matrice[action_index][actual_budget] == action.benefits_units + matrice[action_index-1][actual_budget - action.units] :
            best_combo["actions_list"].append(action)
            best_combo["total_cost"] += action.cost
            actual_budget -= action.units
        action_index -= 1

    for action in best_combo["actions_list"] :
        best_combo["total_benefits"] += action.benefits_euros

    return best_combo


def view_best_combo(best_combo):
    """ Print all the necessary information of the best combo"""
    print("\nList of actions to buy :")
    for action in best_combo["actions_list"] :
        print(
            f"\n> {action.name} :"
            f"\n  Cost : {Action.format_number(action.cost)}€"
            f"\n  Benefits after 2 years : {Action.format_number(action.benefits_euros)}€ ({Action.format_number(action.benefits_pourcent)}%)"
              )
        
    print(f"\nTotal cost : {Action.format_number(best_combo["total_cost"])}€")
    print(f"Total benefits (after 2 years) : {Action.format_number(best_combo["total_benefits"])}€")
    

def timer(func):
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