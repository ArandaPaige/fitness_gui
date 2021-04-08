from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


def create_table_list(user_list):
    date_weight_list = []
    sorted_list = sorted(user_list, key=lambda x: x[0], reverse=True)
    for entry in sorted_list:
        date_item = QTableWidgetItem(type=1)
        weight_item = QTableWidgetItem(type=2)
        date_item.setData(0, entry[0])
        weight_item.setData(0, entry[1])
        date_weight_pair = (date_item, weight_item)
        date_weight_list.append(date_weight_pair)
    return date_weight_list
