from django.urls import path
from dashboard.views import (user_login,
                             user_logout,
                             dashboard,
                            user_register,
                            activate_user,
                             )
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_login, name='login'),
    path('register', user_register, name='register'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate_user'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/admin-logout/', user_logout, name='logout'),

    # 1. Formulaire où l'utilisateur saisit son adresse e-mail
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),

    # 2. Page de confirmation indiquant que l'e-mail a été envoyé
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    # 3. Le lien d'activation sécurisé reçu par e-mail (contient le token)
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # 4. Page finale confirmant que le mot de passe a bien été modifié
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
   ]
