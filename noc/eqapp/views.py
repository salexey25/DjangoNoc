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
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            rack.save()
            return redirect('rack_list')  # Перенаправление на список стоек
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

    return render(request, 'eqapp/node_view.html', {'node': node})

def create_rack(request, nd_id):
    # Если объект не найден, будет возвращена страница с кодом 404 (страница “не найдено”)
    node = get_object_or_404(Rack, nd_id=nd_id)
    return render(request, 'eqapp/create_rack.html', {'node': node})

def node_list(request):
	# Получите все сети из базы данных, у которых net_parent_id равен NULL
    nodes = Rack.objects.filter(nd_parent_id__isnull=True)
    return render(request, 'eqapp/node_list.html', {'nodes': nodes})