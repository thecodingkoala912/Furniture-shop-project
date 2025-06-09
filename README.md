# 🪑 Furniture Store Management System (Tkinter GUI)

This application provides a graphical interface for managing and analyzing sales and product data for a furniture store. Built with **Python** and **Tkinter**, it supports data validation, summarization, searching, filtering, saving, and adding new entries.

---

## 📁 Project Structure

The program works with three CSV files:

- `products.csv` – Contains product IDs, names, and group IDs.
- `sales.csv` – Contains product sales data including quantity, price, and date.
- `group_id.csv` – Maps group IDs to their human-readable names.

---

## ✅ Features by Task

### 🔹 Task 1: Read and Validate Data

- Loads data from `products.csv` and `sales.csv`.
- Verifies at least **10 records** in each file.
- Displays validation results in a **popup**.

### 🔹 Task 2: Visualize CSV Data

Displays tables for:
- Products
- Sales
- Product groups

> Uses a **Treeview widget** for display.

### 🔹 Task 3: Summarize Sales

- Aggregates **total revenue per product**.
- Builds a summary dictionary and shows it in a visual table view.

### 🔹 Task 4: Filter by Date

- User inputs a date (`YYYY-MM-DD` format).
- Filters sales made on that day.
- Displays **summarized revenue** for that date.

### 🔹 Task 5: Sales Over 500 BGN

- Filters and displays sales with value **over 500 BGN**.
- Displays relevant product and sale information.

### 🔹 Task 6: Export Turnover Summary

- Summarizes revenue **per product group**.
- Saves formatted output to `turnover.txt`, including:
  - Total turnover
  - Turnover per group

### 🔹 Task 7: Add New Product

- Provides a form to add new products.
- Validates input (e.g., product names in **Cyrillic**).
- Ensures group ID consistency and structure.

---

## 🚀 Technologies Used

- Python 3.x
- Tkinter (GUI)
- CSV for data handling
- `ttk.Treeview` for tabular display
