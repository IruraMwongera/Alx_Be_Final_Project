from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm 
from .forms import PermitForm
from .models import (
    Permit, Transaction, Property, ParkingZone, ParkingTicket,
    MarketStall, Advertisement, BuildingProject, AuditLog
)
# --------------------
# Permits
# --------------------

@login_required
def create_permit(request):
    if request.method == 'POST':
        form = PermitForm(request.POST)
        if form.is_valid():
            permit_instance = form.save(commit=False)
            permit_instance.owner = request.user
            permit_instance.save()
            return redirect('success_page') 
    else:
        form = PermitForm()
    
    # We now render to a different template name to avoid confusion
    return render(request, 'revenue/new_permit.html', {'form': form})
@login_required
def update_permit(request, uid):
    permit = get_object_or_404(Permit, uid=uid, owner=request.user)

    if request.method == 'POST':
        # Instantiate the form with POST data and the existing object
        form = PermitForm(request.POST, instance=permit)
        if form.is_valid():
            form.save() # The form's save method handles the JSONField update
            return redirect('permit_detail_view', uid=permit.uid)
    else:
        # Pre-populate the form with data from the JSONField for the custom fields
        initial_data = {
            'permit_type': permit.permit_type,
            'business_name': permit.data.get('business_name'),
            'business_type': permit.data.get('business_type'),
            'project_name': permit.data.get('project_name'),
            'project_address': permit.data.get('project_address'),
            'license_type': permit.data.get('license_type'),
            'premises_address': permit.data.get('premises_address'),
        }
        form = PermitForm(instance=permit, initial=initial_data)

    return render(request, 'update_permit.html', {'form': form, 'permit': permit})
@login_required
def permit_success_view(request):
    return render(request, 'revenue/permit_success.html')
@login_required
def pay_mpesa(request, permit_id):
    # Your M-Pesa payment processing logic here
    # ...
    return HttpResponse("Payment processing...")

@login_required
def my_permits_view(request):
    permits = Permit.objects.filter(owner=request.user)
    return render(request, 'revenue/my_permits.html', {'permits': permits})

@login_required
def permit_detail_view(request, uid):
    permit = get_object_or_404(Permit, uid=uid, owner=request.user)
    return render(request, 'revenue/permit_detail.html', {'permit': permit})
def new_property_view(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)   # Don't save to DB yet
            property.owner = request.user        # Assign the current user as owner
            property.save()                      # Now save to DB
            return redirect('my_properties')     # Redirect to a page listing properties
    else:
        form = PropertyForm()

    return render(request, 'revenue/new_property.html', {'form': form})
# --------------------
# Properties
# --------------------
@login_required
def my_properties_view(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'revenue/my_properties.html', {'properties': properties})

@login_required
def property_detail_view(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    return render(request, 'revenue/property_detail.html', {'property': property_obj})

# --------------------
# Transactions
# --------------------
@login_required
def my_transactions_view(request):
    transactions = Transaction.objects.filter(owner=request.user)
    return render(request, 'revenue/my_transactions.html', {'transactions': transactions})

@login_required
def transaction_detail_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, owner=request.user)
    return render(request, 'revenue/transaction_detail.html', {'transaction': transaction})

# --------------------
# Parking Zones
# --------------------
@login_required
def parking_zones_view(request):
    zones = ParkingZone.objects.all()
    return render(request, 'revenue/parking_zones.html', {'zones': zones})

@login_required
def parking_zone_detail_view(request, pk):
    zone = get_object_or_404(ParkingZone, pk=pk)
    return render(request, 'revenue/parking_zone_detail.html', {'zone': zone})

# --------------------
# Parking Tickets
# --------------------
@login_required
def my_parking_tickets_view(request):
    tickets = ParkingTicket.objects.filter(owner=request.user)
    return render(request, 'revenue/my_parking_tickets.html', {'tickets': tickets})

@login_required
def parking_ticket_detail_view(request, pk):
    ticket = get_object_or_404(ParkingTicket, pk=pk, owner=request.user)
    return render(request, 'revenue/parking_ticket_detail.html', {'ticket': ticket})

# --------------------
# Market Stalls
# --------------------
@login_required
def my_market_stalls_view(request):
    stalls = MarketStall.objects.filter(owner=request.user)
    return render(request, 'revenue/my_market_stalls.html', {'stalls': stalls})

@login_required
def market_stall_detail_view(request, pk):
    stall = get_object_or_404(MarketStall, pk=pk, owner=request.user)
    return render(request, 'revenue/market_stall_detail.html', {'stall': stall})

# --------------------
# Advertisements
# --------------------
@login_required
def my_advertisements_view(request):
    ads = Advertisement.objects.filter(owner=request.user)
    return render(request, 'revenue/my_advertisements.html', {'ads': ads})

@login_required
def advertisement_detail_view(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk, owner=request.user)
    return render(request, 'revenue/advertisement_detail.html', {'ad': ad})

# --------------------
# Building Projects
# --------------------
@login_required
def my_building_projects_view(request):
    projects = BuildingProject.objects.filter(owner=request.user)
    return render(request, 'revenue/my_building_projects.html', {'projects': projects})

@login_required
def building_project_detail_view(request, pk):
    project = get_object_or_404(BuildingProject, pk=pk, owner=request.user)
    return render(request, 'revenue/building_project_detail.html', {'project': project})

# --------------------
# Audit Logs (Admin Only)
# --------------------
@login_required
def audit_logs_view(request):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    logs = AuditLog.objects.all()
    return render(request, 'revenue/audit_logs.html', {'logs': logs})

@login_required
def audit_log_detail_view(request, pk):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    log = get_object_or_404(AuditLog, pk=pk)
    return render(request, 'revenue/audit_log_detail.html', {'log': log})
