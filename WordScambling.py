import random
name=input("Enter the file name:\n")
fp1=open(name+".txt","r")
fp2=open(name+"Scrambled.txt","w")
l=list()
for line in fp1:
    l=line.split()
    for word in l:
        if(len(word)<=3):
            fp2.write(word+' ')
        elif(word[len(word)-1]==',' or word[len(word)-1]=='!' or word[len(word)-1]=='.'):
            sword=word[0]
            words=(random.sample(word[1:(len(word)-2)],(len(word)-3)))
            sword+=''.join(str(i) for i in words)
            sword+=word[len(word)-2]
            sword+=word[len(word)-1]
            fp2.write(sword+' ')
        else:
            sword=word[0]
            words=(random.sample(word[1:len(word)-1],(len(word)-2)))
            sword+=''.join(str(i) for i in words)
            sword+=word[len(word)-1]
            fp2.write(sword+' ')
    fp2.write('\n')   
fp1.close()
fp2.close()
