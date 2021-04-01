import datetime
import database

DATETODAY = datetime.date.today()


class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, user_id=None, name=None, weight=None, height=None,
                 weight_history=None, metric=False):
        self.user_id = user_id
        self.name = name
        self.weight = weight
        self.height = height
        self.weight_history = weight_history
        self.metric = metric

    def user_setup(self, name=None, starting_weight=None, current_weight=None, height=None):
        if name != None:
            self.name = name
            print(f'Name is {name.text()}')
        if starting_weight != None:
            self.starting_weight = float(starting_weight.text())
            print(f'Starting weight is {starting_weight.text()}')
        if current_weight != None:
            self.current_weight = float(current_weight.text())
            print(f'Current weight is {current_weight.text()}')
        if height != None:
            self.height = int(height.text())
            print(f'Height is {height.text()}')

    def set_name(self, name):
        self.name = name

    def set__weight(self, weight):
        self.weight = weight

    def set_height(self, height):
        self.height = height

    def convert_height_metric(self):
        height_metric = self.height * 2.54
        return height_metric

    def convert_weight_metric(self):
        weight_metric = self.weight * 0.45359237
        return weight_metric

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