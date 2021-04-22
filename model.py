import datetime

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

DATETODAY = datetime.date.today()


def create_sorted_weight_history(weight_history, reverse=False):
    sorted_list = sorted(weight_history, key=lambda x: x[1], reverse=reverse)
    return sorted_list


def create_table_list(sorted_list):
    """
    Sorts the user's weight history by date and then creates QTableWidget items for each ID, date, and weight entry.
    :param sorted_list: user supplied weight history list
    :return: List: a list of tuples containing ID, date, and weight items
    """
    id_date_weight_list = []
    for entry in reversed(sorted_list):
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


def create_graph_list(user_list, days=0):
    """
    Creates a list of weights that have been sorted by date in descending order
    :param days: list slice by entry
    :param user_list: a list from the user instance
    :return: List
    """
    graph_xlist = []
    graph_ylist = []
    sorted_list = sorted(user_list, key=lambda x: x[1])
    for i, entry in enumerate(sorted_list[days:]):
        graph_x, graph_y = entry[2], i
        graph_ylist.append(graph_x)
        graph_xlist.append(graph_y)
    return graph_xlist, graph_ylist


def create_graph_date_list(sorted_list, days=0):
    """
    Creates a list of weights that have been sorted by date in descending order
    :param days:
    :param sorted_list: a list from the user instance
    :return: List
    """
    graph_xlist = []
    graph_ylist = []
    date_past = DATETODAY - datetime.timedelta(days=days)
    for day in range(days):
        date = DATETODAY - datetime.timedelta(days=1)
        graph_ylist.append(date)
    for entry in sorted_list:
        weight = entry[2], datetime.datetime.strptime(entry[1], '%Y-%m-%d')
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


def weight_delta_calculator(sorted_list):
    if len(sorted_list) > 1:
        start_date, end_date = sorted_list[0][1], sorted_list[-1][1]
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        start_weight, end_weight = sorted_list[0][2], sorted_list[-1][2]
        time_delta = end_date - start_date
        weight = start_weight - end_weight
        if weight <= 0:
            weight_delta = weight / time_delta.days
        else:
            weight_delta = -(weight / time_delta.days)
        return weight_delta
    else:
        return None


def time_to_goal(current_weight, goal_weight, delta):
    if delta is not None:
        difference = current_weight - goal_weight
        days = abs(int(difference / delta))
        end_date = DATETODAY + datetime.timedelta(days=days)
        return end_date, days
    else:
        return None


def lerp_weight(days, start_weight, goal_weight, weight_delta):
    day_range = range(days)
    lerp_x_list = []
    lerp_y_list = []
    date = DATETODAY
    for day in day_range:
        weight = goal_weight + weight_delta * (start_weight - goal_weight)
        start_weight = weight
        date += (datetime.timedelta(days=1))
        lerp_x_list.append(weight)
        lerp_y_list.append(date)
    return lerp_x_list, lerp_y_list


def lerp_weight_entry(days, y_list, start_weight, goal_weight, weight_delta):
    day_range = range(len(y_list), (len(y_list) + days))
    lerp_x_list = []
    lerp_y_list = []
    for day in day_range:
        weight = start_weight + weight_delta
        start_weight = weight
        lerp_x_list.append(day)
        lerp_y_list.append(weight)
    return lerp_x_list, lerp_y_list


def convert_height_metric(height):
    height_metric = height * 2.54
    return height_metric


def convert_weight_metric(weight):
    weight_metric = weight * 0.45359237
    return weight_metric


def convert_stones(weight):
    weight_stone = weight / 14
    return weight_stone
