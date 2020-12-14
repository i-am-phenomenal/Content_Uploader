import os
import pickle

class Queue():
    def __init__(self): 
        self.queue = []
        self.currentFile = None

    def pushVal(self, val):
        self.queue.append(val)

    def popVal(self):
        if len(self.queue) != 0:
            poppedVal = self.queue.pop(0)
            self.queue = self.queue[1: len(self.queue)]
            return poppedVal

    def saveDetailsInFile(self): 
        fileNames = [file.name for file in self.queue]
        with open(os.getcwd() + "/queue_details.txt", "w") as file: 
            file.write(", ".join(fileNames))
            file.write("\n")
            file.write(self.currentFile.name)