import csv, shutil

def write_split_to_csv(csvfilename,filelist):
    f = 'annotate/'+csvfilename+'.csv'
    with open(f,'w',newline='') as csvfile:
        iterator = csv.writer(csvfile,delimiter=',')
        for item in filelist:
            iterator.writerow(item)

def copy_file_to_setdir(csvfilename):
    f = 'annotate/'+csvfilename+'.csv'
    with open(f) as csvfile:
        iterator = csv.reader(csvfile,delimiter=',')
        for item in iterator:
            shutil.copyfile('toefl11_part/preprocessed_train/'+csvfilename.upper()+'_annotation/'+item[0]+'.xml','annotate/'+csvfilename+'/'+item[0]+'.xml')
			
if __name__ == '__main__':
	p1 = [] #broad knowledge or specialization
	p2 = [] #young people enjoy life more than older
	p3 = [] #young people don't give enough time to helping communities
	p4 = [] #ads make products seem better than they really are
	p5 = [] #fewer cars in 20 years than today
	p6 = [] #best way to travel is with tour guide
	p7 = [] #more important for students to understand ideas and concepts than it is for them to learn facts
	p8 = [] #successful people try new things and take risks
	
	with open('toefl11_part/train.csv') as csvfile:
		iterator = csv.reader(csvfile,delimiter=',')
		for row in iterator:
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
				
	all = [p1,p2,p3,p4,p5,p6,p7,p8]
	
	ara = []
	deu = []
	fra = []
	hin = []
	ita = []
	jpn = []
	kor = []
	spa = []
	tel = []
	tur = []
	zho = []
	
	prompts_per_lang = [0,0,0,0,0,0,0,0,0,0,0]
	
	n = 2
	
	for prompt in all:
		for entry in prompt:
			if entry[2] == 'KOR' and prompts_per_lang[6] < n:
				kor.append(entry)
				prompts_per_lang[6] += 1
			elif entry[2] == 'DEU' and prompts_per_lang[1] < n:
				deu.append(entry)
				prompts_per_lang[1] += 1
			elif entry[2] == 'TUR' and prompts_per_lang[9] < n:
				tur.append(entry)
				prompts_per_lang[9] += 1
			elif entry[2] == 'ZHO' and prompts_per_lang[10] < n:
				zho.append(entry)
				prompts_per_lang[10] += 1
			elif entry[2] == 'TEL' and prompts_per_lang[8] < n:
				tel.append(entry)
				prompts_per_lang[8] += 1
			elif entry[2] == 'ARA' and prompts_per_lang[0] < n:
				ara.append(entry)
				prompts_per_lang[0] += 1
			elif entry[2] == 'SPA' and prompts_per_lang[7] < n:
				spa.append(entry)
				prompts_per_lang[7] += 1
			elif entry[2] == 'HIN' and prompts_per_lang[3] < n:
				hin.append(entry)
				prompts_per_lang[3] += 1
			elif entry[2] == 'JPN' and prompts_per_lang[5] < n:
				jpn.append(entry)
				prompts_per_lang[5] +=1
			elif entry[2] == 'FRA' and prompts_per_lang[2] < n:
				fra.append(entry)
				prompts_per_lang[2] += 1
			elif entry[2] == 'ITA' and prompts_per_lang[4] < n:
				ita.append(entry)
				prompts_per_lang[4] += 1
				
		prompts_per_lang = [0,0,0,0,0,0,0,0,0,0,0]

	write_split_to_csv('ara',ara)
	write_split_to_csv('fra',fra)
	write_split_to_csv('hin',hin)
	write_split_to_csv('spa',spa)
	write_split_to_csv('tel',tel)
	write_split_to_csv('zho',zho)
	
	langs = ['ara','fra','hin','spa','tel','zho']
	for lang in langs:
		copy_file_to_setdir(lang)