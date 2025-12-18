import csv 
import time

class Action:
    """ Class that represents an action """
    def __init__(self, name, cost, benefits_pourcent):
        """ 
        Args :
            name : Name of the action (Action-1, etc...) 
            cost : Represent the cost of the action in centimes
            benefits_pourcent : Represent the pourcent of benefits after 2 years
            benefits_centimes : Use benefits_pourcent and cost to calculate and represent the value in euros of benefits after 2 years
        """
        self.name = name
        self.cost = int(cost)
        self.benefits_pourcent = float(benefits_pourcent.replace("%", ""))

    @property
    def cost_centimes(self) :
        return int(self.cost*10)
        
    @property
    def benefits_centimes(self):
        return int(self.benefits_pourcent * self.cost_centimes / 100)
        
    @property
    def benefits_euros(self):
        return round(float(self.benefits_pourcent * self.cost / 100), 2)


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
            benefits = row[2]
            if float(cost) > 0 :
                all_actions.append(Action(name, cost, benefits))

    return all_actions

def get_best_combo(budget_euros, all_actions) :
    budget_centimes = budget_euros*10
    matrice = [[0 for x in range(budget_centimes + 1)] for x in range(len(all_actions) + 1)]

    for action_index in range(1, len(all_actions) + 1):
        for actual_budget in range(1, budget_centimes + 1) :
            if all_actions[action_index-1].cost_centimes <= actual_budget :
                matrice[action_index][actual_budget] = max(
                                                            matrice[action_index-1][actual_budget],
                                                            all_actions[action_index-1].benefits_centimes + matrice[action_index-1][actual_budget - all_actions[action_index-1].cost_centimes]
                                                        )
            else :
                matrice[action_index][actual_budget] = matrice[action_index-1][actual_budget]

    actual_budget = budget_centimes
    action_index = len(all_actions)
    best_combo = {
        "actions_list" : [],
        "total_cost" : 0,
        "total_benefits" : matrice[-1][-1]/10
        }

    while actual_budget >= 0 and action_index >= 0 :
        action = all_actions[action_index-1]
        if matrice[action_index][actual_budget] == action.benefits_centimes + matrice[action_index-1][actual_budget - action.cost_centimes] :
            best_combo["actions_list"].append(action)
            best_combo["total_cost"] += action.cost
            actual_budget -= action.cost_centimes
        
        action_index -= 1

    return best_combo


def view_best_combo(best_combo):
    """ Print all the necessary information of the best combo"""
    print("\nList of actions to buy :")
    for action in best_combo["actions_list"] :
        print(
            f"\n> {action.name} :"
            f"\n  Cost : {action.cost}€"
            f"\n  Benefits after 2 years : {action.benefits_euros}€ ({action.benefits_pourcent}%)"
              )
        
    
    print(f"\nTotal cost : {round(best_combo["total_cost"], 2)}€")
    print(f"Total benefits (after 2 years) : {round(best_combo["total_benefits"], 2)}€")
    

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