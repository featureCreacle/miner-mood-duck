Xf = 9 #Ширина леса в деревьях
Yf = 9 #Высота леса в деревьях

from tkinter import *
from forest_class import *

class main():
    def __init__(self, N=9, M=9):
        self.root = Tk()
        self.root.title("Miner mood duck")
        self.mapFrame = Frame(self.root, width = N, height = M, bg = 'gray')
        self.mapFrame.pack_propagate(0)
        self.mapFrame.grid(row=0, column=0, columnspan=M)
        self.forest = forest_abstract( master=self.mapFrame, N=N, M=M)
        self.bottomFrame = Frame(self.root, bg='gray')
        self.bottomFrame.grid(row=1, column=0, columnspan=M)
        self.labelCopsNum = Label(master=self.bottomFrame, textvariable=self.forest.varCopsNum,
                                  width=2, fg='red')
        self.labelCopsNum.grid(row=1, column=2)
        self.hintBut = Button(master=self.bottomFrame, text='Hint', command=self.forest.hint)
        self.hintBut.grid(row=1, column=1)
        self.AIBut = Button(master=self.bottomFrame, text='Go baka AI', command=self.goBakaGo)
        self.AIBut.grid(row=1, column=3)
        self.AITest = Button(master=self.bottomFrame, text='Test baka AI', command=self.testBakaAI)
        self.AITest.grid(row=1, column=4)
        self.root.mainloop()

    def new_forest(self):
        master = self.mapFrame
        N = Xf
        M = Yf
        self.forest.set_defaults(master=master, N = N, M = M)
        self.forest.restore_all_icons()


    def goBakaGo(self):
        steps = 1
        while self.forest.doStep() and not self.forest.gameIsOver:
            steps += 1
        if not self.forest.gameIsOver:
            messagebox.showinfo("Halp!!1", "Halp me! Im so confused")
        else:
            print('Steps ' + str(steps) + ' Res ' + str(self.forest.Result))
            self.forest.showFinalMessage()
            self.new_forest()

    def testBakaAI(self, numberOfGame = 100):
        testResult = [0,  # loses
                      0,  # confused
                      0]  # wins
        stepsList = []
        print(asctime())
        for gn in range(numberOfGame):
            steps = 0
            while self.forest.doStep() and not self.forest.gameIsOver:
                steps += 1
            stepsList.append(str(steps) + ' R:' + str(self.forest.Result))
            testResult[self.forest.Result] += 1
            self.new_forest()

        print(asctime())
        str1 = 'games: ' + str(numberOfGame) + '\n wins: ' + str(testResult[gameResultEmum['win']]) + \
               ' confused: ' + str(testResult[gameResultEmum['confused']]) + ' loses: ' + \
               str(testResult[gameResultEmum['lose']])
        print(stepsList)
        print(['L', 'C', 'W'])
        print(testResult)
        messagebox.showinfo("Test result", str1)


# print('Field height = ')
# Xf = input()
# print('Field width = ')
# Yf = input()

MainWin = main(N = int(Xf), M = int(Yf))