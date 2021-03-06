import os
import pickle

class ProcessQueue():
    def __init__(self): 
        self.queue = []

    def pushVal(self, val):
        self.queue.append(val)

    def popVal(self):
        if len(self.queue) > 0:
            poppedVal = self.queue.pop(0)
            return poppedVal

    def saveDetailsInFile(self): 
        fileNames = [file.name for file in self.queue]
        with open(os.getcwd() + "/queue_details.txt", "w") as file: 
            file.write(", ".join(fileNames))
            file.write("\n")