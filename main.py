from penyimpanan import PenyimpananData
from perpustakaan import Perpustakaan
from aplikasi import Aplikasi


def main():
    penyimpanan = PenyimpananData("data_buku.txt")
    perpustakaan = Perpustakaan(penyimpanan)

    try:
        penyimpanan.periksa_file()
        perpustakaan.muat_data()
    except (OSError, UnicodeError, ValueError) as error:
        print("\n[!] Aplikasi tidak dapat dijalankan karena data penyimpanan bermasalah.")
        print(f"Detail: {error}")
        print("Periksa file data_buku.txt terlebih dahulu. File tidak akan ditimpa otomatis.")
        return

    aplikasi = Aplikasi(perpustakaan)
    aplikasi.jalankan()


if __name__ == "__main__":
    main()
