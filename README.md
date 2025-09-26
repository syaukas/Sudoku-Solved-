# Sudoku-Solved
Task

Implement function solveSudoku(matrix), that for given incomplete matrix will return solved sudoku. 0 means no value

1. Membangun solusi Sudoku lengkap

Di sini digunakan backtracking dengan randomisasi.

Algoritme bekerja begini:

Mulai dari kotak pertama (0,0).

Pilih angka acak dari 1–9.

Cek validasi:

Angka belum ada di baris yang sama.

Angka belum ada di kolom yang sama.

Angka belum ada di subgrid 3×3 yang sama.

Jika valid, angka ditaruh. Lanjut ke kotak berikutnya.

Jika buntu (tidak ada angka valid), backtrack → mundur ke kotak sebelumnya, ganti angka lain.

Proses berulang sampai semua 81 kotak terisi.

➡️ Karena angka 1–9 diacak tiap kotak, solusi penuh yang dihasilkan berbeda-beda tiap game (tetapi tetap valid).

2. Membuat puzzle dari solusi penuh

Setelah grid penuh terbentuk, sistem “menghapus” angka menjadi puzzle.

Banyaknya kotak yang dihapus tergantung tingkat kesulitan:

Easy → hapus sekitar 35 sel.

Medium → hapus sekitar 45 sel.

Hard → hapus sekitar 55 sel.

Penghapusan dilakukan secara acak dengan tetap menyisakan clue yang cukup agar puzzle bisa diselesaikan (walaupun program ini tidak melakukan pengecekan keunikan solusi—untuk kesederhanaan).

3. Interaksi pengguna

Angka yang dihapus menjadi “cell kosong” yang bisa diisi pemain.

Validasi saat check/solve menggunakan grid solusi penuh yang disimpan.

Jadi, metode utamanya:

Backtracking search (depth-first dengan constraint checking) → untuk generate solusi.

Randomized cell removal → untuk menghasilkan puzzle dengan clue.

Direct solution lookup → untuk cek jawaban pemain, solve otomatis, dan hint.
