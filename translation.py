from bs4 import BeautifulSoup
from googletrans import Translator
import time

translator=Translator()

origin_file = "t1_ru.ts"
trans_lang = 'ru'

with open(origin_file, 'r') as f:
    data=f.read()


Bs_data = BeautifulSoup(data, "lxml")

source_bs = str(Bs_data.find_all('source'))

source_bs = source_bs.replace("[", "")
source_bs = source_bs.replace("<source>", "")
source_bs = source_bs.replace("</source>, ", "\n###\n")
source_bs = source_bs.replace("</source>]", "")
source_bs = source_bs.replace("<source/>", "\n###\n")

source_list = source_bs.split("\n###\n")

#print(Bs_data)

#---------------------------------------------------------

translation_bs = str(Bs_data.find_all('translation'))
translation_bs = translation_bs.replace("[", "")
translation_bs = translation_bs.replace("<translation type=\"unfinished\">", "")
translation_bs = translation_bs.replace("<translation type=\"vanished\">", "")
translation_bs = translation_bs.replace("<translation type=\"obsolete\">", "")
translation_bs = translation_bs.replace("</translation>, ", "\n###\n")
translation_bs = translation_bs.replace("</translation>]", "")
translation_bs = translation_bs.replace("<translation>", "")

translation_list = translation_bs.split("\n###\n")





zipped_translation = list(list(x) for x in zip(source_list, translation_list))


transNo=0

for i in zipped_translation:
    transNo += 1
    print('\r' + str(round(100*transNo/len(zipped_translation), 2)) + "%", end="")

    if len(i[1]) < 2:
        try:
            i[1] = translator.translate(i[0], src='en', dest=trans_lang).text
        except:
            print("Something is no yes with " + (i[0]))
            time.sleep(3)

print("\n")

for i in zipped_translation:
    print(i)


with open('translation.txt', 'w+') as f:
    for trans in zipped_translation:
            f.write(trans[0] + " ### " + trans[1])


translation_no=0
with open(origin_file, 'r') as f1:
    with open(origin_file +'2', 'w+') as f2:
        for line1 in f1:
            if "</tr" in line1:
                if "></tr" in line1:
                    tempLine=line1
                    tempLine=tempLine.replace("></tr", ">"+zipped_translation[translation_no][1]+"</tr")
                    f2.write(tempLine)
                else:
                    f2.write(line1)
                translation_no += 1
            else:
                f2.write(line1)



