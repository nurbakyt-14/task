import csv
from connect import connect

# TABLE CREATE
def create_table():
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

# 2. INSERT FROM CSV
def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted")

# 3. INSERT FROM CONSOLE
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Inserted!")

# 4. UPDATE
def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Updated!")

# 5. QUERY FILTER
def search_contacts():
    keyword = input("Search (name or phone): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE name ILIKE %s OR phone LIKE %s",
        (f"%{keyword}%", f"{keyword}%")
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

# 6. DELETE
def delete_contact():
    keyword = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s OR phone=%s",
        (keyword, keyword)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted!")

# MENU
def menu():
    create_table()
    
    while True:
        print("""
1. Insert from CSV
2. Insert from console
3. Update contact
4. Search contact
5. Delete contact
6. Exit
""")
        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()