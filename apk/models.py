from django.db import models

# Create your models here.

class User(models.Model):
    nama = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    foto_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class Transaksi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keterangan = models.CharField(max_length=255)
    nominal = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.keterangan} ({self.nominal})"

class Video(models.Model):
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    durasi = models.CharField(max_length=20)
    youtube_id = models.CharField(max_length=20)

    def thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"