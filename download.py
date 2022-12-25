import requests
import csv 
import threading
import os
reader = csv.DictReader(open('back testing data - All.csv'))
pdflist = []
pagelist = []
for row in reader:
    for k,v in row.items():
        if 'pdf' in v:
            if v not in pdflist:
                pdflist.append(v)
        else: 
            if v.startswith('http') and v not in pagelist:
                pagelist.append(v)
        
        
with open('pdflist.txt','w') as f:
    f.write('\n'.join(pdflist))
with open('pagelist.txt','w') as f:
    f.write('\n'.join(pagelist))
threads = []
failed_list = []

def download(url):
    filename = 'pdfs/'+url.split('/')[-1].replace('?force_download=true','')
    if os.path.exists(filename):
        print(f'{filename} already exists')
        return
    print(f'downloading {url}')
    try:
     r = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'})
     if r.status_code == 200 and r.headers.get('content-type').startswith('application/pdf'):
        with open(filename,'wb') as f:
            f.write(r.content)
     else:
        failed_list.append(url)
    except:
        failed_list.append(url)

for each in pdflist:
    download(each)
with open('failed.txt','w') as f:
    f.write('\n'.join(failed_list))