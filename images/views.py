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
        page = requests.get(rota, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all('img')
        images_figure = soup.find_all('figure')
        images_ul = soup.find_all('li')

        lista_imagens = []
        lista_imagens_names = []

        for i in images_ul:
            print(i.img)
            try:
                data = 'src'
                if i.img[data][-4:] != '.svg' and '.' in i.img[data][-4:]:
                    data = 'src'
                else:
                    data = 'data-orig-file'
                if i.img[data][-4:] != '.svg' and '.' in i.img[data][-4:]:
                    if i.img[data] not in lista_imagens:
                        lista_imagens.append(i.img[data])

                    url = i.img[data]
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
            except Exception as erro:
                print(erro)

        for i in images_figure:
            try:
                data = 'src'
                if i.img[data][-4:] != '.svg' and '.' in i.img[data][-4:]:
                    data = 'src'
                else:
                    data = 'data-orig-file'
                if i.img[data][-4:] != '.svg' and '.' in i.img[data][-4:]:
                    if i.img[data] not in lista_imagens:
                        lista_imagens.append(i.img[data])

                    url = i.img[data]
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
            except Exception as erro:
                print(erro)

        for i in images:
            try:
                data = 'src'
                if str(i.get(data))[-4:] != '.svg' and '.' in str(i.get(data))[-4:]:
                    data = 'src'
                else:
                    data = 'data-orig-file'
                if i.get(data):
                    if str(i.get(data))[-4:] != '.svg' and '.' in str(i.get(data))[-4:]:
                        if i.get(data) not in lista_imagens:
                            lista_imagens.append(i.get(data))

                        url = str(i.get(data))
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
            except Exception as erro:
                print(erro)

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
