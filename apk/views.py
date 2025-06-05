from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.contrib.auth import logout as django_logout
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password

def menu_awal(request):
    return render(request, 'apk/menu_awal.html')

def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('home', args=[user.id]))
            else:
                error = "Password salah."
        except User.DoesNotExist:
            error = "Username tidak ditemukan."

    return render(request, 'apk/login.html', {'error': error})

def register(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if not all([nama, username, email, password, confirm_password]):
            return render(request, 'apk/register.html', {'error': 'Semua kolom harus diisi.'})

        if password != confirm_password:
            return render(request, 'apk/register.html', {'error': 'Konfirmasi password tidak cocok.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'apk/register.html', {'error': 'Username sudah digunakan.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'apk/register.html', {'error': 'Email sudah digunakan.'})

        try:
            User.objects.create(
                nama=nama,
                username=username,
                email=email,
                password=make_password(password)
            )
            return HttpResponseRedirect(reverse('login'))
        except IntegrityError:
            return render(request, 'apk/register.html', {'error': 'Pendaftaran gagal. Email atau username sudah digunakan.'})

    return render(request, 'apk/register.html')

def home(request, user_id):
    if 'user_id' not in request.session or request.session['user_id'] != user_id:
        return HttpResponseRedirect(reverse('login'))
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
    user = None
    if 'user_id' in request.session:
        try:
            user = User.objects.get(id=request.session['user_id'])
        except User.DoesNotExist:
            user = None
    if request.method == 'POST':
        uang_awal = float(request.POST.get('uang_awal', 0))
        uang_tambahan = float(request.POST.get('uang_tambahan', 0))
        periode = request.POST.get('periode')
        return_investasi = float(request.POST.get('return_investasi', 0))
        tahun = int(request.POST.get('tahun', 0))
        bulan = int(request.POST.get('bulan', 0))
        total_bulan = tahun * 12 + bulan
        if periode == 'hari':
            frekuensi = 30
        elif periode == 'minggu':
            frekuensi = 4
        else:
            frekuensi = 1
        r = return_investasi / 100 / 12
        saldo = uang_awal
        for i in range(total_bulan):
            saldo = saldo * (1 + r) + uang_tambahan * frekuensi
        hasil = saldo
    return render(request, 'apk/kalkulator.html', {'hasil': hasil, 'user': user})

def profil(request, user_id):
    if 'user_id' not in request.session or request.session['user_id'] != user_id:
        return HttpResponseRedirect(reverse('login'))
    user = User.objects.get(id=user_id)
    if request.method == 'POST' and request.FILES.get('foto_profil'):
        user.foto_profil = request.FILES['foto_profil']
        user.save()
    return render(request, 'apk/profil.html', {'user': user})

def edukasi(request):
    user = None
    if 'user_id' in request.session:
        try:
            user = User.objects.get(id=request.session['user_id'])
        except User.DoesNotExist:
            user = None
    edukasi_list = Video.objects.all()
    return render(request, 'apk/edukasi.html', {'edukasi_list': edukasi_list, 'user': user})
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    django_logout(request)
    return HttpResponseRedirect(reverse('menu_awal'))

def catatan(request, user_id):
    if 'user_id' not in request.session or request.session['user_id'] != user_id:
        return HttpResponseRedirect(reverse('menu_awal'))
    user = User.objects.get(id=user_id)
    transaksi_list = Transaksi.objects.filter(user=user).order_by('-tanggal')
    return render(request, 'apk/catatan.html', {
        'user': user,
        'transaksi_list': transaksi_list,
    })