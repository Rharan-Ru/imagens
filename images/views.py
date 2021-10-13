from django.shortcuts import render
from django.views import View
from .models import ImagensModel
from bs4 import BeautifulSoup
import requests
import os
from django.conf import settings
import zipfile


class ImagemView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'images/home.html')

    def post(self, request, *args, **kwargs):
        rota = request.POST['site']
        post = ImagensModel.objects.all()

        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36 Edg/93.0.961.38'}
        headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        headers3 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        headers4 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

        list_headers = [headers, headers2, headers3, headers4]
        proxies = {'https://': '45.70.195.77:5678'}
        page = requests.get(rota, headers=headers)

        for header in list_headers:
            page = requests.get(rota, headers=header)
            if '200' in str(page):
                page = requests.get(rota)
                break
            else:
                continue

        soup = BeautifulSoup(page.content, 'html.parser')
        sounds = soup.findAll('')
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
                r = requests.get(url, allow_redirects=True)
                save_path = os.path.abspath("media/all_images")
                complete = os.path.join(save_path, filename)

                try:
                    open(complete, 'wb').write(r.content)
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
            'post': post,
            'img_total': imagens_total,
            'img_name': lista_imagens_names,
            'tudo': '/media/all_images/all_images.zip',
            'msg': msg,
            'site_status': page,
        }
        return render(request, 'images/home.html', context)
