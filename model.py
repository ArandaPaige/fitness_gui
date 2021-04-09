from PyQt6.QtWidgets import *
import pyqtgraph as pg


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
        id_date_weight = (id_item, date_item, weight_item)
        id_date_weight_list.append(id_date_weight)
    return id_date_weight_list


def create_graph_list(user_list):
    weight_list = []
    sorted_list = sorted(user_list, key=lambda x: x[1])
    for entry in sorted_list:
        sorted_list.append(entry[2])
    return sorted_list


def graph_entries(sorted_list, list_end=None):
    if list_end is not None:
        graph_x = sorted_list[:list_end]
    else:
        graph_x = sorted_list
    graph_y = len(graph_x)
    return graph_x, graph_y


def lerp_weight(sorted_list):
    pass
