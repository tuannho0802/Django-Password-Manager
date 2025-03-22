from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.FERNET_KEY.encode())

# Store verification codes per user session
verification_codes = {}

def home(request):
    """Handles user authentication and password management."""
    if request.method == "POST":
        if "signup-form" in request.POST:
            return handle_signup(request)
        elif "logout" in request.POST:
            return logout_view(request)
        elif "login-form" in request.POST:
            return handle_login(request)
        elif "confirm" in request.POST:
            return confirm_login(request)
        elif "add-password" in request.POST:
            return add_password(request)
        elif "delete" in request.POST:
            return delete_password(request)

    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.filter(user=request.user)
        for password in passwords:
            try:
                password.email = fernet.decrypt(password.email.encode()).decode()
                password.password = fernet.decrypt(password.password.encode()).decode()
            except Exception as e:
                print(f"⚠️ Decryption failed for {password.email}: {e}")
                messages.error(request, "Some stored data is corrupted or incorrectly encrypted.")

        context = {"passwords": passwords}

    return render(request, "home.html", context)


def handle_signup(request):
    """Handles user signup."""
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    password2 = request.POST.get("password2")

    if password != password2:
        messages.error(request, "Passwords do not match!")
        return redirect("home")

    if User.objects.filter(username=username).exists():
        messages.error(request, f"Username {username} already exists!")
        return redirect("home")

    if User.objects.filter(email=email).exists():
        messages.error(request, f"Email {email} already exists!")
        return redirect("home")

    user = User.objects.create_user(username, email, password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, f"Welcome, {username}!")
    return redirect("home")


def handle_login(request):
    """Handles user login and sends email confirmation."""
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.error(request, "Login failed! Invalid username or password.")
        return redirect("home")

    # Generate verification code
    code = str(random.randint(100000, 999999))
    request.session["verification_code"] = code  # Store code in session
    request.session["verification_user"] = user.username  # Store username

    send_mail(
        "Django Password Manager: Confirm Email",
        f"Your verification code is {code}.",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return render(request, "home.html", {"code": code, "user": user.username})


def confirm_login(request):
    """Handles email verification and login."""
    input_code = request.POST.get("code")
    username = request.session.get("verification_user")  # Get stored username
    stored_code = request.session.get("verification_code")  # Get stored code

    # Debugging print statement
    print(f"Input Code: {input_code}, Stored Code: {stored_code}, User: {username}")

    if not stored_code:
        messages.error(request, "Verification code has expired. Please log in again.")
        return redirect("home")

    if input_code != stored_code:
        messages.error(request, "Invalid verification code!")
        return redirect("home")

    # Log in the user
    try:
        user = User.objects.get(username=username)
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("home")

    # Clear verification data from session
    request.session.pop("verification_code", None)
    request.session.pop("verification_user", None)

    return redirect("home")


def logout_view(request):
    """Logs out the user."""
    logout(request)
    messages.success(request, "You have logged out.")
    return redirect("home")


def add_password(request):
    """Handles saving encrypted passwords."""
    url = request.POST.get("url")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Ensure we only encrypt if it's not already encrypted
    try:
        decrypted_email = fernet.decrypt(email.encode()).decode()
        encrypted_email = email  # If already encrypted, keep it
    except:
        encrypted_email = fernet.encrypt(email.encode()).decode()  # Encrypt if needed

    try:
        decrypted_password = fernet.decrypt(password.encode()).decode()
        encrypted_password = password  # If already encrypted, keep it
    except:
        encrypted_password = fernet.encrypt(password.encode()).decode()  # Encrypt if needed

    # Get website title
    try:
        br.open(url)
        title = br.title()
    except:
        title = url

    # Get website favicon
    try:
        icon = favicon.get(url)[0].url
    except:
        icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"

    Password.objects.create(
        user=request.user,
        name=title,
        logo=icon,
        email=encrypted_email,
        password=encrypted_password,
    )

    messages.success(request, f"{title} added successfully!")
    return redirect("home")


def delete_password(request):
    """Handles password deletion."""
    to_delete = request.POST.get("password-id")
    password_entry = Password.objects.get(id=to_delete)
    messages.success(request, f"{password_entry.name} deleted!")
    password_entry.delete()
    return redirect("home")
