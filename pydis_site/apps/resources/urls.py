from django_distill import distill_path

from pydis_site.apps.resources.views import ResourceView

app_name = "resources"
urlpatterns = [
    # Using `distill_path` instead of `path` allows this to be available
    # in static preview builds.
    distill_path("", ResourceView.as_view(), name="index"),
    distill_path("<resource_type>/", ResourceView.as_view(), name="index"),
]
