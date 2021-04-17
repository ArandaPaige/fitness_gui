import datetime

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

DATETODAY = datetime.date.today()


def create_table_list(user_list):
    """
    Sorts the user's weight history by date and then creates QTableWidget items for each ID, date, and weight entry.
    :param user_list: user supplied weight history list
    :return: List: a list of tuples containing ID, date, and weight items
    """
    id_date_weight_list = []
    sorted_list = sorted(user_list, key=lambda x: x[1], reverse=True)
    for entry in sorted_list:
        id_item = QTableWidgetItem(0)
        date_item = QTableWidgetItem(1)
        weight_item = QTableWidgetItem(2)
        id_item.setData(0, entry[0])
        date_item.setData(0, entry[1])
        weight_item.setData(0, entry[2])
        id_item.setText(str(entry[0]))
        date_item.setText(str(entry[1]))
        weight_item.setText(str(entry[2]))
        id_item.setTextAlignment(Qt.AlignCenter)
        date_item.setTextAlignment(Qt.AlignCenter)
        weight_item.setTextAlignment(Qt.AlignCenter)
        id_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        date_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        weight_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        id_date_weight = (id_item, date_item, weight_item)
        id_date_weight_list.append(id_date_weight)
    return id_date_weight_list


def create_graph_list(user_list):
    """
    Creates a list of weights that have been sorted by date in descending order
    :param user_list: a list from the user instance
    :return: List
    """
    graph_xlist = []
    graph_ylist = []
    sorted_list = sorted(user_list, key=lambda x: x[1])
    for i, entry in enumerate(sorted_list):
        graph_x, graph_y = entry[2], i
        graph_ylist.append(graph_x)
        graph_xlist.append(graph_y)
    return graph_xlist, graph_ylist


def graph_entries(sorted_list, list_end=None):
    """
    Creates a tuple of x, y values based on the sorted list. The length of the list is determined by the user's input.
    :param sorted_list:
    :param list_end:
    :return: List
    """
    if list_end is not None:
        graph = sorted_list[:list_end]
    else:
        graph = sorted_list
    return graph


def weight_delta_calculator(start_entry, end_entry):
    time_delta = end_entry[0] - start_entry[0]
    weight = start_entry[1] - end_entry[1]
    weight_delta = weight / time_delta.days
    return weight_delta


def lerp_weight(future_date, start_weight, goal_weight, weight_delta):
    time_delta = future_date - DATETODAY
    date_range = range(time_delta.days)
    lerp_x_list = []
    lerp_y_list = []
    date = DATETODAY
    for day in date_range:
        weight = goal_weight + weight_delta * (start_weight - goal_weight)
        start_weight = weight
        date += datetime.timedelta(days=1)
        lerp_x_list.append(weight)
        lerp_y_list.append(date)
    return lerp_x_list, lerp_y_list
