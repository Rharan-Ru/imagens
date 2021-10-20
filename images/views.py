from django.shortcuts import render, redirect
from django.views import View
from .models import ImagensModel
from bs4 import BeautifulSoup
import requests
import os
from django.conf import settings
import json
import zipfile


class ImagemView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'images/home.html')

    def post(self, request, *args, **kwargs):
        rota = request.POST['site']

        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/93.0.4577.63 Mobile Safari/537.36 Edg/93.0.961.38'}

        page = requests.get(rota, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.findAll('img')

        lista_imagens = []
        lista_imagens_names = []

        for i in images:
            data = ''
            url = ''
            if i:
                if 'http' in str(i.get('src')):
                    data = 'src'
                    url = str(i.get(data))
                elif 'http' in str(i.get('data-path')):
                    data = 'data-path'
                    url = str(i.get(data))
                elif 'http' in str(i.get('data-cfsrc')):
                    data = 'data-cfsrc'
                    url = str(i.get(data))
                elif 'http' in str(i.get('data-origin')):
                    data = 'data-origin'
                    url = str(i.get(data))
                else:
                    try:
                        data = 'src'
                        url = 'http:' + str(i.get(data))
                    except Exception:
                        continue
                if str(i.get(data)) not in lista_imagens:
                    lista_imagens.append(i.get(data))

                filename = url.split('/')[-1]
                try:
                    r = requests.get(url, allow_redirects=True)
                except Exception as erro:
                    print(erro)
                    continue
                save_path = os.path.abspath("media/all_images")
                complete = os.path.join(save_path, filename)
                num_jpg = complete.find('jpg')
                num_png = complete.find('png')
                num_gif = complete.find('gif')
                num_svg = complete.find('svg')
                complete_all = ''
                if num_png != -1:
                    complete_all = complete[0: num_png + 3]
                elif num_jpg != -1:
                    complete_all = complete[0: num_jpg + 3]
                elif num_gif != -1:
                    complete_all = complete[0: num_gif + 3]
                elif num_svg != -1:
                    complete_all = complete[0: num_svg + 3]
                else:
                    continue
                try:
                    open(complete_all, 'wb').write(r.content)
                except Exception as erro:
                    print(erro)

                if f'/media/all_images/{filename}' not in lista_imagens_names:
                    lista_imagens_names.append(f'/media/all_images/{filename}')

        try:
            with zipfile.ZipFile(f'{os.path.abspath("media/all_images")}/all_images.zip', 'w') as zipF:
                for file in lista_imagens:
                    zipF.write(f"media/all_images/{file.split('/')[-1]}", compress_type=zipfile.ZIP_DEFLATED)
                zipF.close()
        except Exception as erro:
            print(erro)

        msg = f'{len(lista_imagens)} Imagens encontradas em {rota}'
        imagens_total = zip(lista_imagens, lista_imagens_names)
        context = {
            'img_total': imagens_total,
            'tudo': '/media/all_images/all_images.zip',
            'msg': msg,
            'site_status': page,
        }
        return render(request, 'images/home.html', context)
