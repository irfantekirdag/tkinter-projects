import tkinter as tk
from tkinter import messagebox
import sqlite3

# Veritabanı başlangıcı
conn = sqlite3.connect('bitki_veritabani.db')
c = conn.cursor()

# Tablonun var olup olmadığını kontrol et
c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bitki'")
tablo_var_mi = c.fetchone()[0]

if not tablo_var_mi:
    # Bitki Tablosu
    c.execute('''
    CREATE TABLE bitki (
    bitki_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bitki_adi TEXT,
    bitki_degeri TEXT,
    bitki_yetistirme_kosul TEXT
    )
    ''')

if not tablo_var_mi:
    # Bölgeler Tablosu
    c.execute('''
    CREATE TABLE bolgeler (
    bolge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bolge_adi TEXT
    )
    ''')

# Herbalist Tablosu
if not tablo_var_mi:
    c.execute('''
    CREATE TABLE herbalist (
    herbalist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    herbalist_adi TEXT,
    herbalist_soyadi TEXT,
    herbalist_tc TEXT,
    herbalist_tarih TEXT,
    herbalist_tel TEXT,
    herbalist_sifre TEXT
    )
    ''')

# Taşlar Tablosu
if not tablo_var_mi:
    c.execute('''
    CREATE TABLE taslar (
    tas_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tas_adi TEXT,
    tas_degeri TEXT
    )
    ''')

# Türler Tablosu
if not tablo_var_mi:
    c.execute('''
    CREATE TABLE turler (
    tur_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tur_adi TEXT
    )
    ''')

# İlişki Tabloları
if not tablo_var_mi:
    c.execute('''
    CREATE TABLE bitki_tur (
    bitki_id INTEGER,
    tur_id INTEGER,
    FOREIGN KEY(bitki_id) REFERENCES bitki(bitki_id),
    FOREIGN KEY(tur_id) REFERENCES turler(tur_id),
    PRIMARY KEY(bitki_id, tur_id)
    )
    ''')

if not tablo_var_mi:
    c.execute('''
    CREATE TABLE bolge_bitki (
    bolge_id INTEGER,
    bitki_id INTEGER,
    FOREIGN KEY(bolge_id) REFERENCES bolgeler(bolge_id),
    FOREIGN KEY(bitki_id) REFERENCES bitki(bitki_id),
    PRIMARY KEY(bolge_id, bitki_id)
    )
    ''')

if not tablo_var_mi:
    c.execute('''
    CREATE TABLE bolge_herbalist (
    bolge_id INTEGER,
    herbalist_id INTEGER,
    FOREIGN KEY(bolge_id) REFERENCES bolgeler(bolge_id),
    FOREIGN KEY(herbalist_id) REFERENCES herbalist(herbalist_id),
    PRIMARY KEY(bolge_id, herbalist_id)
    )
    ''')

if not tablo_var_mi:
    c.execute('''
    CREATE TABLE bolge_tas (
    bolge_id INTEGER,
    tas_id INTEGER,
    FOREIGN KEY(bolge_id) REFERENCES bolgeler(bolge_id),
    FOREIGN KEY(tas_id) REFERENCES taslar(tas_id),
    PRIMARY KEY(bolge_id, tas_id)
    )
    ''')

if not tablo_var_mi:
    c.execute('''
    CREATE TABLE tas_tur (
    tas_id INTEGER,
    tur_id INTEGER,
    FOREIGN KEY(tas_id) REFERENCES taslar(tas_id),
    FOREIGN KEY(tur_id) REFERENCES turler(tur_id),
    PRIMARY KEY(tas_id, tur_id)
    )
    ''')


# Veritabanına örnek veri ekle
if not tablo_var_mi:
    c.execute('''
    INSERT INTO bitki (bitki_adi, bitki_degeri, bitki_yetistirme_kosul)
    VALUES ('Lavanta', 'Değerli', 'Güneşli ve iyi drenajlı toprak')
    ''')

if not tablo_var_mi:
    c.execute('''
    INSERT INTO bolgeler (bolge_adi)
    VALUES ('Ege')
    ''')

if not tablo_var_mi:
    c.execute('''
    INSERT INTO herbalist (herbalist_adi, herbalist_soyadi, herbalist_tc, herbalist_tarih, herbalist_tel, herbalist_sifre)
    VALUES ('Ahmet', 'Yılmaz', '12345678901', '01/01/1990', '555-1234', 'sifre123')
    ''')

if not tablo_var_mi:
    c.execute('''
    INSERT INTO taslar (tas_adi, tas_degeri)
    VALUES ('Ametist', 'Değerli')
    ''')

if not tablo_var_mi:
    c.execute('''
    INSERT INTO turler (tur_adi)
    VALUES ('Çiçek')
    ''')

# Veritabanına örnek bölge verileri ekle
bolgeler = ['Marmara', 'Ege', 'Akdeniz', 'İç Anadolu', 'Doğu Anadolu', 'Güneydoğu Anadolu', 'Karadeniz']

for bolge_adi in bolgeler:
    if not tablo_var_mi:
        c.execute('INSERT INTO bolgeler (bolge_adi) VALUES (?)', (bolge_adi,))

# Bitkileri ve taşları ilgili bölgelere ilişkilendirme
# Örnek olarak sadece bir bitki ve bir taş eklenmiştir, gerçek verilere göre bu kısmı düzenlemelisiniz.

# Bitkiyi bir bölgeye ilişkilendir
if not tablo_var_mi:
    c.execute('SELECT bolge_id FROM bolgeler WHERE bolge_adi=?', ('Marmara',))
    bolge_id = c.fetchone()[0]

    c.execute('INSERT INTO bolge_bitki (bolge_id, bitki_id) VALUES (?, ?)',
              (bolge_id, 1))  # Burada 1, bitki tablosundaki bir bitki örneğidir.

# Taşı bir bölgeye ilişkilendir
if not tablo_var_mi:
    c.execute('INSERT INTO bolge_tas (bolge_id, tas_id) VALUES (?, ?)',
              (bolge_id, 1))  # Burada 1, taslar tablosundaki bir taş örneğidir.

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()

#Veritabanı bitis

def kayit_ol():
    # Kullanıcı bilgilerini al
    isim = isim_entry.get()
    soyisim = soyisim_entry.get()
    telefon = telefon_entry.get()
    tc = tc_entry.get()
    sifre = sifre_entry.get()

    # SQLite veritabanına kayıt ekle
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    # Kullanıcıyı kontrol et
    c.execute('SELECT * FROM herbalist WHERE herbalist_tc=?', (tc,))
    kullanici = c.fetchone()

    if kullanici:
        messagebox.showerror("Hata", "Bu TC kimlik numarası zaten kayıtlı.")
    else:
        # Yeni kullanıcıyı ekleyin
        c.execute('''
        INSERT INTO herbalist (herbalist_adi, herbalist_soyadi, herbalist_tc, herbalist_tel, herbalist_sifre)
        VALUES (?, ?, ?, ?, ?)
        ''', (isim, soyisim, tc, telefon, sifre))

        messagebox.showinfo("Kayıt Başarılı", "Başarıyla kayıt oldunuz.")

    conn.commit()
    conn.close()

def ac_kayit_pencere():
    global kayit_pencere
    kayit_pencere = tk.Toplevel(pen)
    kayit_pencere.title("Kayıt Ol")

    # İsim
    isim_label = tk.Label(kayit_pencere, text="İsim:")
    isim_label.grid(row=0, column=0, padx=10, pady=10)
    global isim_entry
    isim_entry = tk.Entry(kayit_pencere)
    isim_entry.grid(row=0, column=1, padx=10, pady=10)

    # Soyisim
    soyisim_label = tk.Label(kayit_pencere, text="Soyisim:")
    soyisim_label.grid(row=1, column=0, padx=10, pady=10)
    global soyisim_entry
    soyisim_entry = tk.Entry(kayit_pencere)
    soyisim_entry.grid(row=1, column=1, padx=10, pady=10)

    # Telefon
    telefon_label = tk.Label(kayit_pencere, text="Telefon:")
    telefon_label.grid(row=2, column=0, padx=10, pady=10)
    global telefon_entry
    telefon_entry = tk.Entry(kayit_pencere)
    telefon_entry.grid(row=2, column=1, padx=10, pady=10)

    # TC Kimlik Numarası
    tc_label = tk.Label(kayit_pencere, text="TC Kimlik Numarası:")
    tc_label.grid(row=3, column=0, padx=10, pady=10)
    global tc_entry
    tc_entry = tk.Entry(kayit_pencere)
    tc_entry.grid(row=3, column=1, padx=10, pady=10)

    # Şifre
    sifre_label = tk.Label(kayit_pencere, text="Şifre:")
    sifre_label.grid(row=4, column=0, padx=10, pady=10)
    global sifre_entry
    sifre_entry = tk.Entry(kayit_pencere, show="*")
    sifre_entry.grid(row=4, column=1, padx=10, pady=10)

    # Kayıt Ol butonu
    kayit_ol_button = tk.Button(kayit_pencere, text="Kayıt Ol", command=kayit_ol)
    kayit_ol_button.grid(row=5, column=0, columnspan=2, pady=10)

def giris_yap():
    # Kullanıcı Adı ve Parolayı al
    kullanici_adi = kullanici_adi_entry.get()
    parola = parola_entry.get()

    # SQLite veritabanına bağlan
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    # Kullanıcıyı kontrol et
    c.execute('SELECT * FROM herbalist WHERE herbalist_adi=? AND herbalist_sifre=?', (kullanici_adi, parola))
    kullanici = c.fetchone()

    conn.commit()
    conn.close()

    if kullanici:
        # Giriş başarılı mesajını göster ve yeni bir sayfa aç
        messagebox.showinfo("Giriş Başarılı", f"Hoş geldiniz, {kullanici_adi}!")

        # Yeni sayfa oluştur
        yeni_sayfa = tk.Toplevel(pen)
        yeni_sayfa.title("Bitkiler ve Taşlar")

        # Bitkiler Butonu
        bitkiler_button = tk.Button(yeni_sayfa, text="Bitkiler", command=bitkiler_sayfasi)
        bitkiler_button.grid(row=0, column=0, padx=10, pady=10)


        # Taşlar Butonu
        taslar_button = tk.Button(yeni_sayfa, text="Taşlar", command=taslar_sayfasi)
        taslar_button.grid(row=1, column=0, padx=10, pady=10)

        # İsterseniz bu butonlara fonksiyonlar ekleyebilir ve tıklanınca bir şeyler yapabilirsiniz
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya parola hatalı.")


# Bitkiler sayfası
def bitkiler_sayfasi():
    # Yeni sayfa oluştur
    bitkiler_sayfa = tk.Toplevel(pen)
    bitkiler_sayfa.title("Bitkiler")

    # Bitki verilerini al
    bitki_verileri = get_bitki_verileri()

    # Bitki verilerini sayfaya ekle
    for index, bitki in enumerate(bitki_verileri):
        bitki_id_label = tk.Label(bitkiler_sayfa, text=f"Bitki ID: {bitki[0]}")
        bitki_id_label.grid(row=index, column=0, padx=10, pady=10)

        bitki_adi_label = tk.Label(bitkiler_sayfa, text=f"Bitki Adı: {bitki[1]}")
        bitki_adi_label.grid(row=index, column=1, padx=10, pady=10)

        bitki_degeri_label = tk.Label(bitkiler_sayfa, text=f"Bitki Değeri: {bitki[2]}")
        bitki_degeri_label.grid(row=index, column=2, padx=10, pady=10)

        bitki_yetistirme_kosul_label = tk.Label(bitkiler_sayfa, text=f"Yetiştirme Koşulu: {bitki[3]}")
        bitki_yetistirme_kosul_label.grid(row=index, column=3, padx=10, pady=10)

        # Bağlı olduğu bölgeleri al
        bagli_bolgeler = get_bagli_bolgeler(bitki[0])

        if bagli_bolgeler:
            bolge_label = tk.Label(bitkiler_sayfa, text=f"Bölgeler: {', '.join(bagli_bolgeler)}")
            bolge_label.grid(row=index, column=4, padx=10, pady=10)

        # Bitki Ekle butonu
        ekle_button = tk.Button(bitkiler_sayfa, text="Ekle", command=bitki_ekle_sayfasi)
        ekle_button.grid(row=index + 1, column=0, padx=10, pady=10)

        # Bitki Sil butonu
        sil_button = tk.Button(bitkiler_sayfa, text="Sil", command=bitki_sil_sayfasi)
        sil_button.grid(row=index + 1, column=1, padx=10, pady=10)

def get_bagli_bolgeler(bitki_id):
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()
    c.execute('''
    SELECT bolgeler.bolge_adi 
    FROM bolge_bitki 
    INNER JOIN bolgeler ON bolge_bitki.bolge_id = bolgeler.bolge_id 
    WHERE bolge_bitki.bitki_id = ?
    ''', (bitki_id,))
    bagli_bolgeler = c.fetchall()
    conn.close()
    return [bolge[0] for bolge in bagli_bolgeler]

# Taşlar sayfası
def taslar_sayfasi():
    # Yeni sayfa oluştur
    taslar_sayfa = tk.Toplevel(pen)
    taslar_sayfa.title("Taşlar")

    # SQLite bağlantısı ve cursor oluştur
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    # Taş verilerini al
    tas_verileri = get_tas_verileri(c)

    # Taş verilerini sayfaya ekle
    for index, tas in enumerate(tas_verileri):
        tas_id_label = tk.Label(taslar_sayfa, text=f"Taş ID: {tas[0]}")
        tas_id_label.grid(row=index, column=0, padx=10, pady=10)

        tas_adi_label = tk.Label(taslar_sayfa, text=f"Taş Adı: {tas[1]}")
        tas_adi_label.grid(row=index, column=1, padx=10, pady=10)

        tas_degeri_label = tk.Label(taslar_sayfa, text=f"Taş Değeri: {tas[2]}")
        tas_degeri_label.grid(row=index, column=2, padx=10, pady=10)

        # Taşların bağlı olduğu bölgeler
        c.execute('''
            SELECT bolgeler.bolge_adi
            FROM bolgeler
            INNER JOIN bolge_tas ON bolgeler.bolge_id = bolge_tas.bolge_id
            WHERE bolge_tas.tas_id=?
            ''', (tas[0],))
        bolgeler = c.fetchall()

        bolge_label_text = ', '.join([bolge[0] for bolge in bolgeler])
        bolge_label = tk.Label(taslar_sayfa, text=f"Bölgeler: {bolge_label_text}")
        bolge_label.grid(row=index, column=3, padx=10, pady=10)

    # Taş Ekle butonu
    ekle_button = tk.Button(taslar_sayfa, text="Ekle", command=tas_ekle_sayfasi)
    ekle_button.grid(row=index + 1, column=0, padx=10, pady=10)

    # Taş Sil butonu
    sil_button = tk.Button(taslar_sayfa, text="Sil", command=tas_sil_sayfasi)
    sil_button.grid(row=index + 1, column=1, padx=10, pady=10)

    # Bağlantıyı kapat
    conn.close()

def get_bitki_verileri():
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bitki')
    bitki_verileri = c.fetchall()
    conn.close()
    return bitki_verileri

def get_tas_verileri(c):
    c.execute('SELECT * FROM taslar')
    tas_verileri = c.fetchall()
    return tas_verileri

def bitki_ekle():
    bitki_adi = bitki_adi_entry.get()
    bitki_degeri = bitki_degeri_entry.get()
    yetistirme_kosulu = yetistirme_kosulu_entry.get()
    secili_bolgeler = bolgeler_listbox.curselection()

    if not bitki_adi or not bitki_degeri or not yetistirme_kosulu or not secili_bolgeler:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun ve bir veya daha fazla bölge seçin.")
        return

    secili_bolgeler = [bolgeler_listbox.get(index) for index in secili_bolgeler]

    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    # Bitki tablosuna yeni bitkiyi ekle
    c.execute('''
    INSERT INTO bitki (bitki_adi, bitki_degeri, bitki_yetistirme_kosul)
    VALUES (?, ?, ?)
    ''', (bitki_adi, bitki_degeri, yetistirme_kosulu))

    # Eklenen bitkinin ID'sini al
    c.execute('SELECT last_insert_rowid()')
    bitki_id = c.fetchone()[0]

    # Bitki ve seçili bölgeler arasındaki ilişkiyi kur
    for bolge_adi in secili_bolgeler:
        c.execute('SELECT bolge_id FROM bolgeler WHERE bolge_adi=?', (bolge_adi,))
        bolge_id = c.fetchone()[0]
        c.execute('INSERT INTO bolge_bitki (bolge_id, bitki_id) VALUES (?, ?)', (bolge_id, bitki_id))

    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Bitki başarıyla eklendi.")
    bitkiler_sayfasi()

def bitki_ekle_sayfasi():
    pen.iconify()
    ekle_sayfa = tk.Toplevel(pen)
    ekle_sayfa.title("Bitki Ekle")

    # Bitki Adı
    bitki_adi_label = tk.Label(ekle_sayfa, text="Bitki Adı:")
    bitki_adi_label.grid(row=0, column=0, padx=10, pady=10)
    global bitki_adi_entry
    bitki_adi_entry = tk.Entry(ekle_sayfa)
    bitki_adi_entry.grid(row=0, column=1, padx=10, pady=10)

    # Bitki Değeri
    bitki_degeri_label = tk.Label(ekle_sayfa, text="Bitki Değeri:")
    bitki_degeri_label.grid(row=1, column=0, padx=10, pady=10)
    global bitki_degeri_entry
    bitki_degeri_entry = tk.Entry(ekle_sayfa)
    bitki_degeri_entry.grid(row=1, column=1, padx=10, pady=10)

    # Yetiştirme Koşulu
    yetistirme_kosulu_label = tk.Label(ekle_sayfa, text="Yetiştirme Koşulu:")
    yetistirme_kosulu_label.grid(row=2, column=0, padx=10, pady=10)
    global yetistirme_kosulu_entry
    yetistirme_kosulu_entry = tk.Entry(ekle_sayfa)
    yetistirme_kosulu_entry.grid(row=2, column=1, padx=10, pady=10)

    # Bölgeler Listesi
    bolgeler_label = tk.Label(ekle_sayfa, text="Bölgeler:")
    bolgeler_label.grid(row=3, column=0, padx=10, pady=10)
    global bolgeler_listbox
    bolgeler_listbox = tk.Listbox(ekle_sayfa, selectmode=tk.MULTIPLE)
    bolgeler_listbox.grid(row=3, column=1, padx=10, pady=10)

    # Veritabanındaki bölgeleri al
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()
    c.execute('SELECT bolge_adi FROM bolgeler')
    bolgeler = c.fetchall()
    conn.close()

    # Bölgeler listesine ekle
    for bolge in bolgeler:
        bolgeler_listbox.insert(tk.END, bolge[0])

    # Kaydet Butonu
    kaydet_button = tk.Button(ekle_sayfa, text="Kaydet", command=bitki_ekle)
    kaydet_button.grid(row=4, column=0, columnspan=2, pady=10)

def tas_ekle(tas_adi, tas_degeri, secili_bolgeler):
    tas_adi = tas_adi_entry.get()
    tas_degeri = tas_degeri_entry.get()
    secili_bolgeler = bolgeler_listbox.curselection()

    if not tas_adi or not tas_degeri or not secili_bolgeler:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun ve bir veya daha fazla bölge seçin.")
        return

    secili_bolgeler = [bolgeler_listbox.get(index) for index in secili_bolgeler]

    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    # Taş tablosuna yeni taşı ekle
    c.execute('''
    INSERT INTO taslar (tas_adi, tas_degeri)
    VALUES (?, ?)
    ''', (tas_adi, tas_degeri))

    # Eklenen taşın ID'sini al
    c.execute('SELECT last_insert_rowid()')
    tas_id_result = c.fetchone()

    if tas_id_result is not None:
        tas_id = tas_id_result[0]

        # Taş ve seçili bölgeler arasındaki ilişkiyi kur
        for bolge_adi in secili_bolgeler:
            c.execute('SELECT bolge_id FROM bolgeler WHERE bolge_adi=?', (bolge_adi,))
            bolge_id_result = c.fetchone()

            if bolge_id_result is not None:
                bolge_id = bolge_id_result[0]
                c.execute('INSERT INTO bolge_tas (bolge_id, tas_id) VALUES (?, ?)', (bolge_id, tas_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Taş başarıyla eklendi.")
        taslar_sayfasi()
    else:
        messagebox.showerror("Hata", "Taş eklenirken bir hata oluştu.")


def tas_ekle_sayfasi():
    ekle_sayfa = tk.Toplevel(pen)
    ekle_sayfa.title("Taş Ekle")

    # Taş Adı
    tas_adi_label = tk.Label(ekle_sayfa, text="Taş Adı:")
    tas_adi_label.grid(row=0, column=0, padx=10, pady=10)
    global tas_adi_entry
    tas_adi_entry = tk.Entry(ekle_sayfa)
    tas_adi_entry.grid(row=0, column=1, padx=10, pady=10)

    # Taş Değeri
    tas_degeri_label = tk.Label(ekle_sayfa, text="Taş Değeri:")
    tas_degeri_label.grid(row=1, column=0, padx=10, pady=10)
    global tas_degeri_entry
    tas_degeri_entry = tk.Entry(ekle_sayfa)
    tas_degeri_entry.grid(row=1, column=1, padx=10, pady=10)

    # Bölgeler Listesi
    bolgeler_label = tk.Label(ekle_sayfa, text="Bölgeler:")
    bolgeler_label.grid(row=2, column=0, padx=10, pady=10)
    global bolgeler_listbox_tas
    bolgeler_listbox_tas = tk.Listbox(ekle_sayfa, selectmode=tk.MULTIPLE)
    bolgeler_listbox_tas.grid(row=2, column=1, padx=10, pady=10)

    # Veritabanındaki bölgeleri al
    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()
    c.execute('SELECT bolge_id, bolge_adi FROM bolgeler')
    bolgeler = c.fetchall()
    conn.close()

    # Bölgeler listesine ekle
    for bolge in bolgeler:
        bolgeler_listbox_tas.insert(tk.END, f"{bolge[0]} - {bolge[1]}")

    # Kaydet Butonu
    kaydet_button = tk.Button(ekle_sayfa, text="Kaydet", command=lambda: tas_ekle(tas_adi_entry.get(), tas_degeri_entry.get(), bolgeler_listbox_tas.curselection()))
    kaydet_button.grid(row=3, column=0, columnspan=2, pady=10)

def tas_ekle(tas_adi, tas_degeri, secili_bolgeler):
    if not tas_adi or not tas_degeri or not secili_bolgeler:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun ve bir veya daha fazla bölge seçin.")
        return

    secili_bolgeler = [bolgeler_listbox_tas.get(index).split(" - ")[0] for index in secili_bolgeler]

    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    # Taş tablosuna yeni taşı ekle
    c.execute('''
    INSERT INTO taslar (tas_adi, tas_degeri)
    VALUES (?, ?)
    ''', (tas_adi, tas_degeri))

    # Eklenen taşın ID'sini al
    c.execute('SELECT last_insert_rowid()')
    tas_id_result = c.fetchone()

    if tas_id_result is not None:
        tas_id = tas_id_result[0]

        # Taş ve seçili bölgeler arasındaki ilişkiyi kur
        for bolge_id in secili_bolgeler:
            c.execute('INSERT INTO bolge_tas (bolge_id, tas_id) VALUES (?, ?)', (bolge_id, tas_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Taş başarıyla eklendi.")
        taslar_sayfasi()
    else:
        messagebox.showerror("Hata", "Taş eklenirken bir hata oluştu.")

def bitki_sil():
    bitki_id = bitki_id_entry.get()

    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    c.execute('DELETE FROM bitki WHERE bitki_id=?', (bitki_id,))

    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Bitki başarıyla silindi.")
    bitkiler_sayfasi()
def bitki_sil_sayfasi():
    sil_sayfa = tk.Toplevel(pen)
    sil_sayfa.title("Bitki Sil")

    # Bitki ID
    bitki_id_label = tk.Label(sil_sayfa, text="Bitki ID:")
    bitki_id_label.grid(row=0, column=0, padx=10, pady=10)
    global bitki_id_entry
    bitki_id_entry = tk.Entry(sil_sayfa)
    bitki_id_entry.grid(row=0, column=1, padx=10, pady=10)

    # Sil butonu
    sil_button = tk.Button(sil_sayfa, text="Sil", command=bitki_sil)
    sil_button.grid(row=1, column=0, columnspan=2, pady=10)

def tas_sil():
    tas_id = tas_id_entry.get()

    conn = sqlite3.connect('bitki_veritabani.db')
    c = conn.cursor()

    c.execute('DELETE FROM taslar WHERE tas_id=?', (tas_id,))

    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Taş başarıyla silindi.")
    taslar_sayfasi()

def tas_sil_sayfasi():
    sil_sayfa = tk.Toplevel(pen)
    sil_sayfa.title("Taş Sil")

    # Taş ID
    tas_id_label = tk.Label(sil_sayfa, text="Taş ID:")
    tas_id_label.grid(row=0, column=0, padx=10, pady=10)
    global tas_id_entry
    tas_id_entry = tk.Entry(sil_sayfa)
    tas_id_entry.grid(row=0, column=1, padx=10, pady=10)

    # Sil butonu
    sil_button = tk.Button(sil_sayfa, text="Sil", command=tas_sil)
    sil_button.grid(row=1, column=0, columnspan=2, pady=10)


# Ana Sayfa
pen = tk.Tk()
pen.title("Kayıt ve Giriş")

kullanici_adi_label = tk.Label(pen, text="Kullanıcı Adı:")
kullanici_adi_label.grid(row=0, column=0, padx=10, pady=10)
kullanici_adi_entry = tk.Entry(pen)
kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=10)

parola_label = tk.Label(pen, text="Parola:")
parola_label.grid(row=1, column=0, padx=10, pady=10)
parola_entry = tk.Entry(pen, show="*")
parola_entry.grid(row=1, column=1, padx=10, pady=10)

giris_button = tk.Button(pen, text="Giriş Yap", command=giris_yap)
giris_button.grid(row=2, column=0, columnspan=2, pady=10)

kayit_ol_button = tk.Button(pen, text="Kayıt Ol", command=ac_kayit_pencere)
kayit_ol_button.grid(row=3, column=0, columnspan=2, pady=10)

pen.mainloop()
