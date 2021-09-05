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

        page = requests.get(rota)
        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all('img')
        lista_imagens = []
        lista_imagens_names = []

        for i in images:
            if i.get('src'):
                if str(i.get('src'))[-4:] != '.svg' and '.' in str(i.get('src'))[-4:]:
                    lista_imagens.append(i.get('src'))

                    url = str(i.get('src'))
                    filename = url.split('/')[-1]
                    r = requests.get(url, allow_redirects=True)
                    save_path = os.path.abspath("media/all_images")
                    complete = os.path.join(save_path, filename)

                    try:
                        open(complete, 'wb').write(r.content)
                    except Exception as erro:
                        print(erro)

                    save_all = ImagensModel.objects.create(title=filename, img=complete)
                    lista_imagens_names.append(f'/media/all_images/{filename}')

            if str(i.get('original-src'))[-4:] != '.svg' and '.' in str(i.get('original-src'))[-4:]:
                lista_imagens.append(i.get('original-src'))

                url = str(i.get('original-src'))
                filename = url.split('/')[-1]
                r = requests.get(url, allow_redirects=True)
                save_path = os.path.abspath("media/all_images")
                complete = os.path.join(save_path, filename)

                try:
                    open(complete, 'wb').write(r.content)
                except Exception as erro:
                    print(erro)

                save_all = ImagensModel.objects.create(title=filename, img=complete)
                lista_imagens_names.append(f'/media/all_images/{filename}')

        with zipfile.ZipFile(f'{os.path.abspath("media/all_images")}/final.zip', 'w') as zipF:
            for file in lista_imagens:
                zipF.write(f"media/all_images/{file.split('/')[-1]}", compress_type=zipfile.ZIP_DEFLATED)
            zipF.close()

        print(lista_imagens_names)
        msg = f'{len(lista_imagens)} Imagens encontradas em {rota}'
        imagens_total = zip(lista_imagens, lista_imagens_names)
        context = {
            'post': post,
            'img_total': imagens_total,
            'img_name': lista_imagens_names,
            'tudo': '/media/all_images/final.zip',
            'msg': msg,
            'site_status': page,
        }
        return render(request, 'images/home.html', context)
