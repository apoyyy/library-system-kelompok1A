class Buku:
    """Merepresentasikan satu buku beserta validasi atributnya."""

    ATRIBUT_YANG_BOLEH_DIUBAH = {
        "judul",
        "penulis",
        "penerbit",
        "tahun_terbit",
        "jumlah_buku",
    }

    def __init__(
        self,
        kode_buku: str,
        judul: str,
        penulis: str,
        penerbit: str,
        tahun_terbit: int,
        jumlah_buku: int,
    ):
        data = {
            "kode_buku": kode_buku,
            "judul": judul,
            "penulis": penulis,
            "penerbit": penerbit,
            "tahun_terbit": tahun_terbit,
            "jumlah_buku": jumlah_buku,
        }

        # Semua atribut divalidasi sebelum objek selesai dibuat.
        for nama_atribut, nilai in data.items():
            self.validasi_atribut(nama_atribut, nilai)

        self.__kode_buku = kode_buku.strip().upper()
        self.__judul = judul.strip()
        self.__penulis = penulis.strip()
        self.__penerbit = penerbit.strip()
        self.__tahun_terbit = tahun_terbit
        self.__jumlah_buku = jumlah_buku

    @staticmethod
    def validasi_atribut(nama_atribut: str, nilai) -> bool:
        """Memvalidasi satu atribut; ValueError diberikan jika tidak valid."""
        atribut_teks = {"kode_buku", "judul", "penulis", "penerbit"}

        if nama_atribut in atribut_teks:
            if not isinstance(nilai, str) or not nilai.strip():
                raise ValueError(f"{nama_atribut.replace('_', ' ').title()} tidak boleh kosong.")
            if "\n" in nilai or "\r" in nilai:
                raise ValueError("Data teks tidak boleh mengandung baris baru.")

        elif nama_atribut == "tahun_terbit":
            if type(nilai) is not int:
                raise ValueError("Tahun terbit harus berupa bilangan bulat.")
            if not 2000 <= nilai <= 2026:
                raise ValueError("Tahun terbit harus berada pada rentang 2000 sampai 2026.")

        elif nama_atribut == "jumlah_buku":
            if type(nilai) is not int:
                raise ValueError("Jumlah buku harus berupa bilangan bulat.")
            if nilai <= 0:
                raise ValueError("Jumlah buku harus lebih dari 0.")

        else:
            raise ValueError(f"Atribut '{nama_atribut}' tidak dikenal.")

        return True

    def perbarui_atribut(self, data_baru: dict) -> bool:
        """Memvalidasi semua perubahan lebih dahulu, lalu menerapkannya sekaligus."""
        if not isinstance(data_baru, dict) or not data_baru:
            raise ValueError("Data perubahan tidak boleh kosong.")

        # Tahap 1: pastikan semua atribut boleh diubah dan seluruh nilai valid.
        for nama_atribut, nilai in data_baru.items():
            if nama_atribut not in self.ATRIBUT_YANG_BOLEH_DIUBAH:
                raise ValueError(
                    f"Atribut '{nama_atribut}' tidak dapat diperbarui. "
                    "Kode buku tidak dapat diubah."
                )
            self.validasi_atribut(nama_atribut, nilai)

        # Tahap 2: terapkan setelah seluruh validasi berhasil.
        for nama_atribut, nilai in data_baru.items():
            setattr(self, f"_Buku__{nama_atribut}", nilai.strip() if isinstance(nilai, str) else nilai)

        return True

    @property
    def kode_buku(self):
        return self.__kode_buku

    @property
    def judul(self):
        return self.__judul

    @property
    def penulis(self):
        return self.__penulis

    @property
    def penerbit(self):
        return self.__penerbit

    @property
    def tahun_terbit(self):
        return self.__tahun_terbit

    @property
    def jumlah_buku(self):
        return self.__jumlah_buku
