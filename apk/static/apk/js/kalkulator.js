// FAB menu toggle logic agar menu bisa dibuka/tutup
// File: static/apk/js/kalkulator.js
document.addEventListener('DOMContentLoaded', function() {
    const fabMenu = document.getElementById('fabMenu');
    const fabBtn = document.getElementById('fabBtn');
    if (fabBtn && fabMenu) {
        fabBtn.addEventListener('click', function() {
            fabMenu.classList.toggle('open');
        });
    }

    // Kalkulator investasi interaktif tanpa reload
    const form = document.getElementById('formKalkulator');
    const hasilDiv = document.getElementById('hasilInvestasi');
    if (form && hasilDiv) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Ambil nilai input
            const uang_awal = parseFloat(form.uang_awal.value) || 0;
            const uang_tambahan = parseFloat(form.uang_tambahan.value) || 0;
            const periode = form.periode.value;
            const return_investasi = parseFloat(form.return_investasi.value) || 0;
            const tahun = parseInt(form.tahun.value) || 0;
            const bulan = parseInt(form.bulan.value) || 0;
            // Hitung total bulan
            const total_bulan = tahun * 12 + bulan;
            let frekuensi = 1;
            if (periode === 'hari') frekuensi = 30;
            else if (periode === 'minggu') frekuensi = 4;
            // Konversi return ke per bulan
            const r = return_investasi / 100 / 12;
            let saldo = uang_awal;
            let total_tabungan = uang_awal;
            for (let i = 0; i < total_bulan; i++) {
                saldo = saldo * (1 + r) + uang_tambahan * frekuensi;
                total_tabungan += uang_tambahan * frekuensi;
            }
            const hasil_return = saldo - total_tabungan;
            // Tampilkan hasil
            document.getElementById('tabunganAnda').textContent = total_tabungan.toLocaleString('id-ID', {minimumFractionDigits:2, maximumFractionDigits:2});
            document.getElementById('returnInvestasi').textContent = hasil_return.toLocaleString('id-ID', {minimumFractionDigits:2, maximumFractionDigits:2});
            document.getElementById('totalAkhir').textContent = saldo.toLocaleString('id-ID', {minimumFractionDigits:2, maximumFractionDigits:2});
            form.style.display = 'none';
            hasilDiv.style.display = 'block';
        });
        // Tombol kembali ke form
        const btnKembali = document.getElementById('btnKembali');
        if (btnKembali) {
            btnKembali.addEventListener('click', function(e) {
                e.preventDefault();
                hasilDiv.style.display = 'none';
                form.style.display = 'block';
            });
        }
    }
});
