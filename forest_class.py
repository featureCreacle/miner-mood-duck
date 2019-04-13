from tkinter import *
from tkinter import messagebox
from functools import partial
from random import random, randrange
from time   import asctime
from math  import pow
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
gameResultEmum = { 'lose'    : 0,
                   'confused': 1,
                    'win'    : 2}

magicNumber = 8 # shift tge top border for probability

class tree_abstract():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.treeCord = (x,y)

class forest_abstract():
    def __init__(self, master=None, N=16, M=16, copsRate = 0.16):
        self.varCopsNum = StringVar()
        self.icons = []
        self.icons.append(PhotoImage(file='res/sweet.gif'))  # 0
        self.icons.append(PhotoImage(file='res/numbers/one.gif'))  # 1
        self.icons.append(PhotoImage(file='res/numbers/two.gif'))  # 2
        self.icons.append(PhotoImage(file='res/numbers/three.gif'))  # 3
        self.icons.append(PhotoImage(file='res/numbers/four.gif'))  # 4
        self.icons.append(PhotoImage(file='res/numbers/five.gif'))  # 5
        self.icons.append(PhotoImage(file='res/numbers/six.gif'))  # 6
        self.icons.append(PhotoImage(file='res/numbers/seven.gif'))  # 7
        self.icons.append(PhotoImage(file='res/numbers/eight.gif'))  # 8
        self.icons.append(PhotoImage(file='res/alert.gif'))  # 9
        self.icons.append(PhotoImage(file='res/question.gif'))  # 10
        self.icons.append(PhotoImage(file='res/tree.gif'))  # 11
        self.icons.append(PhotoImage(file='res/blank.gif'))  # 12
        self.icons.append(PhotoImage(file='res/cop.gif'))  # 13
        self.icons.append(PhotoImage(file='res/spoted_cop.gif'))  # 14
        self.icons.append(PhotoImage(file='res/sneaky_cop.gif'))  # 15
        self.icons.append(PhotoImage(file='res/wrong_guess.gif'))  # 16
        self.icons.append(PhotoImage(file='res/bad_guess.gif'))  # 17
        self.icons.append(PhotoImage(file='res/ok.gif'))  # 18
        self.icons.append(PhotoImage(file='res/no.gif'))  # 19
        treeButMap = []
        i = 0
        while (i < N):
            j = 0
            rowButtons = []
            while (j < M):
                treeBut = Button(master=master, image=self.icons[iconEnum['tree']],
                                       command=lambda x=i, y=j: self.get_zakladka(x, y))
                treeBut.bind('<Button-2>', self.check_near)
                treeBut.bind('<ButtonRelease-2>', self.check_near)
                treeBut.bind('<Button-3>', self.mark_tree_event)
                treeBut.grid(row=i, column=j, columnspan=1)
                treeBut.treeCord = (i, j)
                treeBut.toolTip = CreateToolTip(treeBut, '')
                rowButtons.append(treeBut)
                j += 1
            treeButMap.append(rowButtons)
            i += 1
        self.treeButMap = treeButMap
        self.set_defaults(master=master, N=N, M=M, copsRate=copsRate)

############################################
    def set_defaults(self,  master=None, N=16, M=16, copsRate = 0.16 ):
        self.master = master
        self.feildSize = (N, M)
        self.StepCounter = 0
        self.copsRate = copsRate
        self.copsSpoted = 0
        self.copsInBush = 0
        self.varCopsNum.set(int(N * M * copsRate))
        self.isNewGame = True
        # AI var
        self.gameIsOver = False
        self.Result = 0
        self.lastBadGuess = []
        treeMap = []
        i = 0
        while (i < N):
            j = 0
            row = []
            while (j < M):
                tree = tree_abstract(x = i, y = j)
                tree.treeStatus = treeStatusEnum['sweet']
                tree.iconNumber = iconEnum['tree']
                tree.copsNear = 0
                tree.pb = 0.0
                tree.copsWithP1 = set()
                row.append(tree)
                j += 1
            treeMap.append(row)
            i += 1
        self.treeMap = treeMap

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

############################################
    def get_zakladka(self, x, y, showMessage = True):
        self.isNewGame = False
        tree = self.treeMap[x][y]
        if tree.iconNumber == iconEnum['alert']:
            return
        if self.StepCounter == 0:
            self.StepCounter += 1
            self.placeCops(x,y)
            if tree.copsNear == 0:
                self.set_icon_by_name(tree, 'sweet')
                self.uncover_blank_area(tree)
            else:
                self.set_icon_by_num(tree, tree.copsNear)
        else:
            if tree.treeStatus == treeStatusEnum['sweet']:
                if tree.copsNear > 0:
                    self.set_icon_by_num(tree, tree.copsNear)
                else:
                    self.set_icon_by_name(tree, 'sweet')
                    self.uncover_blank_area(tree)
            elif tree.treeStatus == treeStatusEnum['cop']:
                self.uncover_forest(tree, showMessage)
            elif tree.treeStatus == treeStatusEnum['none']:
                self.set_blank_icon(tree)
        self.restore_all_icons()
        if self.check_win():
            self.uncover_forest(showMessage=showMessage)

    def mark_tree_event(self, event, showMessage = True):
        self.isNewGame = False
        crd = event.widget.treeCord
        tree = self.treeMap[crd[0]][crd[1]]
        islastMark = self.mark_tree(tree)
        if islastMark:
            self.uncover_forest(showMessage = showMessage)

    def mark_tree(self, tree):
        if tree.iconNumber == iconEnum['tree']:
            self.set_icon_by_name(tree, 'alert')
            self.varCopsNum.set(int(self.varCopsNum.get()) - 1)
            if tree.treeStatus == treeStatusEnum['cop']:
                self.copsSpoted += 1
            if self.copsInBush > 0 and self.copsInBush == self.copsSpoted:
                return self.check_win()
        elif tree.iconNumber == iconEnum['alert']:
            self.set_icon_by_name(tree, 'question')
            if tree.treeStatus == treeStatusEnum['cop']:
                self.copsSpoted -= 1
            self.varCopsNum.set(int(self.varCopsNum.get()) + 1)
        elif tree.iconNumber == iconEnum['question']:
            self.set_icon_by_name(tree, 'tree')

        return False

    def check_near(self, event):
        self.isNewGame = False
        x = event.widget.treeCord[0]
        y = event.widget.treeCord[1]
        tree = self.treeMap[x][y]
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
            if self.itIsNumber(tree):
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
                                if not self.isNewGame:
                                    self.get_zakladka(treeT.treeCord[0], treeT.treeCord[1])
                            self.restore_icon(treeT)
                        j += 1
                    i += 1
            self.restore_all_icons()
            if self.check_win():
                self.uncover_forest()

###########################################
    def set_blank_icon(self, tree):
        x = tree.x
        y = tree.y
        self.treeButMap[x][y]['image'] = self.icons[iconEnum['blank']]

    def set_ok_icon(self, tree):
        x = tree.x
        y = tree.y
        self.treeButMap[x][y]['image'] = self.icons[iconEnum['ok']]

    def set_no_icon(self, tree):
        x = tree.x
        y = tree.y
        self.treeButMap[x][y]['image'] = self.icons[iconEnum['no']]

    def set_badguess_icon(self, tree):
        x = tree.x
        y = tree.y
        self.treeButMap[x][y]['image'] = self.icons[iconEnum['badGuess']]


    def set_icon_by_num(self, tree, iconNum):
        tree.iconNumber = iconNum
        x = tree.x
        y = tree.y
        self.treeButMap[x][y]['image'] = self.icons[tree.iconNumber]

    def set_icon_by_name(self, tree, name):
        self.set_icon_by_num(tree, iconEnum[name])

    def restore_icon(self, tree):
        x = tree.x
        y = tree.y
        self.treeButMap[x][y]['image'] = self.icons[tree.iconNumber]

    def restore_all_icons(self):
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                self.restore_icon(self.treeMap[i][j])
                self.treeButMap[i][j].toolTip.off()
                j += 1
            i += 1

#################################################
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
                            self.set_icon_by_num(treeT, treeT.copsNear)
                        else:
                            self.set_icon_by_name(treeT, 'sweet')
                            self.uncover_blank_area(treeT)
                j += 1
            i += 1

    def uncover_forest(self, tree=None, showMessage=True):
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
                        self.set_icon_by_name(tree, 'sweet')
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
            self.Result = gameResultEmum['win']
            self.gameIsOver = True
            if showMessage:
                self.showFinalMessage(self.Result)
                self.set_defaults(master=self.master, N=self.feildSize[0], M=self.feildSize[1],
                          copsRate=self.copsRate)

        else:
            self.Result = gameResultEmum['lose']
            self.gameIsOver = True
            if showMessage:
                self.showFinalMessage(self.Result)
                self.set_defaults(master=self.master, N=self.feildSize[0], M=self.feildSize[1],
                          copsRate= self.copsRate)

    def check_win(self):
        t = 0
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                if self.treeMap[i][j].iconNumber == iconEnum['tree']:
                    t += 1
                j += 1
            i += 1
        if t > 0:
            return False
        if self.copsSpoted == self.copsInBush and self.copsInBush > 0 and int(self.varCopsNum.get()) == 0:
            self.Result = gameResultEmum['win']
            self.gameIsOver = True
            return True

        return False

    def showFinalMessage(self, msgNo = -1, msgText = '', msgCaption = ''):
        if msgNo == -1:
            msgNo = self.Result
        if msgNo == gameResultEmum['win']:
            messagebox.showinfo("Gratz", "You WIN!!")
        elif msgNo == gameResultEmum['lose']:
            messagebox.showinfo("Busted", "Game Over!")
        elif msgNo == gameResultEmum['confused']:
            messagebox.showinfo("Halp!!1", "Halp me! Im so confused")
        else:
            messagebox.showinfo(msgCaption, msgText)

 #AI section######################################
    def hint(self, imAI = False):
        #probability calculate
        mg = magicNumber
        defaultP = self.countDefaultP()
        averageAmountOfNumber = self.countAverageAmountNumbersNearTrees()
        steps = 3
        for z in range(steps):
            i = 0
            while (i < self.feildSize[0]):
                j = 0
                while (j < self.feildSize[1]):
                    tree = self.treeMap[i][j]
                    self.calcP(tree, averageAmountOfNumber, defaultP, mg)
                    j += 1
                i += 1
        #sort
        crdMinP = []
        crdMaxP = []
        minP = 1.0
        maxP = 0.0
        badGuess = []
        i = 0
        while (i < self.feildSize[0]):
            j = 0
            while (j < self.feildSize[1]):
                tree = self.treeMap[i][j]
                if tree.iconNumber == iconEnum['alert']:
                    if tree.pb <= 0.75:
                        self.set_badguess_icon(tree)
                        badGuess.append(tree.treeCord)
                        treeBut = self.treeButMap[tree.x][tree.y]
                        treeBut.toolTip.set_text(str(tree.pb))
                        treeBut.toolTip.on()
                    j += 1
                    continue
                if tree.pb < minP:
                    crdMinP.clear()
                    crdMinP.append(tree.treeCord)
                    minP = tree.pb
                elif tree.pb == minP:
                    crdMinP.append(tree.treeCord)
                if tree.pb > maxP and tree.pb <= mg:
                    crdMaxP.clear()
                    crdMaxP.append(tree.treeCord)
                    maxP = tree.pb
                elif tree.pb == maxP and tree.pb <= mg:
                    crdMaxP.append(tree.treeCord)
                j += 1
            i += 1
        #display
        self.restore_all_icons()
        for crd in crdMaxP:
            tree = self.treeMap[crd[0]][crd[1]]
            self.set_no_icon(tree)
            treeBut = self.treeButMap[tree.x][tree.y]
            treeBut.toolTip.set_text(str(tree.pb if tree.pb != mg else 1))
            treeBut.toolTip.on()

        for crd in crdMinP:
            tree = self.treeMap[crd[0]][crd[1]]
            self.set_ok_icon(tree)
            treeBut = self.treeButMap[tree.x][tree.y]
            treeBut.toolTip.set_text(str(tree.pb if tree.pb != mg else 1))
            treeBut.toolTip.on()

        if imAI:
            return crdMaxP, crdMinP, badGuess

    def calcP(self, tree, averageAmountOfNumber = 2.5, defaultP = 0.5, magicNumber = 1):
        if tree.iconNumber != iconEnum['tree'] and tree.iconNumber != iconEnum['alert'] and \
                tree.iconNumber != iconEnum['question']:
            tree.pb = magicNumber + 1
            return
        x = tree.treeCord[0]
        y = tree.treeCord[1]
        plist = []
        p = 0
        t = -1
        c = 0
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
        #shortcuts for Prob = 1
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
            p = p if p>0 else defaultP
            tree.pb = p / averageAmountOfNumber if len(plist) > 1 else p

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

    def countNumbersNear(self,tree):
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
                        t = self.countNumbersNear(tree)
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
                if tree.iconNumber == iconEnum['tree']:
                    t += 1
                j += 1
            i += 1

        return int(self.varCopsNum.get()) / t if t > 0 else 0

    def itIsNumber(self,tree):
        if tree.iconNumber >= iconEnum['one'] and tree.iconNumber <= iconEnum['eight']:
            return True
        return  False


    def doStep(self, showMessage=False):
        #self.master.update_idletasks()
        self.master.update()
        if self.StepCounter == 0:
            self.get_zakladka(randrange(0, self.feildSize[0]),
                              randrange(0, self.feildSize[1]))
            return True
        crdMaxP, crdMinP, badGuess = self.hint(imAI=True)
        maxPb = 0
        treeWithMaxPb = None
        mg = magicNumber
        for crd in crdMaxP:
            tree = self.treeMap[crd[0]][crd[1]]
            if tree.pb == mg:
                self.mark_tree(tree)
                return True
            elif maxPb < tree.pb:
                maxPb = tree.pb
                treeWithMaxPb = tree
        minPb = 1.0
        treeWithMinPb = None
        for crd in crdMinP:
            tree = self.treeMap[crd[0]][crd[1]]
            if tree.pb == 0:
                self.get_zakladka(crd[0], crd[1],showMessage=showMessage)
                return True
            elif tree.pb < minPb:
                minPb = tree.pb
                treeWithMinPb = tree

        if minPb < 0.35:
            self.get_zakladka(treeWithMinPb.treeCord[0], treeWithMinPb.treeCord[1],
                              showMessage=showMessage)
            return True

        if int(self.varCopsNum.get()) == 0:
            badGuessP = 1
            worstAlert = None
            i = -1
            for bge in badGuess:
                i += 1
                tree = self.treeMap[bge[0]][bge[1]]
                if badGuessP > tree.pb:
                    badGuess = tree.pb
                    worstAlert = tree

            if worstAlert != None:
                self.mark_tree(worstAlert)
                self.mark_tree(worstAlert)
                worstAlertCrd = [worstAlert.treeCord[0], worstAlert.treeCord[1]]
                if worstAlertCrd == self.lastBadGuess:
                    self.Result = gameResultEmum['confused']
                    return False
                else:
                    self.lastBadGuess = [worstAlertCrd[0], worstAlertCrd[1]]
                return True

        if maxPb > 0.5:
            if self.mark_tree(treeWithMaxPb):
                self.uncover_forest(showMessage=showMessage)
            return True

        self.Result = gameResultEmum['confused']
        return False