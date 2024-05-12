from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeviceForm, RackForm, NodeForm
from .models import Device, Rack


# Create your views here.

def create_node(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            form.save()
 #           return redirect('node_list')
            return redirect('/eqapp/node_%s/'%form.instance.nd_id)# Перенаправление на страницу узла связи
    else:
        form = NodeForm()
    return render(request, 'eqapp/node_form.html', {'form': form})

def rack(request, nd_id):
    #node = = get_object_or_404(Rack, net_id=net_id)
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            rack_instance = form.save(commit=False) # Создание экземпляра без сохранения в базе данных
            node = Rack.objects.get(nd_id=nd_id)
            rack_instance.nd_parent_id = node  # Присвоение значения nd_id полю nd_parent_id
            rack_instance.nd_rack_num = form.cleaned_data['nd_rack_num']
            rack_instance.nd_rack_unit = form.cleaned_data['nd_rack_unit']
            rack_instance.nd_rack_type = form.cleaned_data['nd_rack_type']
            rack_instance.save()  # Сохранение экземпляра в базе данных
            return redirect(f'/eqapp/node_{nd_id}/')
    else:
        form = RackForm()
    return render(request, 'eqapp/create_rack.html', {'form': form})

def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')  # Перенаправление на список устройств
    else:
        form = DeviceForm()
    return render(request, 'eqapp/device_form.html', {'form': form})


def node_view(request, nd_id):
    #Получаем объект Node по его ID или возвращаем 404 ошибку, если не найден
    node = get_object_or_404(Rack, nd_id=nd_id)
    racks = Rack.objects.filter(nd_parent_id=nd_id)
    return render(request, 'eqapp/node_view.html', {'node': node, 'racks': racks})

def create_rack(request, nd_id):
    # Если объект не найден, будет возвращена страница с кодом 404 (страница “не найдено”)
    node = get_object_or_404(Rack, nd_id=nd_id)
    return render(request, 'eqapp/create_rack.html', {'node': node})

def node_list(request):
	# Получите все сети из базы данных, у которых net_parent_id равен NULL
    nodes = Rack.objects.filter(nd_parent_id__isnull=True)
    return render(request, 'eqapp/node_list.html', {'nodes': nodes})