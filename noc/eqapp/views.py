from django.shortcuts import render, redirect
from .forms import DeviceForm, RackForm
from .models import Device, Rack

# Create your views here.
def create_rack(request):
    cities = [('city1', 'City 1'), ('city2', 'City 2'), ('city3', 'City 3')]
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            rack = form.save(commit=False)  # Создаем объект Rack, но не сохраняем его пока в базе данных
            rack.nd_city = request.POST.get('nd_city')  # Получаем выбранное значение из POST-запроса
            rack.nd_address = request.POST.get('nd_address')
            rack.nd_name = request.POST.get('nd_name')
            rack.nd_contact = request.POST.get('nd_contact')
            rack.nd_description = request.POST.get('nd_description')
            rack.nd_rack_num = request.POST.get('nd_rack_num')
            rack.nd_rack_unit = request.POST.get('nd_rack_unit')
            rack.nd_rack_type = request.POST.get('nd_rack_type')
            rack.save()
            return redirect('rack_list')  # Перенаправление на список стоек
    else:
        form = RackForm()
    return render(request, 'eqapp/rack_form.html', {'form': form, 'cities': cities})

def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')  # Перенаправление на список устройств
    else:
        form = DeviceForm()
    return render(request, 'eqapp/device_form.html', {'form': form})