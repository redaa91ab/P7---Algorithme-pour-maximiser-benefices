import csv 

class Action:
    def __init__(self, name, cost, benefits_pourcent):
        self.name = name
        self.cost = int(cost)
        self.benefits_pourcent = int(benefits_pourcent.replace("%", ""))
        self.benefits_euros = self.benefits_pourcent * self.cost / 100
    

def run():
    all_actions = []

    with open('actions_list.csv', mode='r') as csv_file :
        csv_reader = csv.reader(csv_file) 
        next(csv_reader)
        for row in csv_reader :
            name = row[0]
            cost = row[1]
            benefits = row[2]
            all_actions.append(Action(name, cost, benefits))

    for action in all_actions :
        print(action.name, action.cost, action.benefits_pourcent, action.benefits_euros)


run()
        
    

        
