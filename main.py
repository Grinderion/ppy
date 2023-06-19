# Importing tkinter for graphic user interface and maths for math functions
from tkinter import *
from tkinter import ttk
from math import *

# Global variable used to save the current status of a string
# that shows the equation users builds by pressing buttons
equation = ''
all_signs = ['.', '+', '-', '*', '/', '^', '%']


# window popup for errors and information
def popup(string):
    win = Toplevel()
    win.wm_title("Window")

    label = Label(win, text=string)
    label.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)


def evaluate(string):
    bracket_stack = []
    signs = ['+', '-', '*', '/']
    calc_list = []
    sign = ""
    sign_pos = -1
    min1 = -1
    min2 = -1
    answer = string
    for pos in range(len(string)):
        if string[pos] == "(":
            bracket_stack.append(pos)
        elif string[pos] == ")":
            if len(bracket_stack) > 0:
                pos1 = bracket_stack.pop()
                temp = string[pos1:pos + 1]
                temp = evaluate(temp)
                answer = string[:pos1] + temp + string[pos + 1:]
            else:
                popup("Bracket closed before it was opened")
                return string
        elif string[pos] == '.':
            if string[pos] in calc_list:
                popup("Dot present two times in a single number")
                return string
            else:
                continue
        elif string[pos].isnumeric():
            calc_list.append(string[pos])
        elif string[pos] in signs:
            if string[pos] == '-':
                if len(calc_list) == 0 and min1 == -1:
                    min1 = 0
                elif string[pos - 1] in signs:
                    if string[pos - 2] in signs:
                        popup("Too many signs in a row")
                        return string

    if len(bracket_stack) != 0:
        popup("Some brackets were not closed after opening them")
        return string

    return answer


def bracket_number(string):
    """
    This function is just for eliminating brackets when we now that there is only a number inside
    Function throws exception if there is a sign other than dot after removing brackets
    :param string:
    :return: temp
    """
    temp = string[1:-1]
    for char in temp:
        if char in all_signs[1:]:
            raise Exception("There is still a sign other than dot inside string")
    return temp


def power(string):
    """
    Function that takes a string with '^' symbol and returns the result of number before the function taken to the power
    of the number after the function
    :param string:
    :return: temp1
    """
    temp1 = string
    for pos in range(len(temp1)):
        if temp1[pos] == '^':
            beginning = -1
            end = -1
            # Existence of brackets before and after power sign
            first_bracket = False
            second_bracket = False
            # Confirming or denying existence of before mentioned brackets
            if temp1[pos - 1] == ')':
                first_bracket = True
            if temp1[pos + 1] == '(':
                second_bracket = True
            # tracking the position of the first character representing the first number
            for pos1 in range(pos - 1, -1, -1):
                if not first_bracket and temp1[pos1] in all_signs[1:]:
                    beginning = pos1
                    break
                elif first_bracket:
                    for pos3 in range(pos - 1, -1, -1):
                        if temp1[pos3] == '(':
                            beginning = pos3
                            break
            # tracking the position of the last character representing the second number
            for pos2 in range(pos + 1, len(temp1)):
                if not second_bracket and temp1[pos2] in all_signs[1:]:
                    end = pos2
                    break
                elif second_bracket:
                    for pos3 in range(pos + 1, len(temp1)):
                        if temp1[pos3] == ')':
                            end = pos3
                            break
            # should the last character representing the second number not be found we assign the last character
            # of the string to it
            if end == -1:
                end = len(temp1)
            # case with both numbers being in brackets
            if first_bracket and second_bracket:
                first = eval(temp1[beginning + 1:pos - 1])
                second = eval(temp1[pos + 1:end + 1])
                temp1 = temp1[:beginning + 1] + str(pow(float(first), float(second))) + temp1[end:]
                return temp1
            # case with only first number being in brackets
            if first_bracket and not second_bracket:
                first = eval(temp1[beginning + 1:pos - 1])
                temp1 = temp1[:beginning] + str(
                    pow(float(first), float(temp1[pos + 1:end + 1]))) + temp1[end:]
                return temp1
            # should the first character representing the first number not be found we assign the first character
            # of the string to it
            if beginning == -1:
                # case of none of the numbers being in brackets and the power function being the first calculation
                if not second_bracket:
                    beginning = 0
                    temp1 = temp1[:beginning] + str(
                        pow(float(temp1[beginning:pos]), float(temp1[pos + 1:end + 1]))) + temp1[end:]
                    return temp1
                # case of only the second number being in brackets and the power function being the first calculation
                else:
                    second = eval(temp1[pos + 1:end + 1])
                    beginning = 0
                    temp1 = temp1[:beginning] + str(
                        pow(float(temp1[beginning:pos]), float(second))) + temp1[end + 1:]
                    return temp1
            # case of only the second number being in brackets
            if second_bracket:
                second = eval(temp1[pos + 1:end + 1])
                temp1 = temp1[:beginning + 1] + str(
                    pow(float(temp1[beginning:pos]), float(second))) + temp1[end + 1:]
                return temp1
            # other cases
            else:
                temp1 = temp1[:beginning + 1] + str(
                    pow(float(temp1[beginning:pos]), float(temp1[pos + 1:end + 1]))) + temp1[end:]
            break
    return temp1


def squared(string):
    """
    Function that takes a string with 'sqr' symbol and returns the result of squared number inside the brackets
    :param string:
    :return: temp2
    """
    temp2 = string
    beginning = 0
    end = 0
    for pos in range(len(temp2)):
        if temp2[pos] == 's':
            if temp2[pos + 3] == '(':
                beginning = pos + 4
                for pos3 in range(pos + 3, len(temp2), 1):
                    if temp2[pos3] == ')':
                        end = pos3
                        break
                break
    if end != 0:
        temp2 = temp2[:pos] + str(sqrt(float(temp2[beginning:end]))) + temp2[end + 1:]
    return temp2


def calculate():
    """
    Evaluating the equation string when equals(=) button is pressed
    :return:
        None
    """
    try:
        global equation
        temp = equation
        temp1 = equation
        while "^" in temp1:
            temp1 = power(temp1)
        while 'sqr' in temp1:
            temp1 = squared(temp1)
        temp1 = temp1.replace('%', '/100')
        temp1 = temp1.replace('‰', '/1000')
        equation = str(eval(temp1))
        show_equation.set(temp1)
        temp += '=' + temp1 + '\n'
        with open('calculations.txt', 'a') as f:
            f.write(temp)
        f.close()

    except FileExistsError:
        print("File Exists")


def clear_all():
    """
    Clearing equation string of all characters
    :return:
        None
    """
    global equation
    equation = ''
    show_equation.set(equation)


def clear():
    """
    Deleting last character on the equation string when 'clear' button is pushed
    If the show_equation string is empty the button tries to show previous completed equation
    from calculation.txt text file and assigns it to equation string
    :returns:
        None
    """
    global equation
    if len(equation) > 0:
        equation = equation[0:len(equation) - 1]
        show_equation.set(equation)
    else:
        try:
            temp1 = ""
            with open("calculations.txt", "r") as file:
                temp = file.readlines()
                last_line = temp[-1]
                temp1 = temp[0:-1]
                print(last_line)
                print(temp1)
            file.close()
            if len(last_line) > 0:
                pos = last_line.rfind('=')
                equation = last_line[0:pos]
                show_equation.set(equation)
                file = open('calculations.txt', "r+")
                file.truncate(0)
                for line in temp1:
                    file.write(line)
                file.close()

        except FileNotFoundError:
            print("Calculation File Does not Exist")
        except IndexError:
            # if the code is changed might need to change print to better represent errors
            print("File is empty")


def press(button):
    """
    This function is used for all buttons that don't have specific function assigned to them
    after registering pressing of a button adds a corresponding symbol to the equation string
    params:
        button: string that needs to be assigned when calling the function and represents what button was pushed
    returns:
        None
    """
    global equation
    signs = ['.', '+', '-', '*', '/', '^']
    signs1 = ['.', '+', '*', '/', '^', '%']
    if button in signs1 and not equation:
        popup("Cant start with this sign")
    elif equation and button in signs and equation[-1] in signs:
        popup('Wrong Character')
    elif button not in signs and len(equation) > 0 and equation[-1] == '%':
        popup("Can't have numeric after '%' sign")
    elif button == '.' and equation[-1] == '%':
        popup("Can't have dot after '%' sign")
    else:
        equation += button
        show_equation.set(equation)


# This part of the code contains gui
if __name__ == "__main__":
    # window initialization
    gui = Tk()
    gui.configure(background="gray")
    gui.title("Calculator")
    gui.geometry("880x356")
    gui.resizable(False, False)
    # string that represent equation in the window
    show_equation = StringVar()
    expression_field = Entry(gui, textvariable=show_equation)
    expression_field.grid(columnspan=4, ipadx=378, )

    # Buttons that enable the usage of calculator and general lookout of the gui
    button1 = Button(gui, text=' 1 ', fg='white', bg='black', height=3, width=30, command=lambda: press('1'))
    button1.grid(row=2, column=0)
    button2 = Button(gui, text=' 2 ', fg='white', bg='black', height=3, width=30, command=lambda: press('2'))
    button2.grid(row=2, column=1)
    button3 = Button(gui, text=' 3 ', fg='white', bg='black', height=3, width=30, command=lambda: press('3'))
    button3.grid(row=2, column=2)
    button4 = Button(gui, text=' 4 ', fg='white', bg='black', height=3, width=30, command=lambda: press('4'))
    button4.grid(row=3, column=0)
    button5 = Button(gui, text=' 5 ', fg='white', bg='black', height=3, width=30, command=lambda: press('5'))
    button5.grid(row=3, column=1)
    button6 = Button(gui, text=' 6 ', fg='white', bg='black', height=3, width=30, command=lambda: press('6'))
    button6.grid(row=3, column=2)
    button7 = Button(gui, text=' 7 ', fg='white', bg='black', height=3, width=30, command=lambda: press('7'))
    button7.grid(row=4, column=0)
    button8 = Button(gui, text=' 8 ', fg='white', bg='black', height=3, width=30, command=lambda: press('8'))
    button8.grid(row=4, column=1)
    button9 = Button(gui, text=' 9 ', fg='white', bg='black', height=3, width=30, command=lambda: press('9'))
    button9.grid(row=4, column=2)
    button0 = Button(gui, text=' 0 ', fg='white', bg='black', height=3, width=30, command=lambda: press('0'))
    button0.grid(row=5, column=0)
    button_plus = Button(gui, text=' + ', fg='white', bg='black', height=3, width=30, command=lambda: press('+'))
    button_plus.grid(row=2, column=3)
    button_minus = Button(gui, text=' - ', fg='white', bg='black', height=3, width=30, command=lambda: press('-'))
    button_minus.grid(row=3, column=3)
    button_multiply = Button(gui, text=' * ', fg='white', bg='black', height=3, width=30, command=lambda: press('*'))
    button_multiply.grid(row=4, column=3)
    button_divide = Button(gui, text=' / ', fg='white', bg='black', height=3, width=30, command=lambda: press('/'))
    button_divide.grid(row=5, column=3)
    button_clear_all = Button(gui, text=' Clear All ', fg='white', bg='black', height=3, width=30,
                              command=lambda: clear_all())
    button_clear_all.grid(row=5, column=1)
    button_equal = Button(gui, text=' = ', fg='white', bg='black', height=3, width=30, command=lambda: calculate())
    button_equal.grid(row=5, column=2)
    button_dot = Button(gui, text=' . ', fg='white', bg='black', height=3, width=30, command=lambda: press('.'))
    button_dot.grid(row=6, column=0)
    button_clear = Button(gui, text=' Clear ', fg='white', bg='black', height=3, width=30, command=lambda: clear())
    button_clear.grid(row=6, column=1)
    button_left_bracket = Button(gui, text=' ( ', fg='white', bg='black', height=3, width=30, command=lambda: \
        press('('))
    button_left_bracket.grid(row=6, column=2)
    button_right_bracket = Button(gui, text=' ) ', fg='white', bg='black', height=3, width=30, command=lambda: \
        press(')'))
    button_right_bracket.grid(row=6, column=3)
    button_power = Button(gui, text=' ^ ', fg='white', bg='black', height=3, width=30, command=lambda: press('^'))
    button_power.grid(row=7, column=0)
    button_percent = Button(gui, text=' % ', fg='white', bg='black', height=3, width=30, command=lambda: press('%'))
    button_percent.grid(row=7, column=2)
    button_squared = Button(gui, text=' sqr ', fg='white', bg='black', height=3, width=30, command=lambda: press('sqr'))
    button_squared.grid(row=7, column=1)
    button_per_mile = Button(gui, text=' ‰ ', fg='white', bg='black', height=3, width=30, command=lambda: press('‰'))
    button_per_mile.grid(row=7, column=3)
    gui.mainloop()
