from django.shortcuts import render

# Create your views here.
from .os_specific.fileoperations import handle_file_download
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str
from .forms import FileForm
from .models import UploadedFile
import os

context = [
        {'label': 'Get Cover Letter', 'link': 'getCLtemplate'},
        {'label': 'Upload Files', 'link': 'upload'},
    ]


def index(request):
    return render(request, 'pages/index.html', {'context': context})

def home(request):
    return render(request, 'pages/home.html', {'context': context})

def about(request):
    return render(request, 'pages/about.html', {'context': context})

def contact(request):
    return render(request, 'pages/contact.html', {'context': context})

def getCLtemplate(request):
    return render(request, 'pages/getCLtemplate.html', {'context': context})


def download_file(request, file_path):
    try:
        return handle_file_download(file_path)
    except FileNotFoundError:
        raise Http404("File not found")
    
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'pages/upload_successful.html')
    else:
        form = FileForm()
    
    return render(request, 'pages/create.html', {'form': form})

def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file_path = file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{smart_str(os.path.basename(file_path))}"'
            return response
    else:
        raise Http404("File not found")