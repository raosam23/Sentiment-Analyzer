import glob
import os
from django.shortcuts import render
from django.http import HttpResponse

def select(request):
    csv_files = glob.glob('media/csvfiles/*.csv')
    csv_file_names = [os.path.basename(file_path) for file_path in csv_files]
    csv_file_names.sort(key=len)
    return render(request, 'select_file/select_file.html', {'csv_file_names': csv_file_names})


def selected_file(request):
    file_name = request.GET.get('file_name')
    request.session['file_name'] = file_name
    return render(request, 'select_file/success.html', {"file_name": file_name})


def choose_algorithm(request):
    return render(request, 'select_file/select_algo.html')
