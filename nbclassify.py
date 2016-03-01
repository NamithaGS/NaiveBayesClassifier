import json,sys,os,string
outputfile = 'C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/nboutput.txt'
op = open(outputfile,"wb")
#function to tokenize text
#input : String of text(stripped out of punctuation) and stopword file name
#output: tokens of the text without stop words and lower cased
stopwordfilename = r'C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/english-stopwords.txt'
def tokenize_text(text):
    mytextpunclocal = ''.join([s for s in text[i] if not s.isdigit()])
    mytextpunc1 = " ".join("".join([" " if ch in string.punctuation else ch for ch in mytextpunclocal]).split())
    with open(stopwordfilename) as f:
        stopwords = [line.strip() for line in f]
    thistxttokens = mytextpunc1.split()
    # tokenize and remove stopwords and single-letter words, with stemming or not
    thistxttokens = [w.lower() for w in thistxttokens if w.lower() not in stopwords and len(w) > 1]
    return thistxttokens

#Get the Model file
modelfilepath =  r'C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/nbmodel.txt'
fp = open(modelfilepath,"r")
text =  fp.read()
parsed_input = json.loads(text) # This converts from JSON to a python dictionary


conditionalprob= [-0.00,-0.00,-0.00,-0.00]
posterioriprobclass = [0.00,0.00,0.00,0.00]  # Final conditional prob for a file in each of the 4 classes
priorprobclass= [0.00,0.00,0.00,0.00]  #prior probablity of 4 classes
classes = ["posdeceptive","postruth","negdeceptive","negtruth"]
i=0
#Get prior probablity from model
def getpriorprobablity(classname):
    for item in parsed_input["priorprob"]:
        if( (item['cn']) == classname):
            return item['cpp']
for classname in classes:
    priorprobclass[i] = getpriorprobablity(classname)
    i+=1

#Get conditional probablity ( log) for a token given a class.
def getconditionalprob(classname,token):
    for item in parsed_input[classname]:
        if( (item['tn']) == token):
            return item['ty']

def getdefaultconditionalprob(classname):
   for item in parsed_input["defaultprob"]:
        if( (item['cn']) == classname):
            return item['dp']

label_a = ["deceptive" ,"truthful" ]
label_b = ["negative", "positive"]
label_a_index = 0
label_b_index = 0
def foreachpath(textfromeachfile,filename):
    counter=0
    #strip the data and get as a tuple

    testtokens = tokenize_text(textfromeachfile)
    for counter in range(0,4):
        for tokenname in testtokens:
            temp = getconditionalprob(classes[counter],tokenname)
            if temp is None:
                temp = getdefaultconditionalprob(classes[counter])
            conditionalprob[counter] = float(temp) + float(conditionalprob[counter])
        posterioriprobclass[counter] = float(conditionalprob[counter]) + float(priorprobclass[counter])
    indexofclass =posterioriprobclass.index(max(posterioriprobclass))
    if (indexofclass ==0 ):
        label_a_index = 0
        label_b_index= 1
    if(indexofclass == 1 ):
        label_a_index = 1
        label_b_index= 1
    if(indexofclass == 2 ):
        label_a_index = 0
        label_b_index= 0
    if(indexofclass == 3 ):
        label_a_index = 1
        label_b_index= 0
    op.write (label_a[label_a_index]+" "+ label_b[label_b_index] + " " +  filename )




#Get all the features from the test folder
testfolder = "C:/Users/Namithaa/Desktop/NLP/Assignments/Assignment2/op_spam_train_full/negative_polarity/truthful_from_Web/fold4"
dirlist=os.listdir(testfolder)
for directory, dirnames, files in os.walk(testfolder):
            for filename in files:
                with open(os.path.join(directory,filename)) as f:
                    textfromeachfile = f.read()
                    foreachpath(textfromeachfile,os.path.join(directory,filename))

