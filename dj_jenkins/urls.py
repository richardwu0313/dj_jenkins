from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path
from rest_framework import permissions

from dj_jenkins.views import JenkinsViewSet
from dj_jenkins.views import JobViewSet
from dj_jenkins.views import JobBuildViewSet
from dj_jenkins.views import PipelineViewSet
from dj_jenkins.views import PipelineBuildViewSet
from dj_jenkins.views import PipelineBuildStageViewSet

router = DefaultRouter()
router.register(r"jenkins", JenkinsViewSet, basename="jenkins")
router.register(r"jobs", JobViewSet, basename="jobs")
router.register(r"job-builds", JobBuildViewSet, basename="job-builds")
router.register(r"pipelines", PipelineViewSet, basename="pipelines")
router.register(r"pipeline-builds", PipelineBuildViewSet, basename="pipeline-builds")
router.register(r"pipeline-build-stages", PipelineBuildStageViewSet, basename="pipeline-build-stages")

urlpatterns = router.urls

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version="v1",
      description="jenkins api based on django",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns.extend([
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

])