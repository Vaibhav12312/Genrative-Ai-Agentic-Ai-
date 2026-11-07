
# EPFOSathi - Day 01 Introduction

# 1. Project information using variables
product = "EPFOSathi"
target_user = "Employees and EPF account holders"

problem = "Employees often find EPF rules, UAN, contributions and withdrawal procedures confusing."

data_source = "Official EPFO Website and EPFO Member Portal"

# 2. Display project card using f-strings
print("\n===================================")
print(f"       {product} PROJECT CARD")
print("===================================")

print(f"Product: {product}")
print(f"Target Users: {target_user}")
print(f"Problem: {problem}")
print(f"Data Source: {data_source}")

print("===================================")

# 3. Ask user information
user_name = input("\nEnter your name: ")

user_question = input("What is your EPF-related question? ")

# 4. Display personalized response
print("\n---------- USER DETAILS ----------")

print(f"Welcome, {user_name}!")

print(f"Your question: {user_question}")

print("Thank you for using EPFOSathi.")
print("----------------------------------")
