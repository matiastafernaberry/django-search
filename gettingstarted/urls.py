from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

import hello.views
import hello.byg
from hello.views import *
from hello.byg import *


urlpatterns = [
	path("", csrf_exempt(FileClass.as_view())),
    path("nueva-busqueda/", csrf_exempt(NuevaBusquedaClass.as_view())),
    path("bg-documents-sharedcount/", csrf_exempt(ApiGetDocumentsSharedCount7Class.as_view())),
    path("bg-documents-7-days-all-by-client/", csrf_exempt(ApiGetBGDocuments7AllByClient.as_view())),
    path("buzztracker/", csrf_exempt(BuzzTrackerClass.as_view())),
    path("admin/", admin.site.urls),
]
