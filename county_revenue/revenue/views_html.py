from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from decimal import Decimal
from datetime import date, timedelta
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from .models import Permit, PermitType, ParkingSection, ParkingTicket, Vehicle, Town, Area
from .forms import PermitForm, ParkingTicketForm
from rest_framework import viewsets
from .serializers import PermitSerializer
from .models import Permit
from xhtml2pdf import pisa
def home_view(request):
    return render(request, "revenue/home.html") 

class PermitViewSet(viewsets.ModelViewSet):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer

@login_required
def create_permit(request):
    permit_types = PermitType.objects.all()

    if request.method == "POST":
        form = PermitForm(request.POST)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.owner = request.user
            permit.owner_name = request.user.get_full_name() or request.user.username

            permit_type = permit.permit_type

            # ✅ Hawking (monthly)
            if permit_type.is_monthly:
                permit.duration_months = form.cleaned_data.get("duration_months") or 1
                permit.duration_days = None

            # ✅ Alcohol Special Event (daily)
            elif permit_type.is_daily:
                permit.duration_days = form.cleaned_data.get("duration_days") or 1
                permit.duration_months = None

            # ✅ Yearly permits
            elif permit_type.is_yearly:
                permit.duration_years = form.cleaned_data.get("duration_years") or 1
                permit.duration_days = None
                permit.duration_months = None

            # Fee calculation handled in Permit.save()
            permit.save()
            return redirect("permit_success", permit_id=permit.id)
    else:
        form = PermitForm()

    context = {"form": form, "permit_types": permit_types}
    return render(request, "revenue/permit/permit_form.html", context)


@login_required
def permit_edit(request, permit_id):
    permit = get_object_or_404(Permit, id=permit_id, owner=request.user)

    if request.method == "POST":
        form = PermitForm(request.POST, instance=permit)
        if form.is_valid():
            permit = form.save(commit=False)

            permit_type = permit.permit_type

            # ✅ Hawking (monthly)
            if permit_type.is_monthly:
                permit.duration_months = form.cleaned_data.get("duration_months") or 1
                permit.duration_days = None

            # ✅ Alcohol Special Event (daily)
            elif permit_type.is_daily:
                permit.duration_days = form.cleaned_data.get("duration_days") or 1
                permit.duration_months = None

            # ✅ Yearly permits
            elif permit_type.is_yearly:
                permit.duration_years = form.cleaned_data.get("duration_years") or 1
                permit.duration_days = None
                permit.duration_months = None

            permit.save()
            return redirect("permit_detail", permit_id=permit.id)
    else:
        form = PermitForm(instance=permit)

    return render(request, "revenue/permit/permit_form.html", {"form": form, "permit": permit})


@login_required
def permit_success(request, permit_id):
    permit = get_object_or_404(Permit, id=permit_id, owner=request.user)
    return render(request, "revenue/permit/permit_success.html", {"permit": permit})


@login_required
def permit_list(request):
    permits = Permit.objects.filter(owner=request.user).order_by("-start_date")
    return render(request, "revenue/permit/permit_list.html", {"permits": permits})


@login_required
def permit_detail(request, permit_id):
    permit = get_object_or_404(Permit, id=permit_id, owner=request.user)
    return render(request, "revenue/permit/permit_detail.html", {"permit": permit})

@login_required
def generate_permit_pdf(request, permit_id):
    permit = get_object_or_404(Permit, id=permit_id)
    template_path = "revenue/permit/permit_pdf.html"  # adjust path if needed

    context = {
        "permit": permit,
        "permit_type_display": permit.permit_type.name,
        "start_date_display": permit.start_date.strftime("%b %d, %Y") if permit.start_date else "",
        "end_date_display": permit.end_date.strftime("%b %d, %Y") if permit.end_date else "",
    }

    html = render_to_string(template_path, context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="permit_{permit.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had errors <pre>" + html + "</pre>")
    return response

# ------------------------------
# Parking Views
# ------------------------------
@login_required
def create_parking_ticket_view(request, section_id):
    section = get_object_or_404(ParkingSection, pk=section_id)
    area = section.area
    town = area.town

    if request.method == "POST":
        form = ParkingTicketForm(request.POST, section=section)
        if form.is_valid():
            ticket = form.save(commit=False)

            # Assign section, town, and area
            ticket.section = section
            ticket.town_name = town.name
            ticket.area_name = area.name

            # Get or create Vehicle
            vehicle, created = Vehicle.objects.get_or_create(
                owner=request.user,
                plate_number=form.cleaned_data["plate_number"],
                defaults={"vehicle_type": form.cleaned_data["vehicle_type"]}
            )

            # Assign vehicle and copy vehicle info to ticket
            ticket.vehicle = vehicle
            ticket.vehicle_type = vehicle.vehicle_type
            ticket.plate_number = vehicle.plate_number

            # Save ticket (created_at will be set automatically)
            ticket.save()

            return redirect("parking_ticket_detail", pk=ticket.pk)
        else:
            print("Form errors:", form.errors)
    else:
        form = ParkingTicketForm(section=section)

    return render(request, "revenue/parking/new_parking_ticket.html", {
        "form": form,
        "section": section,
        "area": area,
        "town": town
    })


@login_required
def parking_ticket_detail_view(request, pk):
    ticket = get_object_or_404(ParkingTicket, pk=pk, vehicle__owner=request.user)
    return render(request, "revenue/parking/parking_ticket_detail.html", {
        "ticket": ticket, "section": ticket.section,
        "area": ticket.section.area, "town": ticket.section.area.town
    })


@login_required
def my_parking_tickets_view(request):
    tickets = ParkingTicket.objects.filter(vehicle__owner=request.user)
    return render(request, "revenue/parking/my_parking_tickets.html", {"tickets": tickets})


@login_required
def parking_zones_view(request):
    zones = ParkingSection.objects.all()
    return render(request, "revenue/parking/parking_zones.html", {"zones": zones})


@login_required
def parking_zone_detail_view(request, pk):
    section = get_object_or_404(ParkingSection, pk=pk)
    tickets = ParkingTicket.objects.filter(section=section, vehicle__owner=request.user)
    return render(request, "revenue/parking/parking_zone_detail.html", {
        "zone": section, "sections": [section], "tickets": tickets
    })


# ------------------------------
# API / AJAX
# ------------------------------

def api_towns(request):
    towns = Town.objects.all().values("id", "name")
    return JsonResponse(list(towns), safe=False)


def api_areas_by_town(request, town_id):
    areas = Area.objects.filter(town_id=town_id).values("id", "name")
    return JsonResponse(list(areas), safe=False)


def api_sections(request, area_id):
    sections = ParkingSection.objects.filter(area_id=area_id).values("id", "name")
    return JsonResponse({"sections": list(sections)})


def api_section_details(request, section_id):
    section = get_object_or_404(ParkingSection, id=section_id)
    return JsonResponse({
        "id": section.id,
        "name": section.name,
        "area": section.area.name,
        "town": section.area.town.name,
    })


def load_areas(request):
    town_id = request.GET.get("town_id")
    areas = Area.objects.filter(town_id=town_id).values("id", "name")
    return JsonResponse(list(areas), safe=False)


def load_sections(request):
    area_id = request.GET.get("area_id")
    sections = ParkingSection.objects.filter(area_id=area_id).values("id", "name")
    return JsonResponse(list(sections), safe=False)


@login_required
def generate_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(ParkingTicket, id=ticket_id)
    template_path = "revenue/parking/ticket_pdf.html"
    context = {"ticket": ticket}
    html = render_to_string(template_path, context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ticket_{ticket.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had errors <pre>" + html + "</pre>")
    return response
