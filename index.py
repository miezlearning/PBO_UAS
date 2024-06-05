# Selamat Datang di Program Yayasan Budi Pekerti


# ━━━━━━━━━━━━━━━━━━━━━━━━ IMPORT MODULE ━━━━━━━━━━━━━━━━━━━━━━━━ 

# Modul Password Char
import datetime
from pwinput import pwinput as enkripsi_password
# Modul Fitur Tambahan
from etc.fitur_tambahan import validasi_email, kirim_forgot_account, pembersih, lanjut, org_chart, menu_navigasi, kalkulatorzakat, top_up, info,berhasil, donasi_berhasil, error, info, loading_bar
# Modul Fitur Class
from etc.fitur_tambahan import Database, AutoDonasi, warna
# Modul Header
import etc.header as hd
# Modul GUI
import tkinter as tk
from tkinter import messagebox
# Modul Tabel
from tabulate import tabulate
import textwrap





# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━





# <> Inisialisasi Modul database.
db = Database()


# ━━━━━━━━━━━━━━━━━━━━━━━━ CLASS STRUCTURE ━━━━━━━━━━━━━━━━━━━━━━━━ 
class User:
    def __init__(self, user_id, username, password):
        self.__id = user_id
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password
    
    def get_id(self):
        return self.__id


class Donatur(User):
    def __init__(self, user_id, nama, username, password, notelp, email, dompet=0):
        super().__init__(user_id, username, password)
        self.__notelp = notelp
        self.__nama = nama
        self.__email = email
        self.__dompet = dompet
        self.__password = password
        self.cek_login = True
        self.auto_donasi = None

    def get_notelp(self):
        return self.__notelp
    
    def get_nama(self):
        return self.__nama
    
    def get_email(self):
        return self.__email
    
    def get_dompet(self):
        return self.__dompet
    
    def get_password(self):
        return self.__password
    
    def set_dompet(self, dompet):
        self.__dompet = dompet
    
    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_auto_donasi(self, auto_donasi):
        self.auto_donasi = auto_donasi

    def get_auto_donasi(self):
        return self.auto_donasi

    def logout(self):
        if self.auto_donasi:
            self.auto_donasi.stop()  
        self.cek_login = False

    def cek_dompet(self):
        print(f"Saldo dompet Anda adalah: {self.__dompet}.")
    
    def kurangi_dompet(self, nominal_kurang):
        self.__dompet -= nominal_kurang


class Admin(User):
    def __init__(self, user_id, nama, username, password, dompet=0):
        super().__init__(user_id, username, password)
        self.__nama = nama
        self.__dompet = dompet
        self.cek_login = True
    
    def get_nama(self):
        return self.__nama
    
    def get_dompet(self):
        return self.__dompet
    
    def set_dompet(self, dompet):
        self.__dompet = dompet

    def logout(self):
        self.cek_login = False



# =====================================
# Program Yayasan
# =====================================
class Program:
    def __init__(self, nama, deskripsi, target_donasi, donasi_terkumpul, tenggat):
        self._nama = nama
        self._deskripsi = deskripsi
        self._target_donasi = target_donasi
        self._donasi_terkumpul = donasi_terkumpul
        self._tenggat = tenggat

    # Getters
    def get_nama(self):
        return self._nama

    def get_deskripsi(self):
        return self._deskripsi

    def get_target_donasi(self):
        return self._target_donasi

    def get_donasi_terkumpul(self):
        return self._donasi_terkumpul

    def get_tenggat(self):
        return self._tenggat
    
    def tambah_donasi(self, jumlah):
        self._donasi_terkumpul += jumlah

    def cek_terpenuhi_program(self):
        return self._donasi_terkumpul >= self._target_donasi

    def __str__(self):
        return (f"Nama Program: {self._nama}\n"
                f"Deskripsi: {self._deskripsi}\n"
                f"Target Donasi: {self._target_donasi}\n"
                f"Donasi Terkumpul: {self._donasi_terkumpul}\n"
                f"Tenggat: {self._tenggat}\n")

    
class ProgramManager:
    def __init__(self, db):
        self.db = db

    def tambah_program(self, program):
        query = """
        INSERT INTO programs (nama, deskripsi, target_donasi, donasi_terkumpul, tenggat)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            program.get_nama(),
            program.get_deskripsi(),
            program.get_target_donasi(),
            program.get_donasi_terkumpul(),
            program.get_tenggat()
        )
        result = self.db.query(query, params)
        if result is not None:
            berhasil("Program berhasil ditambahkan.")
        else:
            error("Gagal menambahkan program.")

    def lihat_program(self):
        query = "SELECT id_program, nama FROM programs"
        result = self.db.query(query)
        return result

    def lihat_detail_program(self, idx):
        query = "SELECT nama, deskripsi, target_donasi, donasi_terkumpul, tenggat FROM programs WHERE id_program = %s"
        result = self.db.query(query, (idx,))
        if result:
            program = Program(*result[0])
            print(program)
            return program
        else:
            error("Program tidak ditemukan.")
            return None

    def update_donasi_terkumpul(self, program_id, jumlah):
        query = "UPDATE programs SET donasi_terkumpul = donasi_terkumpul + %s WHERE id_program = %s"
        result = self.db.query(query, (jumlah, program_id))
        if result is not None:
            pass

    def catat_donasi(self, id_akun, id_program, jumlah, nama_donatur, pesan):
        query = """
        INSERT INTO donasi (id_akun, id_program, jumlah_donasi, nama_donatur, pesan)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_akun, id_program, jumlah, nama_donatur, pesan)
        result = self.db.query(query, params)
        if result is not None:
            pass
 
    
    def lihat_histori_donasi(self, id_program):
        query = """
        SELECT nama_donatur, pesan, jumlah_donasi, tanggal_donasi
        FROM donasi
        WHERE id_program = %s
        ORDER BY tanggal_donasi DESC
        """
        result = self.db.query(query, (id_program,))
        return result if result else []

    def edit_program(self, idx, **kwargs):
        set_clause = ", ".join([f"{key} = %s" for key in kwargs])
        params = list(kwargs.values()) + [idx]
        query = f"UPDATE programs SET {set_clause} WHERE id_program = %s"
        self.db.query(query, params)

    def hapus_program(self, idx):
        window = tk.Tk()
        window.title("Konfirmasi Hapus")
        
        label = tk.Label(window, text="Apakah Anda yakin ingin menghapus program ini?")
        label.pack(pady=(25, 10))
        
        def hapus():
            query = "DELETE FROM programs WHERE id_program = %s"
            self.db.query(query, (idx,))
            messagebox.showinfo("Informasi", "Program berhasil dihapus.")
            window.destroy()
        
        def batal():
            messagebox.showinfo("Informasi", "Penghapusan program dibatalkan.")
            window.destroy()

        def tombol_ya_enter(event):
            hapus_button.config(bg="green")

        def tombol_ya_leave(event):
            hapus_button.config(bg="SystemButtonFace")

        def tombol_tidak_enter(event):
            batal_button.config(bg="red")

        def tombol_tidak_leave(event):
            batal_button.config(bg="SystemButtonFace")
        
        hapus_button = tk.Button(window, text="Ya", command=hapus)
        hapus_button.pack(side=tk.LEFT, pady=25, padx=65)
        hapus_button.bind("<Enter>", tombol_ya_enter)
        hapus_button.bind("<Leave>", tombol_ya_leave)

        batal_button = tk.Button(window, text="Tidak", command=batal)
        batal_button.pack(side=tk.RIGHT, pady=25, padx=65)
        batal_button.bind("<Enter>", tombol_tidak_enter)
        batal_button.bind("<Leave>", tombol_tidak_leave)

        
        
        window.mainloop()

# ====================================
# Anak Asuh
# ====================================
class AdikAsuh:
    def __init__(self, id_adikasuh, nama, tempat_tinggal, umur, kebutuhan, status='Belum di Asuh', target_donasi=0.00, donasi_terkumpul=0.00):
        self._nama = nama
        self._tempat_tinggal = tempat_tinggal
        self._umur = umur
        self.__id_adikasuh = id_adikasuh
        self.__status = status
        self._kebutuhan = kebutuhan
        self._target_donasi = target_donasi
        self._donasi_terkumpul = donasi_terkumpul

    # Getters
    def get_nama(self):
        return self._nama

    def get_tempat_tinggal(self):
        return self._tempat_tinggal

    def get_umur(self):
        return self._umur

    def get_kebutuhan(self):
        return self._kebutuhan
    
    def get_id_adikasuh(self):
        return self.__id_adikasuh
    
    def get_status(self):
        return self.__status

    def get_target_donasi(self):
        return self._target_donasi

    def get_donasi_terkumpul(self):
        return self._donasi_terkumpul

    # Setters
    def set_nama(self, nama):
        self._nama = nama

    def set_tempat_tinggal(self, tempat_tinggal):
        self._tempat_tinggal = tempat_tinggal

    def set_umur(self, umur):
        self._umur = umur

    def set_kebutuhan(self, kebutuhan):
        self._kebutuhan = kebutuhan
    
    def set_status(self, status):
        self.__status = status

    def set_target_donasi(self, target_donasi):
        self._target_donasi = target_donasi

    def set_donasi_terkumpul(self, donasi_terkumpul):
        self._donasi_terkumpul = donasi_terkumpul

    def __str__(self):
        return (f"Nama: {self._nama}\n"
                f"Tempat Tinggal: {self._tempat_tinggal}\n"
                f"Umur: {self._umur}\n"
                f"Kebutuhan: {self._kebutuhan}\n"
                f"Status: {self.__status}\n"
                f"Target Donasi: {self._target_donasi}\n"
                f"Donasi Terkumpul: {self._donasi_terkumpul}\n")



class AdikAsuhManager:
    def __init__(self, db):
        self.db = db

    def tambah_anak(self, anak):
        query = "INSERT INTO adik_asuh (nama, tempat_tinggal, umur, kebutuhan, status, target_donasi, donasi_terkumpul) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (anak.get_nama(), anak.get_tempat_tinggal(), anak.get_umur(), anak.get_kebutuhan(), anak.get_status(), anak.get_target_donasi(), anak.get_donasi_terkumpul())
        self.db.query(query, values)


    def lihat_anak(self):
        query = "SELECT id, nama, status FROM adik_asuh"
        return self.db.query(query)

    def lihat_detail_anak(self, id):
        query = "SELECT * FROM adik_asuh WHERE id = %s"
        result = self.db.query(query, (id,))
        if result:
            anak = AdikAsuh(*result[0])
            print(anak)
        else:
            print("Anak Asuh tidak ditemukan.")

    def edit_anak(self, id, **kwargs):
        query = "UPDATE adik_asuh SET "
        values = []
        for key, value in kwargs.items():
            query += f"{key} = %s, "
            values.append(value)
        query = query.rstrip(", ") + " WHERE id = %s"
        values.append(id)
        self.db.query(query, tuple(values))

    def hapus_anak(self, id):
        query = "DELETE FROM adik_asuh WHERE id = %s"
        self.db.query(query, (id,))

    def pilih_anak_asuh(self, donatur_id, anak_id):
        query = "INSERT INTO donatur_anak_asuh (donatur_id, anak_id) VALUES (%s, %s)"
        self.db.query(query, (donatur_id, anak_id))
        
        query = "UPDATE adik_asuh SET status = 'Sudah di Asuh' WHERE id = %s"
        self.db.query(query, (anak_id,))

    def lihat_donatur_dan_anak_asuh(self):
        query = """
        SELECT d.nama, a.nama, a.kebutuhan
        FROM donatur_anak_asuh da
        JOIN akun d ON da.donatur_id = d.id_akun
        JOIN adik_asuh a ON da.anak_id = a.id
        """
        return self.db.query(query)
    
    def cek_donatur_memiliki_anak(self, donatur_id):
        query = "SELECT COUNT(*) FROM donatur_anak_asuh WHERE donatur_id = %s"
        params = (donatur_id,)
        result = db.query(query, params)
        return result[0][0] > 0
    
    def lihat_anak_asuh_donatur(self, donatur_id):
        query = """
        SELECT a.id, a.nama, a.status
        FROM adik_asuh a
        JOIN donatur_anak_asuh da ON a.id = da.anak_id
        WHERE da.donatur_id = %s
        """
        params = (donatur_id,)
        return db.query(query, params)

    def bayar_kebutuhan_anak(self, donatur_id, anak_id, jumlah):
        query = "UPDATE adik_asuh SET donasi_terkumpul = donasi_terkumpul + %s WHERE id = %s"
        self.db.query(query, (jumlah, anak_id))

        query = "SELECT donasi_terkumpul, target_donasi FROM adik_asuh WHERE id = %s"
        result = self.db.query(query, (anak_id,))
        if result and result[0][0] >= result[0][1]:
            query = "DELETE FROM donatur_anak_asuh WHERE anak_id = %s"
            self.db.query(query, (anak_id,))
            
            query = "DELETE FROM adik_asuh WHERE id = %s"
            self.db.query(query, (anak_id,))
            return True  
        return False  





program_manager = ProgramManager(db)
adik_asuh_manager = AdikAsuhManager(db)



# ━━━━━━━━━━━━━━━━━━━━━━━━ LOGIN PAGE STRUCTURE ━━━━━━━━━━━━━━━━━━━━━━━━ 


def menuLogin():
    menu = ["• Login", "• Register", "• Forgot Account", "• Exit"]
    info_message = f"Gunakan keyboard kamu untuk memilih menu dan tekan ENTER.\n"
    header = hd.headerMenuUtama()
    while True:
        selected_index = menu_navigasi(header, menu, info_message, info)
        if selected_index == 0:
            login()
        elif selected_index == 1:
            register()
        elif selected_index == 2:
            forgot_account()
        elif selected_index == 3:
            exit(0)

def login():
    maks = 3
    percobaan = 0
    while percobaan < maks:
        options = ["1", "2", "3"]
        menu_items = ["• Username", "• No Telepon", "• Kembali"]
        header = hd.SubheaderMenuUtama_Login()
        selected_index = menu_navigasi(header, menu_items)
        if selected_index == -1 or selected_index >= len(options):
            error("Pilihan tidak valid.")
            continue
        
        pilihan = options[selected_index]
        
        if pilihan == "3":
            print("Kembali ke menu utama.")
            break
        
        if pilihan == "1":
            tipe_kredensial = "Username"
        elif pilihan == "2":
            tipe_kredensial = "No Telp"
        
        credential = input(f"{warna.biru+warna.bold}Masukkan {tipe_kredensial} > {warna.reset}")
        if not credential:
            error("Inputan tidak boleh kosong.")
            continue
        password = enkripsi_password(prompt=f"{warna.biru+warna.bold}Masukkan Password > {warna.reset}", mask="•")
        if not password:
            error("Password tidak boleh kosong.")
            continue

        if tipe_kredensial == "No Telp":
            tipe_kredensial = "notelp"
        elif tipe_kredensial == "Username":
            tipe_kredensial = "username"
        
        try:
            kueri = db.query(f"SELECT id_akun, nama, username, password, role, notelp, email, dompet FROM akun WHERE {tipe_kredensial} = '{credential}' AND password = '{password}'")
            if not kueri:   
                error(f"{tipe_kredensial} atau password yang dimasukkan salah.")
                lanjut()
                percobaan += 1
            else:
                role = kueri[0][4]
                if role == "Donatur":
                    loading_bar()
                    donatur = Donatur(kueri[0][0], kueri[0][1], kueri[0][2], password, kueri[0][5], kueri[0][6], kueri[0][7])# << 
                    menuDonatur(donatur) 
                elif role == "Admin":
                    loading_bar()
                    admin = Admin(kueri[0][0], kueri[0][1], kueri[0][2], password, kueri[0][7])
                    menuAdmin(admin)
                else:
                    error("Role tidak valid.")
                break
        except Exception as e:
            error(f"Terjadi kesalahan saat melakukan login: {e}")
            lanjut()

    if percobaan == maks:
        print("Anda telah melebihi batas percobaan login. Silakan coba lagi nanti.")
        lanjut()




  
def register():
    while True:
        pembersih()
        header = hd.SubheaderMenuUtama_Register()
        print(header)
        nama = input(f"{warna.biru+warna.bold}Masukkan Nama Lengkap > {warna.reset}")
        if not nama:
            error("Nama tidak boleh kosong.")
            lanjut()
            continue
        username = input(f"{warna.biru+warna.bold}Masukkan Username > {warna.reset}")
        if not username:
            error("Username tidak boleh kosong.")
            lanjut()
            continue
        cek_username = db.query(f"SELECT * FROM akun WHERE username = '{username}'")
        if cek_username:
            error("Username sudah digunakan. Silakan coba dengan data yang berbeda.")
            lanjut()
            continue
        password = enkripsi_password(prompt=f"{warna.biru+warna.bold}Masukkan Password > {warna.reset}", mask="•")
        if not password:
            error("Password tidak boleh kosong.")
            lanjut()
            continue
        notelp = input(f"{warna.biru+warna.bold}Masukkan No Telepon > {warna.reset}")
        if not notelp:
            error("Nomor telepon tidak boleh kosong.")
            lanjut()
            continue
        cek_notelp = db.query(f"SELECT * FROM akun WHERE notelp = '{notelp}'")
        if cek_notelp:
            error("Nomor telepon sudah digunakan. Silakan coba dengan data yang berbeda.")
            lanjut()
            continue
        percobaan_email = True
        while percobaan_email:
            email = input(f"{warna.biru+warna.bold}Masukkan Email > {warna.reset}")
            if validasi_email(email):
                percobaan_email = False
            else:
                error("Email tidak valid. Coba masukkan kembali.") 

        cek_email = db.query(f"SELECT * FROM akun WHERE email = '{email}'")
        if cek_email:
            info("Email sudah digunakan. Silakan coba dengan data yang berbeda.")
            lanjut()
            continue

        try:
            donatur = Donatur(None, nama, username, password, notelp, email, 0)
            db.query(f"INSERT INTO akun(nama, username, password, notelp, role, email, dompet) VALUES ('{donatur.get_nama()}','{donatur.get_username()}', '{donatur.get_password()}', '{donatur.get_notelp()}', 'Donatur', '{donatur.get_email()}', {donatur.get_dompet()})")
            berhasil("Berhasil Daftar...")
            lanjut()
            break  
        except Exception as e:
            error(f"Terjadi kesalahan saat melakukan register: {e}")
            lanjut()

    
    
def forgot_account():
    while True:
        menu = ['• Forgot Username', '• Forgot Password', '• Forgot No Telepon', '• Kembali']
        header = hd.SubheaderMenuUtama_ForgotAccount()
        selected_index = menu_navigasi(header, menu)
        if selected_index == 0:
            forgot_username()
        elif selected_index == 1:
            forgot_password()
        elif selected_index == 2:
            forgot_no_telepon()
        elif selected_index == 3:
            menuLogin()
            return False

            

def forgot_username():
    while True:
        pembersih()
        header = hd.SubheaderMenuUtama_Username()
        print(header)
        notelp = input(f"{warna.biru+warna.bold}Masukkan No Telepon > {warna.reset}")
        if not notelp:
            error("No Telepon tidak boleh kosong.")
            continue
        try:
            cari_username = db.query(f"SELECT nama, username, password, notelp, email FROM akun WHERE notelp = '{notelp}'")
            if cari_username:
                nama, username, password, notelp, email = cari_username[0]
                if validasi_email(email):
                    kirim_forgot_account(nama, username, password, notelp, email)
                    berhasil("Informasi akun telah dikirim ke email Anda.")
                    return False
                else:
                    error("Email tidak valid.")
            else:
                info("Nomor telepon tidak ditemukan.")
        except Exception as e:
            error(f"Terjadi kesalahan saat melakukan pencarian username: {e}")

        
def forgot_password():
    while True:
        menu = ['• Dengan Username', '• Dengan No Telepon','• Kembali']
        header = hd.SubheaderMenuUtama_Password()
        pilih_metode = menu_navigasi(header, menu)
        if pilih_metode == 0:
            while True:
                username = input(f"{warna.biru+warna.bold}Masukkan Username > {warna.reset}")
                if not username:
                    error("Inputan tidak boleh kosong.")
                    continue
                try:
                    cari_username = db.query(f"SELECT nama, username, password, notelp, email FROM akun WHERE username = '{username}'")
                    if cari_username:
                        nama, username, password, notelp, email = cari_username[0]
                        if validasi_email(email):
                            kirim_forgot_account(nama, username, password, notelp, email)
                            berhasil("Informasi akun telah dikirim ke email Anda.")
                            return False
                        else:
                            error("Email tidak valid.")
                    else:
                        info("Username tidak ditemukan.")
                except Exception as e:
                    error(f"Terjadi kesalahan saat mencari password berdasarkan username: {e}")

        elif pilih_metode == 1:
            while True:
                notelp = input(f"{warna.biru+warna.bold}Masukkan No Telepon > {warna.reset}")
                if not pilih_metode:
                    print("Inputan tidak boleh kosong.")
                    continue
                try:
                    cari_notelp = db.query(f"SELECT nama, username, password, notelp, email FROM akun WHERE notelp = '{notelp}'")
                    if cari_notelp:
                        nama, username, password, notelp, email = cari_notelp[0]
                        if validasi_email(email):
                            kirim_forgot_account(nama, username, password, notelp, email)
                            print("Informasi akun telah dikirim ke email Anda.")
                            return False
                        else:
                            print("Email tidak valid.")
                    else:
                        print("No Telepon tidak ditemukan.")
                except Exception as e:
                    print(f"Terjadi kesalahan saat mencari password berdasarkan no telepon: {e}")
        elif pilih_metode == 2:
            forgot_account()
            return False

        

def forgot_no_telepon():
    while True:
        pembersih()
        header = hd.SubheaderMenuUtama_NoTelp()
        print(header)
        username = input(f"{warna.biru+warna.bold}Masukkan Username > {warna.reset}")
        if not username:
            error("Inputan tidak boleh kosong.")
        try:
            cari_notelp = db.query(f"SELECT nama, username, password, notelp, email FROM akun WHERE username = '{username}'")
            if cari_notelp:
                nama, username, password, notelp, email = cari_notelp[0]
                if validasi_email(email):
                    kirim_forgot_account(nama, username, password, notelp, email)
                    berhasil("Informasi akun telah dikirim ke email Anda.")
                    return False
                else:
                    error("Email tidak valid.")
            else:
                info("Username tidak ditemukan.")
        except Exception as e:
            error(f"Terjadi kesalahan saat mencari nomor telepon berdasarkan username: {e}")
       



# ━━━━━━━━━━━━━━━━━━━━━━━━ USER STRUCTURE ━━━━━━━━━━━━━━━━━━━━━━━━ 


def menuDonatur(donatur):
    while donatur.cek_login:
        header = hd.headerMenuDonatur(donatur)
        info_message = "Gunakan keyboard kamu untuk memilih menu dan tekan ENTER.\n"
        menu = ['• Tentang Kami', '• Program Kami', '• Donasi', '• Donasi Otomatis', '• Adik Asuh', '• Dompet', '• Pengaturan Akun', '• Logout']

        pilihan = menu_navigasi(header, menu, info_message, info)

        if pilihan == 0:
            TentangKami()
        elif pilihan == 1:
            UserProgramKami()
        elif pilihan == 2:
            donasiProgram(donatur)
        elif pilihan == 3:
            DonasiOtomatis(donatur, program_manager)
        elif pilihan == 4:
            menu_AdikAsuh(donatur, adik_asuh_manager)
        elif pilihan == 5:
            menuDompet(donatur)
            lanjut()
        elif pilihan == 6:
            pengaturan_akun(donatur)
        elif pilihan == 7:
            donatur.logout()
        else:
            break

      

def proses_donasiOtomatis(donatur, program_manager):
    auto_donasi = donatur.get_auto_donasi()

    info_message = f"Perlu diperhatikan dompet yang kamu masukkan akan terus berdonasi, bisa dihentikan ketika logout atau hentikan manual.\n"
    header = hd.Subheader_MenuDonasiOtomatis()
    if auto_donasi and auto_donasi.active:
        menu = ['• Hentikan Donasi Otomatis', '• Kembali']
        info_message1 = f'Donasi otomatis akan berhenti jika kamu logout.'
        pilihan = menu_navigasi(header, menu, info_message1, info)
        if pilihan == 0:
            auto_donasi.stop()
            donatur.set_auto_donasi(None)  
            print("Donasi otomatis dihentikan.")
            lanjut()
        return

    programs = program_manager.lihat_program()
    options = ["• " + nama for id, nama in programs] + ["• Kembali"]
    pilihan = menu_navigasi(header, options, info_message, info)

    if pilihan == len(programs):
        return

    if pilihan < len(programs):
        program_id = programs[pilihan][0]
        program = program_manager.lihat_detail_program(program_id)
        if program:
            if program.cek_terpenuhi_program():
                print("Target donasi untuk program ini sudah terpenuhi. Anda tidak bisa melakukan donasi lagi.")
                lanjut()
                return
            else:
                while True:
                    try:
                        jumlah = int(input(f"{warna.biru+warna.bold}Masukkan Jumlah Donasi > {warna.reset}").strip())
                        if jumlah <= 0:
                            error("Jumlah donasi tidak bisa kurang dari 0.")
                            continue
                        if auto_donasi:
                            auto_donasi.stop()  
                        auto_donasi = AutoDonasi(donatur, program_manager, program_id, jumlah)
                        auto_donasi.start()
                        donatur.set_auto_donasi(auto_donasi)  
                        print("Donasi otomatis dimulai.")
                        lanjut()
                        break
                    except ValueError:
                        error("Inputan harus berupa angka atau inputan tidak valid.")
    



def DonasiOtomatis(donatur, program_manager):
    while True:
        header = hd.headerDonasiOtomatis()
        menu = ['• Donasi Otomatis', '• Kalkulator Zakat', '• Kembali']
        info_message = f'{donatur.get_dompet()} ini adalah sisa dompet kamu'
        pilihan = menu_navigasi(header, menu,info_message, info)

        if pilihan == 0:
            proses_donasiOtomatis(donatur, program_manager)
        elif pilihan == 1:
            kalkulatorzakat()
        elif pilihan == 2:
            break
        else:
            break


def TentangKami():

    while True:
        menu = ['• Profil', '• Visi & Misi', '• Tujuan', '• Struktur Pengurus', '• Laporan Keuangan', '• Kembali']
        header = hd.headerTentangKamiUtama()
        pilihan  = menu_navigasi(header, menu)
        
        if pilihan == 0:
            profil()
        elif pilihan == 1:
            visi_misi()
        elif pilihan == 2:
            tujuan()
        elif pilihan == 3:
            struktur_pengurus()
        elif pilihan == 4:
            laporan_keuangan(program_manager) 
        elif pilihan == 5:
            break
        else:
            error("Pilihan tidak valid.")
            lanjut()


def profil():
    pembersih()
    header = hd.SubheaderTentangKami_Profil()
    print(header)
    
    profil_text = '''
Yayasan kami didirikan untuk memberikan dukungan dan pendidikan bagi anak-anak yang kurang beruntung, menciptakan lingkungan yang penuh kasih dan mendukung perkembangan optimal mereka.
Aplikasi ini memiliki berbagai fitur untuk memudahkan Anda, seperti halaman login yang lengkap dengan opsi register, pemulihan akun, pemulihan kata sandi nama pengguna, dan nomor telepon yang terlupakan.
Menu utama untuk pengguna mencakup informasi tentang kami, profil yayasan, visi, misi, tujuan, struktur pengurus, dan laporan keuangan. Selain itu, Anda dapat menjelajahi program kami, melakukan donasi, mengikuti donasi mingguan, dan mendukung program adik asuh.
Bagi admin, tersedia fitur manajemen program donasi yang mencakup tambah, edit, hapus, lihat, dan konfirmasi program donasi. Juga ada manajemen adik asuh yang memungkinkan admin untuk menambah, mengedit, menghapus, dan melihat data anak.
Fitur tambahan dalam aplikasi ini termasuk koneksi database, karakter kata sandi, pembersihan layar terminal, dan email untuk pemulihan akun yang terlupakan.
Dengan aplikasi ini, kami berharap dapat memudahkan Anda untuk berpartisipasi dalam mendukung anak-anak yang membutuhkan, melalui berbagai program yang kami tawarkan.
    '''

    wrapped_profil = textwrap.fill(profil_text, width=80)
    
    table_data = [
        [f"{warna.bold}{warna.biru_tebel}Selamat datang di aplikasi Yayasan Anak Budi Pekerti!{warna.putih}"],
        [""],
        [wrapped_profil+warna.reset]
    ]

    print(tabulate(table_data, tablefmt="pretty"))
    lanjut()
    pembersih()
    return

def visi_misi():
    pembersih()
    header = hd.SubheaderTentangKami_Visi_Misi()
    print(header)

    visi = "Menjadi yayasan terdepan yang menyediakan pendidikan dan dukungan komprehensif bagi anak-anak yang kurang beruntung, sehingga mereka dapat tumbuh menjadi individu yang berintegritas, berpengetahuan, dan mandiri."
    misi = [
        "1. Menyediakan akses pendidikan berkualitas yang terjangkau bagi anak-anak yang kurang beruntung.",
        "2. Menciptakan lingkungan yang aman, sehat, dan mendukung untuk perkembangan fisik dan mental anak-anak.",
        "3. Mengembangkan program-program yang berfokus pada peningkatan keterampilan hidup, kepercayaan diri, dan kreativitas anak-anak.",
        "4. Menjalin kerjasama dengan berbagai pihak untuk memperluas jangkauan dan efektivitas program-program yayasan.",
        "5. Menyediakan layanan kesehatan dan kesejahteraan yang komprehensif untuk mendukung pertumbuhan optimal anak-anak."
    ]

    # Format visi dan misi dalam bentuk tabel
    table_data = [
        [warna.bold + "Visi" + warna.reset, visi],
        [warna.bold + "Misi" + warna.reset, "\n".join(misi)]
    ]

    # Cetak tabel menggunakan tabulate
    print(tabulate(table_data, tablefmt="plain"))
    lanjut()
    pembersih()
    return

def tujuan():
    pembersih()
    header = hd.SubheaderTentangKami_Tujuan()
    print(header)

    tujuan_data = [
        ["1.", "Meningkatkan kualitas pendidikan dan prestasi akademis anak-anak melalui program pendidikan yang inovatif dan berkelanjutan."],
        ["2.", "Membangun karakter dan integritas anak-anak melalui kegiatan budi pekerti dan nilai-nilai moral."],
        ["3.", "Memastikan setiap anak memiliki akses ke fasilitas kesehatan dasar dan layanan pendukung psikologis."],
        ["4.", "Memberdayakan anak-anak dengan keterampilan hidup yang dibutuhkan untuk menghadapi tantangan masa depan."],
        ["5.", "Menggalang dukungan dan partisipasi masyarakat dalam upaya peningkatan kesejahteraan anak-anak yang kurang beruntung."]
    ]

    # Cetak menggunakan tabulate
    print(tabulate(tujuan_data, headers=["", f"{warna.bold}Tujuan{warna.reset}"], tablefmt="plain"))

    lanjut()
    pembersih()
    return

def struktur_pengurus():
    pembersih()
    header = hd.SubheaderTentangKami_StrukturPengurus()
    print(header)
    org_chart()
    lanjut()
    pembersih()
    return

import matplotlib.pyplot as plt

def laporan_keuangan(program_manager):
    while True:
        header = hd.SubheaderTentangKami_LaporanKeuangan()
        programs = program_manager.lihat_program()
        options = [f"• {nama}" for _, nama in programs] + ["• Kembali"]
        pilihan = menu_navigasi(header, options)

        if pilihan == len(programs):
            break

        if pilihan < len(programs):
            program_id = programs[pilihan][0]
            histori_donasi = program_manager.lihat_histori_donasi(program_id)
            
            # Persiapkan data untuk tabulasi
            table_data = []
            total_donasi = 0
            for donasi in histori_donasi:
                total_donasi += donasi[2]
                table_data.append([donasi[0], donasi[1], donasi[2], donasi[3]])
            
            table_data.append([f"{warna.hijau+warna.bold}Total Donasi Terkumpul: {warna.reset}", "", f"{warna.hijau+warna.bold}{total_donasi}{warna.reset}", ""])

            
            headers = ["Donatur", "Pesan", "Jumlah Donasi", "Tanggal"]
            
            print(tabulate(table_data, headers=headers, tablefmt="rounded_outline"))
            lanjut()
            choices = ["Tampilkan Grafik", "Kembali"]
            header = "Pilihan Anda:"
            selected_index = menu_navigasi(header, choices)
            choice = str(selected_index + 1)

            if choice == "1":
                # Buat grafik
                donatur = [donasi[0] for donasi in histori_donasi]
                jumlah_donasi = [donasi[2] for donasi in histori_donasi]
                
                plt.bar(donatur, jumlah_donasi, color='green')
                plt.xlabel('Donatur')
                plt.ylabel('Jumlah Donasi')
                plt.title('Grafik Donasi per Donatur')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.show()
                
            elif choice == "2":
                lanjut()




def UserProgramKami():
    lihatProgram(program_manager)



def donasiProgram(donatur):
    while True:
            header = hd.headerDonasi()
            programs = program_manager.lihat_program()
            options = ["• " + nama for id, nama in programs] + ["• Kembali"]
            pilihan = menu_navigasi(header, options)
            
            if pilihan == len(programs):
                return
            
            if pilihan < len(programs):
                program_id = programs[pilihan][0]
                program = program_manager.lihat_detail_program(program_id)
                if program:
                    if program.cek_terpenuhi_program():
                        print("Target donasi untuk program ini sudah terpenuhi. Anda tidak bisa melakukan donasi lagi.")
                        lanjut()
                        continue

                    while True:
                        try:
                            print("Jika ingin kembali ketik \"0\"")
                            jumlah_donasi = int(input(f"{warna.biru+warna.bold}Masukkan jumlah donasi > {warna.reset}"))

                            if jumlah_donasi == 0:
                                # Kembali ke menu program donasi
                                break
                            elif jumlah_donasi <= 500:
                                pembersih()
                                print("Jumlah donasi kamu tidak valid. Minimal melakukan donasi 500 Rupiah")
                            else:
                                if donatur.get_dompet() < jumlah_donasi:
                                    print("Saldo dompet Anda tidak mencukupi untuk donasi ini.")
                                    lanjut()
                                    break

                                pesan_donasi = input(f"{warna.biru+warna.bold}Masukkan pesan untuk donasi > {warna.reset}")
                                nama_donatur = donatur.get_nama()
                                program_manager.update_donasi_terkumpul(program_id, jumlah_donasi)
                                program_manager.catat_donasi(donatur.get_id(), program_id, jumlah_donasi, nama_donatur, pesan_donasi)
                                program.tambah_donasi(jumlah_donasi)
                                
                                donatur.kurangi_dompet(jumlah_donasi)
                                update_dompet(donatur.get_id(), -jumlah_donasi)
                                db.tutup_koneksi()
                                donasi_berhasil("Donasi anda berhasil terkirim!.", jumlah_donasi)
                                lanjut()
                                break
                        except ValueError:
                            pembersih()
                            error("Inputan tidak valid.")


def update_dompet(user_id, amount):
    query = "UPDATE akun SET dompet = dompet + %s WHERE id_akun = %s"
    params = (amount, user_id)
    db.query(query, params)

def menuDompet(donatur):
    while True:
        header = hd.headerDompet(donatur)
        menu = ["Cek Dompet", "Top Up Dompet", "Kembali"]
        pilihan = menu_navigasi(header, menu)
        if pilihan == 0:
            cekDompet(donatur)
        elif pilihan == 1 :
            sistemTopUp(donatur)
        elif pilihan == 2:
            break

def cekDompet(donatur):
    pembersih()
    header = hd.SubheaderDompet()
    print(header)
    info(f"Dompet anda : {donatur.get_dompet()}")
    lanjut()

def sistemTopUp(donatur):
    pembersih()
    header = hd.SubheaderTopup()
    print(header)
    try:
        topupamount = input(f"{warna.biru+warna.bold}Masukkan jumlah pengisian dompet > {warna.reset}")
        if topupamount == "":
            error("Jumlah pengisian tidak boleh kosong.")
            lanjut()
            return
        elif topupamount < 500:
            error("Jumlah pengisian minimal adalah Rp. 500.")
            return
        topupamount = int(topupamount)
        top_up(topupamount, donatur)
        lanjut()
        return
    except ValueError:
        error("Jumlah pengisian harus berupa angka.")
        return
    




def menu_AdikAsuh(donatur, adik_asuh_manager):
    while True:
        infotxt = f'Hai, {donatur.get_nama()} kamu hanya bisa memilih 1 adik asuh.\n'
        header = hd.headerAdikasuh()
        options = [
            "• Lihat Daftar Adik Asuh",
            "• Pilih Adik Asuh",
            "• Cek Kebutuhan Adik Asuh",
            "• Bayar Kebutuhan Adik Asuh",
            "• Kembali"
        ]
        pilihan = menu_navigasi(header, options, infotxt,info)
        
        if pilihan == 0:
            lihatDaftarAdikAsuh(adik_asuh_manager)
        elif pilihan == 1:
            pilihAdikAsuh(donatur, adik_asuh_manager)
        elif pilihan == 2:
            cekKebutuhanAdikAsuh(donatur, adik_asuh_manager)
        elif pilihan == 3:
            bayarKebutuhanAdikAsuh(donatur, adik_asuh_manager)
        elif pilihan == 4:
            break
        else:
            error("Pilihan tidak valid. Silakan coba lagi.")
            lanjut()




def lihatDaftarAdikAsuh(adik_asuh_manager):
    pembersih()
    header = hd.SubheaderLihatAdikasuh()
    print(header)
    anak_list = adik_asuh_manager.lihat_anak()
    for anak in anak_list:
        print(f"Nama: {anak[1]}, Status: {anak[2]}")
    lanjut()
    pembersih()

def pilihAdikAsuh(donatur, adik_asuh_manager):
    pembersih()
    header = hd.SubheaderPilihAdikasuh()
    
    if adik_asuh_manager.cek_donatur_memiliki_anak(donatur.get_id()):
        info("Anda sudah memiliki adik asuh dan tidak bisa mengasuh lebih dari satu.")
        lanjut()
        return
    
    anak_list = adik_asuh_manager.lihat_anak()
    options = [f"• {anak[1]} - {anak[2]}" for anak in anak_list if anak[2] == 'Belum di Asuh'] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    
    if pilihan == len(options) - 1:
        return
    
    if pilihan < len(options) - 1:
        id = [anak[0] for anak in anak_list if anak[2] == 'Belum di Asuh'][pilihan]
        adik_asuh_manager.lihat_detail_anak(id)
        konfirmasi = input(f"{warna.biru+warna.bold}Apakah Anda ingin mengasuh anak ini? (ya/tidak) > {warna.reset}")
        if konfirmasi.lower() == 'ya':
            adik_asuh_manager.pilih_anak_asuh(donatur.get_id(), id)
            berhasil("Anda telah berhasil mengasuh anak ini.")
            lanjut()
    else:
        error("Pilihan tidak valid. Silakan coba lagi.")
        lanjut()


def cekKebutuhanAdikAsuh(donatur, adik_asuh_manager):
    pembersih()
    header = hd.SubheaderKebutuhanAdikasuh()
    
    anak_list = adik_asuh_manager.lihat_anak_asuh_donatur(donatur.get_id())
    options = [f"• {anak[1]}" for anak in anak_list] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    
    if pilihan == len(options) - 1:
        return
    
    if pilihan < len(options) - 1:
        id = anak_list[pilihan][0]
        adik_asuh_manager.lihat_detail_anak(id)
        lanjut()
    else:
        error("Pilihan tidak valid. Silakan coba lagi.")
        lanjut()



def bayarKebutuhanAdikAsuh(donatur, adik_asuh_manager):
    pembersih()
    header = hd.SubheaderBayarAdikasuh()
    
    anak_list = adik_asuh_manager.lihat_anak_asuh_donatur(donatur.get_id())
    options = [f"• {anak[1]}" for anak in anak_list] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    
    if pilihan == len(options) - 1:
        return
    
    if pilihan < len(options) - 1:
        id = anak_list[pilihan][0]
        adik_asuh_manager.lihat_detail_anak(id)
        try:
            jumlah = int(input(f"{warna.biru+warna.bold}Masukkan jumlah donasi > {warna.reset}"))
            if jumlah < 1000:
                raise ValueError
        except ValueError:
            error("Jumlah donasi tidak bisa kurang dari Rp 1.000 dan berupa angka.")
            lanjut()
            return
        
        if donatur.get_dompet() >= jumlah:
            donatur.kurangi_dompet(jumlah)
            update_dompet(donatur.get_id(), -jumlah)
            kebutuhan_terpenuhi = adik_asuh_manager.bayar_kebutuhan_anak(donatur.get_id(), id, jumlah)
            
            if kebutuhan_terpenuhi:
                info("Anak yang diasuh kebutuhan sudah terpenuhi, terima kasih sudah berdonasi.")
            else:
                donasi_berhasil("Donasi telah berhasil dilakukan.", jumlah)
        else:
            info("Saldo dompet tidak mencukupi.")
        
        lanjut()
    else:
        error("Pilihan tidak valid. Silakan coba lagi.")
        lanjut()




def pengaturan_akun(donatur):
    while True:
        pembersih()
        header = hd.headerPengaturan()
        menu = ['• Ganti Password', '• Ganti Email', '• Ganti No Telepon', '• Kembali']
        pilihan = menu_navigasi(header, menu)
        
        if pilihan == 0:
            ganti_password(donatur)
        elif pilihan == 1:
            ganti_email(donatur)
        elif pilihan == 2:
            ganti_no_telepon(donatur)
        elif pilihan == 3:
            break
        else:
            error("Pilihan tidak valid. Silakan coba lagi.")
            lanjut()

def ganti_password(donatur):
    pembersih()
    header = hd.SubheaderGantiPassword()
    print(header)
    current_password = input(f"{warna.biru+warna.bold}Masukkan password saat ini > {warna.reset}").strip()
    
    if current_password != donatur.get_password():
        error("Password saat ini salah.")
    else:
        new_password = input(f"{warna.biru+warna.bold}Masukkan password baru > {warna.reset}").strip()
        confirm_password = input(f"{warna.biru+warna.bold}Konfirmasi password baru > {warna.reset}").strip()
        
        if new_password == confirm_password:
            donatur.set_password(new_password)
            # Update the password in the database
            query = "UPDATE akun SET password = %s WHERE id_akun = %s"
            adik_asuh_manager.db.query(query, (new_password, donatur.get_id()))
            berhasil("Password berhasil diubah.")
        else:
            error("Password baru dan konfirmasi tidak cocok.")
    
    lanjut()

def ganti_email(donatur):
    pembersih()
    header = hd.SubheaderGantiPassword()
    print(header)
    new_email = input(f"{warna.biru+warna.bold}Masukkan email baru > {warna.reset}").strip()
    
    if new_email:
        donatur.set_email(new_email)
        # Update the email in the database
        query = "UPDATE akun SET email = %s WHERE id_akun = %s"
        adik_asuh_manager.db.query(query, (new_email, donatur.get_id()))
        berhasil("Email berhasil diubah.")
    else:
        error("Email baru tidak boleh kosong.")
    
    lanjut()

def ganti_no_telepon(donatur):
    pembersih()
    header = "Ganti No Telepon"
    print(header)
    new_no_telepon = input(f"{warna.biru+warna.bold}Masukkan no telepon baru > {warna.reset}").strip()
    
    if new_no_telepon:
        donatur.set_notelp(new_no_telepon)
        # Update the phone number in the database
        query = "UPDATE akun SET notelp = %s WHERE id_akun = %s"
        adik_asuh_manager.db.query(query, (new_no_telepon, donatur.get_id()))
        berhasil("No telepon berhasil diubah.")
    else:
        error("No telepon baru tidak boleh kosong.")
    
    lanjut()

    




        

# ━━━━━━━━━━━━━━━━━━━━━━━━ ADMIN STRUCTURE ━━━━━━━━━━━━━━━━━━━━━━━━ 

def menuAdmin(admin):
    
    while admin.cek_login:
        header = hd.HeaderMenuAdmin(admin)
        menu = ['• Manajemen Program Donasi', '• Manajemen Adik Asuh', '• Cek Rekening', '• Logout']
        pilihan = menu_navigasi(header, menu)

        if pilihan == 0:
            AdminManajemen_ProgramDonasi(admin, program_manager)
        elif pilihan == 1:
            AdminManajemen_AdikAsuh(adik_asuh_manager)
        elif pilihan == 2:
            Admin_CekRekening(admin)
        elif pilihan == 3:
            admin.logout()
        else:
            error("Pilihan tidak valid.")
            lanjut()

def Admin_CekRekening(admin):
    pembersih()
    header = hd.headerCek()
    print(header)
    print(f"Rekening anda : {admin.get_dompet()}")
    lanjut()



def AdminManajemen_ProgramDonasi(admin, program_manager):
    while True:
       
        header = hd.headerManajemenDonasi()
        menu = ['• Lihat Program Yayasan', '• Tambah Program Yayasan', '• Edit Program Yayasan', '• Hapus Program Yayasan', '• Kembali']
        pilihan = menu_navigasi(header,menu)
        

        if pilihan == 0:
            lihatProgram(program_manager)
        elif pilihan == 1:
            tambahProgram(program_manager)
        elif pilihan == 2:
            editProgram(program_manager)
        elif pilihan == 3:
            hapusProgram(admin, program_manager)
        elif pilihan == 4:
            break




def lihatProgram(program_manager):
    while True:
        header = hd.SubheaderLihatProgram()
        programs = program_manager.lihat_program()
        options = ["• " + nama for id, nama in programs] + ["• Kembali"]
        pilihan = menu_navigasi(header, options)
        if pilihan < len(programs):
            program_id = programs[pilihan][0]
            program_nama = programs[pilihan][1]  
            program = program_manager.lihat_detail_program(program_id)
            if program:
                info(f"Progress Donasi: {program.get_donasi_terkumpul()} / {program.get_target_donasi()}")
                lanjut()
                while True:
                    pembersih()
                    detail_header = f"Detail Program {program_nama}"  
                    detail_options = ["• Melihat Histori Donasi", "• Kembali"]

                    detail_pilihan = menu_navigasi(detail_header, detail_options)
                    if detail_pilihan == 0:
                        histori_donasi = program_manager.lihat_histori_donasi(program_id)
                        print("===== Histori Donasi =====")
                        for donasi in histori_donasi:
                            print("==================")
                            print(f"Nama Dermawan : {donasi[0]}")
                            print(f"Pesan Donasi  : {donasi[1]}")
                            print(f"Jumlah Donasi : {donasi[2]}")
                            print(f"Tanggal & Waktu Donasi: {donasi[3]}")
                            print("==================")
                        lanjut()
                    else:
                        break
            lanjut()
        else:
            break



def tambahProgram(program_manager):
    pembersih()
    header = hd.SubheaderTambahDonasi()
    print(header)
    nama = input(f"{warna.biru+warna.bold}Nama Program > {warna.reset}")
    deskripsi = input(f"{warna.biru+warna.bold}Deskripsi Program > {warna.reset}")
    target_donasi = float(input(f"{warna.biru+warna.bold}Target Donasi > {warna.reset}"))
    donasi_terkumpul = 0.0  
    while True:
        tenggat = input(f"{warna.biru+warna.bold}Tenggat Selesai Pengumpulan Dana (YYYY-MM-DD) > {warna.reset}")
        try:
            if not tenggat:
                raise ValueError("Tenggat tidak boleh kosong.")
            tenggat_date = datetime.datetime.strptime(tenggat, '%Y-%m-%d')
            if tenggat_date.date() < datetime.datetime.now().date():
                raise ValueError("Tanggal tidak boleh kurang dari tanggal sekarang.")
            break
        except ValueError as e:
            error(e)

    program = Program(nama, deskripsi, target_donasi, donasi_terkumpul, tenggat)
    program_manager.tambah_program(program)
    lanjut()



def editProgram(program_manager):
    header = hd.SubheaderEditProgram()
    programs = program_manager.lihat_program()
    options = ["• " + nama for id, nama in programs] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    if pilihan < len(programs):
        idx = programs[pilihan][0]
        nama = input(f"{warna.biru+warna.bold}Nama Program (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
        deskripsi = input(f"{warna.biru+warna.bold}Deskripsi Program (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
        target_donasi = input(f"{warna.biru+warna.bold}Target Donasi (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
        while True:
            tenggat = input(f"{warna.biru+warna.bold}Tenggat Selesai Pengumpulan Dana (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
            if tenggat:
                try:
                    tenggat_date = datetime.datetime.strptime(tenggat, '%Y-%m-%d')
                    if tenggat_date.date() < datetime.datetime.now().date():
                        raise ValueError("Tanggal tidak boleh kurang dari tanggal sekarang.")
                    break
                except ValueError as e:
                    error(e)
            else:
                break

        kwargs = {}
        if nama:
            kwargs['nama'] = nama
        if deskripsi:
            kwargs['deskripsi'] = deskripsi
        if target_donasi:
            kwargs['target_donasi'] = float(target_donasi)
        if tenggat:
            kwargs['tenggat'] = tenggat
        program_manager.edit_program(idx, **kwargs)
        berhasil("Program berhasil diedit.")
        lanjut()

def hapusProgram(admin, program_manager):
    header = hd.SubheaderHapusProgram()
    programs = program_manager.lihat_program()
    options = ["• " + nama for id, nama in programs] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    if pilihan < len(programs):
        idx = programs[pilihan][0]
        program = program_manager.lihat_detail_program(idx)
        if program:
            if not program.cek_terpenuhi_program():
                info("Target donasi belum terpenuhi.")
                konfirmasi = input(f"{warna.biru+warna.bold}Apakah Anda yakin ingin menghapus program ini? (y/n) > {warna.reset}")
                if konfirmasi.lower() != 'y':
                    return
            dompetadmin = admin.get_dompet() + program.get_donasi_terkumpul()
            admin.set_dompet(dompetadmin)
            
            try:
                db.query(f"UPDATE akun SET dompet = {dompetadmin} WHERE username = '{admin.get_username()}'")
                db.query(f"DELETE FROM donasi WHERE id_program = '{idx}'")
                program_manager.hapus_program(idx)
                berhasil(f"Program {program.get_nama() + warna.bold} berhasil dihapus dan donasi terkumpul sebesar {program.get_donasi_terkumpul() + warna.bold} telah ditambahkan ke dompet admin.")
            except Exception as e:
                error(f"Terjadi kesalahan saat menghapus program: {e}")
            lanjut()





def AdminManajemen_AdikAsuh(adik_asuh_manager):
    while True:
        header = hd.headerManajemenAdik()
        menu = ['• Lihat Data Adik Asuh', '• Tambah Data Adik Asuh', '• Edit Data Adik Asuh', '• Hapus Data Adik Asuh', '• Lihat Donatur dan Anak Asuh', '• Kembali']
        pilihan = menu_navigasi(header, menu)

        if pilihan == 0:
            lihatAnakAsuh(adik_asuh_manager)
        elif pilihan == 1:
            tambahAnakAsuh(adik_asuh_manager)
        elif pilihan == 2:
            editAnakAsuh(adik_asuh_manager)
        elif pilihan == 3:
            hapusAnakAsuh(adik_asuh_manager)
        elif pilihan == 4:
            lihatDonaturDanAnakAsuh(adik_asuh_manager)
        elif pilihan == 5:
            break

def tambahAnakAsuh(adik_asuh_manager):
    pembersih()
    header = hd.SubheaderTambahAdik()
    print(header)
    while True:
        nama = input(f"{warna.biru+warna.bold}Nama Adik Asuh > {warna.reset}").strip()
        if not nama:
            error("Nama tidak boleh kosong. Silakan masukkan nama yang valid.")
            continue

        tempat_tinggal = input(f"{warna.biru+warna.bold}Tempat Tinggal Adik Asuh > {warna.reset}").strip()
        if not tempat_tinggal:
            error("Tempat tinggal tidak boleh kosong. Silakan masukkan tempat tinggal yang valid.")
            continue

        umur = input(f"{warna.biru+warna.bold}Umur Adik Asuh > {warna.reset}").strip()
        if not umur:
            error("Umur tidak boleh kosong. Silakan masukkan umur yang valid.")
            continue

        kebutuhan = input(f"{warna.biru+warna.bold}Kebutuhan Adik Asuh > {warna.reset}").strip()
        if not kebutuhan:
            error("Kebutuhan tidak boleh kosong. Silakan masukkan kebutuhan yang valid.")
            continue

        try:
            target_donasi = float(input(f"{warna.biru+warna.bold}Target Donasi > {warna.reset}").strip())
            if target_donasi < 5000:
                error("Target donasi tidak bisa kurang dari Rp. 5.000.")
        except ValueError:
            error("Target donasi harus berupa angka. Silakan masukkan jumlah yang valid.")
            continue

        status = 'Belum di Asuh'
        donasi_terkumpul = 0.00  
        anak = AdikAsuh(None, nama, tempat_tinggal, umur, kebutuhan, status, target_donasi, donasi_terkumpul)
        adik_asuh_manager.tambah_anak(anak)
        berhasil("Data adik asuh telah ditambahkan")
        break

    lanjut()
    pembersih()



def editAnakAsuh(adik_asuh_manager):
    pembersih()
    header = hd.SubheaderEditAdik()
    anak_list = adik_asuh_manager.lihat_anak()
    options = [f"• {anak[1]}" for anak in anak_list] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    if pilihan < len(anak_list):
        while True:
            id = anak_list[pilihan][0]
            nama = input(f"{warna.biru+warna.bold}Nama Adik Asuh (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
            tempat_tinggal = input(f"{warna.biru+warna.bold}Tempat Tinggal Adik Asuh (biarkan kosong jika tidak ingin mengubah)> {warna.reset}")
            umur = input(f"{warna.biru+warna.bold}Umur Adik Asuh (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
            kebutuhan = input(f"{warna.biru+warna.bold}Kebutuhan Adik Asuh (biarkan kosong jika tidak ingin mengubah) > {warna.reset}")
            try:
                target_donasi = float(input(f"{warna.biru+warna.bold}Target Donasi (biarkan kosong jika tidak ingin mengubah) > {warna.reset}"))
                if target_donasi < 5000:
                    raise ValueError
            except ValueError:
                error("Target donasi harus sama dengan atau lebih dari Rp. 5.000")
                continue
            kwargs = {}
            if nama:
                kwargs['nama'] = nama
            if tempat_tinggal:
                kwargs['tempat_tinggal'] = tempat_tinggal
            if umur:
                kwargs['umur'] = umur
            if kebutuhan:
                kwargs['kebutuhan'] = kebutuhan
            if target_donasi:
                kwargs['target_donasi'] = float(target_donasi)
            adik_asuh_manager.edit_anak(id, **kwargs)
            berhasil("Data adik asuh telah diedit.")
            lanjut()
            pembersih()
            break


def hapusAnakAsuh(adik_asuh_manager):
    pembersih()
    header = hd.SubheaderHapusAdik()
    anak_list = adik_asuh_manager.lihat_anak()
    options = [f"• {anak[1]}" for anak in anak_list] + ["• Kembali"]
    pilihan = menu_navigasi(header, options)
    if pilihan < len(anak_list):
        id = anak_list[pilihan][0]
        header = "Apakah anda yakin ingin menghapus data ini?"
        options = ['Ya', 'Tidak']
        konfirmasi = menu_navigasi(header, options)
        if konfirmasi == 0:
            adik_asuh_manager.hapus_anak(id)
            berhasil("Data Adik Asuh dihapus")
            lanjut()
            pembersih()
        elif konfirmasi == 1:
            info("Penghapusan dibatalkan")
            lanjut()
            pembersih()


def lihatAnakAsuh(adik_asuh_manager):
    while True:
        header = hd.SubheaderLihatAdikasuh()
        anak_list = adik_asuh_manager.lihat_anak()
        options = [f"• {anak[1]} - {anak[2]}" for anak in anak_list] + ["• Kembali"]
        pilihan = menu_navigasi(header, options)
        if pilihan < len(anak_list):
            id = anak_list[pilihan][0]
            adik_asuh_manager.lihat_detail_anak(id)
            lanjut()
        else:
            break


def lihatDonaturDanAnakAsuh(adik_asuh_manager):
    pembersih()
    header = hd.SubHeaderMenuAdikKakakAsuh()
    print(header)
    donatur_list = adik_asuh_manager.lihat_donatur_dan_anak_asuh()
    for donatur in donatur_list:
        print(f"Nama Donatur: {donatur[0]}")
        print(f"Anak di Asuh: {donatur[1]}")
        print(f"Kebutuhan Anak Asuh: {donatur[2]}\n")
    lanjut()
    pembersih()







menuLogin()