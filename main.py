Xf = 16 #Ширина леса в деревьях
Yf = 16 #Высота леса в деревьях

from tkinter import *
from forest_class import *

class main():
    def __init__(self, N=9, M=9):
        self.root = Tk()
        self.root.title("Кладмен, ну ты и мудак!!1")
        self.mapFrame = Frame(self.root, width = N, height = M, bg = 'gray')
        self.mapFrame.pack_propagate(0)
        self.mapFrame.grid(row=0, column=0, columnspan=N)
        self.forest = forest_abstract( master=self.mapFrame, N=N, M=M)
        self.root.mainloop()

# print('Field height = ')
# Xf = input()
# print('Field width = ')
# Yf = input()

MainWin = main(N = int(Xf), M = int(Yf))