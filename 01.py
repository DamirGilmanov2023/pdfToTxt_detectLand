import pytesseract
from langdetect import detect,detect_langs
from pdf2image import convert_from_path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

iso_1=['af','am','ar','as','az','be','bn','bo','bs','bg','ca','cs','cy','da','de','dz','el','en','et','eu','fa','fi','fr','ga','gl','gu','he','hi','hr','hu','iu','id','is','it','jv','ja','kn','ka','kk','km','ky','ko','ku','lo','lv','lt','ml','mk','mt','ms','my','ne','nl','no','or','pa','pl','pt','ps','ro','ru','sa','si','sk','sl','es','sq','sr','sw','sv','ta','te','tg','tl','th','ti','tr','ug','uk','ur','uz','vi','yi']
iso_2=['afr','amh','ara','asm','aze','bel','ben','bod','bos','bul','cat','ces','cym','dan','deu','dzo','ell','eng','est','eus','fas','fin','fra','gle','glg','guj','heb','hin','hrv','hun','iku','ind','isl','ita','jav','jpn','kan','kat','kaz','khm','kir','kor','kur','lao','lav','lit','mal','mkd','mlt','msa','mya','nep','nld','nor','ori','pan','pol','por','pus','ron','rus','san','sin','slk','slv','spa','sqi','srp','swa','swe','tam','tel','tgk','tgl','tha','tir','tur','uig','ukr','urd','uzb','vie','yid']
i=1
while i<=10:
    print(f'Открытие файла {i}.pdf')
    images = convert_from_path(f'{i}.pdf', 500, poppler_path=r'poppler-0.68.0\bin')
    j=1
    for image in images:
        print(f'Проверка {i}.pdf/{j} страница')
        text = pytesseract.image_to_string(image, lang='eng+rus')#+aze+bel+ben+bos+bul+ceb+ces+dan+deu+est+fin+fra+hrv+hun+ita+jpn+kat+kor+lav+lit+nld+nor+pol+ron+slk+slv+spa+sqi+swe+tur+ukr')
        print(f'Определение языка {j} страницы')
        #det=''

        det = detect_langs(text)
        dett=detect(text)
        print(det)
        if len(det)>1:
            d1=det[0]
            d1=str(d1).split(':')
            det1=d1[0]
            d2=det[1]
            d2=str(d2).split(':')
            det2=d2[0]
            langs_col=2
        else:
            d1 = det[0]
            d1 = str(d1).split(':')
            det1 = d1[0]
            langs_col=1

        if langs_col==1:
            i_iso = 0
            for iso in iso_1:
                if iso==str(det1):
                    lang=iso_2[i_iso]
                    break
                i_iso+=1
            print(f'Язык страницы - {lang}')
            print(f'Перевод страницы в текст')
            try:
                if lang!='eng':
                    text=pytesseract.image_to_string(image, lang=f'{lang}+eng')
                else:
                    text = pytesseract.image_to_string(image, lang=f'{lang}')
            except:
                print("Ошибка")
                continue

            print(f'Запись в файл - {i}_pdf-{j}_лист({lang}).txt')
            w = open(f'{i}_pdf-{j}_лист({lang}).txt', 'w', encoding="utf-8")
            w.write(text)
            w.close()
            print('')
        else:
            i_iso = 0
            for iso in iso_1:
                if iso == str(det1):
                    lang1 = iso_2[i_iso]
                    break
                i_iso += 1
            i_iso = 0
            for iso in iso_1:
                if iso == str(det2):
                    lang2 = iso_2[i_iso]
                    break
                i_iso += 1
            print(f'Язык страницы - {lang1}\{lang2}')
            print(f'Перевод страницы в текст')
            try:
                text = pytesseract.image_to_string(image, lang=f'{lang1}+{lang2}')
            except:
                print("Ошибка")
                continue

            print(f'Запись в файл - {i}_pdf-{j}_лист({lang1}|{lang2}).txt')
            w = open(f'{i}_pdf-{j}_лист({lang1}-{lang2}).txt', 'w', encoding="utf-8")
            w.write(text)
            w.close()
            print('')
        j+=1
    print('----------------------------------------')
    i+=1
