from django.shortcuts import render, redirect
from .models import Node, Equipment
from .forms import NodeForm, EquipmentForm

def create_node(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node_list')
    else:
        form = NodeForm()
    return render(request, 'nodeapp/create_node.html', {'form': form})

def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'nodeapp/create_equipment.html', {'form': form})

