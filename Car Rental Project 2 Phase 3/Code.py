# CSE 3330 - Databases
# Project 2 Phase 3

from tkinter import *
import sqlite3
import re

root = Tk()
root.title("Car Rental 2021")  # name of window
root.geometry("400x400")  # size of window

try:
    conn = sqlite3.connect('car_rental.db')
    print("Opened database successfully")
except Exception as e:
    print("Error during connection: ", str(e))

# create a cursor
c = conn.cursor()

def new_rental():
    def query():
        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()

        click.execute("SELECT Vehicleid, description FROM VEHICLE AS V\
                      WHERE V.Type = :v_type AND V.Category = :v_category\
                      AND V.VehicleID NOT IN (SELECT VehicleID FROM RENTAL\
                      WHERE (strftime(:v_start) BETWEEN StartDate AND ReturnDate) OR\
                      (strftime(:v_end) BETWEEN StartDate AND ReturnDate))",
                      {
                          'v_type': vehicle_type.get(),
                          'v_category': vehicle_category.get(),
                          'v_start': vehicle_start.get(),
                          'v_end': vehicle_end.get()
                      }
                      )

        records = click.fetchall()

        # Loop through results
        print_records = ""
        for record in records:
            print_records += str(record) + "\n"

        query_label = Label(new_rent_win, text=print_records)
        query_label.grid(row=7, column=0, columnspan=2)
        clear_button = Button(new_rent_win, text="Clear Results", command=lambda:
                              query_label.config(text=""))
        clear_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()

    # submit values into the DB

    def reservation(r1, r2, r3, r4, r5, r6, r7, r9):
        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()
        rental_type_value = 0.0
        if r5 == 1:
            click.execute("SELECT R.Daily FROM RATE AS R, VEHICLE AS V WHERE V.Type = R.Type "
                "AND V.Category = R.Category AND V.VehicleID = :r22",
                {
                    'r22': r2
                }
                )
            rental_type_value = float(click.fetchone()[0])
        elif r5 == 7:
            click.execute("SELECT R.Weekly FROM RATE AS R, VEHICLE AS V WHERE V.Type = R.Type "
                "AND V.Category = R.Category AND V.VehicleID = :r22",
                {
                    'r22': r2
                }
                )
            rental_type_value = float(click.fetchone()[0])
        click.execute("INSERT INTO RENTAL VALUES(:r_custid, :r_vehicleid, :r_startdate, :r_orderdate, "
                      ":r_rentaltype, :r_qty, :r_returndate, :r_totalamount, :r_paymentdate, 0)",
                      {
                          'r_custid': r1,
                          'r_vehicleid': r2,
                          'r_startdate': r3,
                          'r_orderdate': r4,
                          'r_rentaltype': r5,
                          'r_qty': r6,
                          'r_returndate': r7,
                          'r_totalamount': rental_type_value,
                          'r_paymentdate': r9
                      }
                      )
                      
       
        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()

    def submit():
        reserve = Toplevel()
        reserve.title("Make a reservation")
        reserve.geometry("400x300")

        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()

        # create text boxes
        r_custid = Entry(reserve, width=30)
        r_custid.grid(row=0, column=1, padx=20)

        r_vin = Entry(reserve, width=30)
        r_vin.grid(row=1, column=1)

        r_rtype = Entry(reserve, width=30)
        r_rtype.grid(row=2, column=1)

        r_qty = Entry(reserve, width=30)
        r_qty.grid(row=3, column=1)

        vehicle_pay = Entry(reserve, width=30)
        vehicle_pay.grid(row=4, column=1)

        r_orderdate = Entry(reserve, width=30)
        r_orderdate.grid(row=5, column=1)

        r_startdate = Entry(reserve, width=30)
        r_startdate.grid(row=6, column=1)

        r_enddate = Entry(reserve, width=30)
        r_enddate.grid(row=7, column=1)
        # create text box labels
        r_custid_label = Label(reserve, text="Customer ID")
        r_custid_label.grid(row=0, column=0)

        r_vin_label = Label(reserve, text="Vehicle ID")
        r_vin_label.grid(row=1, column=0)

        r_rtype_label = Label(reserve, text="Rental Type")
        r_rtype_label.grid(row=2, column=0)

        r_quantity_label = Label(reserve, text="Quantity")
        r_quantity_label.grid(row=3, column=0)

        payment_label = Label(reserve, text="Payment Date")
        payment_label.grid(row=4, column=0)

        orddate_label = Label(reserve, text="Order Date")
        orddate_label.grid(row=5, column=0)

        stdate_label = Label(reserve, text="Start Date")
        stdate_label.grid(row=6, column=0)

        redate_label = Label(reserve, text="Return Date")
        redate_label.grid(row=7, column=0)

        # rental_type_value = 0.0
        query_button = Button(reserve, text="Confirm", command=lambda: reservation(r_custid.get(), r_vin.get(),
                                                                                   r_orderdate.get(), r_startdate.get(),
                                                                                   r_rtype.get(), r_qty.get(),
                                                                                   r_enddate.get(), vehicle_pay.get()))
        query_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        query_button2 = Button(reserve, text="Clear", command=lambda: clear (r_custid,r_vin,r_orderdate,r_startdate,r_rtype,r_qty,r_enddate,vehicle_pay))
        def clear(r1,r2,r3,r4,r5,r6,r7,r8):
            r1.delete(0,END)
            r2.delete(0,END)
            r3.delete(0,END)
            r4.delete(0,END)
            r5.delete(0,END)
            r6.delete(0,END)
            r7.delete(0,END)
            r8.delete(0,END)
        query_button2.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        hint_label = Label(new_rent_win, text="[Guidelines]\nRental Type: 1:Daily, 7:Weekly\nQuantity: number of days/ weeks to rent")
        hint_label.grid(row=10, column=0, columnspan=2)

        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()

    new_rent_win = Toplevel()
    new_rent_win.title('New Rental Information')

    # create text boxes
    vehicle_type = Entry(new_rent_win, width=30)
    vehicle_type.grid(row=0, column=1, padx=20)

    vehicle_category = Entry(new_rent_win, width=30)
    vehicle_category.grid(row=1, column=1)

    vehicle_start = Entry(new_rent_win, width=30)
    vehicle_start.grid(row=2, column=1)

    vehicle_end = Entry(new_rent_win, width=30)
    vehicle_end.grid(row=3, column=1)


    # labels
    v_type_label = Label(new_rent_win, text="Vehicle Type")
    v_type_label.grid(row=0, column=0)

    category_label = Label(new_rent_win, text="Vehicle Category")
    category_label.grid(row=1, column=0)

    start_label = Label(new_rent_win, text="Intended Start Date")
    start_label.grid(row=2, column=0)

    end_label = Label(new_rent_win, text="Intended Return Date")
    end_label.grid(row=3, column=0)
    

    hint_label = Label(new_rent_win, text="[Guidelines]\nType: 1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN\nCategory: 0:Basic, 1:Luxury")
    hint_label.grid(row=8, column=0, columnspan=2)


    # find rental button
    find_button = Button(new_rent_win, text="Find available vehicles during entered period", command=query)
    find_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # reserve button
    reserve_button = Button(new_rent_win, text="Make a reservation", command=submit)
    reserve_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
"""
    reserve_button = Button(new_rent_win, text="Clear Entries", command=lambda:
                            vehicle_type.delete(0,END)
                            vehicle_category.delete(0,END)
                            vehicle_start.delete(0,END)
                            vehicle_end.delete(0,END))
    reserve_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
"""
def search_vehicles():
    def get_vehicles():
        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()
        click.execute("drop view if exists tempview")
        click.execute("create view tempView as select vehicle.vehicleid as VehicleID, vehicle.description as Description,\
            ifnull(OrderAmount,0) as OrderAmount, ifnull(vrentalinfo.TotalDays,0) as totaldays from Vehicle left outer join vrentalinfo\
            on vehicle.vehicleID = vin")
        if vehicle_id.get() != "":
            click.execute("SELECT DISTINCT vehicleid, Description, case when totaldays = 0 then 'Non-Applicable' else '$'||(OrderAmount/ totaldays) end FROM tempView\
                    WHERE vehicleid = :r_id GROUP BY vehicleid",{'r_id': vehicle_id.get()})
        elif description.get() != "":
            click.execute("SELECT DISTINCT vehicleid, Description, case when totaldays = 0 then 'Non-Applicable' else '$'||(OrderAmount/ totaldays) end FROM tempView\
                    WHERE description = :r_id GROUP BY vehicleid",{'r_id': description.get()})
        elif part_des.get() != "":
            click.execute("SELECT DISTINCT vehicleid, Description, case when totaldays = 0 then 'Non-Applicable' else '$'||(OrderAmount/ totaldays) end FROM tempView\
                    WHERE description LIKE ? GROUP BY vehicleid", ('%'+part_des.get()+'%',))
        else:
            click.execute("SELECT DISTINCT vehicleid, Description, case when totaldays = 0 then 'Non-Applicable' else '$'||(OrderAmount/ totaldays) end FROM tempView GROUP BY vehicleid")

        # print(c.fetchall())
        records = click.fetchall()
        # print(records)

        # Loop through results
        print_records = ""
        for record in records:
            print_records += str(record) + "\n"

        my_label = Label(new_car_win, text="VIN, Vehicle's Description, Average Daily Price" + "\n" + print_records)
        my_label.grid(row=8, column=0, columnspan=2)
        query_button2 = Button(new_car_win, text="Clear results", command=lambda: clear (my_label))
        def clear(r1):
            r1.config(text="")
        query_button2.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        click.execute("drop view tempView")
        # clear button to delete all vehicle info

        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()


    new_car_win = Toplevel()
    new_car_win.title('Search For Vehicles(s)')

    # create text boxes
    vehicle_id = Entry(new_car_win, width=30)
    vehicle_id.grid(row=0, column=1, padx=20)

    description = Entry(new_car_win, width=30)
    description.grid(row=1, column=1)

    part_des = Entry(new_car_win, width=30)
    part_des.grid(row=2, column=1)

    # create text box labels
    v_id_label = Label(new_car_win, text="Vehicle ID")
    v_id_label.grid(row=0, column=0)

    des_label = Label(new_car_win, text="Vehicle's Description")
    des_label.grid(row=1, column=0)

    part_des_label = Label(new_car_win, text="Part of Vehicle's Description")
    part_des_label.grid(row=2, column=0)

    # show vehicles button
    show_button = Button(new_car_win, text="Show Records", command=get_vehicles)
    show_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

    query_button2 = Button(new_car_win, text="Clear Entries", command=lambda: clear (vehicle_id, description, part_des))
    def clear(r1,r2,r3):
            r1.delete(0,END)
            r2.delete(0,END)
            r3.delete(0,END)
    query_button2.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # clear result button
    # clear_button = Button(new_car_win, text="Clear Output", command=clear)
    # clear_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)


def search_customer():
    def get_vehicles():
        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()
        click.execute("drop view if exists tempview")
        click.execute("create view tempView as select customer.custid as CustomerID, customer.name as CustomerName, OrderDate, StartDate, ReturnDate,\
            TotalDays, VIN, Vehicle, Type, Category, OrderAmount,\
            ifnull(RentalBalance,0) as RentalBalance from customer left outer join vrentalinfo\
            on customerid = custid")
        if vehicle_id.get() != "":
            click.execute("SELECT DISTINCT CustomerID, CustomerName, '$'||SUM(RentalBalance) FROM tempView\
                    WHERE CUSTOMERID = :r_id GROUP BY CustomerID",{'r_id': vehicle_id.get()})
        elif description.get() != "":
            click.execute("SELECT DISTINCT CustomerID, CustomerName, '$'||SUM(RentalBalance) FROM tempView\
                    WHERE CUSTOMERName = :r_id GROUP BY CustomerID",{'r_id': description.get()})
        elif part_des.get() != "":
            click.execute("SELECT DISTINCT CustomerID, CustomerName, '$'||SUM(RentalBalance) FROM tempView\
                    WHERE CUSTOMERName LIKE ? GROUP BY CustomerID", ('%'+part_des.get()+'%',))
        else:
            click.execute("SELECT DISTINCT CustomerID, CustomerName, '$'||SUM(RentalBalance) FROM tempView GROUP BY CustomerID")

        # print(c.fetchall())
        records = click.fetchall()
        # print(records)

        # Loop through results
        print_records = ""
        for record in records:
            print_records += str(record) + "\n"

        my_label = Label(new_car_win, text="Customer ID, Customer Name, Remaining Balance" + "\n" + print_records)
        my_label.grid(row=8, column=0, columnspan=2)
        query_button2 = Button(new_car_win, text="Clear results", command=lambda: clear (my_label))
        def clear(r1):
            r1.config(text="")
        query_button2.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        click.execute("drop view tempView")
        # clear button to delete all vehicle info

        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()


    new_car_win = Toplevel()
    new_car_win.title('Search For Customer(s)')

    # create text boxes
    vehicle_id = Entry(new_car_win, width=30)
    vehicle_id.grid(row=0, column=1, padx=20)

    description = Entry(new_car_win, width=30)
    description.grid(row=1, column=1)

    part_des = Entry(new_car_win, width=30)
    part_des.grid(row=2, column=1)

    # create text box labels
    v_id_label = Label(new_car_win, text="Customer ID")
    v_id_label.grid(row=0, column=0)

    des_label = Label(new_car_win, text="Name")
    des_label.grid(row=1, column=0)

    part_des_label = Label(new_car_win, text="Part of Name")
    part_des_label.grid(row=2, column=0)

    # show vehicles button
    show_button = Button(new_car_win, text="Show Records", command=get_vehicles)
    show_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

    query_button2 = Button(new_car_win, text="Clear Entries", command=lambda: clear (vehicle_id, description, part_des))
    def clear(r1,r2,r3):
            r1.delete(0,END)
            r2.delete(0,END)
            r3.delete(0,END)
    query_button2.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # clear result button
    # clear_button = Button(new_car_win, text="Clear Output", command=clear)
    # clear_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

def new_customer():
    def submit():
        conn2 = sqlite3.connect('car_rental.db')
        c2 = conn2.cursor()
        max_id = c2.execute("SELECT MAX(CustID)+1 FROM CUSTOMER")
        max_id1 = int(max_id.fetchall()[0][0])
        p = re.compile(r'[0-9]{10}')
        if name.get() != "" and bool(p.fullmatch(phone.get())) is True:
            status.config(text = "Record added to database.")
            c2.execute("INSERT INTO Customer VALUES(:c_id, :name, :phone)",
                   {
                       'c_id': max_id1,
                       'name': name.get(),
                       'phone': phone.get()
                   }
                   )
        elif name.get() == "":
            status.config(text = "Please enter Name.")
        elif phone.get() == "":
            status.config(text = "Please enter Phone Number.")
        elif bool(p.fullmatch(phone.get())) is False:
            status.config(text = "Phone number provided not in valid format.")
        else:
            status.config(text="Record not valid. No record saved.")
        conn2.commit()
        conn2.close()
        name.delete(0, END)
        phone.delete(0, END)
    def backward(prev,records, end):
        prev.config(text = "")
        if end - 30 >= 0:
            button_back = Button(new_cust_win, text = "<<", command = lambda: backward(query_label,records,end-30))
            button_back.grid(row=8, column=0)
        elif end < 30:
            button_back = Button(new_cust_win, text="<<",state = DISABLED)
            
        print_records = ""
        i = end
        while i >= 0:
            print_records = str(records[i]) + "\n" + print_records
            i= i-1
        query_label = Label(new_cust_win, text=print_records)
        query_label.grid(row=8, column=0, columnspan=2)
        button_forward = Button(new_cust_win, text = ">>", command = lambda: forward(query_label,records,i))
        button_forward.grid(row=8, column=2)
    def forward(prev,records, start):
        button_back = Button(new_cust_win, text = "<<", command = lambda: backward(query_label,records,start))
        button_back.grid(row=8, column=0)

        prev.config(text = "")
        print_records = ""
        i = start
        while i < start+30 and i < len(records):
            print_records += str(records[i]) + "\n"
            i= i+1
        query_label = Label(new_cust_win, text=print_records)
        query_label.grid(row=8, column=0, columnspan=2)
        button_forward = Button(new_cust_win, text = ">>", command = lambda: forward(query_label,records,i))
        button_forward.grid(row=8, column=2)
        if len(records) <= 30+start:
            button_forward = Button(new_cust_win, text=">>",state = DISABLED)


    def query():

        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()

        click.execute("SELECT * FROM Customer")

        records = click.fetchall()
        print_records = ""
        """
        i = 0
        
        while i < 30 and i < len(records):
            print_records += str(records[i]) + "\n"
            i= i+1
        i = 0
        query_label = Label(new_cust_win, text=print_records)
        query_label.grid(row=8, column=0, columnspan=2)
        if len(records) > 30:
            button_forward = Button(new_cust_win, text = ">>", command = lambda: forward(query_label,records,30))
            button_forward.grid(row=8, column=2)
        """
        for record in records:
            print_records += str(record) + "\n"
        query_label = Label(new_cust_win, text=print_records)
        query_label.grid(row=8, column=0, columnspan=2)
        query_button = Button(new_cust_win, text="Clear", command=lambda:
                          query_label.config(text=""))
        query_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        
        # commit changes
        new_conn.commit()
        # close connection
        new_conn.close()

    new_cust_win = Toplevel()
    new_cust_win.title('New Customer')
    
    name = Entry(new_cust_win, width=30)
    name.grid(row=1, column=1)
    
    phone = Entry(new_cust_win, width=30)
    phone.grid(row=3, column=1)

    name_label = Label(new_cust_win, text="Name")
    name_label.grid(row=1, column=0)

    name_hint = Label(new_cust_win, text="Preferred format: [First Initial] [Last Name]")
    name_hint.grid(row=2, column=1)

    phone_label = Label(new_cust_win, text="Phone")
    phone_label.grid(row=3, column=0)

    phone_hint = Label(new_cust_win, text="Phone must contain 10 digits typed al-together")
    phone_hint.grid(row=4, column=1)


    submit_button = Button(new_cust_win, text="Add Customer", command=submit)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    query_button = Button(new_cust_win, text="Show Records", command=query)
    query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    status = Label(new_cust_win, text="")
    status.grid(row=9, column=0, columnspan=2)




def new_vehicle():
    # submit values into the DB
    def submit():
        conn2 = sqlite3.connect('car_rental.db')
        c2 = conn2.cursor()

        c2.execute("INSERT INTO Vehicle VALUES(:v_id, :desc, :year, :v_type, :category)",
                   {
                       'v_id': vehicle_id.get(),
                       'desc': description.get(),
                       'year': year.get(),
                       'v_type': v_type.get(),
                       'category': category.get()
                   }
                   )

        # commit changes
        conn2.commit()

        # close connection
        conn2.close()

        # clear the text boxes
        vehicle_id.delete(0, END)
        description.delete(0, END)
        year.delete(0, END)
        v_type.delete(0, END)
        category.delete(0, END)

    def get_vehicles():
        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()

        click.execute("SELECT * FROM Vehicle")

        # print(c.fetchall())
        records = click.fetchall()
        # print(records)

        # Loop through results
        print_records = ""
        for record in records:
            print_records += str(record) + "\n"

        query_label = Label(new_car_win, text=print_records)
        query_label.grid(row=8, column=0, columnspan=2)

        # clear button to delete all vehicle info

        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()

    new_car_win = Toplevel()
    new_car_win.title('New Vehicle')

    # create text boxes
    vehicle_id = Entry(new_car_win, width=30)
    vehicle_id.grid(row=0, column=1, padx=20)

    description = Entry(new_car_win, width=30)
    description.grid(row=1, column=1)

    year = Entry(new_car_win, width=30)
    year.grid(row=2, column=1)

    v_type = Entry(new_car_win, width=30)
    v_type.grid(row=3, column=1)

    category = Entry(new_car_win, width=30)
    category.grid(row=4, column=1)

    # create text box labels
    v_id_label = Label(new_car_win, text="Vehicle ID")
    v_id_label.grid(row=0, column=0)

    des_label = Label(new_car_win, text="Description")
    des_label.grid(row=1, column=0)

    year_label = Label(new_car_win, text="Year")
    year_label.grid(row=2, column=0)

    type_label = Label(new_car_win, text="Type")
    type_label.grid(row=3, column=0)

    category_label = Label(new_car_win, text="Category")
    category_label.grid(row=4, column=0)

    # submit button
    submit_button = Button(new_car_win, text="Add Record", command=submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

    # show vehicles button
    show_button = Button(new_car_win, text="Show Records", command=get_vehicles)
    show_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)


def rental_click():
    def view_amount():
        conn2 = sqlite3.connect('car_rental.db')
        c2 = conn2.cursor()

        # c2.execute("SELECT RentalBalance FROM vRentalInfo WHERE CustomerID=? AND VIN=? AND ReturnDate=?",
        #           (cust_id.get(), v_id.get(), return_date.get(),))

        c2.execute("SELECT RentalBalance FROM vRentalInfo WHERE CustomerName=? AND VIN=? AND ReturnDate=?",
                   (c_name.get(), v_id.get(), return_date.get(),))

        amount_due = c2.fetchall()

        print_total = str(amount_due)  # + "\n"

        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        final_result = "$ "
        # Loop through each char
        for char in print_total:
            if char in numbers:
                final_result += char

        total = Label(rental_window, text="Total Amount Due: ")
        total.grid(row=7, column=0, columnspan=2)

        total_label = Label(rental_window, text=final_result)
        total_label.grid(row=7, column=1, columnspan=2)

        # commit changes
        conn2.commit()

        # close connection
        conn2.close()

    def submit_return():
        conn2 = sqlite3.connect('car_rental.db')
        c2 = conn2.cursor()

        # c2.execute("UPDATE Rental SET Returned=1 WHERE CustID= ? AND VehicleID=? AND ReturnDate=?",
        #           cust_id.get(), v_id.get(), return_date.get())

        c2.execute("UPDATE Rental SET Returned=1 WHERE CustID=(Select CustID FROM customer WHERE Name=?)"
                   "AND VehicleID=? AND ReturnDate=?",
                   (c_name.get(), v_id.get(), return_date.get(),))

        # commit changes
        conn2.commit()

        # close connection
        conn2.close()

        # clear the text boxes
        # cust_id.delete(0, END)
        c_name.delete(0, END)
        v_id.delete(0, END)
        return_date.delete(0, END)

    rental_window = Toplevel()
    rental_window.title('Return a Vehicle')
    instr = Label(rental_window, text="Please enter following information")
    instr.grid(row=0, column=0)

    # create text box labels
    cust_id_label = Label(rental_window, text="Customer Name")
    cust_id_label.grid(row=1, column=0)

    v_id_label = Label(rental_window, text="Vehicle ID")
    v_id_label.grid(row=2, column=0)

    return_label = Label(rental_window, text="Return Date")
    return_label.grid(row=3, column=0)

    # create text boxes
    # cust_id = Entry(rental_window, width=30)
    # cust_id.grid(row=1, column=1, padx=20)
    c_name = Entry(rental_window, width=30)
    c_name.grid(row=1, column=1, padx=20)

    v_id = Entry(rental_window, width=30)
    v_id.grid(row=2, column=1, padx=20)

    return_date = Entry(rental_window, width=30)
    return_date.grid(row=3, column=1, padx=20)

    # view amount button
    view_btn = Button(rental_window, text="View Amount Due", command=view_amount)
    view_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # submit button
    submit_btn = Button(rental_window, text="Submit Return", command=submit_return)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


def search_cars():
    def get_vehicles():
        new_conn = sqlite3.connect('car_rental.db')
        click = new_conn.cursor()

        if vehicle_id.get() == "" and description.get() == "" and part_des.get() == "":
            click.execute("""SELECT VIN, Description, OrderAmount/TotalDays
            FROM vehicle INNER JOIN vRentalInfo ON vehicle.VehicleID=vRentalInfo.VIN""")
        elif vehicle_id.get() != "":
            click.execute("""SELECT Vehicle.VehicleID, Description, OrderAmount/TotalDays
            FROM vehicle INNER JOIN vRentalInfo ON vehicle.VehicleID=vRentalInfo.VIN 
            AND vehicle.VehicleID=?""", (vehicle_id.get(),))
        elif description.get() != "":
            click.execute("""SELECT Vehicle.VehicleID, Description, OrderAmount/TotalDays
            FROM vehicle INNER JOIN vRentalInfo ON vehicle.VehicleID=vRentalInfo.VIN 
            AND Description=?""", (description.get(),))
        else:
            click.execute("""SELECT Vehicle.VehicleID, Description, OrderAmount/TotalDays
            FROM vehicle INNER JOIN vRentalInfo ON vehicle.VehicleID=vRentalInfo.VIN 
            AND Description=?""", (part_des.get(),))

        # print(c.fetchall())
        records = click.fetchall()
        # print(records)

        # Loop through results
        print_records = ""
        for record in records:
            print_records += str(record) + "\n"

        my_label = Label(new_car_win, text=print_records)
        my_label.grid(row=8, column=0, columnspan=2)

        # clear button to delete all vehicle info

        # commit changes
        new_conn.commit()

        # close connection
        new_conn.close()


    new_car_win = Toplevel()
    new_car_win.title('Search For Vehicle(s)')

    # create text boxes
    vehicle_id = Entry(new_car_win, width=30)
    vehicle_id.grid(row=0, column=1, padx=20)

    description = Entry(new_car_win, width=30)
    description.grid(row=1, column=1)

    part_des = Entry(new_car_win, width=30)
    part_des.grid(row=2, column=1)

    # create text box labels
    v_id_label = Label(new_car_win, text="Vehicle ID")
    v_id_label.grid(row=0, column=0)

    des_label = Label(new_car_win, text="Description")
    des_label.grid(row=1, column=0)

    part_des_label = Label(new_car_win, text="Part of Description")
    part_des_label.grid(row=2, column=0)

    # show vehicles button
    show_button = Button(new_car_win, text="Show Records", command=get_vehicles)
    show_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

    # clear result button
    # clear_button = Button(new_car_win, text="Clear Output", command=clear)
    # clear_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)


# create text box labels
welcome_label = Label(root, text="Welcome to Car Rental", font=("Helvetica", 14), bd=1, justify="left")
welcome_label.grid(row=0, column=0, padx=100)

# create buttons in home page
# NEED TO CHANGE FUNCTION NAMES
# Requirement 1: Add information about a new customer
new_cust = Button(root, text="New Customer", width=52, command=new_customer)
new_cust.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

# Requirement 2: Add information about a new vehicle
new_car = Button(root, text="New Vehicle", width=52, command=new_vehicle)
new_car.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

# Requirement 3: Add information about new rental reservation
new_rental = Button(root, text="New Rental", width=52, command=new_rental)
new_rental.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

# Requirement 4: Handle the return of a rented car.This transaction should print the total
# customer payment due for that rental, enter it in the database and update the returned attribute accordingly.
# You need to be able to retrieve a rental by the return date, customer name (the table needs the id),
# and vehicle info.Submit your editable SQL queries (retrieve & update rental) that your code executes.[6 points]

# return vehicle button
return_button = Button(root, text="Return Vehicle", width=52, command=rental_click)
return_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

# Requirement 5a: View's Results - Search Customers
search_cust = Button(root, text="Search Customer(s)", width=52, command=search_customer)
search_cust.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

# Requirement 5b: View's Results - Search Vehicles
search_car = Button(root, text="Search Vehicle(s)", width=52, command=search_vehicles)
search_car.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

# commit changes
conn.commit()

# close connection
conn.close()

root.mainloop()
