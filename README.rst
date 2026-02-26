Peta di Web
===========

Ini adalah aplikasi web yang menampilkan
`peta Indonesia <https://github.com/sugiana/peta/tree/dukcapil>`_ yang
tersimpan di PostgreSQL dalam bentuk PostGIS. Bacalah di tautan itu cara
memasang dan membuat database-nya.

Kemudian `unduh <https://warga.web.id/files/indonesia/download.html>`_
dan restore database-nya.

Buat Python virtual environment::

    python3.13 -m venv ~/env
    ~/env/bin/pip install -U pip

Pasang paket yang dibutuhkan::

    ~/env/bin/pip install -r requirements.txt

Salin file konfigurasi::

    cp peta.ini live.ini

Sesuaikan ``live.ini``. Jalankan::

    ~/env/bin/python app.py

Di web browser buka ``http://localhost:6543``.


Referensi
=========

Aplikasi ini dibuat oleh `Google Antigravity <https://antigravity.google>`_. Berikut pengalamannya.

Setelah dipasang:

1. Buat direktori kerja bernama ``web``
2. Buat file konfigurasi ``live.ini`` seperti yang tadi dibuat.

Di Antigravity:

1. Buka folder ``web``
2. Di kanan bawah pastikan memilih model Gemini 3 Flash agar gratis.

Saatnya memerintah::

    Buatkan web yang menampilkan peta Indonesia menggunakan OpenStreet Map.
    Tampilan pertama tampil batas provinsi. Saat user menurunkan ketinggian
    maka yang tampak batas kabupaten. Bila diturunkan lagi maka tampak batas
    kecamatan. Bila diturunkan lagi maka tampak batas desa.

    Gunakan Python dengan framework Pyramid. Info database ada di @live.ini,
    tabel wilayah, field batas untuk polygon. Gunakan direktori ~/env sebagai
    Python virtual environment.

Dia mulai membuat, meminta izin kita untuk mencoba, memperbaiki, mencoba lagi,
dst.

3 menit kemudian *hang*. Ubuntu menawarkan untuk *reopen* Antigravity.
Disetujui.

Kemudian klik riwayat percakapan terakhir. Ketik::

    Lanjutkan

Akhirnya selesai kurang dari 30 menit.
