import spacy
from nltk import word_tokenize
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import nltk
import string
nlp = spacy.load("en_core_web_sm")
class text_preprocess:
    def __init__(self,text):
        self.text = text
        #self.text = self.text.lower().replace('i','me' )
        self.punct = string.punctuation.replace("'","")
        
        for punc in self.punct:
             if punc in self.text:
                    self.text = self.text.replace(punc, "")
        tok = []
        for w in word_tokenize(self.text):
            if w.lower() == 'i':
                tok.append('me')
            else:
                tok.append(w)
        self.text = " ".join(tok)
        self.removables = ['TO', 'POS', 'FW', 'CC', 'DT', 'JJR', 'JJS', 'NNS', 'NNPS' ]
        self.timers = ["before", "after", "later", "Morning", "Afternoon" ,"Evening", "Night", "Midnight", "Earlier", "Later", "Sooner", "Delayed", "Upcoming"]
        
        self.lemmatizer = WordNetLemmatizer()

    #Remove unwanted sovp formating
    def tagger(self,text):   
        tag_dict = {}
        for tt in nltk.pos_tag(word_tokenize(text)):
            tag_dict[tt[0]] = tt[1]
        return tag_dict
    def parser(self,text):
        parse_dict = {}
        for token in nlp(text):
            parse_dict[token.text] = token.dep_
        return parse_dict

    def unwanted_remove(self,text):   

        new_tokens= []
        self.tense = False
        tag_dict = self.tagger(text)
        parse_dict = self.parser(text)
        if "VBD" in tag_dict.values():
            self.tense = "past"
        
        for token in word_tokenize(text):

            if (parse_dict[token] not in self.removables) and (tag_dict[token] not in self.removables):
                if (parse_dict[token] == "aux") or (parse_dict[token] == 'auxpass'):
                        continue
                new_tokens.append(self.lemmatizer.lemmatize(token, wordnet.VERB))

        new_sent = " ".join(new_tokens)

        return new_tokens,new_sent
    def timeword(self,text):
        self.n_tokens, self.n_sent = self.unwanted_remove(text)
        time = ''
        time_labels = ["DATE", "TIME", "DATETIME", "PERIOD", "DURATION"]

        doc = nlp(self.n_sent)
        for ents in doc.ents:
            if (ents.label_ in time_labels):
                time = ents.text
        if time=='':
            for tokens in doc:
                if (tokens.text.lower() in self.timers) :
                    time = tokens.text
        return time
    def sentence_process(self):
        time = self.timeword(self.text)

        if len(time):
            self.n_tokens.remove(time)
            self.n_tokens.insert(0,time)
            print(self.n_tokens)
        elif self.tense:
            self.n_tokens.insert(0,"past")
        n_sent2 = ' '.join(self.n_tokens)
        return n_sent2

#t = text_preprocess(text="I was walking on street")
#sent= t.sentence_process()
#print(sent)