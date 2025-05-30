from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.contrib.auth import logout as django_logout

# Create your views here.
def menu_awal(request):
    return render(request, 'apk/menu_awal.html')

def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            # Login berhasil, redirect ke halaman home/beranda
            return HttpResponseRedirect(reverse('home', args=[user.id]))
        else:
            error = 'Username atau password salah.'
    return render(request, 'apk/login.html', {'error': error})

def register(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Simpan user baru ke database
        User.objects.create(nama=nama, username=username, email=email, password=password)
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'apk/register.html')

def home(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        jenis = request.POST.get('jenis')
        keterangan = request.POST.get('keterangan')
        nominal = request.POST.get('nominal')
        if jenis == 'pengeluaran':
            nominal = -abs(float(nominal))
        else:
            nominal = abs(float(nominal))
        Transaksi.objects.create(user=user, keterangan=keterangan, nominal=nominal)
    # Ambil semua transaksi untuk saldo/grafik, tapi hanya 3 terakhir untuk tampilan
    semua_transaksi = Transaksi.objects.filter(user=user).order_by('tanggal')
    transaksi_list = Transaksi.objects.filter(user=user).order_by('-tanggal')[:3]
    saldo = 0
    saldo_list = []
    tanggal_list = []
    for t in semua_transaksi:
        saldo += t.nominal
        saldo_list.append(float(saldo))
        tanggal_list.append(t.tanggal.strftime('%d-%m-%Y %H:%M'))
    return render(request, 'apk/home.html', {
        'user': user,
        'transaksi_list': transaksi_list,
        'saldo': saldo,
        'saldo_list': json.dumps(saldo_list),
        'tanggal_list': json.dumps(tanggal_list),
    })

def kalkulator(request):
    hasil = None
    if request.method == 'POST':
        uang_awal = float(request.POST.get('uang_awal', 0))
        uang_tambahan = float(request.POST.get('uang_tambahan', 0))
        periode = request.POST.get('periode')
        return_investasi = float(request.POST.get('return_investasi', 0))
        tahun = int(request.POST.get('tahun', 0))
        bulan = int(request.POST.get('bulan', 0))
        # Hitung total bulan
        total_bulan = tahun * 12 + bulan
        if periode == 'hari':
            frekuensi = 30
        elif periode == 'minggu':
            frekuensi = 4
        else:
            frekuensi = 1
        # Konversi return ke per bulan
        r = return_investasi / 100 / 12
        saldo = uang_awal
        for i in range(total_bulan):
            saldo = saldo * (1 + r) + uang_tambahan * frekuensi
        hasil = saldo
    return render(request, 'apk/kalkulator.html', {'hasil': hasil})

def profil(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST' and request.FILES.get('foto_profil'):
        user.foto_profil = request.FILES['foto_profil']
        user.save()
    return render(request, 'apk/profil.html', {'user': user})

def edukasi(request):
    edukasi_list = Video.objects.all()
    return render(request, 'apk/edukasi.html', {'edukasi_list': edukasi_list})

def logout(request):
    # Hapus session user (jika ada) dan redirect ke menu awal
    if 'user_id' in request.session:
        del request.session['user_id']
    # Jika pakai auth bawaan Django (opsional, jika pakai session login)
    django_logout(request)
    return HttpResponseRedirect(reverse('menu_awal'))
