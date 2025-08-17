from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm 
from .forms import PermitForm
from .models import Town, Area, ParkingSection, Vehicle, ParkingTicket
from .forms import ParkingTicketForm
from django.http import JsonResponse
from .models import Town, Area
from .models import (
    Permit, Transaction, Property, ParkingTicket,
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
            permit = form.save(commit=False)
            permit.owner = request.user  # Set the logged-in user as owner
            permit.save()
            return redirect('new_permit')  # Or redirect to a detail page if needed
    else:
        form = PermitForm()  # GET request shows empty form

    return render(request, 'revenue/new_permit.html', {
        'form': form,
    })
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
@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('my_properties')
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'revenue/edit_property.html', {
        'form': form,
        'property': property_obj
    })
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
# API for Parking Tickets
# --------------------
def api_areas(request, town_id):
    areas = Area.objects.filter(town_id=town_id).values("id", "name")
    return JsonResponse({"areas": list(areas)})


def api_sections(request, area_id):
    sections = ParkingSection.objects.filter(area_id=area_id).values("id", "name")
    return JsonResponse({"sections": list(sections)})


def api_towns(request):
    towns = Town.objects.all().values("id", "name")
    return JsonResponse(list(towns), safe=False)


def api_areas_by_town(request, town_id):
    areas = Area.objects.filter(town_id=town_id).values("id", "name")
    return JsonResponse(list(areas), safe=False)


def api_section_details(request, section_id):
    section = get_object_or_404(ParkingSection, id=section_id)
    return JsonResponse({
        "id": section.id,
        "name": section.name,
        "area": section.area.name,
        "town": section.area.town.name,
    })
# --------------------
# Parking Sections (formerly "Zones")
# --------------------
@login_required
def parking_zones_view(request):
    zones = ParkingSection.objects.all()
    return render(request, 'revenue/parking/parking_zones.html', {'zones': zones})


@login_required
def parking_zone_detail_view(request, pk):
    zone = get_object_or_404(ParkingSection, pk=pk)
    
    # Show all tickets in this section for this user
    tickets = ParkingTicket.objects.filter(section=zone, vehicle__owner=request.user)

    return render(request, 'revenue/parking/parking_zone_detail.html', {
        'zone': zone,
        'tickets': tickets
    })
# --------------------
# Parking Tickets
# --------------------
@login_required
def create_parking_ticket_view(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    town = area.town

    if request.method == "POST":
        form = ParkingTicketForm(request.POST, user=request.user, area=area)
        if form.is_valid():
            ticket = form.save(commit=False)
            section = form.cleaned_data.get("section")
            custom_section_name = form.cleaned_data.get("custom_section_name")

            # Handle custom section
            if not section and custom_section_name:
                section, created = ParkingSection.objects.get_or_create(
                    area=area,
                    name=custom_section_name,
                    defaults={"is_custom": True, "capacity": 1}
                )

            ticket.section = section
            ticket.save()
            return redirect("parking_ticket_detail_view", pk=ticket.pk)
    else:
        form = ParkingTicketForm(user=request.user, area=area)

    return render(request, "revenue/parking/new_parking_ticket.html", {
        "form": form,
        "area": area,
        "town": town,
    })
@login_required    
def parking_ticket_success_view(request, pk):
    ticket = get_object_or_404(
        ParkingTicket,
        pk=pk,
        vehicle__owner=request.user
    )
    return render(request, "revenue/parking/new_parking_ticket.html", {"ticket": ticket})

@login_required
def my_parking_tickets_view(request):
    tickets = ParkingTicket.objects.filter(vehicle__owner=request.user)
    return render(request, 'revenue/parking/my_parking_tickets.html', {'tickets': tickets})
@login_required
def parking_ticket_detail_view(request, pk):
    ticket = get_object_or_404(ParkingTicket, pk=pk, vehicle__owner=request.user)
    
    # Assuming your ParkingTicket model has foreign keys to section, area, town
    section = ticket.section
    area = section.area
    town = area.town
    
    context = {
        'ticket': ticket,
        'section': section,
        'area': area,
        'town': town,
    }
    
    return render(request, 'revenue/parking/parking_ticket_detail.html', context)

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

