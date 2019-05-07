# Django
from django.contrib import admin
from django.urls import path, include

# 3rd party swagger for documentation
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Point Of Sales API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include('core.items.urls')),
    path('purchases/', include('core.purchases.urls')),
    path('docs/', include_docs_urls(title="POS_API Documentation")),
]
