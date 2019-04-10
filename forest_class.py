from tkinter import *
from tkinter import messagebox
from functools import partial
from random import random, randrange
from tool_tip import CreateToolTip

treeStatusEnum = { 'none' : 0, 'sweet': 1, 'cop': 2 }
iconEnum = { 'sweet'   : 0,
             'one'     : 1,
             'two'     : 2,
             'three'   : 3,
             'four'    : 4,
             'five'    : 5,
             'six'     : 6,
             'seven'   : 7,
             'eight'   : 8,
             'alert'   : 9,
             'question': 10,
             'tree'    : 11,
             'blank'   : 12,
             'cop'     : 13,
             'sptdCop' : 14,
             'snkyCop' : 15,
             'wrgGuess': 16,
             'badGuess': 17,
             'ok'      : 18,
             'no'      : 19 }

class TreeInForest(Button):
    """Button widget."""
    def __init__(self, master=None, cnf={}, **kw):
        """Construct a button widget with the parent MASTER.

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

            command, compound, default, height,
            overrelief, state, width
        """
        #treeStatus = treeStatusEnum['sweet']
        #treeCord = (0,0)
        super().__init__(master, cnf, **kw)

class forest_abstract():
    def __init__(self, master=None, N=16, M=16, sizeOfTree=16, copsRate = 0.16 ):
        self.master = master
        self.feildSize = (N,M)
        self.StepCounter = 0
        self.copsRate = copsRate
        self.copsSpoted = 0
        self.copsInBush = 0
        self.isNewGame = True
        self.icons = []
        self.icons.append(PhotoImage(file='res/sweet.gif'))        # 0
        self.icons.append(PhotoImage(file='res/numbers/one.gif'))  # 1
        self.icons.append(PhotoImage(file='res/numbers/two.gif'))  # 2
        self.icons.append(PhotoImage(file='res/numbers/three.gif'))# 3
        self.icons.append(PhotoImage(file='res/numbers/four.gif')) # 4
        self.icons.append(PhotoImage(file='res/numbers/five.gif')) # 5
        self.icons.append(PhotoImage(file='res/numbers/six.gif'))  # 6
        self.icons.append(PhotoImage(file='res/numbers/seven.gif'))# 7
        self.icons.append(PhotoImage(file='res/numbers/eight.gif'))# 8
        self.icons.append(PhotoImage(file='res/alert.gif'))        # 9
        self.icons.append(PhotoImage(file='res/question.gif'))     # 10
        self.icons.append(PhotoImage(file='res/tree.gif'))         # 11
        self.icons.append(PhotoImage(file='res/blank.gif'))        # 12
        self.icons.append(PhotoImage(file='res/cop.gif'))          # 13
        self.icons.append(PhotoImage(file='res/spoted_cop.gif'))   # 14
        self.icons.append(PhotoImage(file='res/sneaky_cop.gif'))   # 15
        self.icons.append(PhotoImage(file='res/wrong_guess.gif'))  # 16
        self.icons.append(PhotoImage(file='res/bad_guess.gif'))    # 17
        self.icons.append(PhotoImage(file='res/ok.gif'))           # 18
        self.icons.append(PhotoImage(file='res/no.gif'))           # 19
        treeMap = []
        i = 0
        while (i < N):
            j = 0
            row = []
            while (j < M):
                tree = TreeInForest( master=master, image = self.icons[iconEnum['tree']] ,
                                     command =  lambda  x=i, y=j : self.get_zakladka(x,y))
                tree.bind('<Button-2>', self.check_near)
                tree.bind('<ButtonRelease-2>', self.check_near)
                tree.bind('<Button-3>', self.mark_tree_event)
                tree.treeStatus = treeStatusEnum['sweet']
                tree.iconNumber = iconEnum['tree']
                tree.copsNear = 0
                tree.pb = 0.0
                tree.copsWithP1 = set()
                tree.toolTip = CreateToolTip(tree, '')
                tree.treeCord = (i,j)
                tree.grid(row=i, column=j, columnspan=1)
                row.append(tree)
                j += 1
            treeMap.append(row)
            i += 1
        self.treeMap = treeMap
        self.varCopsNum = StringVar()
        self.labelCopsNum = Label(master=master, textvariable=self.varCopsNum)
        self.labelCopsNum.grid(row =N, column = M//2)
        self.varCopsNum.set(int((self.feildSize[0] * self.feildSize[1]) * self.copsRate))
        self.hintBut = Button(master=master, text= 'Hint', command=self.hint)
        self.hintBut.grid(row=N,column=M//2-3,columnspan=2)
        self.hintBut = Button(master=master, text='Go baka AI', command=self.goBakaGo)
        self.hintBut.grid(row=N, column=M//2+2,columnspan=4)

    def placeCops(self, denX, denY):
        copNum = int((self.feildSize[0] * self.feildSize[1]) * self.copsRate)
        while self.copsInBush < copNum:
            x = randrange(0, self.feildSize[0]-1)
            y = randrange(0, self.feildSize[1]-1)
            tree = self.treeMap[x][y]
            if tree.treeStatus != treeStatusEnum['cop'] and \
                    x != denX and y != denY:
                tree.treeStatus = treeStatusEnum['cop']
                self.copsInBush += 1
                self.countCops(x, y)

    def countCops(self, x, y):
        i = x-1
        while (i <= x+1):
            j = y-1
            while (j <= y+1):
                if i >= 0 and i < self.feildSize[0] and \
                    j >=0 and j < self.feildSize[1]:
                    self.treeMap[i][j].copsNear += 1
                j += 1
            i += 1

    def countAlerts(self, x, y):
        i = x - 1
        while (i <= x + 1):
            j = y - 1
            while (j <= y + 1):
                if i >= 0 and i < self.feildSize[0] and \
                        j >= 0 and j < self.feildSize[1]:
                    self.treeMap[i][j].alertsNear += 1
                j += 1
            i += 1

    def get_zakladka(self, x, y):
        tree = self.treeMap[x][y]
        if tree.iconNumber == iconEnum['alert']:
            return
        if self.StepCounter == 0:
            self.StepCounter += 1
            self.placeCops(x,y)
            if tree.copsNear == 0:
                self.set_sweet_icon(tree)
                self.uncover_blank_area(tree)
            else:
                self.set_cops_number(tree)
        else:
            if tree.treeStatus == treeStatusEnum['sweet']:
                if tree.copsNear > 0:
                    self.set_cops_number(tree)
                else:
                    self.set_sweet_icon(tree)
                    self.uncover_blank_area(tree)
            elif tree.treeStatus == treeStatusEnum['cop']:
                self.uncover_forest(tree)
            elif tree.treeStatus == treeStatusEnum['none']:
                self.set_blank_icon(tree)
        self.restore_all_icons()

    def mark_tree_event(self, event):
        crd = event.widget.treeCord
        tree = self.treeMap[crd[0]][crd[1]]
        self.mark_tree(tree)

    def mark_tree(self, tree):
        if tree.iconNumber == iconEnum['tree']:
            self.set_alert_icon(tree)
            self.varCopsNum.set(int(self.varCopsNum.get()) - 1)
            if tree.treeStatus == treeStatusEnum['cop']:
                self.copsSpoted += 1
        elif tree.iconNumber == iconEnum['alert']:
            self.set_question_icon(tree)
            if tree.treeStatus == treeStatusEnum['cop']:
                self.copsSpoted -= 1
            self.varCopsNum.set(int(self.varCopsNum.get()) + 1)
        elif tree.iconNumber == iconEnum['question']:
            self.set_tree_icon(tree)

    def check_near(self, event):
        tree = event.widget
        x = tree.treeCord[0]
        y = tree.treeCord[1]
        alertsNear = 0
        if event.type == EventType['ButtonPress']: #нажатие
            i = x - 1
            while (i <= x + 1):
                j = y - 1
                while (j <= y + 1):
                    if i >= 0 and i < self.feildSize[0] and \
                            j >= 0 and j < self.feildSize[1]:
                        treeT = self.treeMap[i][j]
                        if treeT.iconNumber != iconEnum['alert'] and \
                                treeT.iconNumber != iconEnum['question']:
                            self.set_blank_icon(self.treeMap[i][j])
                    j += 1
                i += 1
        elif event.type == EventType['ButtonRelease']: #отжатие
            if self.StepCounter == 0:
                i = x - 1
                while (i <= x + 1):
                    j = y - 1
                    while (j <= y + 1):
                        if i >= 0 and i < self.feildSize[0] and \
                                j >= 0 and j < self.feildSize[1]:
                            self.restore_icon(self.treeMap[i][j])
                        j += 1
                    i += 1
                return
            allCopsSpoted = True if tree.copsNear > 0 else False
            i = x - 1
            while (i <= x + 1):
                j = y - 1
                while (j <= y + 1):
                    if i >= 0 and i < self.feildSize[0] and \
                            j >= 0 and j < self.feildSize[1]:
                        treeT = self.treeMap[i][j]
                        if treeT.iconNumber == iconEnum['alert']:
                            alertsNear += 1
                        if ( treeT.treeStatus == treeStatusEnum['cop'] and treeT.iconNumber != iconEnum['alert'] ) or \
                                ( treeT.treeStatus != treeStatusEnum['cop'] and treeT.iconNumber == iconEnum['alert'] ):
                            allCopsSpoted = False
                    j += 1
                i += 1
            i = x - 1
            while (i <= x + 1):
                j = y - 1
                while (j <= y + 1):
                    if i >= 0 and i < self.feildSize[0] and \
                            j >= 0 and j < self.feildSize[1]:
                        treeT = self.treeMap[i][j]
                        if allCopsSpoted and treeT.iconNumber == iconEnum['tree']:
                            if treeT.copsNear == 0 and \
                                    treeT.treeStatus == treeStatusEnum['sweet']:
                                treeT.iconNumber = iconEnum['sweet']
                                self.uncover_blank_area(treeT)
                            elif treeT.copsNear > 0 and \
                                    treeT.treeStatus == treeStatusEnum['sweet']:
                                treeT.iconNumber = treeT.copsNear
                        if not allCopsSpoted and treeT.iconNumber == iconEnum['tree'] and \
                                tree.copsNear > 0 and tree.copsNear == alertsNear:          #u asked for this
                            self.get_zakladka(treeT.treeCord[0], treeT.treeCord[1])
                        self.restore_icon(treeT)
                    j += 1
                i += 1
            self.restore_all_icons()
            self.check_win()

    def set_tree_icon(self, tree):
        self.set_icon_by_name(tree, 'tree')

    def set_cop_icon(self, tree):
        tree['image'] = self.icons[iconEnum['cop']]

    def set_sweet_icon(self, tree):
        self.set_icon_by_name(tree, 'sweet')

    def set_blank_icon(self, tree):
        tree['image'] = self.icons[iconEnum['blank']]

    def set_alert_icon(self, tree):
        self.set_icon_by_name(tree, 'alert')

    def set_question_icon(self, tree):
        self.set_icon_by_name(tree, 'question')

    def set_cops_number(self, tree):
        if tree.copsNear > 0:
            self.set_icon_by_num(tree, tree.copsNear)

    def set_icon_by_num(self, tree, iconNum):
        tree.iconNumber = iconNum
        tree['image'] = self.icons[tree.iconNumber]

    def set_icon_by_name(self, tree, name):
        tree.iconNumber = iconEnum[name]
        tree['image'] = self.icons[tree.iconNumber]

    def restore_icon(self, tree):
        tree['image'] = self.icons[tree.iconNumber]

    def restore_all_icons(self):
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                self.restore_icon(self.treeMap[i][j])
                self.treeMap[i][j].toolTip.off()
                j += 1
            i += 1

    def uncover_blank_area(self, tree):
        x = tree.treeCord[0]
        y = tree.treeCord[1]
        i = x - 1
        while (i <= x + 1):
            j = y - 1
            while (j <= y + 1):
                if i >= 0 and i < self.feildSize[0] and \
                        j >= 0 and j < self.feildSize[1]:
                    treeT = self.treeMap[i][j]
                    if treeT.treeStatus == treeStatusEnum['sweet'] and \
                            treeT.iconNumber > iconEnum['eight']:
                        if treeT.copsNear > 0:
                            self.set_cops_number(treeT)
                        else:
                            self.set_sweet_icon(treeT)
                            self.uncover_blank_area(treeT)
                j += 1
            i += 1

    def uncover_forest(self, tree=None):
        if tree != None:
            self.set_icon_by_name(tree, 'snkyCop')
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                tree = self.treeMap[i][j]
                if tree.treeStatus == treeStatusEnum['sweet']:
                    if tree.iconNumber == iconEnum['alert']:
                        self.set_icon_by_name(tree, 'wrgGuess')
                    else:
                        self.set_sweet_icon(tree)
                elif tree.treeStatus == treeStatusEnum['cop']:
                    if tree.iconNumber == iconEnum['alert']:
                        self.set_icon_by_name(tree, 'sptdCop')
                    elif tree.iconNumber == iconEnum['tree']:
                        self.set_icon_by_name(tree, 'cop')

                elif tree.treeStatus == treeStatusEnum['none']:
                    self.set_blank_icon(tree)
                j += 1
            i += 1
        if self.copsSpoted == self.copsInBush and self.copsInBush > 0 and int(self.varCopsNum.get()) == 0:
            messagebox.showinfo("Gratz", "You WIN!!")
            self.__init__(master=self.master, N=self.feildSize[0], M=self.feildSize[1], copsRate=self.copsRate)
        else:
            messagebox.showinfo("Busted", "Game Over!")
            self.__init__(master=self.master, N=self.feildSize[0], M=self.feildSize[1], copsRate= self.copsRate)

    def check_win(self):
        if self.copsSpoted == self.copsInBush and self.copsInBush > 0 and int(self.varCopsNum.get()) == 0:
            self.uncover_forest()
        else:
            return False

    def hint(self, imAI = False):
        #probability calculate
        maxPforNormalize = 0
        averageAmountOfNumber = self.countAverageAmountNumbersNearTrees()
        steps = 3
        for z in range(steps):
            i = 0
            while (i < self.feildSize[0]):
                j = 0
                while (j < self.feildSize[1]):
                    tree = self.treeMap[i][j]
                    p = self.calcP(tree, averageAmountOfNumber)
                    #maxPforNormalize = p[0] if p[0] > maxPforNormalize else maxPforNormalize
                    j += 1
                i += 1
        #self.nomalizeMtoP(maxPforNormalize, p[1])
        #sort
        crdMinP = []
        crdMaxP = []
        minP = 1.0
        maxP = 0.0
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                tree = self.treeMap[i][j]
                if tree.iconNumber == iconEnum['alert']:
                    if tree.pb <= 0.75:
                        self.set_badguess_icon(tree)
                        tree.toolTip.set_text(str(tree.pb))
                        tree.toolTip.on()
                    j += 1
                    continue
                if tree.pb < minP:
                    crdMinP.clear()
                    crdMinP.append(tree.treeCord)
                    minP = tree.pb
                elif tree.pb == minP:
                    crdMinP.append(tree.treeCord)
                if tree.pb > maxP and tree.pb <= 1:
                    crdMaxP.clear()
                    crdMaxP.append(tree.treeCord)
                    maxP = tree.pb
                elif tree.pb == maxP and tree.pb <= 1:
                    crdMaxP.append(tree.treeCord)
                j += 1
            i += 1
        #display
        for crd in crdMaxP:
            tree = self.treeMap[crd[0]][crd[1]]
            self.set_no_icon(tree)
            tree.toolTip.set_text(str(tree.pb))
            tree.toolTip.on()

        for crd in crdMinP:
            tree = self.treeMap[crd[0]][crd[1]]
            self.set_ok_icon(tree)
            tree.toolTip.set_text(str(tree.pb))
            tree.toolTip.on()

        if imAI:
            return crdMaxP, crdMinP

    def calcP(self, tree, averageAmountOfNumber = 2.5):
        defaultP = self.countDefaultP()
        if tree.iconNumber != iconEnum['tree'] and tree.iconNumber != iconEnum['alert'] and \
                tree.iconNumber != iconEnum['question']:
            tree.pb = 9
            return (0,0)
        x = tree.treeCord[0]
        y = tree.treeCord[1]
        plist = []
        p = 0
        t = -1
        c = 0
        magicNumber = 1
        p_shortcut = 0.5
        i = x - 1
        while (i <= x + 1):
            j = y - 1
            while (j <= y + 1):
                if i >= 0 and i < self.feildSize[0] and \
                        j >= 0 and j < self.feildSize[1]:
                    treeT = self.treeMap[i][j]
                    if self.itIsNumber(treeT):
                        if (x,y) not in treeT.copsWithP1:
                            t = (treeT.iconNumber - len(treeT.copsWithP1)) / \
                                (self.countTreesNear(treeT) - len(treeT.copsWithP1))
                        elif (x,y) in treeT.copsWithP1:
                            t = 1
                        plist.append(t)
                        p += t
                        c += 1
                        if t == 1 or t == 0:
                            p_shortcut = t
                            tree.pb = t * magicNumber
                j += 1
            i += 1
        #shortcuts for Prob = 1 and Prob = 0
        if p_shortcut == 1:
            i = x - 1
            while (i <= x + 1):
                j = y - 1
                while (j <= y + 1):
                    if i >= 0 and i < self.feildSize[0] and \
                            j >= 0 and j < self.feildSize[1]:
                        treeT = self.treeMap[i][j]
                        if self.itIsNumber(treeT):
                            treeT.copsWithP1.add((x,y))
                    j += 1
                i += 1
        elif p_shortcut != 0:
            p = p if p > 0 else defaultP
            tree.pb = p/averageAmountOfNumber if len(plist) > 1 else p
        # if plist:
        #     tree.toolTip.set_text(str(plist))
        # else:
        #     tree.toolTip.set_text(str(defaultP))
        # tree.toolTip.on()
        return (p , defaultP)

    def countTreesNear(self, tree):
        x = tree.treeCord[0]
        y = tree.treeCord[1]
        t = 0
        i = x - 1
        while (i <= x + 1):
            j = y - 1
            while (j <= y + 1):
                if i >= 0 and i < self.feildSize[0] and \
                        j >= 0 and j < self.feildSize[1]:
                    treeT = self.treeMap[i][j]
                    if treeT.iconNumber == iconEnum['tree'] or \
                        treeT.iconNumber == iconEnum['alert'] or \
                        treeT.iconNumber == iconEnum['question']:
                            t += 1
                j += 1
            i += 1
        return t

    def countNumberNear(self,tree):
        x = tree.treeCord[0]
        y = tree.treeCord[1]
        n = 0
        i = x - 1
        while (i <= x + 1):
            j = y - 1
            while (j <= y + 1):
                if i >= 0 and i < self.feildSize[0] and \
                        j >= 0 and j < self.feildSize[1]:
                    treeT = self.treeMap[i][j]
                    if self.itIsNumber(treeT):
                        n += 1
                j += 1
            i += 1
        return n

    def countAverageAmountNumbersNearTrees(self):
        N = 0
        c = 0
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                tree = self.treeMap[i][j]
                if tree.iconNumber == iconEnum['tree'] or \
                    tree.iconNumber == iconEnum['alert'] or \
                    tree.iconNumber == iconEnum['question']:
                        t = self.countNumberNear(tree)
                        if t > 0:
                            N += t
                            c += 1
                j += 1
            i += 1
        return N/c if c > 0 else 1

    def countDefaultP(self):
        t = 0
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                tree = self.treeMap[i][j]
                if tree.iconNumber == iconEnum['tree'] or \
                    tree.iconNumber == iconEnum['alert']:
                    t += 1
                j += 1
            i += 1
        t -= self.copsSpoted
        defP = int(self.varCopsNum.get()) / t  if self.copsInBush == 0 else ( self.copsInBush - self.copsSpoted ) / t
        return defP

    def nomalizeMtoP(self, Pmax, Pdefault):
        if Pmax == 0:
            return
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                tree = self.treeMap[i][j]
                if tree.pb != Pdefault and tree.pb < 9:
                    tree.pb /= (Pmax * 1.001)
                elif tree.pb == 8:
                    tree.pb /= 8
                j += 1
            i += 1

    def itIsNumber(self,tree):
        if tree.iconNumber >= iconEnum['one'] and tree.iconNumber <= iconEnum['eight']:
            return True
        return  False

    def set_ok_icon(self, tree):
        tree['image'] = self.icons[iconEnum['ok']]

    def set_no_icon(self, tree):
        tree['image'] = self.icons[iconEnum['no']]

    def set_badguess_icon(self, tree):
        tree['image'] = self.icons[iconEnum['badGuess']]

    def goBakaGo(self):
        self.isNewGame = False
        ThisIsWin = False
        if self.StepCounter == 0:
            self.get_zakladka(randrange(0,self.feildSize[0]),
                              randrange(0, self.feildSize[1]))
        while ThisIsWin == False:
            if self.isNewGame:
                break
            crdMaxP, crdMinP = self.hint(imAI=True)
            clicked = False
            maxPb = 0
            treeWithMaxPb = None
            for crd in crdMaxP:
                tree = self.treeMap[crd[0]][crd[1]]
                maxPb = maxPb if maxPb >= tree.pb else tree.pb
                treeWithMaxPb = tree
                if  tree.pb == 1:
                    self.mark_tree(tree)
                    clicked = True
            minPb = 0
            treeWithMinPb = None
            for crd in crdMinP:
                tree = self.treeMap[crd[0]][crd[1]]
                minPb = minPb if minPb >= tree.pb else tree.pb
                treeWithMinPb = tree
                if tree.pb == 0:
                    self.get_zakladka(crd[0],crd[1])
                    clicked = True

            if not clicked and minPb < 0.25:
                self.get_zakladka(tree.treeCord[0],tree.treeCord[1])
                clicked = True

            if not clicked and maxPb > 0.5:
                self.mark_tree(tree)
                clicked = True

            ThisIsWin = self.check_win()
            if not clicked:
                ThisIsWin = True
                messagebox.showinfo("Halp!!1", "Halp me! Im so confused")