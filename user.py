class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, name=None, weight=None, goal=None, height=None,
                 weight_history=None):
        self.user_id = 1
        self.name = name
        self.weight = weight
        self.height = height
        self.goal = goal
        self.weight_history = weight_history

    def set_name(self, name):
        self.name = str(name.text())

    def set_weight(self, weight):
        self.weight = float(weight.text())

    def set_goal_weight(self, goal):
        self.goal = float(goal.text())

    def set_height(self, height):
        self.height = float(height.text())

    def convert_height_metric(self):
        height_metric = self.height * 2.54
        return height_metric

    def convert_weight_metric(self):
        weight_metric = self.weight * 0.45359237
        return weight_metric

    def user_dict_create(self, name, weight, goal, height, weight_history=None):
        '''
        Creates a dictionary with all of the user's personal statistics to be serialized as JSON.
        :param name: User's full name
        :param startingweight: The user's starting weight.
        :param currentweight: The user's current weight.
        :param height: The user's height.
        :param weight_history: User's weight history is mapped by date.
        :return Dictionary: a dictionary containing the user's personal statistics.
        '''

        return {
            'name': name,
            'weight': weight,
            'goal': goal,
            'height': height,
            'weight history': weight_history
            }

