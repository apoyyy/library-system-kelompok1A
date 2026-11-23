from buku import Buku


class Aplikasi:
    """Mengelola seluruh interaksi pengguna melalui console."""

    def __init__(self, perpustakaan):
        self.perpustakaan = perpustakaan

    def jalankan(self):
        while True:
            self.tampilkan_menu()
            pilihan = input("Pilih menu (1-5): ").strip()

            if pilihan == "1":
                self.menu_tambah_buku()
            elif pilihan == "2":
                self.menu_cari_buku()
            elif pilihan == "3":
                self.menu_hapus_buku()
            elif pilihan == "4":
                self.menu_update_buku()
            elif pilihan == "5":
                print("\nTerima kasih telah menggunakan Aplikasi Pengelolaan Buku Perpustakaan.")
                break
            else:
                print("\n[!] Pilihan tidak tersedia. Silakan pilih angka 1 sampai 5.")

            input("\nTekan Enter untuk kembali ke menu...")

    def tampilkan_menu(self):
        print("\n" + "=" * 48)
        print("           APLIKASI PENGELOLAAN BUKU")
        print("=" * 48)
        print("1. Tambah Buku")
        print("2. Cari Buku")
        print("3. Hapus Buku")
        print("4. Update Buku")
        print("5. Keluar")
        print("=" * 48)

    def menu_tambah_buku(self):
        print("\n========== TAMBAH BUKU ==========")
        try:
            kode = self._input_teks("Kode Buku    : ").upper()
            judul = self._input_teks("Judul        : ")
            penulis = self._input_teks("Penulis      : ")
            penerbit = self._input_teks("Penerbit     : ")
            tahun = self._input_integer("Tahun Terbit : ")
            jumlah = self._input_integer("Jumlah Buku  : ")

            buku = Buku(kode, judul, penulis, penerbit, tahun, jumlah)
            if self.perpustakaan.tambah_buku(buku):
                print("\n[✓] Buku berhasil ditambahkan dan disimpan.")
            else:
                print("\n[!] Buku tidak berhasil disimpan. Koleksi dikembalikan ke kondisi semula.")
        except (ValueError, TypeError) as error:
            print(f"\n[!] Gagal menambahkan buku: {error}")
        except OSError as error:
            print(f"\n[!] Terjadi masalah pada file: {error}")

    def menu_cari_buku(self):
        print("\n========== CARI BUKU ==========")
        kode = self._input_teks("Masukkan kode buku: ").upper()
        buku = self.perpustakaan.cari_buku(kode)

        if buku:
            print("\n[✓] Buku ditemukan:")
            self._tampilkan_detail_buku(buku)
        else:
            print(f"\n[!] Buku dengan kode '{kode}' tidak ditemukan.")

    def menu_hapus_buku(self):
        print("\n========== HAPUS BUKU ==========")
        kode = self._input_teks("Masukkan kode buku: ").upper()
        buku = self.perpustakaan.cari_buku(kode)

        if buku is None:
            print(f"\n[!] Buku dengan kode '{kode}' tidak ditemukan.")
            return

        print("\nBuku yang akan dihapus:")
        self._tampilkan_detail_buku(buku)
        konfirmasi = input("\nYakin ingin menghapus buku ini? (y/n): ").strip().lower()

        if konfirmasi != "y":
            print("\nPenghapusan dibatalkan.")
            return

        if self.perpustakaan.hapus_buku(kode):
            print("\n[✓] Buku berhasil dihapus.")
        else:
            print("\n[!] Penghapusan gagal disimpan. Data buku dikembalikan.")

    def menu_update_buku(self):
        print("\n========== UPDATE BUKU ==========")
        kode = self._input_teks("Masukkan kode buku: ").upper()
        buku = self.perpustakaan.cari_buku(kode)

        if buku is None:
            print(f"\n[!] Buku dengan kode '{kode}' tidak ditemukan.")
            return

        print("\nData buku saat ini:")
        self._tampilkan_detail_buku(buku)
        print("\nKosongkan input jika atribut tidak ingin diubah.")

        data_baru = {}
        teks_fields = {
            "judul": "Judul baru",
            "penulis": "Penulis baru",
            "penerbit": "Penerbit baru",
        }

        for atribut, label in teks_fields.items():
            nilai = input(f"{label} ({getattr(buku, atribut)}): ").strip()
            if nilai:
                data_baru[atribut] = nilai

        tahun = input(f"Tahun terbit baru ({buku.tahun_terbit}): ").strip()
        if tahun:
            try:
                data_baru["tahun_terbit"] = int(tahun)
            except ValueError:
                print("\n[!] Tahun terbit harus berupa bilangan bulat. Tidak ada perubahan yang disimpan.")
                return

        jumlah = input(f"Jumlah buku baru ({buku.jumlah_buku}): ").strip()
        if jumlah:
            try:
                data_baru["jumlah_buku"] = int(jumlah)
            except ValueError:
                print("\n[!] Jumlah buku harus berupa bilangan bulat. Tidak ada perubahan yang disimpan.")
                return

        if not data_baru:
            print("\nTidak ada atribut yang diubah.")
            return

        try:
            if self.perpustakaan.update_buku(kode, data_baru):
                print("\n[✓] Seluruh perubahan berhasil diperbarui dan disimpan.")
            else:
                print("\n[!] Update gagal disimpan. Seluruh perubahan dikembalikan.")
        except (ValueError, TypeError) as error:
            print(f"\n[!] Update dibatalkan: {error}")

    def _input_teks(self, pesan: str) -> str:
        while True:
            nilai = input(pesan).strip()
            if nilai:
                return nilai
            print("[!] Input tidak boleh kosong.")

    def _input_integer(self, pesan: str) -> int:
        while True:
            nilai = input(pesan).strip()
            try:
                return int(nilai)
            except ValueError:
                print("[!] Masukkan bilangan bulat yang valid.")

    def _tampilkan_detail_buku(self, buku: Buku):
        print("-" * 39)
        print(f"Kode Buku     : {buku.kode_buku}")
        print(f"Judul         : {buku.judul}")
        print(f"Penulis       : {buku.penulis}")
        print(f"Penerbit      : {buku.penerbit}")
        print(f"Tahun Terbit  : {buku.tahun_terbit}")
        print(f"Jumlah Buku   : {buku.jumlah_buku}")
        print("-" * 39)
