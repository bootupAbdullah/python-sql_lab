import psycopg2 # type: ignore

# If id is managed by the database (e.g., as a SERIAL field that auto-increments), you can make it optional in the Employee class constructor by assigning it a default value (e.g., None).
# This way, you can create an Employee object without supplying an id.
class Employee:
    def __init__(self, id=None, first_name=None, last_name=None, employer_id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.employer_id = employer_id

class Company:
    def __init__(self, name, company_id):
        self.name = name
        self.company_id = company_id

# connects to database
connection = psycopg2.connect(database = 'crm_lab')
cursor = connection.cursor()

# ==== FUNCTIONS ====

# quit function
def quit():
    print('\nThank You for using CRM.')
    connection.close()


# <-------------------------------------------------------- CRUD FUNCTIONALITY  ------------------------------------------------------------------------------------>



#<--------------------- CREATE  ---------------------------------------------------->

# add employee function, enables user to add employee to database, initial prompt when 'add' is selected from 'main menu'
def add_employee_to_db():
    # capture user inputs
    first_name = input("\nEnter the employees's first name: ")
    last_name = input("\nEnter the employees's last name: ")

    cursor.execute("SELECT name, company_id FROM companies")
    results = cursor.fetchall()
    if results:
        print("\nAvailable Companies: ")
        for row in results:
            print(f"\nName: {row[0]}, Company ID: {row[1]}")

        while True:
            try:
                employer_id = int(input("\nEnter a valid Company ID: "))
                # validates if that the employer_id matches the company_id in the companies table
                if any(row[1] == employer_id for row in results):
                      #create employee object
                    employee = Employee(first_name=first_name, last_name=last_name, employer_id=employer_id)

                    #  confirm and insert employee
                    confirmAddEmployee(employee)
                    break
                else:
                    print("\nInvalid Company ID. Please Try again. ")
            except ValueError:
                print("\nPlease enter a numeric Company ID. ")

            #print(employer_id)


# confirm add employee function, enables the user to inspect and finalize their input prior to the 'new employee' being added to the database. #2
def confirmAddEmployee(employee):
    print(f"\nEmployee: {employee.first_name} {employee.last_name}, Employer ID: {employee.employer_id}")
    confirm_employee = input("\nConfirm new Employee? (y/n): ")

    if confirm_employee.lower() == 'y':
        query = "INSERT INTO employees ( first_name, last_name, employer_id) VALUES (%s, %s, %s);"
        try:
            cursor.execute(query, (employee.first_name, employee.last_name, employee.employer_id))
            connection.commit() # commits the created entry
            print(f"\nEmployee {employee.first_name}, {employee.last_name} added successfully")
            mainMenu() # callbacks to the main menu after creation
        except psycopg2.IntegrityError as e:
                connection.rollback()  # roolbacks the transaction on an error
                print(f"\nDatabase error: {e}")
                mainMenu() #callback main menu if error occurs
        except psycopg2.Error as e: 
                print(f"\nUnexpected error: {e}")
                mainMenu() #callback main menu if error occurs

    elif confirm_employee.lower() =='n':
        print("\nCanceled action")
        add_employee_to_db() #callbacks the add employee function if canceled
    
    else:
        print("\nInvalid selection. Please enter 'y' or 'n'.")
        confirmAddEmployee(employee) #retrys confirmation



#<---------------------UPDATE  ---------------------------------------------------->

# update employee function, enables user to update employee, initial prompt when 'update' is selected from 'main menu'
def update_employee():
     
    cursor.execute("SELECT * FROM employees")
    employeeResults = cursor.fetchall()
    print("\nEmployee Results")
    for row in employeeResults:
        print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Employer ID: {row[3]}")
     
    while True:
        try:
     # capture user inputs
            id = int(input("\nEnter a valid Employee ID Number: "))
            # confirms that id exsist in the employees table
            if any(row[0] == id for row in employeeResults):
                first_name = input("\nEnter the employees's first name: ")
                last_name = input("\nEnter the employees's last name: ")

                cursor.execute("SELECT name, company_id FROM companies")
                companyResults = cursor.fetchall()
                if companyResults:
                    print("\nAvailable Companies: ")
                    for row in companyResults:
                        print(f"\nName: {row[0]}, Company ID: {row[1]}")
                    
                    while True:
                        try:
                            employer_id = int(input("\nEnter a valid Company ID: "))
                            # validates if that the employer_id matches the company_id in the companies table
                            if any(row[1] == employer_id for row in companyResults):
                                #create employee object
                                employee = Employee( id=id, first_name=first_name, last_name=last_name, employer_id=employer_id)

                                #  confirm and insert employee
                                confirmUpdateEmployee(employee)
                                break
                            else:
                                print("\nInvalid Company ID. Please Try again. ")
                        except ValueError:
                            print("\nPlease enter a numeric Company ID. ")
            else:
                print('\nNo Employee found')
                viewAllEmployees()

        except ValueError:
            print("\nPlease Enter a numeric Employees")


# Confirm Update Employee - USER is prompted with input information to confirm update
def confirmUpdateEmployee(employee):
    print(f"\n Employee Id: {employee.id}, Employee: {employee.first_name} {employee.last_name}, Employer ID: {employee.employer_id}")
    confirm_employee = input("\nConfirm new Employee? (y/n): ")

    if confirm_employee.lower() == 'y':
        query = "UPDATE employees SET first_name = %s, last_name = %s, employer_id = %s WHERE id = %s"
        try:
            cursor.execute(query, (employee.first_name, employee.last_name, employee.employer_id, employee.id))
            connection.commit() # commits the created entry
            print(f"\nEmployee {employee.first_name}, {employee.last_name} added successfully updated")
            mainMenu() # callbacks to the main menu after creation
        except psycopg2.IntegrityError as e:
                connection.rollback()  # roolbacks the transaction on an error
                print(f"\nDatabase error: {e}")
                mainMenu() #callback main menu if error occurs
        except psycopg2.Error as e: 
                print(f"\nUnexpected error: {e}")
                mainMenu() #callback main menu if error occurs

    elif confirm_employee.lower() =='n':
        print("\nCanceled action")
        add_employee_to_db() #callbacks the add employee function if canceled
    
    else:
        print("\nInvalid selection. Please enter 'y' or 'n'.")
        confirmAddEmployee(employee) #retrys confirmation



# <---------------------DELETE  ---------------------------------------------------->

# DELETE Employee function, enables user to delete employee, initial prompt when 'delete' is selected from 'main menu'
def delete_employee():

    cursor.execute("SELECT * FROM employees")
    employeeResults = cursor.fetchall()

    if employeeResults: 
        print("\nEmployee Results")
        for row in employeeResults:
            print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Employer ID: {row[3]}")
        
        while True:
            try:
            # capture user inputs
                employee_id = int(input("\nEnter a valid Employee ID Number to delete: "))

                #find seleceted employee
                selected_employee = next((row for row in employeeResults if row[0] == employee_id), None)
               
                if selected_employee:
                    #create an object
                    employee = Employee( selected_employee[0], selected_employee[1], selected_employee[2], selected_employee[3])
                    confirmDeleteEmployee(employee)
                    break # exits loop after deletion or cancelation
                                        
                else:
                    print('\nNo Employee found with entered Id, Try again.')
                    

            except ValueError:
                print("\nPlease Enter a numeric Employee Id")
    else:
         print("\nNo Employee found in database.")
         mainMenu() # redirect to main menu)


# Confirm employee deletion, enables user to confirm input prior to delete
def confirmDeleteEmployee(employee):
        print(f"\n Employee Id: {employee.id}, Employee: {employee.first_name} {employee.last_name}, Employer ID: {employee.employer_id}")
        confirm_employee = input("\nConfirm deletion of this employee? (y/n): ")

        if confirm_employee.lower() == 'y':
            query = "DELETE FROM employees WHERE id = %s"
            try:
                cursor.execute(query, (employee.id,))
                connection.commit() # commits the created entry
                print(f"\nEmployee successfully deleted")
                mainMenu() # callbacks to the main menu after creation
            except psycopg2.IntegrityError as e:
                    connection.rollback()  # roolbacks the transaction on an error
                    print(f"\nDatabase error: {e}")
                    mainMenu() #callback main menu if error occurs
            except psycopg2.Error as e: 
                    print(f"\nUnexpected error: {e}")
                    mainMenu() #callback main menu if error occurs

        elif confirm_employee.lower() =='n':
            print("\nAction cancelled.")
            viewAllEmployees() #callbacks to viewing all employees function if canceled
        
        else:
            print("\nInvalid selection. Please enter 'y' or 'n'.")
            confirmDeleteEmployee(employee) #retrys confirmation


# <-------------------------------------------------------- MAIN MENU VIEW ------------------------------------------------------------------------------------>
# Main Menu Function
def mainMenu():

    print('Welcome to CRM')

    print('\nWhat would you like to do, please choose one of the following: ')
    print('\n1. See Companies')
    print('2. See Employees')
    print('3. Quit')
    main_menu_prompt = input('\nEnter Choice: ')

    if main_menu_prompt == '1':
        cursor.execute('SELECT * FROM companies')
        results = cursor.fetchall()
        if results:
            print("\nCompany Results")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Company ID: {row[2]}")
                mainMenu()
    elif main_menu_prompt == '2':
        # put this in a function
       viewAllEmployees()

    elif main_menu_prompt == '3':
        quit()

# <-------------------------------------------------------- SECONDARY MENU once user has clicked '2. See Employees' ------------------------------------------->

# view employees - INITIAL VIEW
def viewAllEmployees():
        cursor.execute('SELECT * FROM employees')
        results = cursor.fetchall()
        if results:
            print("\nEmployee Results")
            for row in results:
                print(f"ID: {row[0]} | First Name: {row[1]} | Last Name: {row[2]} | Employer ID: {row[3]}")
            
            print("\nWhat would you like to do? ")
            print("\n1. Add an Employee")
            print("2. Update an Employee")
            print("3. Delete an Employee")
            print("4. Go back to Main Menu")
            print("5. Quit")

            employeeViewPrompt()

        else: 
            print("\nNo Employee results found. ")
            print("\nWhat would you like to do? ")
            print("\n1. Add an Employee")
            print("2. Go back to Main Menu")
            print("3. Quit")

            noEmployeePrompt()


# employee prompt - FUNCTIONALITY FOR INITIAL VIEW ABOVE (IF EMPLOYEES EXIST IN THE DATABASE)
def employeeViewPrompt():
      
    employee_prompt = input('\nEnter Choice: ')
        
    if employee_prompt == '1':
        add_employee_to_db()
    elif employee_prompt =='2':
        update_employee()
    elif employee_prompt == '3':
        delete_employee()
    elif employee_prompt == '4':
        mainMenu()
    elif employee_prompt == '5':
        quit()
    else:
        print("\nInvalid selection. Please try again")
        employeeViewPrompt()


#noEmployeePrompt - FUNCTIONALITY FOR INITIAL VIEW (IF EMPLOYEES DO NOT EXIST IN THE DATABASE)
def noEmployeePrompt():

    no_employee_prompt = input('\nEnter Choice: ')

    if no_employee_prompt == '1':
            add_employee_to_db()
    elif no_employee_prompt == '2':
            mainMenu()
    elif no_employee_prompt == '3':
        quit()
    else:
        print("\nInvalid selection. Please try again")
        noEmployeePrompt()



# Main Menu Callback to initialize CRM
mainMenu()

    



# ============= GRAVEYARD ==============

# cursor = connection.cursor()
# cursor.execute('SELECT * FROM employees')
# results = cursor.fetchall();

# print(results)