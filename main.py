# Importing tkinter for graphic user interface
from tkinter import *

equation = ''


def calculate():
    try:

        global equation

        temp = equation
        equation = str(eval(equation))
        show_equation.set(equation)
        temp += '=' + equation + '\n'
        with open('calculations.txt', 'a') as f:
            f.write(temp)
        f.close()

    except FileExistsError:
        print("File Exists")


# Clearing whole equation
def clear_all():
    global equation
    equation = ''
    show_equation.set(equation)


# Deleting last used button
# If the show_equation string is empty the button tries to show previous completed calculation
def clear():
    global equation
    if len(equation) > 0:
        equation = equation[0:len(equation) - 1]
        show_equation.set(equation)
    else:
        try:
            with open("calculations.txt", "r") as file:
                last_line = file.readlines()[-1]
            file.close()
            if len(last_line) > 0:
                pos = last_line.rfind('=')
                equation = last_line[0:pos]
                show_equation.set(equation)
        except FileNotFoundError:
            print("Calculation File Does not Exist")


# after pressing a button writes a adds a corresponding symbol to the string
def press(button):
    global equation
    equation += button
    show_equation.set(equation)


if __name__ == "__main__":
    # window initialization
    gui = Tk()
    gui.configure(background="gray")
    gui.title("Calculator")
    gui.geometry("322x148")
    # string that represent equation in the window
    show_equation = StringVar()
    expression_field = Entry(gui, textvariable=show_equation)
    expression_field.grid(columnspan=4, ipadx=100)

    # Buttons that enable the usage of calculator and general lookout of the gui
    button1 = Button(gui, text=' 1 ', fg='white', bg='black', height=1, width=10, command=lambda: press('1'))
    button1.grid(row=2, column=0)
    button2 = Button(gui, text=' 2 ', fg='white', bg='black', height=1, width=10, command=lambda: press('2'))
    button2.grid(row=2, column=1)
    button3 = Button(gui, text=' 3 ', fg='white', bg='black', height=1, width=10, command=lambda: press('3'))
    button3.grid(row=2, column=2)
    button4 = Button(gui, text=' 4 ', fg='white', bg='black', height=1, width=10, command=lambda: press('4'))
    button4.grid(row=3, column=0)
    button5 = Button(gui, text=' 5 ', fg='white', bg='black', height=1, width=10, command=lambda: press('5'))
    button5.grid(row=3, column=1)
    button6 = Button(gui, text=' 6 ', fg='white', bg='black', height=1, width=10, command=lambda: press('6'))
    button6.grid(row=3, column=2)
    button7 = Button(gui, text=' 7 ', fg='white', bg='black', height=1, width=10, command=lambda: press('7'))
    button7.grid(row=4, column=0)
    button8 = Button(gui, text=' 8 ', fg='white', bg='black', height=1, width=10, command=lambda: press('8'))
    button8.grid(row=4, column=1)
    button9 = Button(gui, text=' 9 ', fg='white', bg='black', height=1, width=10, command=lambda: press('9'))
    button9.grid(row=4, column=2)
    button0 = Button(gui, text=' 0 ', fg='white', bg='black', height=1, width=10, command=lambda: press('0'))
    button0.grid(row=5, column=0)
    button_plus = Button(gui, text=' + ', fg='white', bg='black', height=1, width=10, command=lambda: press('+'))
    button_plus.grid(row=2, column=3)
    button_minus = Button(gui, text=' - ', fg='white', bg='black', height=1, width=10, command=lambda: press('-'))
    button_minus.grid(row=3, column=3)
    button_multiply = Button(gui, text=' * ', fg='white', bg='black', height=1, width=10, command=lambda: press('*'))
    button_multiply.grid(row=4, column=3)
    button_divide = Button(gui, text=' / ', fg='white', bg='black', height=1, width=10, command=lambda: press('/'))
    button_divide.grid(row=5, column=3)
    button_clear_all = Button(gui, text=' Clear All ', fg='white', bg='black', height=1, width=10,
                              command=lambda: clear_all())
    button_clear_all.grid(row=5, column=1)
    button_equal = Button(gui, text=' = ', fg='white', bg='black', height=1, width=10, command=lambda: calculate())
    button_equal.grid(row=5, column=2)
    button_dot = Button(gui, text=' . ', fg='white', bg='black', height=1, width=10, command=lambda: press('.'))
    button_dot.grid(row=6, column=0)
    button_clear = Button(gui, text=' Clear ', fg='white', bg='black', height=1, width=10, command=lambda: clear())
    button_clear.grid(row=6, column=1)
    button_left_bracket = Button(gui, text=' ( ', fg='white', bg='black', height=1, width=10, command=lambda: \
        press('('))
    button_left_bracket.grid(row=6, column=2)
    button_right_bracket = Button(gui, text=' ) ', fg='white', bg='black', height=1, width=10, command=lambda: \
        press(')'))
    button_right_bracket.grid(row=6, column=3)

    gui.mainloop()
