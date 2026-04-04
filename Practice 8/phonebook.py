import psycopg2
from psycopg2 import sql
from connect import get_connection

class PhoneBook:
    def __init__(self):
        self.conn = get_connection()
        if self.conn is None:
            raise Exception("Cannot connect to database")
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    #Calling FUNCTIONS 
    
    def search_contacts(self, pattern):
        """Search by name, surname, or phone"""
        try:
            self.cursor.execute("SELECT * FROM search_contacts(%s);", (pattern,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_paginated(self, page_num=1, page_size=10):
        """Get paginated list"""
        try:
            self.cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s);", 
                               (page_num, page_size))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Pagination error: {e}")
            return []
    
    def get_all_contacts(self):
        """Get all contacts"""
        try:
            self.cursor.execute("SELECT * FROM get_all_contacts();")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def find_by_phone(self, phone):
        """Find contact by phone number"""
        try:
            self.cursor.execute("SELECT * FROM find_by_phone(%s);", (phone,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    #Calling PROCEDURES
    
    def upsert_contact(self, name, surname, phone):
        """Insert or update a contact"""
        try:
            self.cursor.execute("CALL upsert_contact(%s, %s, %s);", 
                               (name, surname, phone))
            self.conn.commit()
            print(f"✓ {name} {surname} saved successfully")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Error: {e}")
            return False
    
    def insert_many_contacts(self, contacts_list):
        """Insert multiple contacts
        
        Args:
            contacts_list: List in format [[name, surname, phone], ...]
        """
        try:
            # Convert Python list to PostgreSQL array
            contacts_array = []
            for contact in contacts_list:
                contacts_array.append([contact[0], contact[1], contact[2]])
            
            # Create PostgreSQL array string
            array_str = "{"
            for c in contacts_array:
                array_str += f'{{{c[0]},{c[1]},{c[2]}}},'
            array_str = array_str.rstrip(',') + "}"
            
            self.cursor.execute("CALL insert_many_contacts(%s);", (array_str,))
            self.conn.commit()
            print(f"✓ {len(contacts_list)} contacts processed")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Error: {e}")
            return False
    
    def delete_contact(self, name=None, surname=None, phone=None):
        """Delete a contact"""
        try:
            self.cursor.execute("CALL delete_contact(%s, %s, %s);", 
                               (name, surname, phone))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Delete error: {e}")
            return False
    
    def clear_all(self):
        """Delete all contacts"""
        try:
            self.cursor.execute("CALL clear_all_contacts();")
            self.conn.commit()
            print("✓ All contacts deleted")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"✗ Error: {e}")
            return False

def main():
    print("=" * 50)
    print(" PhoneBook Program")
    print("=" * 50)
    
    pb = PhoneBook()
    
    while True:
        print("\nMenu:")
        print("1. Add/Update contact")
        print("2. Search contact")
        print("3. View all contacts")
        print("4. Pagination mode")
        print("5. Delete contact")
        print("6. Add multiple contacts (example)")
        print("7. Clear all")
        print("0. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == '1':
            name = input("First name: ")
            surname = input("Last name: ")
            phone = input("Phone: ")
            pb.upsert_contact(name, surname, phone)
            
        elif choice == '2':
            pattern = input("Search pattern: ")
            results = pb.search_contacts(pattern)
            print(f"\nResults ({len(results)}):")
            for r in results:
                print(f"  {r[1]} {r[2]} - {r[3]}")
                
        elif choice == '3':
            results = pb.get_all_contacts()
            print(f"\nAll contacts ({len(results)}):")
            for r in results:
                print(f"  {r[1]} {r[2]} - {r[3]}")
                
        elif choice == '4':
            page = int(input("Page number: "))
            size = int(input("Page size: "))
            results = pb.get_paginated(page, size)
            if results:
                total = results[0][4] if results else 0
                print(f"\nPage {page} ({len(results)}/{total}):")
                for r in results:
                    print(f"  {r[1]} {r[2]} - {r[3]}")
                    
        elif choice == '5':
            print("Delete by:")
            print("1. Phone number")
            print("2. Full name")
            print("3. First name only")
            del_choice = input("Choice: ")
            
            if del_choice == '1':
                phone = input("Phone: ")
                pb.delete_contact(phone=phone)
            elif del_choice == '2':
                name = input("First name: ")
                surname = input("Last name: ")
                pb.delete_contact(name=name, surname=surname)
            elif del_choice == '3':
                name = input("First name: ")
                pb.delete_contact(name=name)
                
        elif choice == '6':
            # Sample data
            sample_contacts = [
                ["Test1", "User1", "+77771112233"],
                ["Test2", "User2", "invalid_phone"],
                ["Test3", "User3", "+77774445566"],
                ["Ernar", "Aidar", "+77011234567"],
            ]
            print("Adding sample contacts...")
            pb.insert_many_contacts(sample_contacts)
            
        elif choice == '7':
            confirm = input("Delete all contacts? (y/n): ")
            if confirm.lower() == 'y':
                pb.clear_all()
                
        elif choice == '0':
            print("Goodbye! ")
            break
            
        else:
            print("Invalid choice!")
    
    pb.close()


if __name__ == "__main__":
    main()