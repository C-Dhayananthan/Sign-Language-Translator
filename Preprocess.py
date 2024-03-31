class text_preprocess:
    def __init__(self):
            
        self.counts= -1
        self.prev_char=""
        self.ten_prev_char=[]
        for i in range(10):
            self.ten_prev_char.append(" ")
        self.character = ""
    
    def sentence_preocess(self, char):

        if char=="next" and self.prev_char!="next":
            if self.ten_prev_char[(self.counts - 2)%10]!="next":
                if self.ten_prev_char[(self.counts-2)%10]=="Backspace":
                            character=character[0:-1]
                else:
                    if self.ten_prev_char[(self.counts - 2) % 10] != "Backspace":
                        character = character + self.ten_prev_char[(self.counts-2)%10]
            else:
                if self.ten_prev_char[(self.counts - 0) % 10] != "Backspace":
                        character = character + self.ten_prev_char[(self.counts - 0) % 10]


        if char=="  " and self.prev_char!="  ":
            character = character + "  "

        self.prev_char=char
        self.counts += 1
        self.ten_prev_char[self.counts %10]=character

        print("prev character: ",self.prev_char)
        print("ten prev char: ", self.ten_prev_char)
        print("________Sentence__________",character)