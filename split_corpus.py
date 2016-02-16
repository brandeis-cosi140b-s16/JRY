# first move the unzipped toefl11 directory into the top level
# then create a toefl11_part directory with train/, dev/, and test/ subdirectories
# .gitignore takes care of the rest


import csv
import shutil

def write_split_to_csv(csvfilename,filelist):
    f = 'toefl11_part/'+csvfilename+'.csv'
    with open(f,'w',newline='') as csvfile:
        iterator = csv.writer(csvfile,delimiter=',')
        for item in filelist:
            iterator.writerow(item)

def copy_file_to_setdir(csvfilename):
    f = 'toefl11_part/'+csvfilename+'.csv'
    with open(f) as csvfile:
        iterator = csv.reader(csvfile,delimiter=',')
        for item in iterator:
            shutil.copyfile('toefl11/data/text/responses/tokenized/'+item[0],'toefl11_part/'+csvfilename+'/'+item[0])

if __name__ == '__main__':
    p1 = [] #broad knowledge or specialization
    p2 = [] #young people enjoy life more than older
    p3 = [] #young people don't give enough time to helping communities
    p4 = [] #ads make products seem better than they really are
    p5 = [] #fewer cars in 20 years than today
    p6 = [] #best way to travel is with tour guide
    p7 = [] #more important for students to understand ideas and concepts than it is for them to learn facts
    p8 = [] #successful people try new things and take risks
    all_med = []

    with open ('toefl11/data/text/index.csv') as csvfile:
        iterator = csv.reader(csvfile,delimiter=',')
        iterator.__next__() #skip the header row
        for row in iterator:
            if row[3] == 'medium':
                all_med.append(row)
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

    total_medium = len(all_med)

    print('Prompt 1: {0}\tPrompt 2: {1}\tPrompt 3: {2}\tPrompt 4: {3}'.format(len(p1), len(p2),len(p3),len(p4)) )
    print('Prompt 5: {0}\tPrompt 6: {1}\tPrompt 7: {2}\tPrompt 8: {3}\n'.format(len(p5), len(p6),len(p7),len(p8)) )
    print('Total: {0}'.format(total_medium))

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
        print ('Prompt {0}: {1}\n---------------'.format(i,len(all[i-1])))
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
        print('HIN: {0:<10}JPN: {1:<10}FRA: {2:<10}ITA:{3}\n'.format(by_lang['HIN'],by_lang['JPN'],by_lang['FRA'],by_lang['ITA']))
    
    # split the medium part of the corpus into train/dev/test (82/9/9)
    train = []
    dev = []
    test = []
    for i in range(0,total_medium):
        if len(dev) < total_medium*.09:
            if i % 3 == 0:
                test.append(all_med[i])
            elif i % 3 == 1:
                dev.append(all_med[i])
            else:
                train.append(all_med[i])
        else:
            train.append(all_med[i])
            
    print('Train: {0}\tDev: {1}\tTest: {2}'.format(len(train),len(dev),len(test)))

    # write split to csv
    write_split_to_csv('index',all_med)
    write_split_to_csv('train',train)
    write_split_to_csv('dev',dev)
    write_split_to_csv('test',test)
            
    # do the actual file moving
    copy_file_to_setdir('train')
    copy_file_to_setdir('dev')
    copy_file_to_setdir('test')