#Group 1
#Miles Shinsato
#Nardos Gebremedhin
#Jessica Long-Heinicke
#Joseph Ayo
#Adrian Marquez

import mysql.connector
from tabulate import tabulate

def connect_to_db():
    #Connect to the MySQL database.
    return mysql.connector.connect(
        host="localhost",
        user="winery_user",
        password="wine",
        database="winerycase"
    )

def fetch_and_display_query(query, headers):
    #Fetch data using the query and display it in a tabular format
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    print(tabulate(results, headers=headers, tablefmt="pretty"))

def inventory_status():
    query = """
        SELECT ItemName, Quantity, ReorderLevel,
               CASE WHEN Quantity < ReorderLevel THEN 'Reorder Needed' ELSE 'Sufficient Stock' END AS Status
        FROM Inventory;
    """
    headers = ["Item Name", "Quantity", "Reorder Level", "Status"]
    fetch_and_display_query(query, headers)

def sales_report():
    query = """
        SELECT w.WineName, ws.Quarter1Sales, ws.Quarter2Sales, ws.Quarter3Sales, ws.Quarter4Sales, ws.TotalSales
        FROM WineSales ws
        JOIN Wines w ON ws.WineID = w.WineID;
    """
    headers = ["Wine Name", "Q1 Sales", "Q2 Sales", "Q3 Sales", "Q4 Sales", "Total Sales"]
    fetch_and_display_query(query, headers)

def supplier_delivery_performance():
    query = """
        SELECT s.Name AS SupplierName, d.ScheduledDelivery, d.ActualDelivery, d.Difference AS HoursLate
        FROM Delivery d
        JOIN Suppliers s ON d.SupplierID = s.SupplierID;
    """
    headers = ["Supplier Name", "Scheduled Delivery", "Actual Delivery", "Hours Late"]
    fetch_and_display_query(query, headers)

def employee_work_hours():
    query = """
        SELECT e.EmployeeName, t.Quarter1Hours, t.Quarter2Hours, t.Quarter3Hours, t.Quarter4Hours, t.TotalHours
        FROM TimeTracking t
        JOIN Employees e ON t.EmployeeID = e.EmployeeID;
    """
    headers = ["Employee Name", "Q1 Hours", "Q2 Hours", "Q3 Hours", "Q4 Hours", "Total Hours"]
    fetch_and_display_query(query, headers)

def main():
    while True:
        print("\nWinery Reports Menu")
        print("1. Inventory Status")
        print("2. Sales Report")
        print("3. Supplier Delivery Performance")
        print("4. Employee Work Hours")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            inventory_status()
        elif choice == '2':
            sales_report()
        elif choice == '3':
            supplier_delivery_performance()
        elif choice == '4':
            employee_work_hours()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
