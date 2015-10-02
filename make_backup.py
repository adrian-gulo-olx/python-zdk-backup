import os
import datetime
import csv
import requests

session = requests.Session()

hcenters = ['https://olxar.zendesk.com/', 'https://olxuy.zendesk.com/', 'https://olxec.zendesk.com/', 'https://olxve.zendesk.com/', 'https://olxpe.zendesk.com/', 'https://olxsv.zendesk.com/', 'https://olxgt.zendesk.com/', 'https://olxco.zendesk.com/', 'https://olxhn.zendesk.com/', 'https://olxcr.zendesk.com/', 'https://olxpa.zendesk.com/', 'https://olxbo.zendesk.com/', 'https://olxpy.zendesk.com/', 'https://olxke.zendesk.com/', 'https://olxug.zendesk.com/', 'https://olxtz.zendesk.com/', 'https://olxgh.zendesk.com/', 'https://olxng.zendesk.com/', 'https://olxpt.zendesk.com/', 'https://slando.zendesk.com/', 'https://dubizzle-bh.zendesk.com/', 'https://dubizzle-eg.zendesk.com/', 'https://dubizzle-jo.zendesk.com/', 'https://dubizzle-kw.zendesk.com/', 'https://dubizzle-lb.zendesk.com/', 'https://dubizzle-om.zendesk.com/', 'https://dubizzle-qa.zendesk.com/', 'https://dubizzle-sa.zendesk.com/', 'https://dubizzle-tn.zendesk.com/', 'https://dubizzle.zendesk.com/', 'https://olxro.zendesk.com/', 'https://olxsa.zendesk.com/', 'https://olxid.zendesk.com/', 'https://olxph.zendesk.com/', 'https://olxpk.zendesk.com/', 'https://autovit.zendesk.com/', 'https://otodom.zendesk.com/', 'https://otomoto.zendesk.com/', 'https://olxin.zendesk.com/'] 
# helpcenters not active
# 'https://olxsn.zendesk.com/', 'https://olxcm.zendesk.com/', 'https://olxao.zendesk.com/', 'https://olxmz.zendesk.com/', 'https://olxby1.zendesk.com/', 'https://olxkz1.zendesk.com/', 'https://dubizzle-dz.zendesk.com/', 'https://olxbg.zendesk.com/', 'https://olxuz.zendesk.com/', 


date = datetime.date.today()
log = []

for hc in hcenters:
    folder = hc.replace(hc[:8], '')
    backup_path = os.path.join(str(date), folder)
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    endpoint = hc + '/api/v2/help_center/articles.json?per_page=100'
    response = session.get(endpoint)
    if response.status_code != 200:
        print('Failed to retrieve articles with error {}'.format(response.status_code))
        exit()
    data = response.json()
    for article in data['articles']:
        title = '<h1>' + article['title'] + '</h1>'
        longFilename = '{name}'.format(name=article['name']) + '.html'
        filename = longFilename.replace("/"," ")
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            f.write(title + '\n' + article['body'])
        print('{title} copied!'.format(title=article['title']))

        log.append((filename, article['title'], article['author_id'], article['section_id']))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('File', 'Title', 'Author ID', 'Section ID'))
    for article in log:
        writer.writerow(article)
