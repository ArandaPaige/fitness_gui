from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


def create_table_list(user_list):
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
