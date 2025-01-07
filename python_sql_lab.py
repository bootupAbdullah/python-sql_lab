import psycopg2 # type: ignore

connection = psycopg2.connect(database = 'crm_lab')
cursor = connection.cursor()

# cursor = connection.cursor()
# cursor.execute('SELECT * FROM employees')
# results = cursor.fetchall();

# print(results)

print('Welcome to CRM')

print('What would you like to do, please choose one of the following: ')
print('1. See Companies', '2. See Employees', '3. Quit')
main_menu_prompt = input('Enter Choice: ')

if main_menu_prompt == '1':
    cursor.execute('SELECT * FROM employees')
    results = cursor.fetchall()
    if results:
        print("\nEmployee Results")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Company ID: {row[2]}")
elif main_menu_prompt == '2':
    cursor.execute('SELECT * FROM companies')
    results = cursor.fetchall()
    if results:
        print("\nCompany Results")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Company ID: {row[2]}")
else:
    print('Thank You for using CRM.')
    connection.close()

def add_employee(user_input):
    employee_name = input('Enter the employees first name')
    cursor.execute('INSERT INTO employees')

class add_employee:
    def __init__(self, first_name, last_name, employer_id):
        self.



