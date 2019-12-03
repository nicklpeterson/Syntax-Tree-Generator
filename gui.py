import tkinter as tk
import calculator as calc

class Main:
    def __init__(self):
        window = tk.Tk() # Create a window
        window.title("Recursive Tree") # Set a title

        self.width = 200
        self.height = 200
        self.canvas = tk.Canvas(window, width = self.width, height = self.height,bg="white")
        self.canvas.pack()

        res = tk.Label(window)
        res.pack()

        # Add a label, an entry, and a button to frame1
        frame1 = tk.Frame(window) # Create and add a frame to window
        frame1.pack()

        tk.Label(frame1, text = "Expression: ").pack(side = tk.LEFT)
        self.exp = tk.StringVar()
        entry = tk.Entry(frame1, textvariable = self.exp, justify = tk.LEFT)
        entry.pack(side = tk.LEFT)

        b1 = tk.Button(frame1, text = "Display Syntax Tree")
        b1.bind("<ButtonPress-1>", lambda event, arg=entry, res=res: self.evaluate(event, arg, res))
        b1.pack(side = tk.LEFT)

        window.bind('<Return>', lambda event, arg=entry, res=res: self.evaluate(event, arg, res))
        window.mainloop()

    def evaluate(self, event, entry, res):
        """
        Evaluate the expression
        """
        parser = calc.InputParser()
        tree = parser.parse_input(entry.get())
        res.configure(text = "Result: " + str(parser.evaluate(tree)))   


def print_tree(event, entry):
    """
    Print a sytax tree in the gui window
    """
    pass

if __name__ == "__main__":
    Main()