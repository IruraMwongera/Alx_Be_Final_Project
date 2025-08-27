from django.urls import path
from . import views_html

urlpatterns = [
    # ---------------- Permits ----------------
    path("permits/", views_html.permit_list, name="permit_list"),
    path("permits/new/", views_html.create_permit, name="permit_create"),
    path("permits/<int:permit_id>/", views_html.permit_detail, name="permit_detail"),
    path("permits/success/<int:permit_id>/", views_html.permit_success, name="permit_success"),
    path("permits/<int:permit_id>/edit/", views_html.permit_edit, name="permit_edit"),
    path("permits/<int:permit_id>/pdf/", views_html.generate_permit_pdf, name="generate_permit_pdf"),



    # ---------------- Parking ----------------
    path("parking-zones/", views_html.parking_zones_view, name="parking_zones"),
    path("parking-zone/<int:pk>/", views_html.parking_zone_detail_view, name="parking_zone_detail"),
    path("my-parking-tickets/", views_html.my_parking_tickets_view, name="my_parking_tickets"),
    path("parking-ticket/<int:pk>/", views_html.parking_ticket_detail_view, name="parking_ticket_detail"),
    path("ticket/new/<int:section_id>/", views_html.create_parking_ticket_view, name="create_ticket"),
    path("ticket/<int:ticket_id>/pdf/", views_html.generate_ticket_pdf, name="ticket_pdf"),

    # ---------------- API / AJAX ----------------
    path("api/towns/", views_html.api_towns, name="api_towns"),
    path("api/areas/<int:town_id>/", views_html.api_areas_by_town, name="api_areas_by_town"),
    path("api/sections/<int:area_id>/", views_html.api_sections, name="api_sections"),
    path("api/section/<int:section_id>/", views_html.api_section_details, name="api_section_details"),
    path("ajax/load-areas/", views_html.load_areas, name="ajax_load_areas"),
    path("ajax/load-sections/", views_html.load_sections, name="ajax_load_sections"),
]
