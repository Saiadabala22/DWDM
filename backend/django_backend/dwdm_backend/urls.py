from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return HttpResponse(
        "<h2>DWDM Integrated System - Django API</h2><ul>"
        "<li><a href='/admin/'>Admin</a></li><li><a href='/api/'>API root</a> (JWT required)</li>"
        "<li>POST /api/token/ to get a token</li></ul>"
        "<p>The analysis UI is Streamlit: <code>python manage.py runstreamlit</code> (http://localhost:8501)</p>")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("api.urls")),
]
