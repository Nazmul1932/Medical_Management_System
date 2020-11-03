
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mms import views
from mms.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register("company", views.CompanyViewSet, basename="company")
router.register("companybank", views.CompanyBankViewSet, basename="companybank")
router.register("medicine", views.MedicineViewSet, basename="medicine")
router.register("company_account", views.CompanyAccountViewSet, basename="company_account")
router.register("company_employee", views.EmployeeViewSet, basename="company_employee")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/gettoken/', TokenObtainPairView.as_view(), name="gettoken"),
    path('api/refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
    path('api/companybyname/<str:name>', CompanyNameViewSet.as_view(), name="companybyname"),
    path('api/company_only/', CompanyOnlyViewSet.as_view(), name="company_only"),
]
