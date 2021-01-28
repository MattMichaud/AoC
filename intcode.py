class IntCodeComputer:
    def __init__(self,program_code,id =0, relBase=0,indx=0,empty_space=1000,inptArr=[]):
        self.relativeBase =0
        self.memory =[]
        self.memory = program_code.copy()
        for i in range(empty_space):
            self.memory.append(0)
        self.index=indx
        self.input_array=inptArr.copy()
        self.output_array=[]
        self.id=id
        self.finished = False

    def set_single_memory_address(self, pos, value):
        self.memory[pos] = value

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
            param_mode = str(self.memory[self.index][:3])
            OpCode = str(self.memory[self.index])[-2:]
            self.memory[self.index]=int(self.memory[self.index])
            if (param_mode[2] == "0"):
                parameters.append(int(self.memory[self.index + 1]))
            elif (param_mode[2] == "1"):
                parameters.append(self.index + 1)
            else:#paramMode 2
                parameters.append(int(self.memory[self.index + 1]) +self.relativeBase)

            if (param_mode[1] == "0"):
                parameters.append(int(self.memory[self.index + 2]))
            elif (param_mode[1] == "1"):
                parameters.append(self.index + 2)
            else:#paramMode 2
                parameters.append(self.memory[self.index + 2] + self.relativeBase)

            if (param_mode[0] == "0"):
                parameters.append(int(self.memory[self.index + 3]))
            elif (param_mode[0] == "1"):
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
                if(len(self.input_array)!=0):
                    #print('processing input {} at ip {}'.format(self.input_array[0], self.id))
                    self.memory[parameters[0]]=self.input_array[0]
                    self.index+=2
                    self.input_array.pop(0)
                else:
                    #print("waiting input")
                    break
            elif(OpCode=="04"):
                #print("output from int comp "+str(self.id)+ "  :" +str(self.memory[parameters[0]]))
                self.output_array.append(self.memory[parameters[0]])
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

    def add_input(self,input):
        self.input_array.append(input)

    def print_outputs(self):
        print(self.output_array)

    def get_output(self):
        return self.output_array

    def pop_output(self):
        if len(self.output_array) > 0:
            out = self.output_array.pop()
            return out
        else:
            return None

    def flush_outputs(self):
        self.output_array.clear()


def parse_intcode(filename):
    return [int(c) for c in open(filename, 'r').read().split(',')]