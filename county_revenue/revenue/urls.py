# revenue/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, views_html

# --------------------
# DRF API Router
# --------------------
router = DefaultRouter()
router.register('permits', views.PermitViewSet)
router.register('transactions', views.TransactionViewSet)
router.register('properties', views.PropertyViewSet)
router.register('parking-zones', views.ParkingZoneViewSet)
router.register('parking-tickets', views.ParkingTicketViewSet)
router.register('market-stalls', views.MarketStallViewSet)
router.register('advertisements', views.AdvertisementViewSet)
router.register('building-projects', views.BuildingProjectViewSet)
router.register('audit-logs', views.AuditLogViewSet)

# --------------------
# URL Patterns
# --------------------
urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # HTML views - Permits
    path('new-permit/', views_html.create_permit, name='new_permit'),
    path('my-permits/', views_html.my_permits_view, name='my_permits'),
    path('pay-mpesa/<int:permit_id>/', views_html.pay_mpesa, name='pay_mpesa'),
    path('permit-success/', views_html.permit_success_view, name='success_page'),
    path('permit/<uuid:uid>/', views_html.permit_detail_view, name='permit_detail'),

    # HTML views - Properties
    path('my-properties/', views_html.my_properties_view, name='my_properties'),
    path('property/<int:pk>/', views_html.property_detail_view, name='property_detail'),
    path('properties/new/', views_html.new_property_view, name='new_property'),

    # HTML views - Transactions
    path('my-transactions/', views_html.my_transactions_view, name='my_transactions'),
    path('transaction/<int:pk>/', views_html.transaction_detail_view, name='transaction_detail'),

    # HTML views - Parking
    path('parking-zones/', views_html.parking_zones_view, name='parking_zones'),
    path('parking-zone/<int:pk>/', views_html.parking_zone_detail_view, name='parking_zone_detail'),
    path('my-parking-tickets/', views_html.my_parking_tickets_view, name='my_parking_tickets'),
    path('parking-ticket/<int:pk>/', views_html.parking_ticket_detail_view, name='parking_ticket_detail'),

    # HTML views - Market Stalls
    path('my-market-stalls/', views_html.my_market_stalls_view, name='my_market_stalls'),
    path('market-stall/<int:pk>/', views_html.market_stall_detail_view, name='market_stall_detail'),

    # HTML views - Advertisements
    path('my-advertisements/', views_html.my_advertisements_view, name='my_advertisements'),
    path('advertisement/<int:pk>/', views_html.advertisement_detail_view, name='advertisement_detail'),

    # HTML views - Building Projects
    path('my-building-projects/', views_html.my_building_projects_view, name='my_building_projects'),
    path('building-project/<int:pk>/', views_html.building_project_detail_view, name='building_project_detail'),

    # HTML views - Audit Logs
    path('audit-logs/', views_html.audit_logs_view, name='audit_logs'),
    path('audit-log/<int:pk>/', views_html.audit_log_detail_view, name='audit_log_detail'),
]


