import re, os, sys
import string,math

#Target file to write the model
fp = open('C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/nbmodel.txt', "wb")
#Training set folders and names
classfoldername= ["C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/op_spam_train_test/positive_polarity/deceptive_from_MTurk",
                  "C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/op_spam_train_test/positive_polarity/truthful_from_TripAdvisor",
                  "C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/op_spam_train_test/negative_polarity/deceptive_from_MTurk",
                  "C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/op_spam_train_test/negative_polarity/truthful_from_Web"]
classes = ["posdeceptive","postruth","negdeceptive","negtruth"]

#Parse every file (3 folds) in the folder given
def parsefile(foldername):
    numberoffiles = 0
    dirlist=os.listdir(foldername)
    text = ""
    for x in dirlist:
        for directory, dirnames, files in os.walk(os.path.join(foldername,x)):
            for filename in files:
                with open(os.path.join(directory,filename)) as f:
                    text += ''.join(f.read())
                numberoffiles+=1
    return text,numberoffiles



#function to tokenize text
#input : String of text(stripped out of punctuation) and stopword file name
#output: tokens of the text without stop words and lower cased
def tokenize_text(text):
    with open(stopwordfilename) as f:
        stopwords = [line.strip() for line in f]
    thistxttokens = text.split()
    # tokenize and remove stopwords and single-letter words, with stemming or not
    thistxttokens = [w.lower() for w in thistxttokens if w.lower() not in stopwords and len(w) > 1]
    return thistxttokens

#Parse first class ( posdeceptive) to get the text and the number of files in the class
mytext =["","","",""]
numberoffilesineachclass = [0,0,0,0]
for i in range(0,4):
    (mytext[i],numberoffilesineachclass[i]) = parsefile(classfoldername[i])

#Total number of files available
totalfiles = 0
for i in range(0,4):
    totalfiles = totalfiles  + numberoffilesineachclass[i]

#Remove all the punctuation in text and replace the punctuation by space
mytextpunc =["","","",""]
for i in range(0,4):
    mytextpunc[i] = " ".join("".join([" " if ch in string.punctuation else ch for ch in mytext[i]]).split())

#Do spelling correction somehow
#Do suffix removal
#Remove numbers

#Remove all the stop words and printout a tuple of all tokens
mytextstop = ["","","",""]
stopwordfilename = r'C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/english-stopwords.txt'
for i in range(0,4):
    mytextstop[i] = tokenize_text(mytextpunc[i])


#################################
##### Modelling the features#####
#################################

alltokens = []
for i in range(0,4):
    mytextstring = " ".join(mytextstop[i])
    alltokens = alltokens  + mytextstring.split()

nooftokensinvocab = len(list(set(alltokens)))

#lapalace smoothing to the conditional probablity
def lapalace_smoothing(tokencountinclass, nooftokensinclass ):
    a = (float)(tokencountinclass + 1)/ (float)( nooftokensinclass + nooftokensinvocab )
    return math.log(a)

#Add lapalace smoothing to all tokens
def calcpriorptokens(classtext):
    for mytoken in classtext:
        tokencountinclass = classtext.count(mytoken)
        nooftokensinclass = len(classtext)
        a = lapalace_smoothing(tokencountinclass, nooftokensinclass )
        fp.write('{"tn":"'+ mytoken+'",')
        fp.write('"ty":"' + str(a)+'"},')

#Print all the conditional probablities
fp.write("{")
for i in range(0,4):
    fp.write('"' + classes[i] + '":[')
    calcpriorptokens(mytextstop[i])
    fp.seek(-1, os.SEEK_END)
    fp.truncate()
    fp.write('],\n ')

########################################
#####Prior Probablity###################
######################################

#Calculate prior probability, return log values
def calcpriorp(classname):
    (text,number) = parsefile(classname)
    a = (float(number)/totalfiles)
    b = math.log(a)
    return b

priorprob=[-0.00,-0.00,-0.00,-0.00]
#Calculate each prior probability
for i in range(0,4):
    classnameis = classes[i]
    priorprob[i] = calcpriorp(classfoldername[i])

#Print all the prior probablities
fp.write('"priorprob":[')
for i in range(0,4):
    fp.write('{"cn":"'+ classes[i]+'",')
    fp.write('"cpp":"' + str(priorprob[i])+'"},')
fp.seek(-1, os.SEEK_END)
fp.truncate()
fp.write('],\n ')

############################################
##### Default conditional Probablity########
############################################
#Print Default conditional probablity for each class
fp.write('"defaultprob":[')
for i in range(0,4):
    fp.write('{"cn":"'+ classes[i]+'",')
    fp.write('"dp":"' + str(lapalace_smoothing(0, len(mytextstop[i])))+'"},')
fp.seek(-1, os.SEEK_END)
fp.truncate()
fp.write(']}\n ')
