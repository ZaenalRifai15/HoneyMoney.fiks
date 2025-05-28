from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

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
    transaksi_list = Transaksi.objects.filter(user=user).order_by('tanggal')
    saldo = 0
    saldo_list = []
    tanggal_list = []
    for t in transaksi_list:
        saldo += t.nominal
        saldo_list.append(float(saldo))
        tanggal_list.append(t.tanggal.strftime('%d-%m-%Y %H:%M'))
    transaksi_list = transaksi_list.order_by('-tanggal')
    return render(request, 'apk/home.html', {
        'user': user,
        'transaksi_list': transaksi_list,
        'saldo': saldo,
        'saldo_list': json.dumps(saldo_list),
        'tanggal_list': json.dumps(tanggal_list),
    })
