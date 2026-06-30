from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.forms import CustomerForm
from customers.models import Customer
from django.contrib import messages

'''
    Customer manager
'''
# @login_required
# def customer_manager(request):
#     customers = Customer.objects.all()
#     # customers_filtered = Customer.objects.filter('status')
#     status_query = request.GET.get('status')
#     if status_query:
#         customers_filtered = customers.filter(status = status_query)
#     else:
#         customers_filtered = customers.all()
#
#     context = {'customers': customers, 'customers_filtered': customers_filtered}
#     return render(request, 'customers/customer_manager.html', context)

@login_required
def customer_manager(request):
    customers = Customer.objects.all()

    # Récupère la liste des statuts uniques utilisés par vos clients
    available_statuses = Customer.objects.values_list('status', flat=True).distinct()

    # Gestion du filtrage si le formulaire est soumis
    status_query = request.GET.get('status')
    if status_query:
        customers_list = Customer.objects.filter(status=status_query)
    else:
        customers_list = customers

    context = {
        'customers': customers_list,  # Liste des clients à afficher dans le tableau
        'available_statuses': available_statuses  # Liste des statuts pour le menu déroulant
    }
    return render(request, 'customers/customer_manager.html', context)


'''
    Show one customer details
'''
@login_required
def view_info(request, pk):
    customer_info = get_object_or_404(Customer, pk=pk)
    context = {'customer_info': customer_info}
    return render(request, 'customers/view_info.html', context)
'''
    Customer creation form
'''
@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request, 'Customer Created successfully')
            return redirect('customer_manager')
    else:
        form = CustomerForm()

    return render(request, 'customers/add_customer.html', {'form': form})

'''
    Customer edit form
'''
@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Edited successfully')
            return redirect('customer_manager')
    else:
        form = CustomerForm(instance=customer, initial={'pk': pk})

    return render(request, 'customers/edit_customer.html', {'form': form, 'customer': customer})


'''
    handle 404 page
'''
def customer_404(request, exception=None):
    return render(request, 'customers/404.html', status=404)