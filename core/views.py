from decimal import Decimal
from random import uniform

from django.shortcuts import render

from core.utils import create_class_from_bytes


def home(request):
    fu = 'file_upload'
    context = {'graph_title': 'Quantidade de amostras por intervalo'}
    if request.method == 'POST':
        if request.POST['graph_title'] != '':
            context['graph_title'] = request.POST['graph_title']
        context['result'] = None
        if fu in request.FILES:
            context['result'] = create_class_from_bytes(request.FILES['file_upload'])
        elif 'test' in request.POST:
            data = []
            while len(data) < 50:
                data.append(round(Decimal(uniform(1, 100)), 1))
            context['result'] = create_class_from_bytes([b';'.join(str(i).encode() for i in data)])
    return render(request, 'home.html', context=context)
