import csv 
from itertools import combinations

class Action:
    """ Class that represents an action """
    def __init__(self, name, cost, benefits_pourcent):
        """ 
        Args :
            name : Name of the action (Action-1, etc...) 
            cost : Represent the cost of the action in euros
            benefits_pourcent : Represent the pourcent of benefits after 2 years
            benefits_euros : Use benefits_pourcent and cost to calculate and represent the value in euros of benefits after 2 years
        """
        self.name = name
        self.cost = int(cost)
        self.benefits_pourcent = int(benefits_pourcent.replace("%", ""))
        self.benefits_euros = self.benefits_pourcent * self.cost / 100


def get_all_actions():
    """
    Return a list of Action objects
    Process : Open a csv file, then create an instance of Action class for each line that represent an action, and add it to the list "all_actions" 
    """
    all_actions = []
    with open('actions_list.csv', mode='r') as csv_file :
        csv_reader = csv.reader(csv_file) 
        next(csv_reader)
        for row in csv_reader :
            name = row[0]
            cost = row[1]
            benefits = row[2]
            all_actions.append(Action(name, cost, benefits))

    return all_actions

def get_best_combo(all_actions):
    """
    Return the best combination of actions from the list all_actions
    Process : Use the method combination from itertools to loop every possible combinations, if the actual combo is better than the best_combo: replace it
    """

    best_combo = {
        "actions_list" : None,
        "total_cost" : 0,
        "total_benefits" : 0
        }
    for repetitions in range(20) :
        for actions_list in combinations(all_actions, repetitions) :
            total_cost = 0
            total_benefits = 0
            for action in actions_list : 
                total_cost += action.cost
                total_benefits += action.benefits_euros
            if total_cost < 500 and total_benefits > best_combo["total_benefits"] :
                best_combo["actions_list"] = actions_list
                best_combo["total_cost"] = total_cost
                best_combo["total_benefits"] = round(total_benefits, 2)

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
    print(f"\nTotal cost : {best_combo["total_cost"]}€")
    print(f"Total benefits (after 2 years) : {best_combo["total_benefits"]}€")

def run():
    """
    Main entry
    """
    all_actions = get_all_actions()
    best_combo = get_best_combo(all_actions)
    view_best_combo(best_combo)

run()
    

        
