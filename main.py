import pathlib
import numpy as np
import os
import re

def refr(): os.system('cls' if os.name == 'nt' else 'clear')

NAME = "Data Parser v0.1 - UCI DING LAB"
CONTINUE = "Press ENTER to continue, Ctrl-C to exit."
INS = "\nInstruct: "
P_PREV_F = "Below is the directory you've worked on.\nInstruct 0 to parse a new file.\nInstruct other number to parse the selected file.\n[0] New File"
P_ACT = "The ultimate goal of this program is to parse the data into standard csv format.\nBelow is a series of instructions.\nExtra lines can be added to the data.\n[0] Done(Export)\n[1] GRTK Format\n[2] Info\n[3] Show Current Extra Lines\n[4] Add Extra Line\n[5] Remove Extra Line"
P_GRTK_F = "GRTK requires TWO extra lines, the first one is curve type, the second one is curve name.\nMake sure instruct [3] to check there exists exactly two extra lines filled with english letter curve info.\nBoth of them must have a position of 0, which means insert in the very front of the export file.\nOrder matters!"
P_NEWL_I = "You are creating a new line to be added to the data.\nPlease enter the content of each column seperated by a comma.\n\nFor example:\nCurveA,CurveB,CurveC\nYou will also be prompted to enter where do you want to insert it after you enter the content.\nYou can enter -1 when you want the program to insert the line at the very end of the data."

class err(object):
    @staticmethod
    def checkPath(string: str):
        if not pathlib.Path(string).exists(): raise FileNotFoundError(f"Path '{string}' does not exist.")
        return string

class container(object):
    def __init__(self, d: np.array):
        self.data = d
        self.extra = []
    
    def addExtraLine_S(self, content: list, pos=-1):
        self.extra.append((content, pos))
        self.extra.sort(key=lambda x: (x[1] == -1, x[1]))
    
    def remvExtraLine(self, pos: int):
        for i, e in enumerate(self.extra):
            if e[1] == pos:
                self.extra.pop(i)
                return
    
    def export(self, filename: str):
        combined = self.data.tolist()
        for e in self.extra:
            if e[1] == -1:
                combined.append(e[0])
            else:
                combined.insert(e[1], e[0])
        combined_array = np.array(combined, dtype=str)
        np.savetxt(filename, combined_array, fmt='%s', delimiter=",")

class parserKing(object):
    def __init__(self):
        self.main()
    
    def main(self):
        refr()
        prevF = open("prevF.txt", "a+")
        prevF.seek(0)
        prevPath = prevF.readlines()
        for i in range(len(prevPath)):
            prevPath[i] = prevPath[i].rstrip()
        while True:
            print(NAME)
            print(P_PREV_F)
            for i, path in enumerate(prevPath):
                print(f"[{i+1}] {path}")
            print(CONTINUE)
            instruct = input(INS)
            if instruct == "0":
                path = input("Enter new file path: ")
            elif instruct.isdigit() and int(instruct) <= len(prevPath):
                path = prevPath[int(instruct)-1]
            else:
                print("Invalid instruction.")
                continue
            refr()
            if path not in prevPath:
                prevF.write(str(path)+"\n")
            prevF.close()
            break
        
        path = err.checkPath(path)
        f = open(path, "r")
        lines = f.readlines()
        d = [[float(x) for x in re.split(r'[,\s\t\n;]+', line) if x.strip()] for line in lines]
        self.c = container(np.array(d))
        f.close()
        
        while True:
            print(P_ACT)
            print(CONTINUE)
            instruct = input(INS)
            if not (instruct.isdigit() and int(instruct) < 5):
                continue
            if instruct == "0":
                refr()
                exp_f = input("Enter export file name: ")
                print("Exporting...")
                self.c.export(exp_f)
                print("Export complete.")
                print("\n\n")
            if instruct == "1":
                refr()
                print(P_GRTK_F)
                print("\n\n")
            if instruct == "2":
                refr()
                print("Data Shape:", self.c.data.shape)
                print("Extra Lines Added:", len(self.c.extra))
                print("\n\n")
            if instruct == "3":
                refr()
                if len(self.c.extra) == 0:
                    print("No extra lines added.")
                for line, pos in self.c.extra:
                    print(f"{line} > {pos}")
                print("\n\n")
            if instruct == "4":
                refr()
                columnCount = self.c.data.shape[1]
                rowCount = self.c.data.shape[0]
                print(P_NEWL_I)
                print("\n")
                print(f"Your column count is {columnCount}. Your input must have {columnCount} columns.")
                userIn = input("\nEnter new line: ")
                newLine = [x.strip() for x in userIn.split(",")]
                if len(newLine) != columnCount:
                    print("Invalid input.")
                    continue
                print(f"\nYour row count is {rowCount}. Your insert position input must be between 0 and {rowCount}.")
                userIn = input("\nEnter insert position: ")
                if not userIn.isdigit() or int(userIn) < 0 or int(userIn) > rowCount:
                    print("Invalid input.")
                    continue
                self.c.addExtraLine_S(newLine, int(userIn))
                refr()
                print(f"Confirmed: {newLine} INSERTED at {userIn}\n\n")
            if instruct == "5":
                refr()
                print("Enter the position of the line you want to remove.")
                userIn = input("\nEnter position: ")
                if not userIn.isdigit() or int(userIn) < 0:
                    print("Invalid input.")
                    continue
                self.c.remvExtraLine(int(userIn))
                refr()
                print(f"Confirmed: Line at position {userIn} REMOVED\n\n") 

if __name__ == "__main__":
    parserKing()
    exit()