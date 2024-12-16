# Group 1
# Miles Shinsato
# Nardos Gebremedhin
# Jessica Long-Heinicke
# Joseph Ayo
# Adrian Marquez


# Import Statements
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate

config = {
    "user": "winery_user",
    "password": "wine",
    "host": "127.0.0.1",
    "database": "winerycase"
}

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print(f"Database user {config['user']} connected to MySQL on host {config['host']} with database {config['database']}\n")

    # Function to execute and display reports
    def display_report(query, headers, report):
        cursor.execute(query)
        results = cursor.fetchall()
        if not results:
            print(f"No data available for {report}")
        else:
            print(f"{report}:\n")
            print(tabulate(results, headers=headers, tablefmt="fancy_grid"))
            print("\n" + "-" * 60 + "\n")

    # Supplier delivery performance report
    supplier_delivery_query = """
    SELECT SupplierID, ScheduledDelivery, ActualDelivery, 
           DATEDIFF(ActualDelivery, ScheduledDelivery) AS DelayDays
    FROM Delivery
    ORDER BY DelayDays DESC;
    """
    display_report(supplier_delivery_query, 
                   ["SupplierID", "Scheduled Delivery", "Actual Delivery", "Delay (Days)"], 
                   "Supplier Delivery Performance Report")

    # Wine sales and distribution report
    wine_sales_query = """
    SELECT Wines.WineName, Distributors.DistributorName, SUM(Orders.UnitsSold) AS TotalSold
    FROM Orders
    JOIN Wines ON Orders.WineID = Wines.WineID
    JOIN Distributors ON Orders.DistributorID = Distributors.DistributorID
    GROUP BY Wines.WineName, Distributors.DistributorName
    ORDER BY TotalSold DESC;
    """
    display_report(wine_sales_query, 
                   ["Wine Name", "Distributor Name", "Total Sold"], 
                   "Wine Sales and Distribution Report")

    # Employee time tracking report
    employee_time_query = """
    SELECT EmployeeID, 
           SUM(Quarter1Hours) AS Q1_Hours, 
           SUM(Quarter2Hours) AS Q2_Hours, 
           SUM(Quarter3Hours) AS Q3_Hours, 
           SUM(Quarter4Hours) AS Q4_Hours, 
           SUM(Quarter1Hours + Quarter2Hours + Quarter3Hours + Quarter4Hours) AS TotalHours
    FROM TimeTracking
    GROUP BY EmployeeID
    ORDER BY TotalHours DESC;
    """
    display_report(employee_time_query, 
                   ["EmployeeID", "Q1 Hours", "Q2 Hours", "Q3 Hours", "Q4 Hours", "Total Hours"], 
                   "Employee Time Tracking Report")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Invalid username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print(err)
finally:
    if 'db' in locals() and db.is_connected():
        db.close()
        print("Database connection closed.")
