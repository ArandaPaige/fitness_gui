class User:
    """
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    """

    def __init__(self, name=None, weight=None, goal=None, height=None,
                 weight_history=None):
        """Initializes user instance with user metrics provided or defaults them to None.

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
        """Sets the name of the user."""
        self.name = str(name)

    def set_weight(self, weight):
        """Sets the weight of the user."""
        self.weight = float(weight)

    def set_goal_weight(self, goal):
        """Sets the goal weight of the user."""
        self.goal = float(goal)

    def set_height(self, height):
        """Sets the user's height."""
        self.height = int(height)

    def set_weight_history(self, weight_history):
        """Sets the user's weight history to a new list of weight entries."""
        self.weight_history = weight_history
