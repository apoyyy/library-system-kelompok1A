from pathlib import Path
import os


class PenyimpananData:
    """Menangani pembacaan dan penulisan data buku dalam format TXT."""

    PEMISAH_RECORD = "---------------------"
    LABEL_KE_ATRIBUT = {
        "Kode Buku": "kode_buku",
        "Judul": "judul",
        "Penulis": "penulis",
        "Penerbit": "penerbit",
        "Tahun Terbit": "tahun_terbit",
        "Jumlah Buku": "jumlah_buku",
    }
    ATRIBUT_WAJIB = set(LABEL_KE_ATRIBUT.values())

    def __init__(self, nama_file: str):
        self.nama_file = Path(nama_file)

    def periksa_file(self):
        """Membuat file jika belum tersedia; tidak mengubah file yang sudah ada."""
        self.nama_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.nama_file.exists():
            self.nama_file.write_text("", encoding="utf-8")

    def baca_data(self) -> list:
        """Mengembalikan list dictionary. Data rusak akan menghasilkan ValueError."""
        self.periksa_file()
        isi = self.nama_file.read_text(encoding="utf-8")

        if not isi.strip():
            return []

        records = []
        record_sekarang = {}

        for nomor_baris, baris in enumerate(isi.splitlines(), start=1):
            if not baris.strip():
                raise ValueError(f"Baris kosong tidak diharapkan pada baris {nomor_baris}.")

            if baris.strip() == self.PEMISAH_RECORD:
                if not record_sekarang:
                    raise ValueError(f"Record kosong pada baris {nomor_baris}.")
                records.append(self._validasi_record(record_sekarang, len(records) + 1))
                record_sekarang = {}
                continue

            if ":" not in baris:
                raise ValueError(f"Format baris {nomor_baris} tidak valid: pemisah ':' tidak ditemukan.")

            label, nilai = baris.split(":", 1)
            label = label.strip()
            nilai = nilai.strip()

            if label not in self.LABEL_KE_ATRIBUT:
                raise ValueError(f"Label '{label}' pada baris {nomor_baris} tidak dikenal.")

            atribut = self.LABEL_KE_ATRIBUT[label]
            if atribut in record_sekarang:
                raise ValueError(f"Atribut '{label}' tercatat lebih dari sekali.")

            record_sekarang[atribut] = nilai

        # Record terakhir tidak wajib diakhiri garis pemisah.
        if record_sekarang:
            records.append(self._validasi_record(record_sekarang, len(records) + 1))

        # Konversi tipe data dasar dilakukan di lapisan penyimpanan.
        hasil = []
        for nomor_record, record in enumerate(records, start=1):
            try:
                record["tahun_terbit"] = int(record["tahun_terbit"])
                record["jumlah_buku"] = int(record["jumlah_buku"])
            except ValueError as error:
                raise ValueError(
                    f"Tahun terbit atau jumlah buku pada record {nomor_record} bukan angka yang valid."
                ) from error
            hasil.append(record)

        return hasil

    def _validasi_record(self, record: dict, nomor_record: int) -> dict:
        atribut_hilang = self.ATRIBUT_WAJIB - set(record)
        if atribut_hilang:
            daftar = ", ".join(sorted(atribut_hilang))
            raise ValueError(f"Record {nomor_record} tidak lengkap. Atribut hilang: {daftar}.")
        if set(record) != self.ATRIBUT_WAJIB:
            raise ValueError(f"Record {nomor_record} memiliki atribut yang tidak sesuai.")
        return dict(record)

    def simpan_data(self, data_buku: list) -> bool:
        """Menulis seluruh data melalui file sementara agar file lama tidak terpotong."""
        self.periksa_file()

        baris_file = []
        for data in data_buku:
            baris_file.extend([
                f"Kode Buku     : {data['kode_buku']}",
                f"Judul         : {data['judul']}",
                f"Penulis       : {data['penulis']}",
                f"Penerbit      : {data['penerbit']}",
                f"Tahun Terbit  : {data['tahun_terbit']}",
                f"Jumlah Buku   : {data['jumlah_buku']}",
                self.PEMISAH_RECORD,
            ])

        isi = "\n".join(baris_file)
        if isi:
            isi += "\n"

        file_sementara = self.nama_file.with_name(self.nama_file.name + ".tmp")
        try:
            file_sementara.write_text(isi, encoding="utf-8")
            os.replace(file_sementara, self.nama_file)
            return True
        except OSError:
            try:
                if file_sementara.exists():
                    file_sementara.unlink()
            except OSError:
                pass
            return False
