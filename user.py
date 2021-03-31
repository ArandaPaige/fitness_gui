class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, username=None, name=None, starting_weight=None, current_weight=None, height=None,
                 weight_history=None):
        self.name = name
        self.starting_weight = starting_weight
        self.current_weight = current_weight
        self.height = height
        self.weight_history = weight_history

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

    def set_name(self):
        pass

    def set_starting_weight(self):
        pass

    def set_current_weight(self):
        pass

    def set_height(self):
        pass
