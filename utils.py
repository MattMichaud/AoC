def data_import(filename, cast=str, split_char=None, rstrip=False):
    data = []
    with open(filename) as file:
        line = file.readline()
        while line:
            if rstrip and line.rstrip() or line.strip():

                if split_char is not None:
                    line = line.split(split_char)
                    data.append([cast(item.strip()) for item in line])
                else:
                    data.append(cast(rstrip and line.rstrip() or line.strip()))

            line = file.readline()
    return data

def tuple_add(a, b):
    return(tuple(map(sum, zip(a, b))))


class IntCodeComputer:
    def __init__(self,programCode,id =0, relBase=0,indx=0,emptySpace=1000,inptArr=[]):
        self.relativeBase =0
        self.memory =[]
        self.memory = programCode.copy()
        for i in range(emptySpace):
            self.memory.append(0)
        self.index=indx
        self.inputArray=inptArr.copy()
        self.outputArray=[]
        self.id=id
        self.finished = False

    def compute(self):#computes until there's an input requiered
        while(True):
            #formatting OPCODE
            TempLen = len(str(self.memory[self.index]))
            StringToAdd = ""
            for i in range(5 - TempLen):
                StringToAdd += "0"
            self.memory[self.index] = StringToAdd + str(self.memory[self.index])

            #reading parameters according to the given parameter modes ----------------------
            parameters = []
            parameterMode = str(self.memory[self.index][:3])
            OpCode = str(self.memory[self.index])[-2:]
            self.memory[self.index]=int(self.memory[self.index])
            if (parameterMode[2] == "0"):
                parameters.append(int(self.memory[self.index + 1]))
            elif (parameterMode[2] == "1"):
                parameters.append(self.index + 1)
            else:#paramMode 2
                parameters.append(int(self.memory[self.index + 1]) +self.relativeBase)

            if (parameterMode[1] == "0"):
                parameters.append(int(self.memory[self.index + 2]))
            elif (parameterMode[1] == "1"):
                parameters.append(self.index + 2)
            else:#paramMode 2
                parameters.append(self.memory[self.index + 2] + self.relativeBase)

            if (parameterMode[0] == "0"):
                parameters.append(int(self.memory[self.index + 3]))
            elif (parameterMode[0] == "1"):
                parameters.append(self.index + 3)
            else:#paramMode 2
                parameters.append(int(self.memory[self.index + 3]) + self.relativeBase)
            #param read end -----------------------------------------

            #reacting according to the OP CODE-----------------------------------------
            if(OpCode=="01"):
                self.memory[parameters[2]] = int(self.memory[parameters[0]]) + int(self.memory[parameters[1]])
                self.index +=4
            elif(OpCode=="02"):
                self.memory[parameters[2]] = int(self.memory[parameters[0]]) * int(self.memory[parameters[1]])
                self.index += 4
            elif(OpCode=="03"):
                if(len(self.inputArray)!=0):
                    self.memory[parameters[0]]=self.inputArray[0]
                    self.index+=2
                    self.inputArray.pop(0)
                else:
                    #print("waiting input")
                    break
            elif(OpCode=="04"):
                #print("output from int comp "+str(self.id)+ "  :" +str(self.memory[parameters[0]]))
                self.outputArray.append(self.memory[parameters[0]])
                self.index+=2
            elif(OpCode=="05"):
                if(self.memory[parameters[0]]!=0):
                    self.index = int(self.memory[parameters[1]])
                else:
                    self.index+=3
            elif(OpCode=="06"):
                if (self.memory[parameters[0]] == 0):
                    self.index = int(self.memory[parameters[1]])
                else:
                    self.index += 3
            elif(OpCode=="07"):
                if(int(self.memory[parameters[0]]) < int(self.memory[parameters[1]])):
                    self.memory[parameters[2]]=1
                else:
                    self.memory[parameters[2]]=0
                self.index+=4
            elif(OpCode=="08"):
                if (self.memory[parameters[0]] == self.memory[parameters[1]]):
                    self.memory[parameters[2]] = 1
                else:
                    self.memory[parameters[2]] = 0
                self.index += 4
            elif(OpCode=="09"):
                self.relativeBase += self.memory[parameters[0]]
                self.index+=2
            elif(OpCode=="99"):
                #print(str(self.id)+ ". computer has finished")
                self.finished=True
                break

    def addInput(self,input):
        self.inputArray.append(input)
