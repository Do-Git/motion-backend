from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
   openapi.Info(
      title="Django API",
      default_version='v1',
      description="Description of your Django App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="learn@propulsionacademy.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False, # Set to False restrict access to protected endpoints
   permission_classes=(permissions.AllowAny,), # Permissions for docs access
)

urlpatterns = [
    # Admin Area
    path('backend/admin/', admin.site.urls),

    # Posts
    path('backend/api/posts/', include('post.urls')),
    # User Profiles
    path('backend/api/user_profiles/', include('user_profile.urls')),
    # Comments
    path('backend/api/comments/', include('comment.urls')),
    # Friend Requests
    path('backend/api/friend_requests/', include('friend_request.urls')),
    path('backend/api/auth/registration/', include('registration.urls')),


    # JWT Authentication URLS
    path('backend/api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('backend/api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_refresh'),

    # Swagger API
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
