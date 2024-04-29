from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import IPNetworkForm, NetworkDivisionForm
from .models import IPNetwork, DeletedNetwork, IPAddress
import ipaddress
from django.http import HttpResponse
from django.db import transaction
import uuid
from ipaddress import ip_network, ip_interface, NetmaskValueError
from django.core.validators import validate_ipv4_address
from django.views import View


@login_required
def create_network(request):
    if request.method == 'POST':
        form = IPNetworkForm(request.POST)
        if form.is_valid():
            try:
                subnet = form.cleaned_data['net_prefix']  # Получите значение поля net_prefix из формы
                ip_v4 = ipaddress.ip_network(subnet) #Перобразуем значение subnet из формы в объект сети, в нашем случае это ipv4
                mask = str(ip_v4.netmask) #Получаем значение маски и преобразуем ее в int для сравнения
                if "255.255.128.0" <= mask <= "255.255.255.0":
                    if ip_v4.is_loopback:
                        form.add_error('net_prefix',
                                        "Error - loopback network RFC3330. Попробуйте другую сеть или обратитесь в тех отдел")  # Добавьте ошибку к полю net_prefix
                    elif ip_v4.is_reserved:
                        form.add_error('net_prefix',
                                        "Error - Reserved диапазон - RFC1700. Попробуйте другую сеть или обратитесь в тех отдел.")
                    elif ip_v4.is_multicast:
                        form.add_error('net_prefix',
                                        "Error - Multicast диапазон - RFC3171. Попробуйте другую сеть или обратитесь в тех отдел.")
                    elif ip_v4.is_link_local:
                        form.add_error('net_prefix',
                                        "Error - Link-local адрес - RFC3927. Попробуйте другую сеть или обратитесь в тех отдел.")
                    elif ip_v4.is_unspecified:
                        form.add_error('net_prefix',
                                        "Error - Неуказанный ip адрес - RFC5735. Попробуйте другую сеть или обратитесь в тех отдел.")
                    elif ip_v4.is_private:
                        form.save()
                        # Редирект на страницу созданной сети для дальнейших действий
                        return redirect('/ipnetapp/net_v4_%s/'%form.instance.net_id)
                    elif ip_v4.is_global:
                        form.save()
                        # Редирект на страницу созданной сети для дальнейших действий
                        return redirect('/ipnetapp/net_v4_%s/'%form.instance.net_id)
                else:
                    form.add_error('net_prefix', "Неправильная маска")
            except ValueError:
                form.add_error('net_prefix', "Запрещенный формат сети")
    else:
        form = IPNetworkForm()
    return render(request, 'ipnetapp/create_network.html', {'form': form})


def divide_network(request):
    if request.method == 'POST':
        form = NetworkDivisionForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['division_choice']
            # В зависимости от выбора пользователя, выполните нужные действия
            if choice == 'subnets':
                # Разделение на подсети
                pass
            elif choice == 'ip_list':
                # Разделение на список IP-адресов
                pass
    else:
        form = NetworkDivisionForm()
    return render(request, 'ipnetapp/divide_network.html', {'form': form})

#список сетей
@login_required
def network_list(request):
#    networks = IPNetwork.objects.all()  # Получите все сети из базы данных
    # Получите все сети из базы данных, у которых net_parent_id равен NULL
    networks = IPNetwork.objects.filter(net_parent_id__isnull=True)
    return render(request, 'ipnetapp/network_list.html', {'networks': networks})

#динамическая страница создания сети
def nets_v4_view(request, net_id):
    #Получаем объект NetV4 по его ID или возвращаем 404 ошибку, если не найден
    netv4 = get_object_or_404(IPNetwork, net_id=net_id)
    #Получение объекта network по его ID
    networks = IPNetwork.objects.filter(net_parent_id=net_id)
#    return render(request, 'ipnetapp/net_v4_view.html', {'netv4': netv4, 'networks': networks})
	# Получите значение маски из net_prefix
    subnet = ip_network(netv4.net_prefix)
    prefixlen = subnet.prefixlen

    if prefixlen >= 25:
        ip_addresses_exist = IPAddress.objects.filter(ip_parent_id=net_id).exists()
        if not ip_addresses_exist:
            #Генерируем IP-адреса для данной сети
            ip_addresses = generate_ip_addresses(subnet)  # Предполагается, что у вас есть функция generate_ip_addresses
            for ip_address in ip_addresses:
                #Сохраняем IP-адреса в базе данных, используя модель IPAddress
                ip_obj = IPAddress.objects.create(
                    ip_add=str(ip_address),
                    ip_description=f"Generated IP for {subnet}",
                    ip_parent_id=netv4
                )
                ip_obj.save()
        ip_adds = IPAddress.objects.filter(ip_parent_id=net_id)
        return render(request, 'ipnetapp/net_ipv4_view.html', {'netv4': netv4, 'ip_adds': ip_adds})
    else:
        return render(request, 'ipnetapp/net_v4_view.html', {'netv4': netv4, 'networks': networks})


#Генератор ip адресов для функции ipv4_view
def generate_ip_addresses(subnet):
    #Generate IP addresses from the given network.
    ip_addresses = list(ip_network(subnet).hosts())
    return ip_addresses

#Динамическая страница на которую мы переходим с subnet сети
def ipv4_view(request, net_id):
    # Получаем объект NetV4 по его ID или возвращаем 404 ошибку, если не найден
    netv4 = get_object_or_404(IPNetwork, net_id=net_id)

    #Забираем из объекта netv4 поле net_prefix и переводим его в network
    subnet = ip_network(netv4.net_prefix)

    # Проверяем наличие IP-адресов в базе данных
    ip_addresses_exist = IPAddress.objects.filter(ip_parent_id=net_id).exists()

    if not ip_addresses_exist:
        #Генерируем IP-адреса для данной сети
        ip_addresses = generate_ip_addresses(subnet)

        # Сохраняем IP-адреса в базе данных, используя модель IPAddress
        for ip_address in ip_addresses:
            ip_obj = IPAddress.objects.create(
                ip_add=str(ip_address),
                ip_description=f"Generated IP for {subnet}",
                ip_parent_id=netv4
            )
            ip_obj.save()

    ip_adds = IPAddress.objects.filter(ip_parent_id=net_id)

    return render(request, 'ipnetapp/net_ipv4_view.html', {'netv4': netv4, 'ip_adds': ip_adds})

#Функция редактирования поля description у Ip address в форме net_ipv4_view.html
# class EditIPDescriptionView(View):
#     template_name = 'ipnetapp/net_ipv4_view.html'  # Укажите имя вашего шаблона
#
#     def post(self, request, ip_id):
#         ip_obj = get_object_or_404(IPAddress, ip_id=ip_id)
#         ip_parent_id = ip_obj.ip_parent_id
#
#         # Обновление описания IP-адреса
#         if request.method == 'POST':
#             new_description = request.POST.get('ip_description')
#             ip_obj.ip_description = new_description
#             ip_obj.save()
#
#         # Отображение страницы net_ipv4_view.html с переданным ip_parent_id
#         #return render(request, self.template_name, {'ip_parent_id': ip_parent_id})
#         # Вызов второй функции с переданным ip_parent_id
#         return self.render_second_function(ip_parent_id)
#
#     def render_second_function(self, ip_parent_id):
#         # Отображение страницы net_ipv4_view.html с переданным ip_parent_id
#         return render(self.request, self.template_name, {'ip_parent_id': ip_parent_id})
# def edit_ip_description(request, ip_id):
#     ip_obj = get_object_or_404(IPAddress, ip_id=ip_id)
#     ip_parent_id = ip_obj.ip_parent_id_id
#     if request.method == 'POST':
#         new_description = request.POST.get('ip_description')
#         ip_obj.ip_description = new_description
#         ip_obj.save()
#
#     return redirect('ipnetapp/net_ipv4_view', net_id=ip_obj.ip_parent_id.net_id)

#функция для переадресации на страницу деления сети
def split_network(request, net_id):
    networks = IPNetwork.objects.filter(net_parent_id=net_id)
    # Если объект не найден, будет возвращена страница с кодом 404 (страница “не найдено”)
    netv4 = get_object_or_404(IPNetwork, net_id=net_id)
    #networks = IPNetwork.objects.filter(net_parent_id=netv4.net_id)
    #networks = IPNetwork.objects.all()
    #masks = ip_network(networks.net_prefix).prefixlen

    # Ваш код для обработки формы разделения сети
    # ...
    #return render(request, 'ipnetapp/split_network.html', {'netv4': netv4, 'networks': networks})
    # Получите значение маски из net_prefix
    # Получите значение маски из net_prefix
    subnet = ip_network(netv4.net_prefix)
    prefixlen = subnet.prefixlen

    if prefixlen > 24:
        ip_addresses_exist = IPAddress.objects.filter(ip_parent_id=net_id).exists()
        if not ip_addresses_exist:
            # Генерируем IP-адреса для данной сети
            ip_addresses = generate_ip_addresses(subnet)  # Предполагается, что у вас есть функция generate_ip_addresses
            for ip_address in ip_addresses:
                # Сохраняем IP-адреса в базе данных, используя модель IPAddress
                ip_obj = IPAddress.objects.create(
                    ip_add=str(ip_address),
                    ip_description=f"Generated IP for {subnet}",
                    ip_parent_id=netv4
                )
                ip_obj.save()
        ip_adds = IPAddress.objects.filter(ip_parent_id=net_id)
        return render(request, 'ipnetapp/net_ipv4_view.html', {'netv4': netv4, 'ip_adds': ip_adds})
    else:
        return render(request, 'ipnetapp/split_network.html', {'netv4': netv4, 'networks': networks})

#функция удаления сети
def delete_network(request, net_id):
    netv4 = get_object_or_404(IPNetwork, net_id=net_id)
    # Ваш код для удаления сети из базы данных
    netv4.delete()

    # Получите текущего пользователя
    deleted_by_user = request.user

    DeletedNetwork.objects.create(
        net_prefix=netv4.net_prefix,
        net_description=netv4.net_description,
        net_createdate=netv4.net_createdate,
        deleted_by=deleted_by_user
    )

    # После удаления, перенаправьте пользователя на другую страницу
    return redirect('/ipnetapp/list/')  # Измените URL на нужный

#Функция для просмотра удаленных сетей
def deleted_network_list(request):
    deleted_networks = DeletedNetwork.objects.all()
    return render(request, 'ipnetapp/deleted_network_list.html', {'deleted_networks': deleted_networks})

#Проверка битовой маски создаваемой subnet. Это вспомогательная функция проверки для def subnet
def validate_subnet_mask(network, subnet_mask):
    try:
        #Создаем объект subnet через функцию ipaddress.ip_network() и указываем strict=True, чтобы
        #маска подсети была строго валидной
        subnet = ipaddress.ip_network(f"{network}{subnet_mask}", strict=True)
        return True
    #Поднимаем исключение, так как если маска невалидна, то будет ошибка типа "ValueError: 192.168.1.8/28 has host bits set"
    except ValueError as e:
        return False


#Создаем subnet, выполняем проверку на вхождение в родительскую сеть и проверку на пересечение subnet внутри родительской
def subnet(request, net_id):
    if request.method == 'POST':
        # Получаем объект IPNetwork на основе net_id
        parent_net = get_object_or_404(IPNetwork, net_id=net_id)

        # Получаем значения из формы
        subnet_mask = request.POST.get('subnet_mask')
        network = request.POST.get('network')
        description = request.POST.get('description')

        #Проверяем валидность маски, так как есть строгие правила по делению сети. Делаем это через дополнительную
        #функцию def validate_subnet_mask, которая возвращаем нам True или Flase
        if validate_subnet_mask(network, subnet_mask):
        # Создаем новую подсеть с новой маской
            new_prefix = network + subnet_mask
            new_net = IPNetwork(net_parent_id=parent_net, net_prefix=new_prefix, net_description=description)

        # Преобразуем в объекты ip_network
            parent_subnet = ip_network(parent_net.net_prefix)
            new_subnet = ip_network(new_net.net_prefix)

            # Проверьте маски подсетей, маска подсети не должна быть меньше родительской
            if new_subnet.prefixlen >= parent_subnet.prefixlen:
                # subnet_of - Возвращает True если эта сеть является подсетью другой
                if new_subnet.subnet_of(parent_subnet):
                    existing_subnets = IPNetwork.objects.filter(net_parent_id=parent_net)
                    overlap_found = False
                    for existing_subnet in existing_subnets:
                        #overlaps - True, если new_subnet частично или полностью содержиться в
                        #другой подсети, или другая полностью содержиться в этой
                        if ip_network(new_net.net_prefix).overlaps(ip_network(existing_subnet.net_prefix)):
                            overlap_found = True
                            break
                    #Условие проверки overlap subnet, если есть, то выводим сообщение о пересечении сетей.
                    if overlap_found:
                        networks = IPNetwork.objects.filter(net_parent_id=net_id)
                        return render(request, 'ipnetapp/split_network.html',
                                          {'netv4': parent_net,'networks': networks, 'message': 'Пересечение сетей'})
                    else:
                        # Проверяем наличие IP-адресов с таким же net_id
                        existing_ips = IPAddress.objects.filter(ip_parent_id=parent_net.net_id)
                        if existing_ips.exists():
                            networks = IPNetwork.objects.filter(net_parent_id=net_id)
                            ip_addresses = IPAddress.objects.filter(ip_parent_id=parent_net.net_id)
                            return render(request, 'ipnetapp/split_network.html',
                                          {'netv4': parent_net, 'networks': networks,'ip_addresses': ip_addresses,
                                                   'message': 'Родительская сеть разбита на IP-адреса'})
                        else:
                            new_net.save()
                            networks = IPNetwork.objects.filter(net_parent_id=net_id)
                            ip_addresses = IPAddress.objects.filter(ip_parent_id=parent_net.net_id)
                            return render(request, 'ipnetapp/split_network.html',
                                  {'netv4': parent_net,'networks': networks, 'ip_addresses': ip_addresses,
                                            'message': f'Новая подсеть создана: {new_subnet}'})
                            #return HttpResponse(f'filter{existing_subnets}')

                else:
                    networks = IPNetwork.objects.filter(net_parent_id=net_id)
                    return render(request, 'ipnetapp/split_network.html',
                                  {'netv4': parent_net,'networks': networks, 'message': 'Новая подсеть не входит в состав родительской сети.'})

            else:
                networks = IPNetwork.objects.filter(net_parent_id=net_id)
                return render(request, 'ipnetapp/split_network.html',
                              {'netv4': parent_net,'networks': networks, 'message': 'Маска новой подсети больше маски родительской подсети.'})
        else:
            networks = IPNetwork.objects.filter(net_parent_id=net_id)
            return render(request, 'ipnetapp/split_network.html',
                          {'netv4': parent_net,'networks': networks, 'message': 'Неправильная маска подсети.'})
    else:
        # Если метод GET, просто отобразить форму
        parent_net = get_object_or_404(IPNetwork, net_id=net_id)
        return render(request, 'split_network.html', {'netv4': parent_net})



###############
# def subnet(request, net_id):
#     if request.method == 'POST':
#         parent_net = get_object_or_404(IPNetwork, net_id=net_id)
#         subnet_mask = request.POST.get('subnet_mask')
#         network = request.POST.get('network')
#         description = request.POST.get('description')
#         new_prefix = network + subnet_mask
#         new_net = ip_network(new_prefix)
#         parent_subnet = ip_network(parent_net.net_prefix)
#         # return HttpResponse(f"Значение parent_subnet: {parent_subnet}, тип: {type(parent_subnet)}"
#         #                     f"Значение new_net: {new_net}, тип: {type(new_net)}")
#        if new_net.prefixlen <= parent_subnet.prefixlen:
#             # Проверьте адреса
#             if ip_interface(new_net.network).ip in parent_subnet:
#                 new_net.save()
#                 return HttpResponse(f'Новая подсеть создана с net_id родительской сети: {new_net.net_parent_id.net_id}, и маской: {new_net.net_prefix}')
#             else:
#                 return HttpResponse('Новая подсеть не входит в состав родительской сети.')
#         else:
#             return HttpResponse('Маска новой подсети превышает маску родительской сети.')


def create_subnet(request):
    if request.method == 'POST':
        subnet_size = request.POST.get('subnet_size')  # Получаем выбранную маску из формы
        parent_network_prefix = request.POST.get('parent_network_prefix')  # Получаем префикс основной сети из формы
        parent_network = IPNetwork.objects.get(net_prefix=parent_network_prefix)  # Основная сеть
        subnet = IPNetwork.objects.create(
            net_parent_id=parent_network,
            net_prefix=f'{parent_network_prefix}{subnet_size}',  # Пример: "192.168.10.0/25"
            net_description='Subnet from main network'
        )
        return redirect(f'/ipnetapp/net_v4_{subnet.net_id}/')  # Редирект на новую страницу
    else:
        form = NetworkDivisionForm()
    return render(request, 'subnet_creation_form.html', {'form': form})

