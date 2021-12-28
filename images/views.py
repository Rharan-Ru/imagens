import re
import requests
import os
import zipfile
from urllib.request import urlopen
from urllib.error import HTTPError

from django.shortcuts import render
from django.views import View

from bs4 import BeautifulSoup


def get_all_images(url):
    """
    Utilty function used to get a Beautiful Soup object from a given URL
    """
    list_images = []
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    try:
        req = session.get(url, headers=headers)
    except requests.exceptions.RequestException:
        return None
    try:
        bs = BeautifulSoup(req.text, 'html.parser')
        images = bs.findAll('img', {'src': re.compile('(jpg|png|gif|svg|ico)$')})
        for img in images:
            list_images.append(img['src'])
    except AttributeError as error:
        print('Erro de atributo')
        return None
    return list_images


class ImagemView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'images/home.html')

    def post(self, request, *args, **kwargs):
        url = request.POST['site']
        image_list = get_all_images(url)

        lista_imagens_names = []

        for i in image_list:
            filename = i.split('/')[-1]
            save_path = os.path.abspath("media/all_images")
            complete = os.path.join(save_path, filename)
            try:
                r = requests.get(i, allow_redirects=False)
            except Exception as erro:
                print(erro)
                continue

            try:
                print(filename)
                open(complete, 'wb').write(r.content)
            except Exception as erro:
                print(erro)

            if complete not in lista_imagens_names:
                lista_imagens_names.append(complete)

        with zipfile.ZipFile(f'{os.path.abspath("media/all_images")}/all_images.zip', 'w') as zipF:
            for file in lista_imagens_names:
                try:
                    zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
                except Exception as erro:
                    print(erro)
                    continue
            zipF.close()

        msg = f'{len(lista_imagens_names)} Imagens encontradas em {url}'
        imagens_total = zip(image_list, lista_imagens_names)
        context = {
            'img_total': imagens_total,
            'tudo': '/media/all_images/all_images.zip',
            'msg': msg,
            'site_status': url,
        }
        return render(request, 'images/home.html', context)
