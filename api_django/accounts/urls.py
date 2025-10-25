from django.urls import path
from .views.auth.logout import LogoutView
from .views.auth.google_login import GoogleLoginView
from .views.auth.password_reset import PasswordResetRequestView, PasswordResetConfirmView
from .views.auth.enable_2fa import Enable2FAView, Verify2FAView
from .views.auth.token import EmailTokenObtainPairView, DocumentedTokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),    # email+senha
    path('token/refresh/', DocumentedTokenRefreshView.as_view(), name='token_refresh'),
    path('token/google/', GoogleLoginView.as_view(), name='google_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('2fa/enable/', Enable2FAView.as_view(), name='enable_2fa'),
    path('2fa/verify/', Verify2FAView.as_view(), name='verify_2fa'),
]