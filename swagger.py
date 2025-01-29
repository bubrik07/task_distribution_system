from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Task Distribution System API",
      default_version='v1',
      description="API documentation for the Task Distribution System",
      contact=openapi.Contact(
         name="Oleksandr Bubriak",
         email="s.bubryak2002@gmail.com",
      ),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
