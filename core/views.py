from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from core.utils import create_class_from_bytes


def home(request):
    fu = 'file_upload'
    context = {}
    if request.method == 'POST':
        context['result'] = None
        if fu in request.FILES:
            context['result'] = create_class_from_bytes(request.FILES['file_upload'])
        elif 'test' in request.POST:
            context['result'] = create_class_from_bytes([b'100;100;55;78;22;86;90;30;12;75;66;28;17;15'])
    return render(request, 'home.html', context=context)