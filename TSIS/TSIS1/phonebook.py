import json
import csv
from connect import get_connection, execute_query, execute_procedure

class PhoneBook:
    def __init__(self):
        self.conn = get_connection()
        self.cur = None
        if self.conn:
            self.cur = self.conn.cursor()
        self.current_page = 0
        self.page_size = 5
        self.current_sort = "name"
    
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    
    def ensure_connection(self):
        if not self.conn or self.conn.closed:
            self.conn = get_connection()
            if self.conn:
                self.cur = self.conn.cursor()
            else:
                raise Exception("No database connection")
    
    def filter_by_group(self, group_name):
        self.ensure_connection()
        query = """
            SELECT c.name, c.email, c.birthday, g.name as group_name,
                   string_agg(p.phone || '(' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name = %s
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
        """
        self.cur.execute(query, (group_name,))
        return self.cur.fetchall()
    
    def search_by_email(self, email_pattern):
        self.ensure_connection()
        query = """
            SELECT c.name, c.email, c.birthday, g.name as group_name,
                   string_agg(p.phone || '(' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
        """
        self.cur.execute(query, (f'%{email_pattern}%',))
        return self.cur.fetchall()
    
    def sort_contacts(self, sort_by='name'):
        self.ensure_connection()
        valid_sort = {'name': 'c.name', 'birthday': 'c.birthday', 'date_added': 'c.id'}
        if sort_by not in valid_sort:
            sort_by = 'name'
        
        query = f"""
            SELECT c.name, c.email, c.birthday, g.name as group_name,
                   string_agg(p.phone || '(' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY {valid_sort[sort_by]}
        """
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def paginated_navigation(self, page=0, page_size=5, sort_by='name'):
        self.ensure_connection()
        offset = page * page_size
        query = f"""
            SELECT c.name, c.email, c.birthday, g.name as group_name,
                   string_agg(p.phone || '(' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY {sort_by}
            LIMIT %s OFFSET %s
        """
        self.cur.execute(query, (page_size, offset))
        return self.cur.fetchall()
    
    def display_paginated_menu(self):
        self.current_page = 0
        self.current_sort = 'name'
        
        while True:
            contacts = self.paginated_navigation(self.current_page, self.page_size, self.current_sort)
            
            print(f"\n{'='*60}")
            print(f"Page {self.current_page + 1} - Sorted by: {self.current_sort}")
            print(f"{'='*60}")
            
            if not contacts:
                print("No contacts found on this page.")
            else:
                for i, contact in enumerate(contacts, 1):
                    print(f"\n{i}. Name: {contact[0]}")
                    print(f"   Email: {contact[1] or 'N/A'}")
                    print(f"   Birthday: {contact[2] or 'N/A'}")
                    print(f"   Group: {contact[3] or 'No group'}")
                    print(f"   Phones: {contact[4] or 'No phones'}")
            
            print(f"\n{'='*60}")
            print("Commands: [n]ext, [p]rev, [s]ort, [q]uit")
            cmd = input("Your choice: ").lower()
            
            if cmd == 'n':
                next_page = self.paginated_navigation(self.current_page + 1, 1, self.current_sort)
                if next_page:
                    self.current_page += 1
                else:
                    print("You're on the last page!")
            elif cmd == 'p':
                if self.current_page > 0:
                    self.current_page -= 1
                else:
                    print("You're on the first page!")
            elif cmd == 's':
                print("Sort by: [n]ame, [b]irthday, [d]ate added")
                sort_choice = input("Choice: ").lower()
                sort_map = {'n': 'name', 'b': 'birthday', 'd': 'date_added'}
                if sort_choice in sort_map:
                    self.current_sort = sort_map[sort_choice]
                    self.current_page = 0
                    print(f"Now sorting by {self.current_sort}")
            elif cmd == 'q':
                break
            else:
                print("Invalid command!")
    
    def export_to_json(self, filename='contacts_export.json'):
        self.ensure_connection()
        query = """
            SELECT 
                c.name, 
                c.email, 
                c.birthday::text,
                g.name as group_name,
                json_agg(
                    json_build_object('phone', p.phone, 'type', p.type)
                ) as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE p.phone IS NOT NULL
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
        """
        self.cur.execute(query)
        contacts = self.cur.fetchall()
    
        data = []
        for contact in contacts:
            phones = contact[4] if contact[4] and contact[4][0] is not None else []
            data.append({
                'name': contact[0],
                'email': contact[1],
                'birthday': contact[2],
                'group': contact[3],
                'phones': phones
            })
    
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
        print(f"Exported {len(data)} contacts to {filename}")
        return len(data)
    
    def import_from_json(self, filename='contacts_export.json'):
        self.ensure_connection()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found!")
            return 0
    
        imported = 0
        for contact in contacts:
            self.cur.execute("SELECT id FROM contacts WHERE name = %s", (contact['name'],))
            exists = self.cur.fetchone()
        
            if exists:
                print(f"Contact '{contact['name']}' already exists.")
                choice = input("Skip (s) or Overwrite (o)? ").lower()
                if choice == 'o':
                    self.cur.execute("DELETE FROM contacts WHERE name = %s", (contact['name'],))
                    self.conn.commit()
                else:
                    continue
        
            group_id = None
            if contact.get('group') and contact['group']:
                self.cur.execute("SELECT id FROM groups WHERE name = %s", (contact['group'],))
                group = self.cur.fetchone()
                if group:
                    group_id = group[0]
                else:
                    self.cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (contact['group'],))
                    group_id = self.cur.fetchone()[0]
        
            birthday = None
            if contact.get('birthday') and contact['birthday'] and contact['birthday'] != 'None':
                birthday = contact['birthday']
        
            self.cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (contact['name'], contact.get('email'), birthday, group_id))
        
            contact_id = self.cur.fetchone()[0]
        
            for phone in contact.get('phones', []):
                phone_num = phone.get('phone')
                phone_type = phone.get('type', 'mobile')
            
                if phone_num and phone_num.strip():
                    self.cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, phone_num, phone_type))
        
            imported += 1
            self.conn.commit()
            print(f"Imported: {contact['name']}")
    
        print(f"Successfully imported {imported} contacts")
        return imported
    
    def import_from_csv(self, filename='contacts.csv'):
        self.ensure_connection()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        except FileNotFoundError:
            print(f"File {filename} not found!")
            return 0
        
        imported = 0
        for row in contacts:
            self.cur.execute("SELECT id FROM contacts WHERE name = %s", (row['name'],))
            if self.cur.fetchone():
                print(f"Contact {row['name']} already exists, skipping...")
                continue
            
            group_id = None
            if row.get('group'):
                self.cur.execute("SELECT id FROM groups WHERE name = %s", (row['group'],))
                group = self.cur.fetchone()
                if group:
                    group_id = group[0]
                else:
                    self.cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (row['group'],))
                    group_id = self.cur.fetchone()[0]
            
            birthday = row.get('birthday') if row.get('birthday') else None
            self.cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (row['name'], row.get('email'), birthday, group_id))
            
            contact_id = self.cur.fetchone()[0]
            
            phone_fields = [k for k in row.keys() if k.startswith('phone')]
            for phone_field in phone_fields:
                phone_num = row[phone_field]
                phone_type = row.get(phone_field.replace('phone', 'type'), 'mobile')
                if phone_num:
                    self.cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, phone_num, phone_type))
            
            imported += 1
        
        self.conn.commit()
        print(f"Imported {imported} contacts from CSV")
        return imported
    
    def add_phone(self, contact_name, phone, phone_type):
        self.ensure_connection()
        try:
            self.cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
            self.conn.commit()
            print(f"Phone {phone} ({phone_type}) added to {contact_name}")
            return True
        except Exception as e:
            print(f"Error adding phone: {e}")
            self.conn.rollback()
            return False

    def move_to_group(self, contact_name, group_name):
        self.ensure_connection()
        try:
            self.cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
            self.conn.commit()
            print(f"Contact {contact_name} moved to group {group_name}")
            return True
        except Exception as e:
            print(f"Error moving contact: {e}")
            self.conn.rollback()
            return False

    def search_contacts(self, query):
        self.ensure_connection()
        self.cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        return self.cur.fetchall()
    
    def display_results(self, results):
        if not results:
            print("\nNo results found.")
            return
        
        print(f"\n{'='*60}")
        print(f"Found {len(results)} contact(s)")
        print(f"{'='*60}")
        
        for i, row in enumerate(results, 1):
            print(f"\n{i}. Name: {row[0]}")
            print(f"   Email: {row[2] if len(row) > 2 else 'N/A'}")
            print(f"   Birthday: {row[3] if len(row) > 3 else 'N/A'}")
            print(f"   Group: {row[4] if len(row) > 4 else 'N/A'}")
            print(f"   Phones: {row[5] if len(row) > 5 else row[1]}")
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("PHONEBOOK EXTENDED - Main Menu")
            print("="*50)
            print("1. Filter by group")
            print("2. Search by email")
            print("3. Sort contacts")
            print("4. Paginated navigation")
            print("5. Export to JSON")
            print("6. Import from JSON")
            print("7. Import from CSV")
            print("8. Add phone to contact")
            print("9. Move contact to group")
            print("10. Search contacts")
            print("0. Exit")
            
            choice = input("\nYour choice: ")
            
            if choice == '1':
                group = input("Enter group name (Family/Work/Friend/Other): ")
                results = self.filter_by_group(group)
                self.display_results(results)
            
            elif choice == '2':
                pattern = input("Enter email pattern (e.g., 'gmail'): ")
                results = self.search_by_email(pattern)
                self.display_results(results)
            
            elif choice == '3':
                print("Sort by: [n]ame, [b]irthday, [d]ate added")
                sort_choice = input("Choice: ").lower()
                sort_map = {'n': 'name', 'b': 'birthday', 'd': 'date_added'}
                if sort_choice in sort_map:
                    results = self.sort_contacts(sort_map[sort_choice])
                    self.display_results(results)
            
            elif choice == '4':
                self.display_paginated_menu()
            
            elif choice == '5':
                self.export_to_json()
            
            elif choice == '6':
                filename = input("JSON filename (default: contacts_export.json): ") or 'contacts_export.json'
                self.import_from_json(filename)
            
            elif choice == '7':
                filename = input("CSV filename (default: contacts.csv): ") or 'contacts.csv'
                self.import_from_csv(filename)
            
            elif choice == '8':
                name = input("Contact name: ")
                phone = input("Phone number: ")
                ptype = input("Phone type (home/work/mobile): ")
                self.add_phone(name, phone, ptype)
            
            elif choice == '9':
                name = input("Contact name: ")
                group = input("Group name: ")
                self.move_to_group(name, group)
            
            elif choice == '10':
                query = input("Search query: ")
                results = self.search_contacts(query)
                self.display_results(results)
            
            elif choice == '0':
                print("Goodbye!")
                break

if __name__ == "__main__":
    pb = PhoneBook()
    try:
        pb.main_menu()
    finally:
        pb.close()