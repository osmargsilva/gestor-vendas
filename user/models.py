from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from uuid import uuid4
from django.forms import ValidationError

from user.signos import obter_signo

def validar_ext(value): 
    """
    Validate the file extension of the uploaded image.
    """
    valid_extensions = ['jpg', 'jpeg', 'png']
    ext = value.name.split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}')
    return value

def size(value):
    """
    Validate the size of the uploaded image.
    """
    limit = 7 * 1024 * 1024  
    if value.size > limit:
        raise ValidationError(f'File size exceeds the limit of {limit / (1024 * 1024)} MB')
    return value

def upload_to(instance, filename):
    img = filename.split('.')
    ext = img[-1]
    return f'user_photos/{uuid4()}.{ext}'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username.
    """
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=30, blank=True)
    nasc = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('B', 'Bissexual')], blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(
        upload_to= upload_to, 
        blank=True, 
        null=True, 
        validators=[size, validar_ext]
        )
    telefone = models.CharField(max_length=15, blank=True)
    signo = models.CharField(max_length=20, blank=True, null=True, editable=False)
    is_whatsapp = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'nasc']
    
    def save(self, *args, **kwargs):
        if self.nasc:
            self.signo = obter_signo(self.nasc.strftime('%d-%m-%Y'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email