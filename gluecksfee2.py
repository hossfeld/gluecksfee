# -*- coding: utf-8 -*-
"""
SeKo Gluecksfee zur Seminarteilnehmer Auslosung

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  randomly initialize the random number generator with
                        that seed
  -i INPUT, --input INPUT
                        Name des Excel-Files zur Eingabe
  -o OUTPUT, --output OUTPUT
                        Die Ausgabe wird im angebenen Excel File gespeichert.
                        Default: output.xlsx
  -m MAXIMUM, --maximum MAXIMUM
                        Die maximale Anzahl von Seminaren, die pro Person
                        zugewiesen wird. Default: 999
  -v [VERBOSE], --verbose [VERBOSE]
                        Gibt eine ausführliche Ausgabe auf der Konsole aus
                        (True or False). Default: True

Created on Sat Nov 6 14:52:22 2021

@author: Tobias Hoßfeld

"""

import argparse
from datetime import datetime
import hashlib
import numpy as np
import os.path 

from pandas import read_excel, DataFrame, ExcelWriter

#%% Parse Input Arguments
now = datetime.now()

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
        
        

parser = argparse.ArgumentParser(description="SeKo Gluecksfee zur Seminarteilnehmer Auslosung")
parser.add_argument("-s", "--seed", 
                    help="randomly initialize the random number generator with that seed",
                    default=now.strftime("%m/%d/%Y, %H:%M:%S"))
parser.add_argument("-i", "--input", 
                    help="Name des Excel-Files zur Eingabe",
                    default="input.xlsx")
parser.add_argument("-o", "--output", 
                    help="Die Ausgabe wird im angebenen Excel File gespeichert. Default: output.xlsx",
                    default="output.xlsx")
parser.add_argument("-m", "--maximum", 
                    help="Die maximale Anzahl von Seminaren, die pro Person zugewiesen wird. Default: 999",
                    default=999)

parser.add_argument("-v", "--verbose",  type=str2bool, nargs='?',
                        const=True, default=False,
                    help="Gibt eine ausführliche Ausgabe auf der Konsole aus (True or False). Default: True")

args = parser.parse_args()

print("Die SeKo Gluecksfee schwingt ihren Zauberstaub...\n")
print(f'Seed für Zufallszahlen: "{args.seed}"')
print(f'Eingabe-Datei: {args.input}')
print(f'Ausgabe-Datei: {args.output}')
print(f'Maximale #Seminare: {args.maximum}')
print(f'Verbose: {args.verbose}\n')

#%% Read Input File
if not os.path.isfile(args.input):
    raise FileNotFoundError(args.input)    

WS = read_excel(args.input, sheet_name='registrierung')
x = np.array(WS)

#%% Initialize Random Generator
hash = hashlib.sha256(args.seed.encode('utf-8'))
seed = np.sum(np.frombuffer(hash.digest(), dtype='uint32'))
if args.verbose:
    print(f'Random Number Generation initialisiert mit {seed}')
#rng = np.random.RandomState(seed)
#%% Check if number of Plaetze is provided in the input file
def checkPlaetze(v):
    if isinstance(v, int):
        return v==-99
    else:
        return v.lower() in ['platz','plaetze','plätze']

try:
    tmp = next(i for i,v in enumerate(x[:,0]) if checkPlaetze(v))
    numParticipantsPerSeminar = x[tmp,1:]
    x = np.delete(x, tmp, axis=0)
except StopIteration:
    numParticipantsPerSeminar = [14]*(x.shape[1]-1)

#%% Assignment of people to requested seminars: there are several more options implemented, but we are using here the default values only
# x[user_id, seminar_id]
def assignmentMatrix(matrix, whichOrder=3, weightAssignedPlaces=1, rel=False, numParticipantsPerSeminar=numParticipantsPerSeminar, maxSeminarsAssignedPerParticipant=int(args.maximum), seed=seed, verbose=args.verbose):
    x = matrix[:,1:].astype('int')
    userid = matrix[:,0]
    
    np.random.seed(seed)
    y = np.zeros_like(x) 
    n, numSeminars = y.shape
    
    if whichOrder==3: # smallest seminars first, but relative
        I = np.argsort(x.sum(axis=0)/numParticipantsPerSeminar) 
    elif whichOrder==1: # smallest seminars first
        I = np.argsort(x.sum(axis=0)) 
    elif whichOrder==2: # largest seminars first
        I = np.argsort(x.sum(axis=0))[::-1]
    else: # order of seminars
        I = range(numSeminars)
        
    if verbose:
        print(f'Seminarreihenfolge: {I}')
        
    for i in I: 
        registeredUsers = np.squeeze(np.argwhere(x[:,i]>0))
        
        #print(maxSeminarsAssignedPerParticipant)
        alreadyMaximumAssignedSeminars = np.squeeze(np.argwhere(y.sum(axis=1) >= maxSeminarsAssignedPerParticipant ))
        registeredUsers = np.setdiff1d(registeredUsers, alreadyMaximumAssignedSeminars)
        
        if len(registeredUsers) <= numParticipantsPerSeminar[i]:
            y[registeredUsers,i] = 1
            if verbose:
                    print(f'seminar {i} ({numParticipantsPerSeminar[i]} places): registrations {len(registeredUsers)}')
                    print(f'   registered users: {registeredUsers}')
                    print('   Wahrscheinlichkeit: alle TN zugewiesen')
        else:
            if weightAssignedPlaces==1:
                curMax = np.max(y[registeredUsers,:].sum(axis=1))
                if rel:
                    p = (1-y[registeredUsers,:].sum(axis=1)/x[registeredUsers,:].sum(axis=1))
                else:
                    p = (curMax+0.1-y[registeredUsers,:].sum(axis=1))                    
                p = p/p.sum()
                                
                select = np.random.choice(registeredUsers, replace=False, size=numParticipantsPerSeminar[i], p=p)
            else:
                p = np.ones(len(registeredUsers))
                p = p/p.sum()
                select = np.random.choice(registeredUsers, replace=False, size=numParticipantsPerSeminar[i])
            if verbose:                
                print(f'seminar {i} ({numParticipantsPerSeminar[i]} places): registrations {len(registeredUsers)}')
                print(f'    registered users: {registeredUsers}')
                for (theuser,theass,thereq,theprob) in zip(registeredUsers, y[registeredUsers,:], x[registeredUsers,:],p):
                    print(f'    user {theuser} has {theass.sum()} seminars assigned: {np.squeeze(np.argwhere(theass))} and requested {np.squeeze(np.argwhere(thereq))}; prob. for next seminar {theprob*100:.2f}%')
                print(f'    Zugewiesene Teilnehmer for seminar {i}: ({len(select)}) people = {np.sort(select)}')
            y[select,i] = 1
    return y, userid


#%% Let's do the assignment and extract the seminar names
y, userid = assignmentMatrix(x)
seminarNames = WS.columns[1:]
#%% Generate the data for the output file: seminar view
if args.verbose: print('\n')
for i in range(len(userid)):    
    tmp = np.squeeze(np.argwhere(y[i,:]>0))
    if tmp.size==1:
        s=seminarNames[tmp]
    elif tmp.size>1:
        s = np.array2string(seminarNames[tmp], separator=', ')
    else:
        s = "-- keine --"
    if args.verbose: print(f'Teilnehmer {userid[i]} in Seminaren: {s}')
    
#%% Generate the data for the output file: participant/user view
if args.verbose: print('\n')
for i in range(y.shape[1]):
    tmp = np.squeeze(np.argwhere(y[:,i]>0))
    if tmp.size==1:
        s=userid[tmp]
    elif tmp.size>1:
        s = np.array2string(userid[tmp], separator=', ')
    else:
        s = "-- keine --"
    if args.verbose: print(f'Seminar {WS.columns[i+1]} mit {len(tmp)} Teilnehmern bei {np.sum(x[1:,i+1])} Registrierungen (max. {numParticipantsPerSeminar[i]}): {s}')
    
#%% Store the data in a lista
seminar = []
for i in range(len(seminarNames)):
    tmp = np.squeeze(np.argwhere(y[:,i]>0))
    seminar.append(userid[tmp])
    
n = len(userid)
k = len(seminarNames)
endLetter = chr(ord('A')+k+1)

#%% Generate proper Pandas data frame to write the information into excel
df = DataFrame(seminar, index=seminarNames, columns=np.arange(1,y.sum(axis=0).max()+1))    
df.insert(0,'Plaetze',numParticipantsPerSeminar)
df.insert(1,'Teilnehmer',y.sum(axis=0))

anfragen = x[:,1:].astype('int').sum(axis=0)
df.insert(2,'Anfragen', anfragen)
df.insert(3,'Zugewiesen', y.sum(axis=0)/anfragen)
#%% Output the data to Excel sheets: Seminar sheet and Assignment sheet
writer = ExcelWriter(args.output, engine='xlsxwriter')

red_format = writer.book.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

green_format = writer.book.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})



df.to_excel(writer,sheet_name='Seminar', index=True, index_label='Seminar')

df = DataFrame(y, index=userid,  columns=seminarNames)
df.to_excel(writer,sheet_name='Assignment', index=True, index_label='Person')

#%% Output the data to Excel sheets: Difference sheet
z = 2*y-x[:,1:]
df = DataFrame(z, index=userid, columns=seminarNames)
df.to_excel(writer,sheet_name='Difference', index=True, index_label='Person')

#%% Output the data to Excel sheets: Stats_Person sheet
v = x[:,1:].sum(axis=1).astype('int')
z = np.stack((v, y.sum(axis=1), y.sum(axis=1)/v ) )
df = DataFrame(z.T, index=userid, columns=['requested','assigned', 'ratio'])
df.to_excel(writer,sheet_name='Stats_Person', index=True, index_label='Person')

#%% Output the data to Excel sheets: Parameters sheet
z = [f'Seed für Zufallszahlen: "{args.seed}"', f'Eingabe-Datei: {args.input}', 
     f'Ausgabe-Datei: {args.output}', f'Maximale #Seminare: {args.maximum}', f'Verbose: {args.verbose}'
    ]
df = DataFrame(z, columns=['Parameter'])
df.to_excel(writer,sheet_name='Parameters', index=False)

#%% Let's make the excel sheet nicer with some conditional formatting
writer.sheets['Assignment'].conditional_format(f'A1:{endLetter}{n+2}', {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    1,
                                    'format':   green_format})

writer.sheets['Difference'].conditional_format(f'A1:{endLetter}{n+2}', {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    -1,
                                    'format':   red_format})
writer.sheets['Difference'].conditional_format(f'A1:{endLetter}{n+2}', {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    +1,
                                    'format':   green_format})


writer.sheets['Stats_Person'].conditional_format(f'D1:D{n+2}', {'type': '3_color_scale',
                                         'min_color': "#FF0000",
                                         'mid_color': "#FFFF00",
                                         'max_color': "#00FF00"})

writer.sheets['Stats_Person'].conditional_format(f'C1:C{n+2}', {'type': '3_color_scale',
                                         'min_color': "#FF0000",
                                         'mid_color': "#FFFF00",
                                         'max_color': "#00FF00"})

format_percent = writer.book.add_format({'num_format': '0.0%'})
writer.sheets['Stats_Person'].set_column('D:D', 10, format_percent)


writer.sheets['Seminar'].set_column('B:B', 10)
writer.sheets['Seminar'].set_column('C:C', 12)
writer.sheets['Seminar'].set_column('E:E', 15, format_percent)
#%% save the output and write it to the file
writer.save()
    

