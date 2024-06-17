#Required libraries: Pandas, Numpy, Tabulate, Matplotlib, Math
#Given Data File
#KKR Batting innings vs csk

f=open('data.txt','r')
a=list((f.read()).split("\n"))
f.close

for i in a:
    if(len(i)==1):
        a.remove(i)
        
b=[]
for i in a:
    if(len(i)==3 or len(i)==4):
            b.append(i)
            b.append(a[a.index(i)+1])
            a.remove(i)
            
#Processed And Cleaned Data file
f=open('Datatemp.txt','w')
for i in b:
    f.write(i)
    f.write("\n")
f.close()

#importing Data to Script as list
f=open('Datatemp.txt','r')
data=list((f.read()).split("\n"))
f.close()
ball_no=data[::2]
ball_info=data[1::2]
datacln=list(zip(ball_no,ball_info))
datacln.reverse()
count=0
all1=[]
ts=0

#Batting Team
kxip11="Sunil Narine, Chris Lynn, Robin Uthappa, Nitish Rana, Dinesh Karthik (c & wk), Andre Russell, Shubman Gill, Piyush Chawla, Kuldeep Yadav, Prasidh Krishna, Harry Gurney"

kxi=kxip11.split(",")
kxi=[i.strip() for i in kxi]

#Batting Team + Bowling Team
Playingxiall="Shane Watson, Faf du Plessis, Suresh Raina, Ambati Rayudu, Kedar Jadhav, MS Dhoni (c & wk), Ravindra Jadeja, Mitchell Santner, Deepak Chahar, Shardul Thakur, Imran Tahir,Sunil Narine, Chris Lynn, Robin Uthappa, Nitish Rana, Dinesh Karthik (c & wk), Andre Russell, Shubman Gill, Piyush Chawla, Kuldeep Yadav, Prasidh Krishna, Harry Gurney"

pxi=Playingxiall.split(",")
pxi=[i.strip() for i in pxi]
pxit=[i.lower() for i in pxi]
catchmiss=[]

#Extarction of values from the cleaned data
for i in datacln:
    nw=0
    n0=0
    n1=0
    n2=0
    n3=0
    n4=0
    n6=0
    nwi=0
    nlb=0
    nnb=0
    nb=0
    bn=float(i[0])
    dat=i[1]
    dat=dat.replace("!","")
    raw_ls=dat.split(",")
    names=raw_ls[0]
    name_split=names.split(" to ")
    #try:
    b=name_split[0]#Bowler Name
    c=name_split[1]#Batsmen
    runs=raw_ls[1]
    runs=runs.strip()
    runs=runs.lower()
    runs_split=runs.split()
    extra=0
    out="Not Out"
    run=0
    #evaluating runs, extras and out type
    if(len(runs_split)==1):
        if (runs=='six' or runs=='6'):
            run=6
            n6=1
        elif (runs=='four'or runs=='4'):
            run=4
            n4=1
        elif (runs=='wide'):
            run=0
            nwi=1
            extra+=1
    elif(len(runs_split)==2):
        if(runs_split[0]=='no' and (runs_split[1]=='run' or runs_split[1]=='runs') ):
            run=0
            n0=1
        elif(runs_split[0]=='no' and runs_split[1]=='ball' ):
            nnb=1
            extra+=1
        elif(runs_split[0]=='leg'):
            runs1=raw_ls[2]
            runs1=runs1.strip()
            runs1=runs1.lower()
            runs1_split=runs1.split()
            run=int(runs1_split[0])
            extra=extra+run
            nlb=run
            run=0

        else:
            run=int(runs_split[0])
            if(run==1):
                n1=1
            elif(run==2):
                n2=1
            elif(run==3):
                n3=1
    elif('out' in runs_split):
        if('caught' in runs_split):
            out='c '+ str(runs_split[runs_split.index('caught')+2])+" b " + b
            nw=1
        elif('bowled' in runs_split):
            out="b " + b
            nw=1
        elif('lbw' in runs_split):
            out="lbw " + b
            nw=1
    out=(out)
    d=run#runs_Scored
    e=extra#extras
    ts+=run+extra
    #evaluating for runout
    for i in raw_ls:
        i=i.lower()
        if 'run out' in i:
            isplt=i.split(".")
            ifsplit=isplt[-1].split(" run out ")
            c=ifsplit[0]
            otsplt=ifsplit[1].split(")")
            outspl=otsplt[0]
            out="Runout "+ outspl[1:]
            d=0
            e=0
            f=0
            nw=1
            n0=0
            n1=0
            n2=0
            n3=0
            n4=0
            n6=0
            nwi=0
            nlb=0
            nnb=0
            nb=0
    #checking for any dropped catches
    for ier in raw_ls:
        ier=ier.lower()
        if 'drop' in ier and 'catch' in ier:
            cat=[]
            cat.append(bn)
            cat.append(c)
            for der in pxit:
                if der in ier:
                    cat.append(pxi[pxit.index(der)])
            catchmiss.append(cat)
#checking for availability of ball speed        
    f=-1
    for i in raw_ls:
        if('km/h' in i):
            i=i.strip()
            t=i.split()
            for x in t:
                if('km/h' in x):
                    x=x.replace("@","")
                    x=x[:-4]
                    f=float(x)#Bowling Speed
    result=list([bn,b,c,d,e,f,out,ts,nw,n0,n1,n2,n3,n4,n6,nwi,nlb,nb,nnb])
    all1.append(result)
    
#Convertion of unstructured data to structured format
import pandas as pd
df = pd.DataFrame(all1,columns=['Ball Number','Bowler','Batsmen','Runs Scored of that ball','Extras','Ball Speed','Out','Team Score','Total Wickets','No of Dots','No of Ones','No of Twos','No of Threes','No of Fours','No of Sixes','No of Wides','Leg Byes','Byes','NoBall'])
df.to_csv (r'export_dataframe.csv', index = None, header=True)
bats=set(list(df['Batsmen']))
bowls=set(list(df['Bowler']))
balls=(list(df['Ball Number']))
Sc_bat=[]

#extraction of batsmen details for score card
#BatsmenName Out/Not Out Runs NoOfBalls 4s 6s SR
for i in bats:
    a=df.loc[df['Batsmen'] == i]
    batsman=[]
    batsman.append(i.lower())
    o=list(set(list(a['Out'])))
    if len(o)>1 and 'Not Out' in o:
        o.pop(o.index('Not Out'))
    if len(o)==2:
        batsman.append(o[0])
    else:
        batsman.append(o[0])
    runs=sum(list(a['Runs Scored of that ball']))
    ballsno=len(set(list(a['Ball Number'])))
    fours=sum(list(a['No of Fours']))
    sixes=sum(list(a['No of Sixes']))
    Sr=round((runs/ballsno)*100,2)
    Sr=float(Sr)
    if 'run' or 'Run' in o.split():
        ballsno=ballsno-1
    batsman.append(runs)
    batsman.append(ballsno)
    batsman.append(fours)
    batsman.append(sixes)
    batsman.append(Sr)
    batsman.append(a.iloc[0,0])
    Sc_bat.append(batsman)
    
Batsdf=pd.DataFrame(Sc_bat,columns=['Batsman','          ','R','B','4s','6s','SR','Key'])
Batsdf=Batsdf.sort_values(by=['Key'])
SC_Bat=Batsdf.loc[:, ['Batsman','          ','R','B','4s','6s','SR']]
header=list(['Batsman','          ','R','B','4s','6s','SR'])
nwickets=sum(list(df['Total Wickets']))    
extras=sum(list(df['Extras']))
nwides=sum(list(df['No of Wides']))
nbyes=sum(list(df['Byes']))
nlegbyes=sum(list(df['Leg Byes']))    
nnoball=sum(list(df['NoBall']))
a1=df.loc[df['Out']!='Not Out']

#Checking for the fall ow wickets and gatherig required info
Fall_wick=[]
nwicks=0
ball_wick=(list(a1['Ball Number']))
for i in ball_wick:
    a2=a1.loc[a1['Ball Number'] == i]
    nwicks=nwicks+int(a2['Total Wickets'])
    strtemp=str(a2.iloc[0,7])+"-"+str(nwicks)+"("+str(a2.iloc[0,2])+","+ str(i)+")"
    Fall_wick.append(strtemp)
Fall_wick.reverse()

#calculating extras overal
Extras=str(extras)+"(b "+str(nbyes)+", lb "+str(nlegbyes)+", w "+str(nwides)+" ,nb "+str(nnoball)+")"

#Replacing the short name of Bowler, Fielder and Batsmen to full names in the score card
Batsls=[]
for i in range(0,(len(SC_Bat))):
    Batsls.append(list(SC_Bat.iloc[i]))
Batsls1=Batsls[:]
for i in range(0,len(Batsls)):
     for string in pxit:
             x=Batsls[i][0]
             x=x.lower()
             x=x.split(" ")
             for t in x:
                 if(len(t)<2):
                     x.pop(x.index(t))
             if x[0] in string:
                Batsls[i][0]=pxi[pxit.index(string)]
tempext=[]
for i in range(0,len(Batsls)):
     temp=Batsls[i][1].split()
     temp=[i.strip() for i in temp]
     temp=[i.lower() for i in temp]
     #temp=[i.replace("c ","") for i in temp]
     if("" in temp):
         temp.remove("")
     if("Not Out" in temp):
         temp.remove("Not Out")
     for w in temp:
         tempext.append(w)
temp_fin=[]
for ij in tempext:
    if(len(ij)>=3 and (ij!='not' and ij!='out')):
        temp_fin.append(ij)
temp_fin=list(set(temp_fin))
for i in range(0,len(Batsls)):
       for y in temp_fin:
            x=Batsls[i][1]
            x=x.replace(" a "," ")
            x=x.lower()            
            if y in str(x):
                for w in pxit:
                    if y in w:
                       Batsls[i][1]=x.replace(y,pxi[pxit.index(w)])
for i in range(0,len(Batsls)):
    x=Batsls[i][1].split()
    for d in range(0,len(x)):
        if(len(x[d])>1):
            x[d]=x[d].capitalize()
    x=str(x)
    x=x.replace("[","")
    x=x.replace("]","")
    x=x.replace("'","")
    x=x.replace(",","")
    Batsls[i][1]=str(x)
    
#Finding those who did not Bat
Batted=[]
for i in range(0,len(Batsls)):
    Batted.append(Batsls[i][0])
Batted=set(Batted)
kxi=set(kxi)
didnotbat=list(kxi-Batted)

#Calculating Total Overs Batted
import math
overs=max(balls)
if(overs*10)%10==6:
    overs=math.ceil(overs)
bats_catchmiss=[]
for s in catchmiss:
    bats_catchmiss.append((s[0],s[1],s[2]))
    
#Finding the runs at which a batsmen was dropped, if dropped
try:
    bats_catchmiss=list(set(bats_catchmiss))
    bats_catchmis=[]
    for i in bats_catchmiss:
        runctm=0
        bat=[]
        a=df.loc[df['Batsmen'] == i[1]]    
        for l in range(0,len(a)):
            if float(a.iloc[l,0])<=float(i[0]):
              runctm=runctm+int(a.iloc[l,3])
        bat.append(i[0])
        bat.append(i[1])
        bat.append(i[2])
        bat.append(runctm)
        bats_catchmis.append(bat)
except:
    print()
    
from tabulate import tabulate #displaying in a table format
print("\n\nINNINGS SCORECARD \t\t\t\t\t\t\t"+str(ts)+"-"+str(nwicks)+"("+str(overs)+")")
print()
print("Batting:")
print()
print (tabulate(Batsls, headers=header, tablefmt='orgtbl'))
print()
print("\t\t\t\t\t\t\tTotal: "+str(ts)+"("+str(nwicks)+" wkts,"+str(overs)+" Ov)")
print()
print("FALL OF WICKETS:")
print()
q=[print(i) for i in Fall_wick]
print()
print("Extras:\t\t\t"+Extras)
print()
dnb=""
for i in didnotbat:
    dnb=dnb+i+", "
print("Did Not Bat: \t\t"+dnb)
Bowlls=[]
for i in bowls:
    a=df.loc[df['Bowler'] == i]
    #Bowler Overs Maidens Runs Wickets NB WD ECO
    bls=[]
    bls.append(i)
    over_ball=list(a['Ball Number'])
    over_ball1=list(set(over_ball))
    overs=int(len(over_ball1)/6)+float((len(over_ball1)-6*int(len(over_ball1)/6))/10)
    bls.append(overs)
    over_nos=[math.floor(x) for x in over_ball]
    onos=set(over_nos)
    nmaid=0
    ain=a[['Ball Number','Runs Scored of that ball','Extras']]
    ain=ain.applymap(int)
    for y in onos:
        ovt=ain.loc[ain['Ball Number']==y]
        if(sum(list(ovt['Runs Scored of that ball']))+sum(list(ovt['Extras'])))==0:
            nmaid+=1
    bls.append(nmaid)
    nruns=sum(list(a['Runs Scored of that ball']))
    nwicks=sum(list(a['Total Wickets']))
    nnoball=sum(list(a['NoBall']))
    nwides=sum(list(a['No of Wides']))
    ndts=sum(list(a['No of Dots']))
    nruns=nruns+nwides+nnoball
    eco=round(float(nruns/overs),2)
    bls.append(nruns)
    bls.append(nwicks)
    bls.append(nnoball)
    bls.append(nwides)
    bls.append(ndts)
    bls.append(eco)
    Bowlls.append(bls)
for i in range(0,len(Bowlls)):
     for string in pxit:
             x=Bowlls[i][0].split()
             x=[i.lower() for i in x]
             x=[i.strip() for i in x]
             for u in x:
                 if(len(u)<2):
                     x.pop(x.index(u))
             if x[0] in string:
                Bowlls[i][0]=pxi[pxit.index(string)]
head_bowl=['Bowler','O','M','R','W','NB','WD','Dots','ECO']
print()
print("Bowling:")
print()
print (tabulate(Bowlls, headers=head_bowl, tablefmt='orgtbl'))
print ()
fastblls=max(list(df['Ball Speed']))
fb=df.loc[df['Ball Speed']==fastblls]
if fastblls !=-1:
    print ("Fastest Ball of the Innings")
    print("Ball Number: "+str(fb.iloc[0,0])+"\tBowler: "+str(fb.iloc[0,1])+"\tBall Speed: "+str(fastblls))
ovmx=df[['Ball Number','Runs Scored of that ball','Extras','Team Score']]
ovmx=ovmx.applymap(int)
ovmx['Bowler']=df['Bowler']
ovcnt=list(range(0,20))
rncnt=[]
for y in ovcnt:
        ovt=ovmx.loc[ovmx['Ball Number']==y]
        truns=sum(list(ovt['Runs Scored of that ball']))+sum(list(ovt['Extras']))
        rncnt.append(truns)
max_run_over=max(sorted(zip(rncnt,ovcnt)))
mxr=ovmx.loc[ovmx['Ball Number']==max_run_over[1]]
print()
print("Over with Maximum Runs: ")
print("Over: "+str(max_run_over[1]+1)+", Runs Scored: "+str(max_run_over[0])+", Bowler: "+ mxr.iloc[0,4])
print()
print("Bowler with Maximum Dot Percentage:")
blname=[]
bldots=[]
blov=[]
for i in range(0,len(Bowlls)):
    blname.append(Bowlls[i][0])
    bldots.append(Bowlls[i][7])
    blov.append(Bowlls[i][1])
bdp=[round((x/(y*6))*100,2) for x,y in zip(bldots,blov)]
bdp_max=max(sorted(zip(bdp,blname)))
print("Bowler Name: "+str(bdp_max[1])+"\t"+" Dot Percentage: "+str(bdp_max[0]))
print()
print("Batsman with Maximum Boundary Percentage:")
btname=[]
bt4=[]
bt6=[]
btrun=[]
for i in range(0,len(Batsls)):
    if int(Batsls[i][2])!=0:
        btname.append(Batsls[i][0])
        bt4.append(Batsls[i][4])
        bt6.append(Batsls[i][5])
        btrun.append(Batsls[i][2])
bbp=[round((((x*4)+(y*6))/z)*100,2) for x,y,z in zip(bt4,bt6,btrun)]
bbp_max=max(sorted(zip(bbp,btname)))
print("Batsman Name: "+str(bbp_max[1])+"\t"+" Boundary Percentage: "+str(bbp_max[0]))
print()
if len(bats_catchmis)>0:
    print("Missed Catches:" )
for i in bats_catchmis:
    print("Ball Number: "+str(i[0])+", Batsman Dropped: "+str(i[1])+" ,Dropped by: "+str(i[2])+", Dropped on: "+str(i[3]))

#Plotting Run scoring Trend with respect to overs
import matplotlib.pyplot as plt
xwick=[]
yvalu=[]
for k in Fall_wick:
    hls=k.split(",")
    yval=hls[0]
    yval=yval[:yval.find("-")]
    yval=int(yval)
    xval=hls[1]
    xval=xval[:-1]
    xval=float(xval)
    xwick.append(xval)
    yvalu.append(yval)
    
import numpy as np
x=np.array(df['Ball Number'])
y=np.array(df['Team Score']) 
plt.plot(x,y,'-b')
plt.plot(xwick,yvalu,'or',label="wickets")    
plt.title('Run Progression')
plt.xlabel('Overs')
plt.ylabel('Runs')
plt.legend(loc='upper left')
plt.figlegend
plt.show()

#distribution of runs from bowler side
blnames=[]
blruns=[]
for i in range(0,len(Bowlls)):
    blnames.append(Bowlls[i][0])
    blruns.append(Bowlls[i][3])
blpie=[(x/sum(blruns))*360 for x in blruns]
slki=sorted(zip(blpie,blruns,blnames))
blpie,blruns,blnames=[i[0] for i in slki],[i[1] for i in slki],[i[2] for i in slki]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
exp=[] 
for i in range(0,len(blruns)):
    if(i==blruns.index(min(blruns))):
        exp.append(1)
    else:
        exp.append(0)
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','lightgreen','pink']
plt.pie(blpie, explode=exp, labels=blnames, autopct='%1.1f%%',colors=colors)
plt.title('Bowler Runs Provided Percentage')
plt.show()

#distribution of runs from batsman side
btnames=[]
btruns=[]
for i in range(0,len(Batsls1)):
    btnames.append(Batsls1[i][0])
    if(Batsls1[i][2])>0:
        btruns.append(Batsls1[i][2])
btpie=[(x/sum(btruns))*360 for x in btruns]
slk=sorted(zip(btpie,btruns,btnames))
btpie,btruns,btnames=[i[0] for i in slk],[i[1] for i in slk],[i[2] for i in slk]

exp=[] 
for i in range(0,len(btruns)):
    if(i==btruns.index(max(btruns))):
        exp.append(1)
    else:
        exp.append(0)
colors = ['gold', 'orange', 'lavender', 'lightskyblue','yellow','pink']
plt.pie(btpie, explode=exp, labels=btnames, autopct='%1.1f%%',colors=colors)
plt.title('Batsmen Runs Scored Percentage')
plt.show()