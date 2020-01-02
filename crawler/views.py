# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import PyPDF2
from urllib import urlopen
# from urllib.request import urlopen

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
from .models import PDF, URL

# Create your views here.

def handle_uploaded_file(f):
    print("handle_uploaded_file, file name: %s" % f.name)
    # PDFFile = open('pdf.pdf','rb')

    try:
        pdf_file = PyPDF2.PdfFileReader(f)
    except PyPDF2.utils.PdfReadError:
        print("handle_uploaded_file can't read PDF file")
        return 1

    file, created = PDF.objects.get_or_create(filename = f.name)
    pages = pdf_file.getNumPages()
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    # Let's use this set to ensure that we handle the URL only once
    urls = set()

    for page in range(pages):

        pageSliced = pdf_file.getPage(page)
        pageObject = pageSliced.getObject()

        if pageObject.has_key(key):
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                if u.has_key(ank) and u[ank].has_key(uri):
                    print u[ank][uri]
                    if u[ank][uri] not in urls:
                        # We will handle the URL only once in this PDF file
                        urls.add(u[ank][uri])
                        # Check that URL is alive
                        # To siplicity assume that alive means that URL returns HTTP code 200                        
                        alive = True if urlopen(u[ank][uri]).getcode() == 200 else False
                        if alive:
                            print("Alive!")
                            # print(urlopen(u[ank][uri]).getcode())
                        url, new_url = URL.objects.get_or_create(uri = u[ank][uri], defaults={'alive': alive})

                        print("Adding %s url to the file" % url.uri)
                        file.urls.add(url)

                        if not new_url:
                            # Update alive status for existing URL
                            url.alive = alive
                            url.save()

    return 0



def files(request):
    pdfs = list(PDF.objects.annotate(num_urls=Count('urls')).values())
    return JsonResponse(pdfs, safe=False)

def file_info(request, id):
    pdf = get_object_or_404(PDF, id=id)
    pdf_urls = list(pdf.urls.values())
    return JsonResponse(pdf_urls, safe=False)    

def urls(request):
    all_urls = list(URL.objects.annotate(num_files=Count('pdfs')).values())
    return JsonResponse(all_urls, safe=False)

def success(request):
    return HttpResponse('success')

def error(request):
    return HttpResponse('error')

@csrf_exempt
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