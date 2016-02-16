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
print('Prompt 5: {0}\tPrompt 6: {1}\tPrompt 7: {2}\tPrompt 8: {3}'.format(len(p5), len(p6),len(p7),len(p8)) )