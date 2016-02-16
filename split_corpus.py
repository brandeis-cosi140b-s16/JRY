# split corpus into subcorpus
# take only medium
# percentage per prompt
# equal numbers of L1s

# requires original corpus in toefl11 folder and will output smaller corpus into toefl11_part

import csv

p1 = [] #broad knowledge or specialization
p2 = [] #young people enjoy life more than older
p3 = [] #young people don't give enough time to helping communities
p4 = [] #ads make products seem better than they really are
p5 = [] #fewer cars in 20 years than today
p6 = [] #best way to travel is with tour guide
p7 = [] #more important for students to understand ideas and concepts than it is for them to learn facts
p8 = [] #successful people try new things and take risks

with open ('toefl11/data/text/index.csv') as csvfile:
    iterator = csv.reader(csvfile,delimiter=',')
    iterator.__next__() #skip the header row
    for row in iterator:
        if row[3] == 'medium':
            if row[1] == 'P1':
                p1.append(row)
            elif row[1] == 'P2':
                p2.append(row)
            elif row[1] == 'P3':
                p3.append(row)
            elif row[1] == 'P4':
                p4.append(row)
            elif row[1] == 'P5':
                p5.append(row)
            elif row[1] == 'P6':
                p6.append(row)
            elif row[1] == 'P7':
                p7.append(row)
            elif row[1] == 'P8':
                p8.append(row)

print('Prompt 1: {0}\tPrompt 2: {1}\tPrompt 3: {2}\tPrompt 4: {3}'.format(len(p1), len(p2),len(p3),len(p4)) )
print('Prompt 5: {0}\tPrompt 6: {1}\tPrompt 7: {2}\tPrompt 8: {3}\n'.format(len(p5), len(p6),len(p7),len(p8)) )

# get L1
all = [p1,p2,p3,p4,p5,p6,p7,p8]
for i in range (1,9):
    by_lang = {
        'KOR':0,
        'DEU':0,
        'TUR':0,
        'ZHO':0,
        'TEL':0,
        'ARA':0,
        'SPA':0,
        'HIN':0,
        'JPN':0,
        'FRA':0,
        'ITA':0}
    print ('Prompt {0}: {1}\n----------'.format(i,len(all[i-1])))
    medium_prompt = all[i-1]
    for entry in medium_prompt:
        if entry[2] == 'KOR':
            by_lang['KOR'] += 1
        elif entry[2] == 'DEU':
            by_lang['DEU'] += 1
        elif entry[2] == 'TUR':
            by_lang['TUR'] += 1
        elif entry[2] == 'ZHO':
            by_lang['ZHO'] += 1
        elif entry[2] == 'TEL':
            by_lang['TEL'] += 1
        elif entry[2] == 'ARA':
            by_lang['ARA'] += 1
        elif entry[2] == 'SPA':
            by_lang['SPA'] += 1
        elif entry[2] == 'HIN':
            by_lang['HIN'] += 1
        elif entry[2] == 'JPN':
            by_lang['JPN'] += 1
        elif entry[2] == 'FRA':
            by_lang['FRA'] += 1
        elif entry[2] == 'ITA':
            by_lang['ITA'] += 1
    
    print('KOR: {0:<10}DEU: {1:<10}TUR: {2:<10}ZHO: {3}'.format(by_lang['KOR'],by_lang['DEU'],by_lang['TUR'],by_lang['ZHO']))
    print('TEL: {0:<10}ARA: {1:<10}SPA: {2:<10}'.format(by_lang['TEL'],by_lang['ARA'],by_lang['SPA']))
    print('HIN: {0:<10}JPN: {1:<10}FRA: {2:<10}ITA:{3}'.format(by_lang['HIN'],by_lang['JPN'],by_lang['FRA'],by_lang['ITA']))