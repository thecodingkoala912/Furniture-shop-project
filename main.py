import csv
import os  # Task 7
import re  # Task 7
from collections import defaultdict  # Tasks 3, 4, 6
from datetime import datetime  # Task 4

from tkinter import *
from tkinter import messagebox  # All tasks
from tkinter import simpledialog  # Task 4
from tkinter import ttk  # Tasks 1, 3, 4, 5 and the interface
from tkinter import Tk  # Interface

# Reusable functions
def show_table(parent, heading, columns, rows):  # Used in tasks: 1, 3, 4, 5
    Label(parent, text=heading, font=("Arial", 14, "bold")).pack(pady=10)

    frame = Frame(parent)
    frame.pack()

    table_height = min(len(rows), 20) if rows else 1
    table = ttk.Treeview(frame, columns=columns, show="headings", height=table_height)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=150)

    for row in rows:
        table.insert("", END, values=[row[col] for col in columns])

    table.pack()

def read_files():  # Used in tasks: 1, 2, 3, 4, 5, 6
    with open("products.csv", encoding='utf-8') as f1, \
         open("sales.csv", encoding='utf-8') as f2, \
         open("group_id.csv", encoding='utf-8') as f3:

        products = list(csv.DictReader(f1))
        sales = list(csv.DictReader(f2))
        group = list(csv.DictReader(f3))

    return (
        sorted(products, key=lambda x: x.get('product_id', '')),
        sorted(sales, key=lambda x: x.get('product_id', '')),
        sorted(group, key=lambda x: x.get('group_id', ''))
    )

def build_dicts(groups, products):  # Used in tasks: 3, 4, 5, 6
    group_dict = {g['group_id']: g['group'] for g in groups if g.get('group_id') and g.get('group')}
    product_dict = {p['product_id']: p for p in products if p.get('product_id')}
    return group_dict, product_dict

def update_aggregated(aggregated, product_id, quantity, unit_price):  # Used in tasks: 3, 4
    aggregated[product_id]['quantity'] += quantity
    aggregated[product_id]['sales_sum'] += quantity * unit_price
    aggregated[product_id]['unit_price'] = unit_price

def create_aggregated_dict():  # Used in tasks: 3, 4
    return defaultdict(lambda: {'quantity': 0, 'sales_sum': 0.0, 'unit_price': 0.0})

def build_summarized_data(aggregated, product_dict, group_dict, id_key='product_id'):  # Used in tasks: 3, 4
    summarized_data = []
    for product_id, data in aggregated.items():
        product = product_dict.get(product_id)
        if not product:
            continue
        group_id = product.get('group_id')
        group_name = group_dict.get(group_id, "Unknown")
        name = product.get('name')

        row = {
            id_key: product_id if id_key == 'product_id' else f"{product_id}   {group_id}",
            'group': group_name,
            'name': name,
            'unit_price': f"{data['unit_price']:.2f}",
            'sales_sum': f"{data['sales_sum']:.2f}",
        }
        summarized_data.append(row)
    return summarized_data