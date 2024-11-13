from datetime import datetime
import pandas as pd
import csv
import os



#Function to add expense
def add_expense(input_list):
    try:
        '''
        Get the input from user repeatedly untill user doesnot want to proceed ahead
        return list of dictionary having Date, Category, Amount & Desc as key
        '''

        # input_list = [{'date': '2024-05-05', 'category': 'food', 'amount': '1000', 'desc': 'food'}, 
        #                {'date': '2024-06-06', 'category': 'travel', 'amount': '500', 'desc': 'travel'}]

        
        # proceed = 'y'
        

        # while proceed == 'y' or proceed == 'Y':

        # input_dic = {"date":"","category":"","amount":"","desc":""}
        input_dic = {}

        while(True):
            expense_date = ""
            expense_date = input("Enter date of expense (YYYY-MM-DD) : ")
            if not get_validation_result(expense_date,"date"):
                print("Invalid Expense Record! ")
                continue
            input_dic["date"] = expense_date
            break
        
        while(True):
            expense_category = ""
            expense_category = input("Enter category of expense : ")
            if not get_validation_result(expense_category,"category"):
                print("Invalid Expense Record! ")
                continue
            input_dic["category"] = expense_category
            break
        
        while(True):
            expense_amount = 0
            expense_amount = input("Enter amount spend on expense : ")
            if not get_validation_result(expense_amount,"amount"):
                print("Invalid Expense Record! ")
                continue
            input_dic["amount"] = expense_amount
            break
        
        while(True):
            expense_desc = ""
            expense_desc = input("Enter a brief description of the expense : ")
            if not get_validation_result(expense_desc,"desc"):
                print("Invalid Expense Record! ")
                continue
            input_dic["desc"] = expense_desc
            break

        
        input_list.append(input_dic)

            # proceed = input("Do you want to add more expense Y/N : ")

        return input_list
    except Exception as e:
        print("Error occured in add_expense flow : ",e)



#Function to validate if user entered correct details
def get_validation_result(expense_value,key_name):
    try:
        '''
        Input: 
        expense_value - value entered by user
        key_name - what type of expense detail Date/Category/Amount/Desc
        Output:
        boolean: validation pass or fail
        Steps:
        General step - Function validate if value is empty or not
        for date- if date is in correct format
        for amount- if amount is in acceptable numeric type
        '''
        
        if expense_value == "":
            return False
        if key_name == "date":
            try:
                temp_val = datetime.fromisoformat(expense_value)
                
            except Exception as e:
                return False
        if key_name == "amount":
            try:
                temp_val = float(expense_value)
            except Exception as e:
                return False
        
        return True
    except Exception as e:
        print("Error occured in get_validation_result: ",e)


# Function to view all expenses
def view_expense(input_list):
    try:
        '''
        Input:
        input_list -  Stored expenses in list
        Step:
        Display all stored expenses in table format
        '''
        expense_df = pd.DataFrame(input_list)
        print("Please refer the below summary of expenses")
        print(expense_df)

    except Exception as e:
        print("Error occured in view_expense flow : ",e)

# Function to set and track a monthly budget
def set_budget():
    try:
        '''
        Output: Budget
        Steps:
        Take a input from the user what is the amount to set for monthly budget
        store as a float variable.
        '''

        budget_amt = 0
        while(True):
                budget_amt = input("Enter the Budget for the month\n")
                if not get_validation_result(budget_amt,"amount"):
                    print("Invalid Budget! ")
                    continue
                break
        
        return budget_amt
    except Exception as e:
        print("Error occured in set_budget flow : ",e)


# Function to track expenses by category and check against the budget
def track_budget(input_list, budget):
    try:
        '''
        Input:
        input_list : Expense entered by user
        budget: budget set by the user
        Steps:
        Loop through your expenses list and fetch amount field
        Keep summing up amount field and store the final summed value to a variable - total_expenses
        Compare above total_expenses against budget variable
        if total_expenses > budget raise an alarm to the user - "Warning: You have exceeded your budget!"
        Else - You are within your budget, You have {budget - total_expenses} remaining."
        '''

        total_expense = 0
        total_budget = float(budget)
        for item in input_list:        
                total_expense += float(item["amount"])

        
        if total_budget < total_expense:
            print("You have exceeded your budget!")
        else:
            print(f" You have {total_expense - total_budget} left for the month")
    except Exception as e:
        print("Error occured in set_budget flow : ",e)

    
# Function to save expenses to a file
def save_expenses(expenses = [], filename='expense_tracker.csv'):
    try: 
        '''
        Use Open function to open the file in write mode
        use hint:  writer = csv.writer(file) to write any content to file, writer.writerow(['a','b','c','d'])
        Ideally CSV needs a header file, hence first row add header info such as - [date, category, amount, description]
        Once header is written loop through you expenses list and fetch corresponding fields to store into the file
        '''
        headers = list(expenses[0].keys())
        row_count = 0
        if os.path.exists(filename):
            #Get count of rows
            with open(filename,'r') as csvfile:
                
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    row_count += 1
        

            csvfile.close

        #Append the expenses 
        with open(filename,'a') as csvfile:
            
            csvwriter = csv.DictWriter(csvfile,headers)
            if row_count == 0:
                csvwriter.writeheader()
            
            csvwriter.writerows(expenses)
        
        csvfile.close

        print("Expense is saved in ",filename)
    
    except Exception as e:
        print("Error occured in save_expenses flow : ",e)


        

# Function to load expenses from a file
def load_expenses(filename='expense_tracker.csv'):
    try:
        '''
        Loop through the reader object and fetch one row at a time, check if each row's filds contains all the keys, 
        if not display a print message invalid key entry and do not store them.
        Append each row in expenses list, keep building thsis list
        file not found display a message - "No existing expenses found. Starting fresh."
        '''
    
        expenses = []
        #Get count of rows
        with open(filename,'r') as csvfile:
            
            csvreader = csv.DictReader(csvfile)
            
            for row in csvreader:
                if "date" in row.keys() and "category" in row.keys() and "desc" in row.keys() and "amount" in row.keys():
                    expenses.append(row)
                else:
                    print("Invalid key entry! ")

        csvfile.close

        return expenses
    except FileNotFoundError:
        print("No existing expenses found. Starting fresh.")
        return expenses
    except Exception as e:
        print("Error occured in load_expenses flow : ",e)


# Main interactive menu
def main():
    try:
        '''
            The interactive menu allows users to navigate through the options of adding an expense, viewing expenses, 
            tracking their budget, saving expenses, or exiting the program. When exiting, 
            it ensures that any newly added expenses are saved to the file.
        '''
        input_option = 5
        expense_list = []

        expense_list = load_expenses()
        budget = set_budget()

        while True:
        
            print("Menu List")
            print("1. Add Expense")
            print("2. View Expense")
            print("3. Track Budget")
            print("4. Save Expense")
            print("5. Exit")

            input_option = input("Hey there!! Please pick one of options to proceed : ")
            if input_option == "1" or input_option == "2" or input_option == "3" or input_option == "4" or input_option == "5" :
                if input_option == "1":
                    expense_list = add_expense(expense_list)
                elif input_option == "2":
                    view_expense(expense_list)
                elif input_option == "3":
                    track_budget(expense_list,budget)
                elif input_option == "4":
                    save_expenses(expense_list)
                elif input_option == "5":
                    break
            else:
                break

        return input_option
    except Exception as e:
        print("Error occured in main flow : ",e)
    

    



if __name__ == "__main__":
  main()






    
    


