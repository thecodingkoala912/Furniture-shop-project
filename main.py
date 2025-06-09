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

# Task 1 - Reading data from files (at least 10 lines of data) + added logic for validation
def read_data_from_files():
    win = Toplevel(root)
    win.title("Read and Validate Data")

    text_output = Text(win, height=10, width=70, font=("Consolas", 10))
    text_output.pack(padx=10, pady=10)

    messagebox.showinfo("Task 1", "Reading data from files (at least 10 lines of data)")
    text_output.delete("1.0", END)

    try:
        products, sales, _ = read_files()

        if len(products) < 10 or len(sales) < 10:
            text_output.insert(END, "❌ Not enough data!\n")
            if len(products) < 10:
                text_output.insert(END, f"- 'products.csv' has {len(products)} lines. Needs {10 - len(products)} more.\n")
            if len(sales) < 10:
                text_output.insert(END, f"- 'sales.csv' has {len(sales)} lines. Needs {10 - len(sales)} more.\n")
        else:
            text_output.insert(END, "✅ Files successfully read! Sufficient data.\n")

    except FileNotFoundError:
        text_output.insert(END, "❌ Error: One of the files is missing (products.csv, sales.csv, group_id.csv)\n")

# Task 2 - Transfer data from files into lists and visualize them
def show_tables():
    messagebox.showinfo("Task 2", "Transferring data from files into lists and visualizing them.")

    win = Toplevel(root)
    win.title("Tables: Products, Sales, Groups")
    win.geometry("700x800")

    products, sales, group = read_files()

    if products:
        show_table(win, "Products", list(products[0].keys()), products)

    if sales:
        show_table(win, "Sales", list(sales[0].keys()), sales)

    if group:
        show_table(win, "Groups", list(group[0].keys()), group)

# Task 3 - Filling a dictionary from the lists with data summarization and visualization.
def show_summarized_table():
    messagebox.showinfo("Task 3", "Filling a dictionary from the lists with data summarization and visualization.")

    products, sales, groups = read_files()
    group_dict, product_dict = build_dicts(groups, products)
    aggregated = create_aggregated_dict()

    for sale in sales:
        product_id = sale.get('product_id')
        try:
            quantity = int(sale.get('quantity', 0))
            unit_price = float(sale.get('unit_price', 0))
        except ValueError:
            continue
        update_aggregated(aggregated, product_id, quantity, unit_price)

    summarized_data = build_summarized_data(aggregated, product_dict, group_dict, id_key='product_id')

    win = Toplevel(root)
    win.title("Summarized Revenue Table by Products")

    show_table(
        parent=win,
        heading="Summarized Revenue Table by Products",
        columns=['product_id', 'group', 'name', 'unit_price', 'sales_sum'],
        rows=summarized_data
    )

# Task 4 - Search data from the dictionary and display results
def show_sales_by_date():
    messagebox.showinfo("Task 4", "Search data from the lists and display the results.")

    date_input = simpledialog.askstring("Enter Date", "Enter date (YYYY-MM-DD):")
    if not date_input:
        return

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format!")
        return

    products, sales, groups = read_files()
    group_dict, product_dict = build_dicts(groups, products)
    aggregated = create_aggregated_dict()

    for sale in sales:
        if sale.get('date') != date_input:
            continue

        product_id = sale.get('product_id')
        try:
            quantity = int(sale.get('quantity', 0))
            unit_price = float(sale.get('unit_price', 0))
        except ValueError:
            continue

        update_aggregated(aggregated, product_id, quantity, unit_price)

    summarized_data = build_summarized_data(
        aggregated, product_dict, group_dict, id_key='product_id'
    )

    if not summarized_data:
        messagebox.showinfo("No Data", f"No sales on {date_input}.")
        return

    win = Toplevel(root)
    win.title(f"Revenue for {date_input}")

    show_table(
        parent=win,
        heading=f"Summary revenue table by product for {date_input}",
        columns=['product_id', 'group', 'name', 'unit_price', 'sales_sum'],
        rows=summarized_data
    )

# Task 5 - Transfer data based on a specific criterion into a new list and display it
def show_sales_over_500():
    messagebox.showinfo("Task 5", "Transfer data based on a specific criterion into a new list and display it.")

    products, sales, groups = read_files()
    group_dict, product_dict = build_dicts(groups, products)

    filtered_sales = []
    for sale in sales:
        try:
            quantity = int(sale.get('quantity', 0))
            unit_price = float(sale.get('unit_price', 0))
        except (ValueError, TypeError):
            continue

        sales_sum = quantity * unit_price
        if sales_sum <= 500:
            continue

        product_id = sale.get('product_id')
        date = sale.get('date', '')
        product = product_dict.get(product_id, {})
        name = product.get('name', 'Unknown')

        filtered_sales.append({
            'product_id': product_id,
            'name': name,
            'date': date,
            'unit_price': f"{unit_price:.2f}",
            'quantity': quantity,
            'sales_sum': f"{sales_sum:.2f}"
        })

    if not filtered_sales:
        messagebox.showinfo("No Results", "No sales over 500 BGN.")
        return

    filtered_sales.sort(key=lambda x: float(x['sales_sum']), reverse=True)

    win = Toplevel(root)
    win.title("Sales over 500 BGN")

    show_table(
        parent=win,
        heading="Sales with value over 500 BGN",
        columns=['product_id', 'name', 'date', 'unit_price', 'quantity', 'sales_sum'],
        rows=filtered_sales
    )
# Task 6 - Save data from the list to a text file in a suitable format
def save_turnover_summary():
    messagebox.showinfo("Task 6", "Save data from the list to a text file in a suitable format.")

    products, sales, groups = read_files()

    group_dict, product_dict = build_dicts(groups, products)

    turnover_by_group = defaultdict(float)

    for sale in sales:
        product_id = sale.get('product_id')
        product = product_dict.get(product_id)
        if not product:
            continue

        try:
            quantity = int(sale.get('quantity', 0))
            unit_price = float(sale.get('unit_price', 0))
        except ValueError:
            continue

        group_id = product.get('group_id')
        group_name = group_dict.get(group_id, "Unknown group")
        turnover_by_group[group_name] += quantity * unit_price

    total_turnover = sum(turnover_by_group.values())

    try:
        with open("turnover.txt", "w", encoding="utf-8") as f:
            f.write(f"{'Group':<25} | {'Turnover (BGN)':>15}\n")
            f.write("-" * 43 + "\n")
            for group_name, turnover in sorted(turnover_by_group.items()):
                f.write(f"{group_name:<25} | {turnover:>15.2f}\n")
            f.write("-" * 43 + "\n")
            f.write(f"{'Total':<25} | {total_turnover:>15.2f}\n")

        messagebox.showinfo("Success", "File 'turnover.txt' was saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving the file: {e}")

# GUI
root = Tk()
root.title("Furniture Store Management")
root.geometry("500x400")  

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)

ttk.Button(root, text="Task 1", width=30, command=read_data_from_files).pack(pady=5)
ttk.Button(root, text="Task 2", width=30, command=show_tables).pack(pady=5)
ttk.Button(root, text="Task 3", width=30, command=show_summarized_table).pack(pady=5)
ttk.Button(root, text="Task 4", width=30, command=show_sales_by_date).pack(pady=5)
ttk.Button(root, text="Task 5", width=30, command=show_sales_over_500).pack(pady=5)
ttk.Button(root, text="Task 6", width=30, command=save_turnover_summary).pack(pady=5)

root.mainloop()
