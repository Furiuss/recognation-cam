def introduction():
    print("Comparing Numbers and Their Average Program")
    print("This program calculates the average of three integer values and compares each value to the average.")
    print("You will need to enter each number one at a time withou commas.")
    print("To continue the program after one result, enter 'calculator' as the password.")
    print("The set of data will end if password 'funcalculator' is entered by the user.")
    print("My name is Meina Huang.")
    print()

def pegarDadosUsuario():
    while True:
            password = input('Please enter the password to continue: ')

            # check if the password is "calculator"
            if password.lower() == 'funcalculator':
                print("Program has stopped.")
                break

            # ask the user to enter 3 integer values
            int1 = int(input('Please enter the first integer: '))
            int2 = int(input('Please enter the second integer: '))
            int3 = int(input('Please enter the third integer: '))
            lista_dahora = [int1, int2, int3]
            break

    return lista_dahora

def fazerCalculoDeMedia(int1, int2, int3):
    return (int1 + int2 + int3) / 3

def mostrarMedia():
    print()
    int1, int2, int3 = pegarDadosUsuario()
    # printing the integers
    print(f'The numbers entered are {int1}, {int2}, {int3}')

    # calculating the average of the three integers
    avg = fazerCalculoDeMedia(int1, int2, int3)

    print(f'The average of the three numbers is: {avg:.2f}')

    lista_dahora = [int1, int2, int3]

    for inteiro in lista_dahora:
        if inteiro > avg:
            print(f'{inteiro} is greater than the average.')
        elif inteiro < avg:
            print(f'{inteiro} is less than the average.')
        else:
            print(f'{inteiro} is equal to the average.')

    print("Done! To continue and add new numbers, please enter the password again.")


introduction()
mostrarMedia()