import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# =========================
# DATABASE CONNECTION
# =========================

def connect_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Strong@6767",
            database="health_insurance"
        )
        return db

    except mysql.connector.Error as err:
        messagebox.showerror(
            "Database Error",
            f"Could not connect to MySQL.\n\n{err}"
        )
        return None


# =========================
# VIEW CUSTOMERS
# =========================

def view_customers():

    window = tk.Toplevel(root)
    window.title("Customer Directory")
    window.geometry("1200x650")
    window.configure(bg="#F5F7F5")


    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#123B3A",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)


    tk.Label(
        header,
        text="Customer Directory",
        bg="#123B3A",
        fg="white",
        font=("Arial", 22, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 2)
    )


    tk.Label(
        header,
        text="Search and manage registered customers",
        bg="#123B3A",
        fg="#B8CAC6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )


    # =========================
    # SEARCH AREA
    # =========================

    search_frame = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=20
    )


    tk.Label(
        search_frame,
        text="Search:",
        bg="#F5F7F5",
        fg="#24403F",
        font=("Arial", 11, "bold")
    ).pack(
        side="left"
    )


    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    search_entry.pack(
        side="left",
        padx=10,
        ipady=5
    )


    # =========================
    # TABLE FRAME
    # =========================

    table_frame = tk.Frame(
        window,
        bg="#ffffff"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=30
    )


    columns = (
        "ID",
        "First Name",
        "Last Name",
        "Date of Birth",
        "Gender",
        "Phone",
        "Email",
        "Address"
    )


    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    # Column headings

    for column in columns:

        table.heading(
            column,
            text=column
        )


    # Column widths

    table.column(
        "ID",
        width=50,
        anchor="center"
    )

    table.column(
        "First Name",
        width=110
    )

    table.column(
        "Last Name",
        width=110
    )

    table.column(
        "Date of Birth",
        width=110,
        anchor="center"
    )

    table.column(
        "Gender",
        width=80,
        anchor="center"
    )

    table.column(
        "Phone",
        width=120
    )

    table.column(
        "Email",
        width=220
    )

    table.column(
        "Address",
        width=180
    )


    # =========================
    # SCROLLBARS
    # =========================

    vertical_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    horizontal_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=table.xview
    )


    table.configure(
        yscrollcommand=vertical_scroll.set,
        xscrollcommand=horizontal_scroll.set
    )


    table.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scroll.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scroll.grid(
        row=1,
        column=0,
        sticky="ew"
    )


    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )


    # =========================
    # RECORD COUNT
    # =========================

    count_label = tk.Label(
        window,
        text="",
        bg="#F5F7F5",
        fg="#6B7C78",
        font=("Arial", 10)
    )

    count_label.pack(
        anchor="w",
        padx=30,
        pady=(8, 0)
    )


    # =========================
    # LOAD CUSTOMERS
    # =========================

    def load_customers(search_text=""):

        # Clear existing records

        for item in table.get_children():

            table.delete(item)


        db = connect_database()

        if db is None:
            return


        cursor = db.cursor()


        try:

            if search_text:

                query = """
                    SELECT
                        customer_id,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        phone,
                        email,
                        address
                    FROM Customer
                    WHERE
                        first_name LIKE %s
                        OR last_name LIKE %s
                        OR email LIKE %s
                        OR phone LIKE %s
                        OR address LIKE %s
                    ORDER BY customer_id
                """

                search_pattern = f"%{search_text}%"

                values = (
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern
                )

                cursor.execute(
                    query,
                    values
                )

            else:

                cursor.execute("""
                    SELECT
                        customer_id,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        phone,
                        email,
                        address
                    FROM Customer
                    ORDER BY customer_id
                """)


            records = cursor.fetchall()


            # Add records to table

            for record in records:

                table.insert(
                    "",
                    tk.END,
                    values=record
                )


            # Update count

            count_label.config(
                text=f"{len(records)} customer(s) found"
            )


        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                f"Could not retrieve customers.\n\n{err}"
            )


        finally:

            cursor.close()
            db.close()


    # =========================
    # SEARCH FUNCTION
    # =========================

    def search_customers():

        search_text = search_entry.get().strip()

        load_customers(
            search_text
        )


    # =========================
    # REFRESH FUNCTION
    # =========================

    def refresh_customers():

        search_entry.delete(
            0,
            tk.END
        )

        load_customers()


    # =========================
    # BUTTONS
    # =========================

    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        command=search_customers,
        bg="#0F766E",
        fg="white",
        activebackground="#0B5F59",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=10,
        cursor="hand2"
    )

    search_button.pack(
        side="left",
        padx=5,
        ipady=4
    )


    refresh_button = tk.Button(
        search_frame,
        text="REFRESH",
        command=refresh_customers,
        bg="#E1E8E5",
        fg="#24403F",
        activebackground="#B8CAC6",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=10,
        cursor="hand2"
    )

    refresh_button.pack(
        side="left",
        padx=5,
        ipady=4
    )


    # =========================
    # CLOSE BUTTON
    # =========================

    close_button = tk.Button(
        window,
        text="CLOSE",
        command=window.destroy,
        bg="#24403F",
        fg="white",
        activebackground="#123B3A",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=15,
        cursor="hand2"
    )

    close_button.pack(
        pady=15
    )


    # =========================
    # ENTER KEY SEARCH
    # =========================

    search_entry.bind(
        "<Return>",
        lambda event: search_customers()
    )


    # =========================
    # INITIAL LOAD
    # =========================

    load_customers()

    search_entry.focus()

# =========================
# ADD CUSTOMER
# =========================

def add_customer():

    window = tk.Toplevel(root)
    window.title("Add Customer")
    window.geometry("600x650")
    window.configure(bg="#F5F7F5")
    window.resizable(False, False)

    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#123B3A",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Add New Customer",
        bg="#123B3A",
        fg="white",
        font=("Arial", 22, "bold")
    ).pack(anchor="w", padx=30, pady=(20, 2))

    tk.Label(
        header,
        text="Enter customer information below",
        bg="#123B3A",
        fg="#B8CAC6",
        font=("Arial", 10)
    ).pack(anchor="w", padx=30)


    # =========================
    # FORM
    # =========================

    form = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    form.pack(
        padx=40,
        pady=25,
        fill="both"
    )


    # Function for labels

    def create_label(text, row):

        tk.Label(
            form,
            text=text,
            bg="#F5F7F5",
            fg="#24403F",
            font=("Arial", 10, "bold")
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=8
        )


    # First Name

    create_label("First Name *", 0)

    first_name_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    first_name_entry.grid(
        row=0,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=5
    )


    # Last Name

    create_label("Last Name *", 1)

    last_name_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    last_name_entry.grid(
        row=1,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=5
    )


    # Date of Birth

    create_label("Date of Birth *", 2)

    dob_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    dob_entry.grid(
        row=2,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=5
    )

    tk.Label(
        form,
        text="Format: YYYY-MM-DD",
        bg="#F5F7F5",
        fg="#6B7C78",
        font=("Arial", 8)
    ).grid(
        row=3,
        column=1,
        sticky="w",
        padx=(25, 0)
    )


    # Gender

    create_label("Gender", 4)

    gender_combo = ttk.Combobox(
        form,
        values=["Male", "Female", "Other"],
        width=33,
        state="readonly",
        font=("Arial", 10)
    )

    gender_combo.grid(
        row=4,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=4
    )


    # Phone

    create_label("Phone", 5)

    phone_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    phone_entry.grid(
        row=5,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=5
    )


    # Email

    create_label("Email", 6)

    email_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    email_entry.grid(
        row=6,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=5
    )


    # Address

    create_label("Address", 7)

    address_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    address_entry.grid(
        row=7,
        column=1,
        padx=(25, 0),
        pady=8,
        ipady=5
    )


    # =========================
    # VALIDATION
    # =========================

    def save_customer():

        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        dob = dob_entry.get().strip()
        gender = gender_combo.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()


        # Required fields

        if not first_name or not last_name or not dob:

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all required fields marked with *."
            )

            return


        # Validate date format

        try:

            from datetime import datetime

            datetime.strptime(
                dob,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Date of Birth must be in YYYY-MM-DD format.\n\nExample: 2005-01-15"
            )

            return


        # Validate phone

        if phone:

            if not phone.isdigit() or len(phone) != 10:

                messagebox.showerror(
                    "Invalid Phone",
                    "Phone number must contain exactly 10 digits."
                )

                return


        # Validate email

        if email:

            if "@" not in email or "." not in email:

                messagebox.showerror(
                    "Invalid Email",
                    "Please enter a valid email address."
                )

                return


        # =========================
        # DATABASE INSERT
        # =========================

        db = connect_database()

        if db is None:
            return

        cursor = db.cursor()


        try:

            query = """
                INSERT INTO Customer
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    phone,
                    email,
                    address
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                first_name,
                last_name,
                dob,
                gender,
                phone,
                email,
                address
            )


            cursor.execute(
                query,
                values
            )

            db.commit()


            # Get generated ID

            new_customer_id = cursor.lastrowid


            messagebox.showinfo(
                "Customer Added",
                f"Customer added successfully!\n\n"
                f"Customer ID: {new_customer_id}"
            )


            # Clear form

            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            dob_entry.delete(0, tk.END)
            gender_combo.set("")
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)


            first_name_entry.focus()


        except mysql.connector.Error as err:

            # Handle duplicate email

            if err.errno == 1062:

                messagebox.showerror(
                    "Duplicate Email",
                    "This email address already exists.\n\n"
                    "Please use a different email."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Could not add customer.\n\n{err}"
                )


        finally:

            cursor.close()
            db.close()


    # =========================
    # BUTTONS
    # =========================

    button_frame = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    button_frame.pack(
        pady=10
    )


    save_button = tk.Button(
        button_frame,
        text="ADD CUSTOMER",
        command=save_customer,
        bg="#0F766E",
        fg="white",
        activebackground="#0B5F59",
        activeforeground="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        width=18,
        height=2,
        cursor="hand2"
    )

    save_button.pack(
        side="left",
        padx=8
    )


    cancel_button = tk.Button(
        button_frame,
        text="CANCEL",
        command=window.destroy,
        bg="#E1E8E5",
        fg="#24403F",
        activebackground="#B8CAC6",
        font=("Arial", 11, "bold"),
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )

    cancel_button.pack(
        side="left",
        padx=8
    )


    # Focus first field

    first_name_entry.focus()

# =========================
# DELETE CUSTOMER
# =========================

def delete_customer():

    window = tk.Toplevel(root)
    window.title("Delete Customer")
    window.geometry("550x400")
    window.configure(bg="#F5F7F5")
    window.resizable(False, False)


    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#123B3A",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)


    tk.Label(
        header,
        text="Delete Customer",
        bg="#123B3A",
        fg="white",
        font=("Arial", 22, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 2)
    )


    tk.Label(
        header,
        text="Remove an existing customer record",
        bg="#123B3A",
        fg="#B8CAC6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )


    # =========================
    # CONTENT
    # =========================

    content = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    content.pack(
        padx=40,
        pady=30
    )


    tk.Label(
        content,
        text="Customer ID",
        bg="#F5F7F5",
        fg="#24403F",
        font=("Arial", 11, "bold")
    ).pack(
        pady=(0, 8)
    )


    customer_id_entry = tk.Entry(
        content,
        width=30,
        font=("Arial", 12),
        relief="solid",
        borderwidth=1,
        justify="center"
    )

    customer_id_entry.pack(
        ipady=7
    )


    tk.Label(
        content,
        text="Enter the ID of the customer you want to delete.",
        bg="#F5F7F5",
        fg="#6B7C78",
        font=("Arial", 9)
    ).pack(
        pady=8
    )


    # =========================
    # DELETE FUNCTION
    # =========================

    def remove_customer():

        customer_id = customer_id_entry.get().strip()


        # Check empty

        if not customer_id:

            messagebox.showwarning(
                "Missing Customer ID",
                "Please enter a Customer ID."
            )

            return


        # Check numeric

        if not customer_id.isdigit():

            messagebox.showerror(
                "Invalid Customer ID",
                "Customer ID must be a number."
            )

            return


        db = connect_database()

        if db is None:
            return

        cursor = db.cursor()


        try:

            # Find customer

            cursor.execute(
                """
                SELECT
                    first_name,
                    last_name,
                    email
                FROM Customer
                WHERE customer_id = %s
                """,
                (customer_id,)
            )


            customer = cursor.fetchone()


            # Customer doesn't exist

            if customer is None:

                messagebox.showerror(
                    "Customer Not Found",
                    f"No customer exists with ID {customer_id}."
                )

                return


            first_name = customer[0]
            last_name = customer[1]
            email = customer[2]


            # Confirmation

            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete:\n\n"
                f"Customer ID: {customer_id}\n"
                f"Name: {first_name} {last_name}\n"
                f"Email: {email or 'N/A'}\n\n"
                f"This action cannot be undone."
            )


            if not confirm:
                return


            # Delete

            cursor.execute(
                """
                DELETE FROM Customer
                WHERE customer_id = %s
                """,
                (customer_id,)
            )


            db.commit()


            messagebox.showinfo(
                "Customer Deleted",
                f"Customer {customer_id} was deleted successfully."
            )


            customer_id_entry.delete(
                0,
                tk.END
            )


        except mysql.connector.Error as err:

            # Foreign key error

            if err.errno == 1451:

                messagebox.showerror(
                    "Cannot Delete Customer",
                    "This customer cannot be deleted because "
                    "they have related policy records.\n\n"
                    "Delete the related records first."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Could not delete customer.\n\n{err}"
                )


        finally:

            cursor.close()
            db.close()


    # =========================
    # BUTTONS
    # =========================

    button_frame = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    button_frame.pack(
        pady=5
    )


    delete_button = tk.Button(
        button_frame,
        text="DELETE CUSTOMER",
        command=remove_customer,
        bg="#C94B4B",
        fg="white",
        activebackground="#A83D3D",
        activeforeground="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        width=18,
        height=2,
        cursor="hand2"
    )

    delete_button.pack(
        side="left",
        padx=8
    )


    cancel_button = tk.Button(
        button_frame,
        text="CANCEL",
        command=window.destroy,
        bg="#E1E8E5",
        fg="#24403F",
        activebackground="#B8CAC6",
        font=("Arial", 11, "bold"),
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )

    cancel_button.pack(
        side="left",
        padx=8
    )


    customer_id_entry.focus()

def view_policies():

    window = tk.Toplevel(root)
    window.title("Policy Portfolio")
    window.geometry("1250x650")
    window.configure(bg="#F5F7F5")


    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#123B3A",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)


    tk.Label(
        header,
        text="Policy Portfolio",
        bg="#123B3A",
        fg="white",
        font=("Arial", 22, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 2)
    )


    tk.Label(
        header,
        text="Browse active and historical policies",
        bg="#123B3A",
        fg="#B8CAC6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )


    # =========================
    # SEARCH
    # =========================

    search_frame = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=20
    )


    tk.Label(
        search_frame,
        text="Search:",
        bg="#F5F7F5",
        fg="#24403F",
        font=("Arial", 11, "bold")
    ).pack(
        side="left"
    )


    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    search_entry.pack(
        side="left",
        padx=10,
        ipady=5
    )


    # =========================
    # TABLE
    # =========================

    table_frame = tk.Frame(
        window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=30
    )


    columns = (
        "Policy ID",
        "Customer",
        "Company",
        "Policy Type",
        "Start Date",
        "End Date",
        "Premium",
        "Sum Insured",
        "Status"
    )


    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    for column in columns:

        table.heading(
            column,
            text=column
        )


    table.column(
        "Policy ID",
        width=70,
        anchor="center"
    )

    table.column(
        "Customer",
        width=150
    )

    table.column(
        "Company",
        width=170
    )

    table.column(
        "Policy Type",
        width=120
    )

    table.column(
        "Start Date",
        width=100,
        anchor="center"
    )

    table.column(
        "End Date",
        width=100,
        anchor="center"
    )

    table.column(
        "Premium",
        width=100,
        anchor="e"
    )

    table.column(
        "Sum Insured",
        width=120,
        anchor="e"
    )

    table.column(
        "Status",
        width=90,
        anchor="center"
    )


    # =========================
    # SCROLLBARS
    # =========================

    vertical_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    horizontal_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=table.xview
    )


    table.configure(
        yscrollcommand=vertical_scroll.set,
        xscrollcommand=horizontal_scroll.set
    )


    table.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scroll.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scroll.grid(
        row=1,
        column=0,
        sticky="ew"
    )


    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )


    # =========================
    # COUNT
    # =========================

    count_label = tk.Label(
        window,
        text="",
        bg="#F5F7F5",
        fg="#6B7C78",
        font=("Arial", 10)
    )

    count_label.pack(
        anchor="w",
        padx=30,
        pady=(8, 0)
    )


    # =========================
    # LOAD POLICIES
    # =========================

    def load_policies(search_text=""):

        for item in table.get_children():
            table.delete(item)


        db = connect_database()

        if db is None:
            return


        cursor = db.cursor()


        try:

            query = """
                SELECT
                    p.policy_id,
                    CONCAT(c.first_name, ' ', c.last_name)
                        AS customer_name,
                    ic.company_name,
                    pt.type_name,
                    p.start_date,
                    p.end_date,
                    p.premium,
                    p.sum_insured,
                    p.status
                FROM Policy p

                JOIN Customer c
                    ON p.customer_id = c.customer_id

                JOIN Insurance_Company ic
                    ON p.company_id = ic.company_id

                JOIN Policy_Type pt
                    ON p.policy_type_id = pt.policy_type_id
            """


            if search_text:

                query += """
                    WHERE
                        CONCAT(c.first_name, ' ', c.last_name)
                            LIKE %s
                        OR ic.company_name LIKE %s
                        OR pt.type_name LIKE %s
                        OR p.status LIKE %s
                """

                pattern = f"%{search_text}%"

                cursor.execute(
                    query + " ORDER BY p.policy_id",
                    (
                        pattern,
                        pattern,
                        pattern,
                        pattern
                    )
                )

            else:

                cursor.execute(
                    query + " ORDER BY p.policy_id"
                )


            records = cursor.fetchall()


            for record in records:

                table.insert(
                    "",
                    tk.END,
                    values=record
                )


            count_label.config(
                text=f"{len(records)} policy/policies found"
            )


        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                f"Could not retrieve policies.\n\n{err}"
            )


        finally:

            cursor.close()
            db.close()


    # =========================
    # SEARCH
    # =========================

    def search_policies():

        search_text = search_entry.get().strip()

        load_policies(
            search_text
        )


    # =========================
    # REFRESH
    # =========================

    def refresh_policies():

        search_entry.delete(
            0,
            tk.END
        )

        load_policies()


    # =========================
    # BUTTONS
    # =========================

    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        command=search_policies,
        bg="#0F766E",
        fg="white",
        activebackground="#0B5F59",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=10,
        cursor="hand2"
    )

    search_button.pack(
        side="left",
        padx=5,
        ipady=4
    )


    refresh_button = tk.Button(
        search_frame,
        text="REFRESH",
        command=refresh_policies,
        bg="#E1E8E5",
        fg="#24403F",
        activebackground="#B8CAC6",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=10,
        cursor="hand2"
    )

    refresh_button.pack(
        side="left",
        padx=5,
        ipady=4
    )


    # =========================
    # CLOSE
    # =========================

    close_button = tk.Button(
        window,
        text="CLOSE",
        command=window.destroy,
        bg="#24403F",
        fg="white",
        activebackground="#123B3A",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=15,
        cursor="hand2"
    )

    close_button.pack(
        pady=15
    )


    # Enter = Search

    search_entry.bind(
        "<Return>",
        lambda event: search_policies()
    )


    # Initial load

    load_policies()

    search_entry.focus()

def add_policy():

    window = tk.Toplevel(root)
    window.title("Add Policy")
    window.geometry("650x700")
    window.configure(bg="#F5F7F5")
    window.resizable(False, False)


    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#123B3A",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Add New Policy",
        bg="#123B3A",
        fg="white",
        font=("Arial", 22, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 2)
    )

    tk.Label(
        header,
        text="Create a new insurance policy",
        bg="#123B3A",
        fg="#B8CAC6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )


    # =========================
    # FORM
    # =========================

    form = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    form.pack(
        padx=40,
        pady=25
    )


    def create_label(text, row):

        tk.Label(
            form,
            text=text,
            bg="#F5F7F5",
            fg="#24403F",
            font=("Arial", 10, "bold")
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=9
        )


    # =========================
    # LOAD DATABASE OPTIONS
    # =========================

    db = connect_database()

    if db is None:
        window.destroy()
        return

    cursor = db.cursor()

    try:

        # Customers

        cursor.execute("""
            SELECT customer_id,
                   CONCAT(first_name, ' ', last_name)
            FROM Customer
            ORDER BY first_name
        """)

        customers = cursor.fetchall()


        # Insurance companies

        cursor.execute("""
            SELECT company_id,
                   company_name
            FROM Insurance_Company
            ORDER BY company_name
        """)

        companies = cursor.fetchall()


        # Policy types

        cursor.execute("""
            SELECT policy_type_id,
                   type_name
            FROM Policy_Type
            ORDER BY type_name
        """)

        policy_types = cursor.fetchall()


    except mysql.connector.Error as err:

        messagebox.showerror(
            "Database Error",
            f"Could not load policy information.\n\n{err}"
        )

        cursor.close()
        db.close()
        window.destroy()
        return

    finally:

        cursor.close()
        db.close()


    # =========================
    # CUSTOMER
    # =========================

    create_label("Customer *", 0)

    customer_values = [
        f"{customer[0]} - {customer[1]}"
        for customer in customers
    ]

    customer_combo = ttk.Combobox(
        form,
        values=customer_values,
        width=38,
        state="readonly",
        font=("Arial", 10)
    )

    customer_combo.grid(
        row=0,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # INSURANCE COMPANY
    # =========================

    create_label("Insurance Company *", 1)

    company_values = [
        f"{company[0]} - {company[1]}"
        for company in companies
    ]

    company_combo = ttk.Combobox(
        form,
        values=company_values,
        width=38,
        state="readonly",
        font=("Arial", 10)
    )

    company_combo.grid(
        row=1,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # POLICY TYPE
    # =========================

    create_label("Policy Type *", 2)

    type_values = [
        f"{policy_type[0]} - {policy_type[1]}"
        for policy_type in policy_types
    ]

    type_combo = ttk.Combobox(
        form,
        values=type_values,
        width=38,
        state="readonly",
        font=("Arial", 10)
    )

    type_combo.grid(
        row=2,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # START DATE
    # =========================

    create_label("Start Date *", 3)

    start_date_entry = tk.Entry(
        form,
        width=40,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    start_date_entry.grid(
        row=3,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    tk.Label(
        form,
        text="Format: YYYY-MM-DD",
        bg="#F5F7F5",
        fg="#6B7C78",
        font=("Arial", 8)
    ).grid(
        row=4,
        column=1,
        sticky="w",
        padx=(25, 0)
    )


    # =========================
    # END DATE
    # =========================

    create_label("End Date *", 5)

    end_date_entry = tk.Entry(
        form,
        width=40,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    end_date_entry.grid(
        row=5,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # PREMIUM
    # =========================

    create_label("Premium *", 6)

    premium_entry = tk.Entry(
        form,
        width=40,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    premium_entry.grid(
        row=6,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # SUM INSURED
    # =========================

    create_label("Sum Insured *", 7)

    sum_insured_entry = tk.Entry(
        form,
        width=40,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    sum_insured_entry.grid(
        row=7,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # STATUS
    # =========================

    create_label("Status *", 8)

    status_combo = ttk.Combobox(
        form,
        values=[
            "Active",
            "Expired",
            "Cancelled"
        ],
        width=38,
        state="readonly",
        font=("Arial", 10)
    )

    status_combo.grid(
        row=8,
        column=1,
        padx=(25, 0),
        pady=9,
        ipady=5
    )


    # =========================
    # SAVE POLICY
    # =========================

    def save_policy():

        # Make sure selections exist

        if not customer_combo.get():
            messagebox.showwarning(
                "Missing Information",
                "Please select a customer."
            )
            return

        if not company_combo.get():
            messagebox.showwarning(
                "Missing Information",
                "Please select an insurance company."
            )
            return

        if not type_combo.get():
            messagebox.showwarning(
                "Missing Information",
                "Please select a policy type."
            )
            return


        start_date = start_date_entry.get().strip()
        end_date = end_date_entry.get().strip()
        premium = premium_entry.get().strip()
        sum_insured = sum_insured_entry.get().strip()
        status = status_combo.get().strip()


        # Required fields

        if not start_date or not end_date:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both start and end dates."
            )
            return


        if not premium or not sum_insured:
            messagebox.showwarning(
                "Missing Information",
                "Please enter premium and sum insured."
            )
            return


        if not status:
            messagebox.showwarning(
                "Missing Information",
                "Please select a policy status."
            )
            return


        # =========================
        # DATE VALIDATION
        # =========================

        from datetime import datetime

        try:

            start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            )

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Dates must use YYYY-MM-DD format."
            )

            return


        if end <= start:

            messagebox.showerror(
                "Invalid Dates",
                "End Date must be later than Start Date."
            )

            return


        # =========================
        # NUMBER VALIDATION
        # =========================

        try:

            premium_value = float(premium)
            sum_insured_value = float(sum_insured)

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Premium and Sum Insured must be numbers."
            )

            return


        if premium_value <= 0:

            messagebox.showerror(
                "Invalid Premium",
                "Premium must be greater than zero."
            )

            return


        if sum_insured_value <= 0:

            messagebox.showerror(
                "Invalid Sum Insured",
                "Sum Insured must be greater than zero."
            )

            return


        # =========================
        # EXTRACT FOREIGN KEYS
        # =========================

        customer_id = int(
            customer_combo.get().split(" - ")[0]
        )

        company_id = int(
            company_combo.get().split(" - ")[0]
        )

        policy_type_id = int(
            type_combo.get().split(" - ")[0]
        )


        # =========================
        # INSERT POLICY
        # =========================

        db = connect_database()

        if db is None:
            return

        cursor = db.cursor()

        try:

            query = """
                INSERT INTO Policy
                (
                    customer_id,
                    company_id,
                    policy_type_id,
                    start_date,
                    end_date,
                    premium,
                    sum_insured,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                customer_id,
                company_id,
                policy_type_id,
                start_date,
                end_date,
                premium_value,
                sum_insured_value,
                status
            )


            cursor.execute(
                query,
                values
            )

            db.commit()


            new_policy_id = cursor.lastrowid


            messagebox.showinfo(
                "Policy Added",
                f"Policy added successfully!\n\n"
                f"Policy ID: {new_policy_id}"
            )


            # Clear form

            customer_combo.set("")
            company_combo.set("")
            type_combo.set("")
            start_date_entry.delete(0, tk.END)
            end_date_entry.delete(0, tk.END)
            premium_entry.delete(0, tk.END)
            sum_insured_entry.delete(0, tk.END)
            status_combo.set("")


        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                f"Could not add policy.\n\n{err}"
            )


        finally:

            cursor.close()
            db.close()


    # =========================
    # BUTTONS
    # =========================

    button_frame = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    button_frame.pack(
        pady=10
    )


    save_button = tk.Button(
        button_frame,
        text="ADD POLICY",
        command=save_policy,
        bg="#0F766E",
        fg="white",
        activebackground="#0B5F59",
        activeforeground="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        width=18,
        height=2,
        cursor="hand2"
    )

    save_button.pack(
        side="left",
        padx=8
    )


    cancel_button = tk.Button(
        button_frame,
        text="CANCEL",
        command=window.destroy,
        bg="#E1E8E5",
        fg="#24403F",
        activebackground="#B8CAC6",
        font=("Arial", 11, "bold"),
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    
    )

    cancel_button.pack(
        side="left",
        padx=8
    )

def view_claims():

    window = tk.Toplevel(root)
    window.title("Claims Register")
    window.geometry("1350x700")
    window.configure(bg="#F5F7F5")


    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#123B3A",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)


    tk.Label(
        header,
        text="Claims Register",
        bg="#123B3A",
        fg="white",
        font=("Arial", 22, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 2)
    )


    tk.Label(
        header,
        text="Review submitted and processed claims",
        bg="#123B3A",
        fg="#B8CAC6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )


    # =========================
    # SEARCH AREA
    # =========================

    search_frame = tk.Frame(
        window,
        bg="#F5F7F5"
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=20
    )


    tk.Label(
        search_frame,
        text="Search:",
        bg="#F5F7F5",
        fg="#24403F",
        font=("Arial", 11, "bold")
    ).pack(
        side="left"
    )


    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    search_entry.pack(
        side="left",
        padx=10,
        ipady=5
    )


    # =========================
    # TABLE
    # =========================

    table_frame = tk.Frame(
        window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=30
    )


    columns = (
        "Claim ID",
        "Customer",
        "Policy ID",
        "Hospital",
        "Treatment",
        "Claim Date",
        "Claimed",
        "Approved",
        "Status",
        "Remarks"
    )


    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    for column in columns:

        table.heading(
            column,
            text=column
        )


    table.column(
        "Claim ID",
        width=70,
        anchor="center"
    )

    table.column(
        "Customer",
        width=140
    )

    table.column(
        "Policy ID",
        width=80,
        anchor="center"
    )

    table.column(
        "Hospital",
        width=150
    )

    table.column(
        "Treatment",
        width=150
    )

    table.column(
        "Claim Date",
        width=100,
        anchor="center"
    )

    table.column(
        "Claimed",
        width=100,
        anchor="e"
    )

    table.column(
        "Approved",
        width=100,
        anchor="e"
    )

    table.column(
        "Status",
        width=90,
        anchor="center"
    )

    table.column(
        "Remarks",
        width=220
    )


    # =========================
    # SCROLLBARS
    # =========================

    vertical_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    horizontal_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=table.xview
    )


    table.configure(
        yscrollcommand=vertical_scroll.set,
        xscrollcommand=horizontal_scroll.set
    )


    table.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scroll.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scroll.grid(
        row=1,
        column=0,
        sticky="ew"
    )


    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )


    # =========================
    # COUNT
    # =========================

    count_label = tk.Label(
        window,
        text="",
        bg="#F5F7F5",
        fg="#6B7C78",
        font=("Arial", 10)
    )

    count_label.pack(
        anchor="w",
        padx=30,
        pady=(8, 0)
    )


    # =========================
    # LOAD CLAIMS
    # =========================

    def load_claims(search_text=""):

        # Clear table

        for item in table.get_children():

            table.delete(item)


        db = connect_database()

        if db is None:
            return


        cursor = db.cursor()


        try:

            query = """
                SELECT
                    cl.claim_id,

                    CONCAT(
                        c.first_name,
                        ' ',
                        c.last_name
                    ) AS customer_name,

                    cl.policy_id,

                    h.hospital_name,

                    t.treatment_name,

                    cl.claim_date,

                    cl.amount_claimed,

                    cl.amount_approved,

                    cl.status,

                    cl.remarks

                FROM Claim cl

                JOIN Policy p
                    ON cl.policy_id = p.policy_id

                JOIN Customer c
                    ON p.customer_id = c.customer_id

                JOIN Hospital h
                    ON cl.hospital_id = h.hospital_id

                JOIN Treatment t
                    ON cl.treatment_id = t.treatment_id
            """


            if search_text:

                query += """
                    WHERE
                        CONCAT(
                            c.first_name,
                            ' ',
                            c.last_name
                        ) LIKE %s

                        OR h.hospital_name LIKE %s

                        OR t.treatment_name LIKE %s

                        OR cl.status LIKE %s

                        OR cl.remarks LIKE %s
                """

                pattern = f"%{search_text}%"

                cursor.execute(
                    query + " ORDER BY cl.claim_id",
                    (
                        pattern,
                        pattern,
                        pattern,
                        pattern,
                        pattern
                    )
                )

            else:

                cursor.execute(
                    query + " ORDER BY cl.claim_id"
                )


            records = cursor.fetchall()


            # Add records

            for record in records:

                table.insert(
                    "",
                    tk.END,
                    values=record
                )


            count_label.config(
                text=f"{len(records)} claim(s) found"
            )


        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                f"Could not retrieve claims.\n\n{err}"
            )


        finally:

            cursor.close()
            db.close()


    # =========================
    # SEARCH
    # =========================

    def search_claims():

        search_text = search_entry.get().strip()

        load_claims(
            search_text
        )


    # =========================
    # REFRESH
    # =========================

    def refresh_claims():

        search_entry.delete(
            0,
            tk.END
        )

        load_claims()


    # =========================
    # BUTTONS
    # =========================

    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        command=search_claims,
        bg="#0F766E",
        fg="white",
        activebackground="#0B5F59",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=10,
        cursor="hand2"
    )

    search_button.pack(
        side="left",
        padx=5,
        ipady=4
    )


    refresh_button = tk.Button(
        search_frame,
        text="REFRESH",
        command=refresh_claims,
        bg="#E1E8E5",
        fg="#24403F",
        activebackground="#B8CAC6",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=10,
        cursor="hand2"
    )

    refresh_button.pack(
        side="left",
        padx=5,
        ipady=4
    )


    # =========================
    # CLOSE
    # =========================

    close_button = tk.Button(
        window,
        text="CLOSE",
        command=window.destroy,
        bg="#24403F",
        fg="white",
        activebackground="#123B3A",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=15,
        cursor="hand2"
    )

    close_button.pack(
        pady=15
    )


    # Enter key = Search

    search_entry.bind(
        "<Return>",
        lambda event: search_claims()
    )


    # Initial load

    load_claims()

    search_entry.focus()

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Health Insurance Management System")
root.geometry("1000x650")
root.configure(bg="#F5F7F5")


# =========================
# UI THEME
# =========================

style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground="#18302F",
    rowheight=30,
    fieldbackground="#FFFFFF",
    font=("Arial", 10),
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background="#DCE9E6",
    foreground="#123B3A",
    font=("Arial", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", "#CFE7E2")],
    foreground=[("selected", "#123B3A")]
)

style.configure(
    "TCombobox",
    fieldbackground="#FFFFFF",
    background="#FFFFFF",
    foreground="#18302F",
    bordercolor="#B7C8C4",
    arrowsize=14
)


# =========================
# COLORS
# =========================

SIDEBAR_COLOR = "#123B3A"
MAIN_COLOR = "#F5F7F5"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#18302F"
SECONDARY_TEXT = "#6B7C78"


# =========================
# SIDEBAR
# =========================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR_COLOR,
    width=250
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# Application title

app_title = tk.Label(
    sidebar,
    text="HEALTHCARE\nINSURANCE",
    bg=SIDEBAR_COLOR,
    fg="white",
    font=("Arial", 18, "bold"),
    justify="left"
)

app_title.pack(
    anchor="w",
    padx=24,
    pady=(30, 5)
)


subtitle = tk.Label(
    sidebar,
    text="Policy & Claims Hub",
    bg=SIDEBAR_COLOR,
    fg="#9ca3af",
    font=("Arial", 10)
)

subtitle.pack(
    anchor="w",
    padx=24,
    pady=(0, 28)
)


# =========================
# SIDEBAR BUTTON FUNCTION
# =========================

def sidebar_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=SIDEBAR_COLOR,
        fg="white",
        activebackground="#24403F",
        activeforeground="white",
        relief="flat",
        borderwidth=0,
        font=("Arial", 11),
        anchor="w",
        padx=25,
        height=2,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        pady=2
    )

    return button


# Sidebar buttons

sidebar_button(
    "  🏠  Dashboard",
    lambda: show_dashboard()
)

sidebar_button(
    "  👤  View Customers",
    view_customers
)

sidebar_button(
    "  📋  View Policies",
    view_policies
)

sidebar_button(
    "  📄  View Claims",
    view_claims
)

sidebar_button(
    "  ➕  Add Policy",
    add_policy
)

sidebar_button(
    "  ➕  Add Customer",
    add_customer
)

sidebar_button(
    "  🗑  Delete Customer",
    delete_customer
)


# Separator

separator = tk.Frame(
    sidebar,
    bg="#24403F",
    height=1
)

separator.pack(
    fill="x",
    padx=20,
    pady=25
)


sidebar_button(
    "  ✕  Exit",
    root.destroy
)


# =========================
# MAIN CONTENT AREA
# =========================

main_area = tk.Frame(
    root,
    bg=MAIN_COLOR
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================
# DASHBOARD
# =========================

def show_dashboard():

    # Clear main area

    for widget in main_area.winfo_children():
        widget.destroy()


    # Header

    header = tk.Frame(
        main_area,
        bg=MAIN_COLOR
    )

    header.pack(
        fill="x",
        padx=40,
        pady=(35, 20)
    )


    title = tk.Label(
        header,
        text="Operations Hub",
        bg=MAIN_COLOR,
        fg=TEXT_COLOR,
        font=("Arial", 26, "bold")
    )

    title.pack(
        anchor="w"
    )


    description = tk.Label(
        header,
        text="Policy, customer and claims management",
        bg=MAIN_COLOR,
        fg=SECONDARY_TEXT,
        font=("Arial", 11)
    )

    description.pack(
        anchor="w",
        pady=(5, 0)
    )


    # =========================
    # STAT CARDS
    # =========================

    cards_frame = tk.Frame(
        main_area,
        bg=MAIN_COLOR
    )

    cards_frame.pack(
        fill="x",
        padx=40,
        pady=10
    )


    # Get database statistics

    customer_count = 0
    policy_count = 0
    claim_count = 0

    db = connect_database()

    if db:

        cursor = db.cursor()

        try:

            cursor.execute(
                "SELECT COUNT(*) FROM Customer"
            )

            customer_count = cursor.fetchone()[0]


            cursor.execute(
                "SELECT COUNT(*) FROM Policy"
            )

            policy_count = cursor.fetchone()[0]


            cursor.execute(
                "SELECT COUNT(*) FROM Claim"
            )

            claim_count = cursor.fetchone()[0]

        except mysql.connector.Error:
            pass

        finally:

            cursor.close()
            db.close()


    # Card creation function

    def create_card(parent, title, value):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR,
            width=190,
            height=128,
            highlightbackground="#E1E8E5",
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        card.pack_propagate(False)


        card_title = tk.Label(
            card,
            text=title,
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=("Arial", 11)
        )

        card_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        card_value = tk.Label(
            card,
            text=str(value),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 24, "bold")
        )

        card_value.pack(
            anchor="w",
            padx=20
        )


    create_card(
        cards_frame,
        "Customers",
        customer_count
    )

    create_card(
        cards_frame,
        "Policies",
        policy_count
    )

    create_card(
        cards_frame,
        "Claims",
        claim_count
    )


    # =========================
    # QUICK ACTIONS
    # =========================

    actions_title = tk.Label(
        main_area,
        text="Quick Actions",
        bg=MAIN_COLOR,
        fg=TEXT_COLOR,
        font=("Arial", 18, "bold")
    )

    actions_title.pack(
        anchor="w",
        padx=48,
        pady=(35, 15)
    )


    actions_frame = tk.Frame(
        main_area,
        bg=MAIN_COLOR
    )

    actions_frame.pack(
        fill="x",
        padx=40
    )


    # View button

    view_card = tk.Button(
        actions_frame,
        text="CUSTOMER DIRECTORY\n\nBrowse & search records",
        command=view_customers,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground="#E1E8E5",
        relief="flat",
        borderwidth=0,
        font=("Arial", 11, "bold"),
        height=5,
        cursor="hand2"
    )

    view_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )


    # Add button

    add_card = tk.Button(
        actions_frame,
        text="NEW CUSTOMER\n\nCreate a record",
        command=add_customer,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground="#E1E8E5",
        relief="flat",
        borderwidth=0,
        font=("Arial", 11, "bold"),
        height=5,
        cursor="hand2"
    )

    add_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )


    # Delete button

    delete_card = tk.Button(
        actions_frame,
        text="REMOVE CUSTOMER\n\nDelete a record",
        command=delete_customer,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground="#E1E8E5",
        relief="flat",
        borderwidth=0,
        font=("Arial", 11, "bold"),
        height=5,
        cursor="hand2"
    )

    delete_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )


    # =========================
    # DATABASE STATUS
    # =========================

    status_frame = tk.Frame(
        main_area,
        bg=CARD_COLOR,
        height=70,
        highlightbackground="#E1E8E5",
        highlightthickness=1
    )

    status_frame.pack(
        fill="x",
        padx=48,
        pady=40
    )

    status_frame.pack_propagate(False)


    status_label = tk.Label(
        status_frame,
        text="●  LIVE DATABASE",
        bg=CARD_COLOR,
        fg="#168A70",
        font=("Arial", 11, "bold")
    )

    status_label.pack(
        side="left",
        padx=20,
        pady=20
    )


    info_label = tk.Label(
        status_frame,
        text="MySQL  •  health_insurance",
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT,
        font=("Arial", 10)
    )

    info_label.pack(
        side="right",
        padx=20
    )


# =========================
# SHOW DASHBOARD
# =========================

show_dashboard()


# =========================
# START APPLICATION
# =========================

root.mainloop()