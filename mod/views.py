from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Mod, ModImage, ModFile
from game.models import Game
from .forms import ModForm
import io
import zipfile
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.core.files.base import ContentFile
from django.urls import reverse

class ModListView(ListView):
    model = Mod
    paginate_by = 4

class ModDetailView(DetailView):
    model = Mod

class ModCreateView(View):
    def get(self, request: HttpRequest, *args, **kargs):
        form = ModForm()

        if (request.GET.get('game') is not None):
            try:
                form = ModForm(initial={
                    'related_game': Game.objects.get(id=request.GET['game'])
                })
            except:
                pass

        return render(request, 'mod/mod_create.html', context={
            'form': form
        })
    
    def post(self, request: HttpRequest, *args, **kargs):
        form = ModForm(request.POST, request.FILES)
        
        if not form.is_valid():
            return render(request, 'mod/mod_create.html', context={
                'form': form
            })
        else:         
            instance = form.save(commit=False)
            instance.author = request.user

            total_size = 0
            for file in request.FILES.getlist('files'):
                total_size = total_size + file.size

            instance.data_size = total_size
            instance.save()

            for file in request.FILES.getlist('files'):
                ModFile.objects.create(related_mod=instance, file=file, original_file_name=file.name)
            
            for image in request.FILES.getlist('images'):
                ModImage.objects.create(related_mod=instance, image=image)        

            return redirect(reverse('mod-detail', args=[str(instance.pk)]))

def download_mod_content(request, pk):   
    mod = None
    try:
        mod = Mod.objects.get(pk=pk)
    except:
        return Http404()
    
    buf = io.BytesIO()
    zip_mem = zipfile.ZipFile(buf, 'w', zipfile.ZIP_STORED)
    files = ModFile.objects.filter(related_mod=mod)
    for file in files:
        zip_mem.writestr(file.original_file_name, file.file.read())
    zip_mem.close()    

    response = HttpResponse()
    response.status_code = 200
    response.content = buf.getvalue()
    response.headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': 'attachment; filename="modcontent.zip"'
    }

    return response