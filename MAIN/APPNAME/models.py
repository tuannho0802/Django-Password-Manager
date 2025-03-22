from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cryptography.fernet import Fernet

# Ensure you have a valid FERNET_KEY in settings.py
fernet = Fernet(settings.FERNET_KEY)

class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    logo = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        if not self.pk:  # Encrypt only if new
            self.email = fernet.encrypt(self.email.encode()).decode()
            self.password = fernet.encrypt(self.password.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_password(self):
        """Decrypt and return the original password"""
        return fernet.decrypt(self.password.encode()).decode()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
