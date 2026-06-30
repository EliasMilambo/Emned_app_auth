from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings  # Import à ajouter pour utiliser settings.DEFAULT_FROM_EMAIL

User = get_user_model()

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

'''
    login page 
'''
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, 'login.html')


'''
    register page 
'''

def user_register(request):
    if request.method == 'POST':
        # Récupération des données du formulaire HTML
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        username = request.POST.get('username')

        # 1. Vérification : Mots de passe identiques
        if password != password_confirm:
            messages.error(request, "The two passwords do not match.")
            return render(request, 'register.html')

        # 2. Vérification : L'identifiant ou l'email existe déjà ?
        if User.objects.filter(username=username).exists():
            messages.error(request, "This identifier is already in use.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, 'register.html')

        # 3. Création si tout est OK
        user = User.objects.create_user(
            username=username,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=email,
            phone=request.POST.get('phone'),
            password=password
        )

        # Correction logique : On force is_active à False après création pour bloquer l'accès
        user.is_active = False
        user.save()

        # 4. Processus d'activation (CORRECTION DE L'INDENTATION ICI)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Construction du lien d'activation
        protocol = 'https' if request.is_secure() else 'http'
        domain = request.get_host()
        link = f"{protocol}://{domain}/activate/{uid}/{token}/"

        # Envoi du mail
        subject = "Welcome ! Kindly confirm your Email address"
        message = f"Hello {user.first_name},\n\nWelcome to your Management Dashboard.\nTo activate your account and log in, please click on the link below :\n\n{link}\n\nThe Emned Empire team."

        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     # Utilise la conf de settings plutôt que 'noreply@emned.com' pour éviter le crash SMTP
        #     [user.email],
        #     fail_silently=False,
        # )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,  # Relever une erreur si l'envoi échoue
            )
        except Exception as e:
            # Permet de voir l'erreur exacte dans vos logs Django
            print(f"Erreur d'envoi SMTP : {e}")

        messages.success(request, "A confirmation email has been sent to you. Please check your inbox.")
        return redirect('login')

    else:
        # En mode GET, on affiche le formulaire vide
        return render(request, 'register.html')


# Vue qui intercepte le clic sur le lien dans le mail
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Vérification de la validité du token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Le compte est enfin activé
        user.save()
        messages.success(request, "Your account has been successfully activated! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "The activation link is invalid or has expired.")
        return redirect('login')


'''
    logout page
'''
def user_logout(request):
    logout(request)
    return redirect('login')
