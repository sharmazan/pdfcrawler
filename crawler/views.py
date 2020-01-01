# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import PyPDF2 

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm

# Create your views here.

def handle_uploaded_file(f):
    print("handle_uploaded_file")
    # PDFFile = open('pdf.pdf','rb')

    try:
        PDF = PyPDF2.PdfFileReader(f)
    except PyPDF2.utils.PdfReadError:
        print("handle_uploaded_file can't read PDF file")
        return 1

    pages = PDF.getNumPages()
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    for page in range(pages):

        pageSliced = PDF.getPage(page)
        pageObject = pageSliced.getObject()

        if pageObject.has_key(key):
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                if u[ank].has_key(uri):
                    print u[ank][uri]
    return 0



def files(request):
    return HttpResponse('Files')

def urls(request):
    return HttpResponse('URLs')

def success(request):
    return HttpResponse('success')

def error(request):
    return HttpResponse('error')

def home(request):
    if request.method == 'POST':
        print("POST @ home")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if handle_uploaded_file(request.FILES['file']) == 0:
                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/error/')
        else:
            print("form invalid")

    else:
        print("GET @ home")

        form = UploadFileForm()
    return render(request, 'crawler/base.html', {'form': form})