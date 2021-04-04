import datetime
import database

DATETODAY = datetime.date.today()


class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, user_id=None, name=None, weight=None, goal=None, height=None,
                 weight_history=None):
        self.user_id = user_id
        self.user_name = name
        self.weight = weight
        self.height = height
        self.goal = goal
        self.bmi = None
        self.weight_history = weight_history

    def user_setup(self, person_name=None, weight=None, goal=None, height=None):
        if person_name != None:
            self.user_name = str(person_name.text())
            print(f'Name is {person_name.text()}')
        if weight != None:
            self.weight = float(weight.text())
            print(f'Current weight is {weight.text()}')
        if goal != None:
            self.goal = float(goal.text())
            print(f'Weight goal is {goal.text()}')
        if height != None:
            self.height = int(height.text())
            print(f'Height is {height.text()}')

    def set_name(self, name):
        self.user_name = name

    def set__weight(self, weight):
        self.weight = weight

    def set_goal_weight(self, weight):
        self.goal = weight

    def set_height(self, height):
        self.height = height

    def convert_height_metric(self):
        height_metric = self.height * 2.54
        return height_metric

    def convert_weight_metric(self):
        weight_metric = self.weight * 0.45359237
        return weight_metric

    def calculate_bmi(self):
        pass

    def user_dict_create(self, name, startingweight, currentweight, height, weight_history=None):
        '''
        Creates a dictionary with all of the user's personal statistics to be serialized as JSON.
        :param name: User's full name
        :param startingweight: The user's starting weight.
        :param currentweight: The user's current weight.
        :param height: The user's height.
        :param weight_history: User's weight history is mapped by date.
        :return Dictionary: a dictionary containing the user's personal statistics.
        '''
        if weight_history == None:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': {
                    str(DATETODAY): currentweight
                }
            }
        else:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': weight_history
            }