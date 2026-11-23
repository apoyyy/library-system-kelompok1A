from buku import Buku


class Perpustakaan:
    """Mengelola koleksi objek Buku dan koordinasi penyimpanan."""

    def __init__(self, penyimpanan):
        self.koleksi_buku = {}
        self.penyimpanan = penyimpanan

    def muat_data(self):
        """Memuat dictionary dari file, memvalidasi, lalu membuat objek Buku."""
        data_tersimpan = self.penyimpanan.baca_data()
        koleksi_baru = {}

        for nomor_record, data in enumerate(data_tersimpan, start=1):
            try:
                buku = Buku(**data)
            except (TypeError, ValueError) as error:
                raise ValueError(f"Data buku pada record {nomor_record} tidak valid: {error}") from error

            if buku.kode_buku in koleksi_baru:
                raise ValueError(f"Ditemukan kode buku duplikat: {buku.kode_buku}")

            koleksi_baru[buku.kode_buku] = buku

        # Koleksi lama diganti hanya setelah seluruh record berhasil divalidasi.
        self.koleksi_buku = koleksi_baru

    def tambah_buku(self, buku: Buku) -> bool:
        if not isinstance(buku, Buku):
            raise TypeError("Data yang ditambahkan harus berupa objek Buku.")

        kode = buku.kode_buku
        if kode in self.koleksi_buku:
            raise ValueError(f"Kode buku '{kode}' sudah digunakan.")

        self.koleksi_buku[kode] = buku
        if self._simpan_koleksi():
            return True

        del self.koleksi_buku[kode]
        return False

    def cari_buku(self, kode_buku: str):
        kode = kode_buku.strip().upper()
        return self.koleksi_buku.get(kode)

    def hapus_buku(self, kode_buku: str) -> bool:
        kode = kode_buku.strip().upper()
        buku_dihapus = self.koleksi_buku.get(kode)

        if buku_dihapus is None:
            return False

        del self.koleksi_buku[kode]
        if self._simpan_koleksi():
            return True

        self.koleksi_buku[kode] = buku_dihapus
        return False

    def update_buku(self, kode_buku: str, data_baru: dict) -> bool:
        buku = self.cari_buku(kode_buku)
        if buku is None:
            return False

        # Simpan snapshot atribut yang dapat diperbarui untuk kebutuhan rollback.
        snapshot = {
            "judul": buku.judul,
            "penulis": buku.penulis,
            "penerbit": buku.penerbit,
            "tahun_terbit": buku.tahun_terbit,
            "jumlah_buku": buku.jumlah_buku,
        }

        buku.perbarui_atribut(data_baru)

        if self._simpan_koleksi():
            return True

        # Jika penulisan gagal, kembalikan seluruh atribut ke kondisi semula.
        buku.perbarui_atribut(snapshot)
        return False

    def _simpan_koleksi(self) -> bool:
        data_buku = []
        for buku in self.koleksi_buku.values():
            data_buku.append({
                "kode_buku": buku.kode_buku,
                "judul": buku.judul,
                "penulis": buku.penulis,
                "penerbit": buku.penerbit,
                "tahun_terbit": buku.tahun_terbit,
                "jumlah_buku": buku.jumlah_buku,
            })

        return self.penyimpanan.simpan_data(data_buku)
