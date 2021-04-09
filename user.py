class User:
    """
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    """

    def __init__(self, name=None, weight=None, goal=None, height=None,
                 weight_history=None):
        """
        Initializes the user object with all the user's personal metrics and identifiers. New users are initialized with
        null values that are set in the new user introductory menu.
        :param name: the user's name
        :param weight: the user's weight
        :param goal: the user's goal weight
        :param height: the user's height
        :param weight_history: the user's history of weight entries by date and ID
        """
        self.user_id = 1
        self.name = name
        self.weight = weight
        self.height = height
        self.goal = goal
        self.weight_history = weight_history

    def set_name(self, name):
        """
        Sets the name of the user.
        :param name: the user's name
        :return: None
        """
        self.name = str(name.text())

    def set_weight(self, weight):
        """
        Sets the weight of the user.
        :param weight: the user's weight
        :return: None
        """
        self.weight = float(weight.text())

    def set_goal_weight(self, goal):
        """
        Sets the goal weight of the user
        :param goal: the user's goal weight
        :return: None
        """
        self.goal = float(goal.text())

    def set_height(self, height):
        """
        Sets the user's height.
        :param height:
        :return: None
        """
        self.height = float(height.text())

    def set_weight_history(self, weight_history):
        """
        Sets the user's weight history to a new list of weight entries.
        :param weight_history: the user's history of weight entries by date and ID
        :return: None
        """
        self.weight_history = weight_history

    def convert_height_metric(self):
        height_metric = self.height * 2.54
        return height_metric

    def convert_weight_metric(self):
        weight_metric = self.weight * 0.45359237
        return weight_metric
