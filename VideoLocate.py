import pandas as pd
import numpy as np
from text import text_preprocess
from nltk.tokenize import word_tokenize
import os
data = pd.read_json(r"D:\PYTHON\Final_Year\wlasl dataset\WLASL_v0.3.json")
folder = r'D:\PYTHON\Final_Year\wlasl dataset\videos'
data2 = {'x' : '26733x',
'l' : '26721l',
'c' : '26712c',
'y':'26734y',
'z': '26735'
}
class VideoPath:
    def __init__(self,text):
        
        self.txt =text
        self.pre = text_preprocess(self.txt)
        self.pre_text = self.pre.sentence_process().lower()

        self.tokens = [t for t in word_tokenize(self.pre_text)]
        
        self.tokens2 = []
    def video_finder(self, gloss):
        return data[data["gloss"] == gloss]['instances'].values

    def video_extract(self,folder,gloss):
        #print(gloss)
        ids_files = self.video_finder(gloss)
        if len(ids_files)>=1:
            for idx in ids_files[0]:
                video_id = idx['video_id']
                if video_id+'.mp4' in os.listdir(folder):
                    self.tokens2.append(gloss)
                    return video_id+'.mp4'
                    break

        else:
            videos_ids = []
            for w in gloss:
                ids_files = self.video_finder(w)
                if len(ids_files)>=1:
                    for idx in ids_files[0]:
                        video_id = idx['video_id']
                        if video_id+'.mp4' in os.listdir(folder):
                            self.tokens2.append(w+"(fs)")
                            videos_ids.append(video_id+'.mp4')
                            break
            
                elif w in data2:
                    video_id= data2[w]
                    if video_id+'.mp4' in os.listdir(folder):
                        self.tokens2.append(w+"(fs)")
                        videos_ids.append(video_id+'.mp4')

                else:
                    return 'IndexError'
                
        return videos_ids
                    



        #print(gloss)
        #for idx in ids_files:
        #    #idx = np.random.randint(0,len(ids_files),1)[0]
        #    video_id = idx['video_id']
        #    if video_id+'.mp4' in os.listdir(folder):
        #        return video_id+'.mp4'
        #        break
        #    else:
        #        for w in gloss:
        #            
        #else:
        #    return "IndexError"
        #if gloss in data2:
        #        return data2[gloss]+'.mp4'
        #else:
        #    return "IndexError"
    def path(self):
        path = {}
        path2_lst = []
        word_type = []
        for tok in self.tokens:
            pa = self.video_extract(folder , tok)
            path[tok]= pa
        for fi in path.keys():
            if type(path[fi]) != str:
                path2_lst+=path[fi]
                word_type.append(True)
            else:
                path2_lst+=[path[fi]]
                word_type.append(False)
        return path2_lst,path,word_type
    
#sent = VideoPath("XXadaeqas")
#print(sent.path())
#print(sent.tokens2)
#print(sent)