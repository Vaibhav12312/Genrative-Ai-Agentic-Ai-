
# EPFOSathi - Day 01 Interactive Menu

while True:

    print("\n================================")
    print("       WELCOME TO EPFOSATHI")
    print("================================")

    print("1. About EPFOSathi")
    print("2. Sample EPF Questions")
    print("3. EPF Rule Check")
    print("0. Exit")

    print("================================")

    choice = input("Enter your choice: ")

    # Option 1: About the project
    if choice == "1":

        print("\nAbout EPFOSathi")
        print("EPFOSathi provides simple EPF information")
        print("and guidance for employees.")

    # Option 2: Sample questions
    elif choice == "2":

        print("\nSample EPF Questions")

        print("1. What is UAN?")
        print("2. How can I check my PF balance?")
        print("3. What is an EPF withdrawal?")
        print("4. How can I check my PF claim status?")

    # Option 3: One EPF rule check
    elif choice == "3":

        print("\nEPF Membership Rule Check")

        salary = float(input("Enter your monthly basic salary + DA: "))

        if salary <= 0:
            print("Please enter a valid salary greater than zero.")
        elif salary <= 15000:
            print("You meet the basic wage threshold, subject to applicable EPF rules.")

    # Option 0: Exit
    elif choice == "0":

        print("\nThank you for using EPFOSathi!")
        print("Exiting the program...")
        break

    # Invalid option
    else:

        print("\nInvalid choice!")
        print("Please select a valid menu option.")
