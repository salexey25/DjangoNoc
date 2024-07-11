from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeviceForm, RackForm, NodeForm
from .models import Device, Rack


#Создать узел. После создания узла выполняется редирект через url на функцию def node_view
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

#Функция, которая перекидывает на страницу создания стойки, когда нажимаем кнопку на node_view.html "Create Rack"
def create_rack(request, nd_id):
    # Если объект не найден, будет возвращена страница с кодом 404 (страница “не найдено”)
    node = get_object_or_404(Rack, nd_id=nd_id)
    return render(request, 'eqapp/create_rack.html', {'node': node})


#Создать стойку. После создания стойки выполняется редирект через url на функцию def node_view, но другим способом
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

#Функция, которорая отправляет на страницу node_view. Эту функцию используют функции creat_node и rack через url маршрут
def node_view(request, nd_id):
    #Получаем объект Node по его ID или возвращаем 404 ошибку, если не найден
    node = get_object_or_404(Rack, nd_id=nd_id)
    racks = Rack.objects.filter(nd_parent_id=nd_id)
    return render(request, 'eqapp/node_view.html', {'node': node, 'racks': racks})

#Список узлов. Функция используется через кнопку "List node" на странице node_view.html
def node_list(request):
	# Получите все сети из базы данных, у которых net_parent_id равен NULL
    nodes = Rack.objects.filter(nd_parent_id__isnull=True)
    return render(request, 'eqapp/node_list.html', {'nodes': nodes})


#Функция создания оборудования - первая версия. Пока не будет развиваться, у нее есть маршрут
#path('device/', views.create_device, name='create_device'),
#есть страница для нее device_form.html
# def create_device(request):
#     if request.method == 'POST':
#         form = DeviceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('device_list')  # Перенаправление на список устройств
#     else:
#         form = DeviceForm()
#     return render(request, 'eqapp/device_form.html', {'form': form})

