import mysql.connector
from datetime import datetime,date

class VT_olustur():

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74"
        )
        self.imlec = self.mydb.cursor()

        vt_adi = "osman_db"

        
        print("\n\n---KURULUM İŞLEMLERİ BAŞLATILDI---\n")
        self.imlec.execute(f"CREATE DATABASE IF NOT EXISTS {vt_adi};")
        self.imlec.execute(f"USE {vt_adi}")
        self.mydb.commit()


    def tablolariOlustur(self):
        ###############################################################################################################
        # PERSONEL TABLOSU
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS Personel 
                            (	Personel_ID INT PRIMARY KEY AUTO_INCREMENT,
                                TC VARCHAR(11) NOT NULL,
                                Ad VARCHAR(20) NOT NULL,
                                Soyad VARCHAR(20) NOT NULL,
                                Telefon VARCHAR(11) NOT NULL,
                                Cinsiyet ENUM('Erkek','Kadın') NOT NULL,
                                Dogum_Tarih DATE NOT NULL,
                                Unvan VARCHAR(15) NOT NULL,
                                Maas DECIMAL(10,2) NOT NULL,
                                K_Adi VARCHAR(15) NOT NULL,
                                K_Sifre VARCHAR(30) NOT NULL,
                                Ise_Baslangic DATE NOT NULL,
                                Mail VARCHAR(50) NOT NULL
                            )engine=InnoDB;""")
        
        ###############################################################################################################
        # ÜYE TABLOSU
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS Uye 
                            (	Uye_ID INT PRIMARY KEY AUTO_INCREMENT,
                                TC VARCHAR(11) NOT NULL,
                                Ad VARCHAR(20) NOT NULL,
                                Soyad VARCHAR(20) NOT NULL,
                                Cinsiyet ENUM('Erkek','Kadın') NOT NULL,
                                Telefon VARCHAR(11) NOT NULL,
                                Dogum_Tarih DATE NOT NULL,
                                Dogum_Yer VARCHAR(20) NOT NULL,
                                Mail VARCHAR(50) NOT NULL,
                                Kayıt_Tarih DATE NOT NULL
                            )engine=InnoDB;""")

 # SATIS TABLOSU
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS Satis 
                            (	
                                Satis_ID INT PRIMARY KEY AUTO_INCREMENT,
                                Musteri_ID INT NOT NULL,
                                Urun_ID INT NOT NULL,
                                Adet INT NOT NULL,
                                Toplam_Fiyat DECIMAL(10,2) NOT NULL,
                                Satis_Tarih DATE NOT NULL,
                                CONSTRAINT fk_Satis_Musteri FOREIGN KEY (Musteri_ID) REFERENCES Musteriler(Musteri_ID),
                                CONSTRAINT fk_Satis_Urun FOREIGN KEY (Urun_ID) REFERENCES Urunler(Urun_ID)
                            )engine=InnoDB;""")
# ÜRÜN TABLOSU
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS Urun 
                            (	
                                Urun_ID INT PRIMARY KEY AUTO_INCREMENT,
                                Ad VARCHAR(30) NOT NULL,
                                Marka VARCHAR(30) NOT NULL,
                                Fiyat DECIMAL(10,2) NOT NULL,
                                Stok_Miktar INT NOT NULL,
                                Eklenme_Tarih DATE NOT NULL,
                            )engine=InnoDB;""")

# ÜRÜN GÖRÜNÜMÜ
        self.imlec.execute("""CREATE VIEW UrunView AS
                            SELECT 
                                Urun.Urun_ID,
                                Urun.Ad,
                                Urun.Marka,
                                Urun.Fiyat,
                                Urun.Stok_Miktar,
                                Urun.Eklenme_Tarih,
                            FROM Urun                   
                            """)

       

        ###############################################################################################################
        # IADE ALMA TABLOSU
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS Iade_Alma 
                            (	
                                Iade_ID INT PRIMARY KEY AUTO_INCREMENT,
                                Satis_ID INT NOT NULL,
                                Musteri_ID INT NOT NULL,
                                Urun_ID INT NOT NULL,
                                Alis_Tarih DATE NOT NULL,
                                Teslim_Tarih DATE NOT NULL,
                                Iade_Durum ENUM('Teslim Edilmedi','Teslim Edildi') DEFAULT 'Teslim Edilmedi',
                                Personel_ID INT NOT NULL,
                                CONSTRAINT fk_Iade_Satis FOREIGN KEY (Satis_ID) REFERENCES Satis(Satis_ID),
                                CONSTRAINT fk_Iade_Musteri FOREIGN KEY (Musteri_ID) REFERENCES Musteriler(Musteri_ID),
                                CONSTRAINT fk_Iade_Urun FOREIGN KEY (Urun_ID) REFERENCES Urunler(Urun_ID),
                                CONSTRAINT fk_Iade_Personel FOREIGN KEY (Personel_ID) REFERENCES Personel(Personel_ID)
                            )engine=InnoDB;""")

        ###############################################################################################################
        # GORUNUMLER
        self.imlec.execute("""CREATE VIEW satislist
                            AS 
                            SELECT
                                S.Satis_ID,
                                CONCAT(M.Ad, ' ', M.Soyad) AS Musteri_Ad_Soyad,
                                U.Urun_Ad AS Urun_Adi,
                                S.Adet,
                                S.Toplam_Fiyat,
                                S.Satis_Tarih
                            FROM
                                Satis S
                                INNER JOIN Musteriler M ON S.Musteri_ID = M.Musteri_ID
                                INNER JOIN Urunler U ON S.Urun_ID = U.Urun_ID;""")

        self.imlec.execute("""CREATE VIEW iadelist
                            AS
                            SELECT
                                IA.Iade_ID,
                                S.Satis_ID,
                                CONCAT(M.Ad, ' ', M.Soyad) AS Musteri_Ad_Soyad,
                                U.Urun_Ad AS Urun_Adi,
                                IA.Alis_Tarih,
                                IA.Teslim_Tarih,
                                IA.Iade_Durum,
                                P.Personel_ID
                            FROM
                                Iade_Alma IA
                                INNER JOIN Satis S ON IA.Satis_ID = S.Satis_ID
                                INNER JOIN Musteriler M ON IA.Musteri_ID = M.Musteri_ID
                                INNER JOIN Urunler U ON IA.Urun_ID = U.Urun_ID
                                INNER JOIN Personel P ON IA.Personel_ID = P.Personel_ID;""")

        self.mydb.commit()          
        print("\nTablolar Olusturuldu\n")


    def verileriGir(self):
        self.imlec.execute(f"""Insert Into personel values      (null, '11111111113', 'Selin', 'Çalışkan', '0531XXXXXXX', 'Kadın', '1995-01-15', 'Müdür', '20000.00', 'Şirket12', '1234', '2023-12-27', 'selin.caliskan@ornek.com'),
                                                            (null, '22222222224', 'Taylan', 'Durmaz', '0532XXXXXXX', 'Erkek', '1990-02-20', 'Çalışan', '18000.00', 'Şirket13', '5678', '2023-11-15', 'taylan.durmaz@ornek.com'),
                                                            (null, '33333333335', 'Ülkü', 'Erdem', '0533XXXXXXX', 'Kadın', '1987-03-25', 'Çalışan', '16000.00', 'Şirket14', '9101', '2023-10-10', 'ulku.erdem@ornek.com'),
                                                            (null, '44444444446', 'Volkan', 'Fidan', '0534XXXXXXX', 'Erkek', '1986-04-30', 'Çalışan', '19000.00', 'Şirket15', '1112', '2023-09-05', 'volkan.fidan@ornek.com'),
                                                            (null, '55555555557', 'Yasemin', 'Göktürk', '0535XXXXXXX', 'Kadın', '1992-05-05', 'Çalışan', '17000.00', 'Şirket16', '1314', '2023-08-20', 'yasemin.gokturk@ornek.com'),
                                                            (null, '66666666668', 'Zafer', 'Hacıoğlu', '0536XXXXXXX', 'Erkek', '1985-06-10', 'Çalışan', '22000.00', 'Şirket17', '1516', '2023-07-25', 'zafer.hacioglu@ornek.com'),
                                                            (null, '77777777779', 'Aslı', 'İlhan', '0537XXXXXXX', 'Kadın', '1991-07-15', 'Çalışan', '15000.00', 'Şirket18', '1718', '2023-06-30', 'asli.ilhan@ornek.com'),
                                                            (null, '88888888890', 'Burak', 'Johnson', '0538XXXXXXX', 'Erkek', '1984-08-20', 'Çalışan', '20000.00', 'Şirket19', '1920', '2023-05-15', 'burak.johnson@ornek.com'),
                                                            (null, '99999999991', 'Ceren', 'Kurtuluş', '0539XXXXXXX', 'Kadın', '1998-09-25', 'Çalışan', '14000.00', 'Şirket20', '2021', '2023-04-10', 'ceren.kurtulus@ornek.com'),
                                                            (null, '12345678902', 'Deniz', 'Levent', '0530XXXXXXX', 'Erkek', '1996-10-30', 'Çalışan', '21000.00', 'Şirket21', '2223', '2023-03-05', 'deniz.levent@ornek.com');""")
        
        self.imlec.execute(f"""Insert Into uye values      (null, '11111111114', 'Ege', 'Şentürk', 'Erkek', '0531XXXXXXX', '1997-01-05', 'İstanbul/Üsküdar', 'ege.senturk@ornek.com', '2023-12-27'),
                                                        (null, '22222222225', 'Fulya', 'Kurtuluş', 'Kadın', '0532XXXXXXX', '1992-02-10', 'Ankara/Çankaya', 'fulya.kurtulus@ornek.com', '2023-12-28'),
                                                        (null, '33333333336', 'Gazi', 'Topçu', 'Erkek', '0533XXXXXXX', '2001-03-15', 'İzmir/Konak', 'gazi.topcu@ornek.com', '2023-12-28'),
                                                        (null, '44444444447', 'Hazal', 'Öztürk', 'Kadın', '0534XXXXXXX', '1995-04-20', 'AntaMuratpaşa', 'hazal.ozturk@ornek.com', '2023-12-29'),
                                                        (null, '55555555558', 'İlkay', 'Çolak', 'Erkek', '0535XXXXXXX', '2000-05-25', 'Adana/Seyhan', 'ilkay.colak@ornek.com', '2023-12-30'),
                                                        (null, '66666666669', 'Janset', 'Yılmaz', 'Kadın', '0536XXXXXXX', '1996-06-30', 'Trabzon/Ortahisar', 'janset.yilmaz@ornek.com', '2024-01-01'),
                                                        (null, '77777777780', 'Kaan', 'Kılıç', 'Erkek', '0537XXXXXXX', '1993-08-05', 'Eskişehir/Tepebaşı', 'kaan.kilic@ornek.com', '2024-01-02'),
                                                        (null, '88888888891', 'Lale', 'Acar', 'Kadın', '0538XXXXXXX', '2002-09-10', 'Gaziantep/Şahinbey', 'lale.acar@ornek.com', '2024-01-03'),
                                                        (null, '99999999992', 'Mert', 'Ünlü', 'Erkek', '0539XXXXXXX', '1998-10-15', 'Bursa/Osmangazi', 'mert.unlu@ornek.com', '2024-01-04'),
                                                        (null, '12345678903', 'Nazlı', 'Çelik', 'Kadın', '0540XXXXXXX', '2003-11-20', 'İstanbul/Kadıköy', 'nazli.celik@ornek.com', '2024-01-05'),
                                                        (null, '23456789014', 'Okan', 'Kaya', 'Erkek', '0541XXXXXXX', '1996-12-25', 'Bursa/Karacabey', 'okan.kaya@ornek.com', '2024-01-06'),
                                                        (null, '34567890124', 'Pınar', 'Sarı', 'Kadın', '0542XXXXXXX', '2004-01-30', 'Konya/Meram', 'pinar.sari@ornek.com', '2023-12-27');""")

        self.imlec.execute(f"""Insert Into urun values         (null,'Gaming RAM 16GB','159','87145746532','2023-12-27','RAM','1','13','2021-04-19','1. Baskı'),
                                                                (null,'SSD 500GB','208','9788402156746','2023-12-27','Storage','2','26','2016-10-01','1. Baskı'),
                                                                (null,'Gaming GPU RTX 3080','320','9786210815327','2023-12-27','Graphics Card','3','26','2021-10-19','1. Baskı'),
                                                                (null,'Mechanical Gaming Keyboard','230','9786210815328','2023-12-27','Keyboard','4','26','1999-01-01','1. Baskı'),
                                                                (null,'Wireless Gaming Mouse','419','9786210815329','2023-12-28','Mouse','6','26','2013-09-01','3. Baskı'),
                                                                (null,'27-inch Gaming Monitor','304','9786210815330','2023-12-28','Monitor','7','5','2023-06-02','1. Baskı'),
                                                                (null,'Gaming Headset','256','9786210815331','2023-12-28','Headset','9','13','2023-08-14','1. Baskı'),
                                                                (null,'High-Performance Graphics Card','512','9786210815332','2023-12-28','Graphics Card','10','26','2022-01-04','1. Baskı'),
                                                                (null,'Gaming Laptop','360','9786210815333','2023-12-28','Laptop','11','26','2023-10-09','1. Baskı'),
                                                                (null,'RGB PC Case','112','9786210815334','2023-12-27','PC Case','5','32','2016-01-01','1. Baskı');""")      

 # Satis Tablosu Veri Ekleme
        self.imlec.execute(f"""Insert Into Satis values (null, 1, 1, 2, 318.00, '2023-12-27'),
                                                (null, 2, 3, 1, 320.00, '2023-12-28'),
                                                (null, 3, 5, 3, 657.00, '2023-12-28'),
                                                (null, 4, 7, 1, 256.00, '2023-12-28'),
                                                (null, 5, 9, 2, 720.00, '2023-12-28'),
                                                (null, 6, 11, 1, 360.00, '2023-12-28'),
                                                (null, 7, 2, 4, 832.00, '2023-12-28'),
                                                (null, 8, 4, 2, 838.00, '2023-12-28'),
                                                (null, 9, 6, 1, 419.00, '2023-12-28'),
                                                (null, 10, 8, 3, 1536.00, '2023-12-27');""")

# Iade_Alma Tablosu Veri Ekleme
        self.imlec.execute(f"""Insert Into Iade_Alma values (null, 1, 1, 1, '2023-12-27', '2023-12-28', 'Teslim Edildi', 1),
                                                     (null, 3, 5, 2, '2023-12-28', '2023-12-29', 'Teslim Edildi', 3),
                                                     (null, 5, 9, 1, '2023-12-28', '2023-12-29', 'Teslim Edildi', 5),
                                                     (null, 7, 2, 3, '2023-12-28', '2023-12-29', 'Teslim Edildi', 7),
                                                     (null, 9, 6, 1, '2023-12-28', '2023-12-29', 'Teslim Edildi', 9),
                                                     (null, 10, 8, 2, '2023-12-27', '2023-12-28', 'Teslim Edilmedi', 10),
                                                     (null, 2, 3, 1, '2023-12-28', '2023-12-29', 'Teslim Edildi', 2),
                                                     (null, 4, 7, 1, '2023-12-28', '2023-12-29', 'Teslim Edildi', 4),
                                                     (null, 6, 11, 1, '2023-12-28', '2023-12-29', 'Teslim Edildi', 6),
                                                     (null, 8, 4, 2, '2023-12-28', '2023-12-29', 'Teslim Edildi', 8);""")


        self.mydb.commit()
        print("Örnek Veriler Girildi\n")

    def baglantiyiKapat(self):
            self.mydb.close()
            print("Bağlantı kapatıltı\n\n---KURULUM İŞLEMLERİ TAMAMLANDI---\n")

class Login():

    def __init__(self):
            
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74"
        )
            self.imlec = self.mydb.cursor()
            self.imlec.execute("USE osman_db")
            self.mydb.commit()

    def login(self):
        while True:
            print("Sistemi kullanabilmek için personel girişi yapmanız gerekiyor.\n")
            kadi = input("Lütfen kullanıcı adını giriniz.\n")
            sifre = input("Lütfen şifrenizi giriniz.\n")
            if(len(kadi) <= 15 and len(sifre) <= 30):
                self.imlec.execute("SELECT * FROM personel WHERE K_Adi=%s AND K_Sifre=%s", (kadi, sifre,))
                sonuc = self.imlec.fetchall()
                count = self.imlec.rowcount
                if(count == 1):
                    return sonuc[0][0]
                else:
                    print("\033[1;31;40m Lütfen geçerli bir kullanıcı adı veya şifre girin. \033[0;0m\n")
            else:
                print("\033[1;31;40m Lütfen geçerli bir kullanıcı adı veya şifre girin. \033[0;0m\n")

class VT_Kontrol():

    def __init__(self):
            
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74"
        )
        self.imlec = self.mydb.cursor()
        self.imlec.execute("SHOW DATABASES LIKE 'osman_db';")
        sonuc=self.imlec.fetchall()
        count=self.imlec.rowcount
        if(count == 0):
            try:
                ilk_kurulum = VT_olustur()
                ilk_kurulum.tablolariOlustur()
                ilk_kurulum.verileriGir()
                ilk_kurulum.baglantiyiKapat()
            except:
                print("\n\nHata var\n\n")
        else:return None
        self.mydb.commit()
class Uye(): 

    def __init__(self):
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74"
        )
            self.imlec = self.mydb.cursor()
            self.imlec.execute("USE osman_db")
            self.mydb.commit()

    def listele(self):
            kod = "SELECT * FROM Uye;"
            self.imlec.execute(kod)
            self.sonuc = self.imlec.fetchall()

            for index, row in enumerate(self.sonuc, 1):
                print(f"{index}- TC => '{row[1]}' AD => '{row[2]}' SOYAD => '{row[3]}' CİNSİYET => '{row[4]}' TELEFON => '{row[5]}' DOĞUM_TARİHİ => '{row[6]}' DOĞUM_YERİ => '{row[7]}' MAİL => '{row[8]}' KAYIT_TARİHİ => '{row[9]}'\n")

    def __idkontrol(self):
            while True:
                id = input("Lütfen işlem yapmak istediğiniz numarayı giriniz (Çıkmak için x giriniz)\n")
                if (id == "x"):
                    return "x"
                elif (id.isdigit() and int(id) > 0):
                    try:
                        self.id = self.sonuc[int(id)-1][0]
                        break
                    except IndexError:
                        print("\033[1;31;40m Girdiğiniz sayı geçersiz. \033[0;0m\n")
                else:
                    print("\033[1;31;40m Lütfen geçerli bir sayı giriniz. \033[0;0m\n")


    def sutunGoruntule(self):
            self.imlec.execute("DESCRIBE Uye")
            self.columns = [column[0] for column in self.imlec.fetchall()]
            print("Sütunlar:")
            for i, column in enumerate(self.columns, 1):
                print(f"{i}. {column}")

    def sutunGoruntuleFiltre(self):
            self.imlec.execute("DESCRIBE Uye")
            self.columns = [column[0] for column in self.imlec.fetchall() if column[0] not in ['Uye_ID', 'Kayıt_Tarih']]

            print("Sütunlar:")
            for i, column in enumerate(self.columns, 1):
             print(f"{i}. {column}")

    def sutunKontrol(self):
            while True:
                ind = input("Seçmek istediğiniz sütunların numaralarını virgülle ayırarak girin: ").split(',')
                if (ind[0] == "x"):
                    return "x"
            
                elif all(index.isdigit()  and int(index) > 0 for index in ind):
                    try:
                        self.selected_columns = [self.columns[int(index) - 1] for index in ind]
                        break
                    except BaseException as error:
                        print('HATA: {}'.format(error))


    def veriEkle(self):
            print("!!!Girilecek Değerlerin Başında Eğer (*) Var İse Boş Bırakılamaz Lütfen Dikkate Alarak Doldurunuz!!! (Çıkmak için x giriniz.)\n")
            if(self.__tc() == "x"): return 1    
            if(self.__ad() == "x"): return 1    
            if(self.__soyad() == "x"): return 1 
            if(self.__cinsiyet() == "x"): return 1  
            if(self.__telefon() == "x"): return 1   
            if(self.__tarih() == "x"): return 1 
            if(self.__dogumYer() == "x"): return 1  
            if(self.__mail() == "x"): return 1 
            tarih = date.today()
            self.imlec.execute("INSERT INTO Uye (TC, Ad, Soyad, Cinsiyet, Telefon, Dogum_Tarih, Dogum_Yer, Mail, Kayıt_Tarih) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.tc, self.ad, self.soyad, self.cinsiyet, self.telefon, self.tarih, self.yer, self.mail, tarih))
            self.mydb.commit()
            print("Üye Ekleme İşlemi Başarıyla Tamamlandı...")

    
    def __tc(self):
        while True:
            self.tc = input("\n*TC: ")
            if(self.tc == "x"): return "x"
            elif(self.tc.isdigit() and len(self.tc) == 11):
                self.imlec.execute("SELECT * FROM uye WHERE TC=%s", (self.tc,))
                self.imlec.fetchall()
                count = self.imlec.rowcount
                if(count == 0):
                    break
                else:
                    print("\033[1;31;40m Sistemde bu TC numarası ile kayıtlı üye var. \033[0;0m\n")
            else:
                print("\033[1;31;40m Girdiğiniz TC numarası yanlış. \033[0;0m\n")
    
    def __ad(self):
        while True:
            self.ad = input("\n*Ad: ")
            if(self.ad == "x"): return "x"
            elif(len(self.ad) <= 20 and self.ad[0] != " " and self.ad[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz isim 20 karakterden uzun. \033[0;0m\n")
    
    def __soyad(self):
        while True:
            self.soyad = input("\n*Soyad: ")
            if(self.soyad == "x"): return "x"
            elif(len(self.soyad) <= 20 and self.soyad[0] != " " and self.soyad[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz isim 20 karakterden uzun. \033[0;0m\n")
    
    def __cinsiyet(self):
        while True:
            self.cinsiyet = input("\n*Cinsiyet (Erkek/Kadın): ")
            if(self.cinsiyet == "x"): return "x"
            elif(self.cinsiyet=="Erkek" or self.cinsiyet=="Kadın"):
                break
            else:
                print("\033[1;31;40m Yalnız Erkek veya Kadın seçebilirsiniz. \033[0;0m\n")

    def __telefon(self):
        while True:
            self.telefon = input("\n*Telefon (0 ile başlayacak): ")
            if(self.telefon == "x"): return "x"
            elif(self.telefon.isdigit() and len(self.telefon) == 11 and self.telefon.startswith('0')):
                break
            else:
                print("\033[1;31;40m Telefon numarasını 0 ile başlayacak şekilde girin. \033[0;0m\n")

    def __tarih(self):
        while True:
            self.tarih = input("\n*Doğum Tarihi (YYYY-MM-DD): ")
            if(self.tarih == "x"): return "x"
            try:
                format = "%Y-%m-%d"
                datetime.strptime(self.tarih, format)
                break
            except ValueError:
                print("\033[1;31;40m Doğum tarihi doğru formatta değil. \033[0;0m\n")

    def __dogumYer(self):
        while True:
            self.yer = input("\n*Doğum Yeri(İl/İlçe): ")
            if(self.yer == "x"): return "x"
            elif(len(self.yer) <= 20 and self.yer[0] != " " and self.yer[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz doğum yeri 20 karakterden uzun. \033[0;0m\n")

    def __mail(self):
        while True:
            self.mail = input("\n*Mail: ")
            if(self.mail == "x"): return "x"
            elif(len(self.mail) <= 50 and "@" in self.mail and "." in self.mail.split("@")[1]):
                break
            else:
                print("\033[1;31;40m Girdiğiniz mail 50 karakterden uzun veya mail formatında değil. \033[0;0m\n")


    def veriGuncelle(self):  
        self.listele()
        self.__idkontrol()
        self.sutunGoruntuleFiltre()

        def cagir(dgr):
            self.imlec.execute("UPDATE Uye SET {} = %s WHERE Uye_ID = %s".format(secili_kolon), (dgr, self.id))
            self.mydb.commit()
            print("Güncelleme İşlemi Başarıyla Tamamlandı.")

        while True: 
            secili_kolon = input("Lütfen Güncellemek İstediğiniz Numarayı Giriniz\n")
            if (str(secili_kolon) == "x"):
                return "x"
            
            elif (secili_kolon.isdigit() and int(secili_kolon) > 0):
                try:
                    secili_kolon = self.columns[int(secili_kolon)-1]
                    

                    if(secili_kolon=="TC"):
                        if(self.__tc() == "x"): return 1
                        cagir(self.tc)
                        break

                    elif(secili_kolon=="Telefon"):
                        if(self.__telefon() == "x"): return 1
                        cagir(self.telefon)
                        break

                    elif(secili_kolon=="Ad"):
                        if(self.__ad() == "x"): return 1
                        cagir(self.ad)
                        break
                    
                    elif(secili_kolon=="Soyad"):
                        if(self.__soyad() == "x"): return 1
                        cagir(self.soyad)
                        break
                    
                    elif(secili_kolon=="Cinsiyet"):
                        if(self.__cinsiyet() == "x"): return 1
                        cagir(self.cinsiyet)
                        break

                    elif(secili_kolon=="Dogum_Tarih"):
                        if(self.__tarih() == "x"): return 1
                        cagir(self.tarih)
                        break
                    

                    elif(secili_kolon=="Dogum_Yer"):
                        if(self.__dogumYer() == "x"): return 1
                        cagir(self.yer)
                        break

                    elif(secili_kolon=="Mail"):
                        if(self.__mail() == "x"): return 1
                        cagir(self.mail)
                        break

                except BaseException as error:
                    print('HATA: {}'.format(error))



    def veriSil(self):
        self.listele()
        s = self.__idkontrol()
        if (s == "x"):
            return 1
        try:
            self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
            self.imlec.execute("DELETE FROM Uye WHERE Uye_ID = %s;",(self.id,))
            self.mydb.commit()
            print("Üye Silme İşlemi Başarıyla Tamamlandı")

        except BaseException as error:
            print('HATA: {}'.format(error))


    def tümVerileriGetir(self):
        self.listele()


    def secilenSütunlarıGörüntüle(self):
        self.sutunGoruntule()
        s = self.sutunKontrol()
        if (s == "x"):
            return 1

        try:
            columns_str = ', '.join(self.selected_columns)

            self.imlec.execute(f"SELECT {columns_str} FROM Uye")
            result = self.imlec.fetchall()

            for row in result:
                print(', '.join(str(value) for value in row))

        except BaseException as error:
                    print('HATA: {}'.format(error))

         
    def sorguSilme(self):
        self.sutunGoruntule()
        self.sutunKontrol()
        while True:
            try:
                sorgu_degerleri = {}
                for column in self.selected_columns:
                    deger = input(f"{column} Sütunu için sorgu değerini girin: ")
                    sorgu_degerleri[column] = deger

                sorgu_kosullari = ' AND '.join(f"{column}"+"= %s" for column in self.selected_columns)

                self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
                sql_sorgusu = f"DELETE FROM Uye WHERE {sorgu_kosullari}"
                self.imlec.execute(sql_sorgusu, tuple(sorgu_degerleri.values()))

                self.mydb.commit()
                islem_sayisi = self.imlec.rowcount
                print(islem_sayisi, "Adet Silme İşlemi Başarıyla Gerçekleştirildi")
                break
            except BaseException as error:
                print('HATA: {}'.format(error))


    def __tc2(self):
        while True:
            self.tcc = input("\n*TC: ")
            if(self.tcc == "x"): return "x"
            elif(self.tcc.isdigit() and len(self.tcc) == 11):
                break
            else:
                print("\033[1;31;40m Girdiğiniz TC numarası yanlış. \033[0;0m\n")


    def TcUyeSorgula(self):
        print("Lütfen Sorgulamak İstediğiniz Üye'nin TC Kimlik Numarasını Giriniz\n")
        self.__tc2()
        try:
            self.imlec.execute("SELECT * FROM Uye WHERE TC = %s", (self.tcc,))
            members = self.imlec.fetchall()

            if members:
                 for index, row in enumerate(members, 1):
                    print(f"{index}-TC => '{row[1]}' AD => '{row[2]}' SOYAD => '{row[3]}' CİNSİYET => '{row[4]}' TELEFON => '{row[5]}' DOĞUM_TARİHİ => '{row[6]}' DOĞUM_YERİ => '{row[7]}' MAİL => '{row[8]}' KAYIT_TARİHİ => '{row[9]}'\n")

            else:
                print("\033[1;31;40m ÜYE BULUNAMADI. \033[0;0m\n")

            self.mydb.commit()

        except BaseException as error:
            print('HATA: {}'.format(error))


#ürün crud işlemleri
class Urun():
    def __init__(self):
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74"
        )
            self.imlec = self.mydb.cursor()
            self.imlec.execute("USE osman_db")
            self.mydb.commit()

    def listele(self):
        kod = "SELECT * FROM Urun;"
        self.imlec.execute(kod)
        self.sonuc = self.imlec.fetchall()

        for index, row in enumerate(self.sonuc, 1):
            print(f"{index}- AD => '{row[1]}' MARKA => '{row[2]}' FIYAT => '{row[3]}' STOK_MIKTAR => '{row[4]}' EKLENME_TARIH  => '{row[5]}'\n")

    def __idkontrol(self):
        while True:
            id = input("Lütfen işlem yapmak istediğiniz numarayı giriniz (Çıkmak için x giriniz)\n")
            if id == "x":
                return "x"
            elif id.isdigit() and int(id) > 0:
                try:
                    self.id = self.sonuc[int(id)-1][0]
                    break
                except IndexError:
                    print("\033[1;31;40m Girdiğiniz sayı geçersiz. \033[0;0m\n")
            else:
                print("\033[1;31;40m Lütfen geçerli bir sayı giriniz. \033[0;0m\n")

    def __urunAd(self):
        while True:
            self.urunad = input("\n*Ürün Ad: ")
            if self.urunad == "x":
                return "x"
            elif len(self.urunad) <= 30 and self.urunad[0] != " " and self.urunad[-1] != " ":
                break
            else:
                print("\033[1;31;40m Girdiğiniz ürün adı 30 karakterden uzun. \033[0;0m\n")

    def __urunMarka(self):
        while True:
            self.urunmarka = input("\n*Ürün Marka: ")
            if self.urunmarka == "x":
                return "x"
            elif len(self.urunmarka) <= 30 and self.urunmarka[0] != " " and self.urunmarka[-1] != " ":
                break
            else:
                print("\033[1;31;40m Girdiğiniz ürün marka adı 30 karakterden uzun. \033[0;0m\n")

    def __urunFiyat(self):
        while True:
            self.urunfiyat = input("\n*Ürün Fiyat: ")
            if self.urunfiyat == "x":
                return "x"
            elif len(self.urunfiyat) <= 10 and self.urunfiyat[0] != " " and self.urunfiyat[-1] != " " and self.urunfiyat.replace('.', '', 1).isdigit():
                break
            else:
                print("\033[1;31;40m Girdiğiniz fiyat uygun değil. \033[0;0m\n")

    def __urunStokMiktar(self):
        while True:
            self.urunstok = input("\n*Ürün Stok Miktar: ")
            if self.urunstok == "x":
                return "x"
            elif len(self.urunstok) <= 11 and self.urunstok[0] != " " and self.urunstok[-1] != " " and self.urunstok.isdigit():
                break
            else:
                print("\033[1;31;40m Lütfen geçerli bir stok miktarı giriniz. \033[0;0m\n")

    def veriEkle(self):
        try:
            print("!!!Girilecek Değerlerin Başında Eğer (*) Var İse Boş Bırakılamaz Lütfen Dikkate Alarak Doldurunuz!!! (Çıkmak için x giriniz.)\n")
            if self.__urunAd() == "x":
                return 1
            if self.__urunMarka() == "x":
                return 1
            if self.__urunFiyat() == "x":
                return 1
            if self.__urunStokMiktar() == "x":
                return 1
            eklenmetarih = date.today()
            self.imlec.execute("INSERT INTO Urun (Ad, Marka, Fiyat, Stok_Miktar, Eklenme_Tarih) VALUES (%s, %s, %s, %s, %s)", (self.urunad, self.urunmarka, self.urunfiyat, self.urunstok, eklenmetarih))
            self.mydb.commit()
            print("Ürün Ekleme İşlemi Başarıyla Tamamlandı...")

        except BaseException as error:
            print('HATA: {}'.format(error))

    def veriGuncelle(self):
        self.listele()
        self.__idkontrol()

        def cagir(dgr):
            self.imlec.execute("UPDATE Urun SET {} = %s WHERE Urun_ID = %s".format(secili_kolon), (dgr, self.id))
            self.mydb.commit()
            print("Güncelleme İşlemi Başarıyla Tamamlandı.")

        while True:
            secili_kolon = input("Lütfen Güncellemek İstediğiniz Numarayı Giriniz\n")
            if str(secili_kolon) == "x":
                return "x"
            
            elif secili_kolon.isdigit() and int(secili_kolon) > 0:
                try:
                    secili_kolon = self.columns[int(secili_kolon)-1]

                    if secili_kolon == "Ad":
                        if self.__urunAd() == "x":
                            return 1
                        cagir(self.urunad)
                        break

                    elif secili_kolon == "Marka":
                        if self.__urunMarka() == "x":
                            return 1
                        cagir(self.urunmarka)
                        break

                    elif secili_kolon == "Fiyat":
                        if self.__urunFiyat() == "x":
                            return 1
                        cagir(self.urunfiyat)
                        break

                    elif secili_kolon == "Stok_Miktar":
                        if self.__urunStokMiktar() == "x":
                            return 1
                        cagir(self.urunstok)
                        break

                except BaseException as error:
                    print('HATA: {}'.format(error))

    def veriSil(self):
        self.listele()
        s = self.__idkontrol()
        if s == "x":
            return 1
        try:
            self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
            self.imlec.execute("DELETE FROM Urun WHERE Urun_ID = %s;", (self.id,))
            
            self.mydb.commit()
            print("Ürün Silme İşlemi Başarıyla Tamamlandı")

        except BaseException as error:
            print('HATA: {}'.format(error))

    def tümVerileriGetir(self):
        self.listele()

    def secilenSütunlarıGörüntüle(self):
        sorgu_kosullari = self.sutunKontrol()
        if sorgu_kosullari == "x":
            return 1

        try:
            columns_str = ', '.join(self.selected_columns)

            self.imlec.execute(f"SELECT {columns_str} FROM Urun")
            result = self.imlec.fetchall()

            for row in result:
                print(', '.join(str(value) for value in row))

        except BaseException as error:
            print('HATA: {}'.format(error))

    def sorguSilme(self):
        self.sutunGoruntule()
        sorgu_kosullari = self.sutunKontrol()
        while True:
            try:
                sorgu_degerleri = {}
                for column in sorgu_kosullari:
                    deger = input(f"{column} Sütunu için sorgu değerini girin: ")
                    sorgu_degerleri[column] = deger

                sorgu_kosullari_str = ' AND '.join(f"{column}"+"= %s" for column in sorgu_kosullari)

                self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
                sql_sorgusu = f"DELETE FROM Urun WHERE {sorgu_kosullari_str}"
                self.imlec.execute(sql_sorgusu, tuple(sorgu_degerleri.values()))

                self.mydb.commit()
                islem_sayisi = self.imlec.rowcount
                print(islem_sayisi, "Adet Silme İşlemi Başarıyla Gerçekleştirildi")
                break
            except BaseException as error:
                print('HATA: {}'.format(error))

    def __ISBN2(self):
        while True:
            self.isbn2 = input("\n*ISBN: ")
            if self.isbn2 == "x":
                return "x"
            elif self.isbn2.isdigit() and len(self.isbn2) == 13:
                break
            else:
                print("\033[1;31;40m Girdiğiniz ISBN Numarası Yanlış. \033[0;0m\n")

    def ISBNurunSorgula(self):
        print("Lütfen Sorgulamak İstediğiniz Ürün'ün ISBN Numarasını Giriniz\n")
        self.__ISBN2()
        try:
            self.imlec.execute(f"SELECT * FROM Urun WHERE ISBN = {self.isbn2}")
            urunler = self.imlec.fetchall()

            if urunler:
                 for index, row in enumerate(urunler, 1):
                    print(f"{index}- AD => '{row[1]}' MARKA => '{row[2]}' FIYAT => '{row[3]}' STOK_MIKTAR => '{row[4]}' EKLENME_TARIH  => '{row[5]}'\n")

            else:
                print("\033[1;31;40m ÜRÜN BULUNAMADI. \033[0;0m\n")

            self.mydb.commit()

        except BaseException as error:
            print('HATA: {}'.format(error))


            #=============================================== PERSONEL TABLOSU ===========================================================
class Personel(): 
                
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74"
        )
        self.imlec = self.mydb.cursor()
        self.imlec.execute("USE osman_db")
        self.mydb.commit()
    def listele(self):
                    kod = "SELECT * FROM Personel;"
                    self.imlec.execute(kod)
                    self.sonuc = self.imlec.fetchall()
        
                    for index, row in enumerate(self.sonuc, 1):
                        print(f"{index}- TC => '{row[1]}' AD => '{row[2]}' SOYAD => '{row[3]}' TELEFON => '{row[4]}' CİNSİYET => '{row[5]}' ÜNVAN => '{row[6]}' MAAŞ => '{row[7]}' K.ADİ => '{row[8]}' SİFRE => '{row[9]}' İSE_BASLANGİC => '{row[10]}' ADRES => '{row[11]}' MAİL => '{row[12]}'\n")

    def __idkontrol(self):
        while True:
            id = input("Lütfen işlem yapmak istediğiniz numarayı giriniz (Çıkmak için x giriniz)\n")
            if (id == "x"):
                        return "x"
            elif (id.isdigit() and int(id) > 0):
                try:
                    self.id = self.sonuc[int(id)-1][0]
                    break
                except IndexError:
                    print("\033[1;31;40m Girdiğiniz sayı geçersiz. \033[0;0m\n")
            else:
                print("\033[1;31;40m Lütfen geçerli bir sayı giriniz. \033[0;0m\n")


    def sutunGoruntule(self):
        self.imlec.execute("DESCRIBE Personel")
        self.columns = [column[0] for column in self.imlec.fetchall()]
        print("Sütunlar:")
        for i, column in enumerate(self.columns, 1):
            print(f"{i}. {column}")

    def sutunGoruntuleFiltre(self):
        self.imlec.execute("DESCRIBE Personel")
        self.columns = [column[0] for column in self.imlec.fetchall() if column[0] not in ['Personel_ID']]

        print("Sütunlar:")
        for i, column in enumerate(self.columns, 1):
            print(f"{i}. {column}")

    def sutunKontrol(self):
        while True:
            ind = input("Seçmek istediğiniz sütunların numaralarını virgülle ayırarak girin: ").split(',')
            if (ind == "x"):
                return "x"
            
            elif all(index.isdigit()  and int(index) > 0 for index in ind):
                try:
                    self.selected_columns = [self.columns[int(index) - 1] for index in ind]
                    break
                except BaseException as error:
                    print('HATA: {}'.format(error))



    def veriEkle(self):
        print("!!!Girilecek Değerlerin Başında Eğer (*) Var İse Boş Bırakılamaz Lütfen Dikkate Alarak Doldurunuz!!! (Çıkmak için x giriniz.)\n")
        if(self.__tc() == "x"): return 1    
        if(self.__ad() == "x"): return 1    
        if(self.__soyad() == "x"): return 1 
        if(self.__cinsiyet() == "x"): return 1  
        if(self.__telefon() == "x"): return 1   
        if(self.__dtarih() == "x"): return 1 
        if(self.__Unvan() == "x"): return 1  
        if(self.__maas() == "x"): return 1  
        if(self.__kad() == "x"): return 1 
        if(self.__ksifre() == "x"): return 1  
        if(self.__mail() == "x"): return 1 
        if(self.__istarih() == "x"): return 1  
        self.imlec.execute("INSERT INTO Personel (TC, Ad, Soyad, Telefon, Cinsiyet, Dogum_Tarih, Unvan, Maas, K_Adi,K_Sifre,Ise_Baslangic,Mail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",(self.tc, self.ad, self.soyad, self.telefon, self.cinsiyet, self.dtarih, self.unvan, self.maas,self.kad,self.ksifre,self.istarih,self.mail))
        self.mydb.commit()
        print("Personel Ekleme İşlemi Başarıyla Tamamlandı...")

    
    def __tc(self):
        while True:
            self.tc = input("\n*TC: ")
            if(self.tc == "x"): return "x"
            elif(self.tc.isdigit() and len(self.tc) == 11):
                self.imlec.execute("SELECT * FROM Personel WHERE TC=%s", (self.tc,))
                self.imlec.fetchall()
                count = self.imlec.rowcount
                if(count == 0):
                    break
                else:
                    print("\033[1;31;40m Sistemde bu TC numarası ile kayıtlı personel var. \033[0;0m\n")
            else:
                print("\033[1;31;40m Girdiğiniz TC numarası yanlış. \033[0;0m\n")
    
    def __ad(self):
        while True:
            self.ad = input("\n*Ad: ")
            if(self.ad == "x"): return "x"
            elif(len(self.ad) <= 20 and self.ad[0] != " " and self.ad[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz isim 20 karakterden uzun. \033[0;0m\n")
    
    def __soyad(self):
        while True:
            self.soyad = input("\n*Soyad: ")
            if(self.soyad == "x"): return "x"
            elif(len(self.soyad) <= 20 and self.soyad[0] != " " and self.soyad[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz isim 20 karakterden uzun. \033[0;0m\n")
    
    def __cinsiyet(self):
        while True:
            self.cinsiyet = input("\n*Cinsiyet (Erkek/Kadın): ")
            if(self.cinsiyet == "x"): return "x"
            elif(self.cinsiyet=="Erkek" or self.cinsiyet=="Kadın"):
                break
            else:
                print("\033[1;31;40m Yalnız Erkek veya Kadın seçebilirsiniz. \033[0;0m\n")

    def __telefon(self):
        while True:
            self.telefon = input("\n*Telefon (0 ile başlayacak): ")
            if(self.telefon == "x"): return "x"
            elif(self.telefon.isdigit() and len(self.telefon) == 11 and self.telefon.startswith('0')):
                break
            else:
                print("\033[1;31;40m Telefon numarasını 0 ile başlayacak şekilde girin. \033[0;0m\n")

    def __dtarih(self):
        while True:
            self.dtarih = input("\n*Doğum Tarihi (YYYY-MM-DD): ")
            if(self.dtarih == "x"): return "x"
            try:
                format = "%Y-%m-%d"
                datetime.strptime(self.dtarih, format)
                break
            except ValueError:
                print("\033[1;31;40m Doğum tarihi doğru formatta değil. \033[0;0m\n")

    def __istarih(self):
        while True:
            self.istarih = input("\n*İşe Başlangıç Tarihi (YYYY-MM-DD): ")
            if(self.istarih == "x"): return "x"
            try:
                format = "%Y-%m-%d"
                datetime.strptime(self.istarih, format)
                break
            except ValueError:
                print("\033[1;31;40m Tarih doğru formatta değil. \033[0;0m\n")
    def __Unvan(self):
        while True:
            self.unvan = input("\n*Ünvan: ")
            if(self.unvan == "x"): return "x"
            elif(len(self.unvan) <= 15 and self.unvan[0] != " " and self.unvan[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz Ünvan 15 karakterden uzun. \033[0;0m\n")
    
    def __maas(self):
        while True:
            self.maas = input("\n*Maaş : ")
            if(self.maas == "x"): return "x"
            elif(self.maas.isdigit() and len(self.maas) <= 12):
                break
            else:
                print("\033[1;31;40m Girdiğiniz Maaş 12 karakter den uzun. \033[0;0m\n")


    def __mail(self):
        while True:
            self.mail = input("\n*Mail: ")
            if(self.mail == "x"): return "x"
            elif(len(self.mail) <= 50 and "@" in self.mail and "." in self.mail.split("@")[1]):
                break
            else:
                print("\033[1;31;40m Girdiğiniz mail 50 karakterden uzun veya mail formatında değil. \033[0;0m\n")

    def __kad(self):
        while True:
            self.kad = input("\n*Kulllanıcı Ad: ")
            if(self.kad == "x"): return "x"
            elif(len(self.kad) <= 15 and self.kad[0] != " " and self.kad[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz Kullanıcı adı 15 karakterden uzun. \033[0;0m\n")
    
    def __ksifre(self):
        while True:
            self.ksifre = input("\n*Kulllanıcı Şifre: ")
            if(self.ksifre == "x"): return "x"
            elif(len(self.ksifre) <= 15 and self.ksifre[0] != " " and self.ksifre[-1] != " "):
                break
            else:
                print("\033[1;31;40m Girdiğiniz şifre 30 karakterden uzun. \033[0;0m\n")
    

    def veriGuncelle(self):  
        self.listele()
        self.__idkontrol()
        self.sutunGoruntuleFiltre()

        def cagir(dgr):
            self.imlec.execute("UPDATE Personel SET {} = %s WHERE Personel_ID = %s".format(secili_kolon), (dgr, self.id))
            self.mydb.commit()
            print("Güncelleme İşlemi Başarıyla Tamamlandı.")

        while True: 
            secili_kolon = input("Lütfen Güncellemek İstediğiniz Numarayı Giriniz\n")
            if (str(secili_kolon) == "x"):
                return "x"
            
            elif (secili_kolon.isdigit() and int(secili_kolon) > 0):
                try:
                    secili_kolon = self.columns[int(secili_kolon)-1]
                    

                    if(secili_kolon=="TC"):
                        if(self.__tc() == "x"): return 1
                        cagir(self.tc)
                        

                    elif(secili_kolon=="Ad"):
                        if(self.__ad() == "x"): return 1
                        cagir(self.ad)
                        break
                    
                    elif(secili_kolon=="Soyad"):
                        if(self.__soyad() == "x"): return 1
                        cagir(self.soyad)
                        break

                    elif(secili_kolon=="Telefon"):
                        if(self.__telefon() == "x"): return 1
                        cagir(self.telefon)
                        break
                    
                    elif(secili_kolon=="Cinsiyet"):
                        if(self.__cinsiyet() == "x"): return 1
                        cagir(self.cinsiyet)
                        break

                    elif(secili_kolon=="Dogum_Tarih"):
                        if(self.__dtarih() == "x"): return 1
                        cagir(self.dtarih)
                        break
                    
                    elif(secili_kolon=="Unvan"):
                        if(self.__Unvan() == "x"): return 1
                        cagir(self.unvan)
                        break

                    elif(secili_kolon=="Maas"):
                        if(self.__maas() == "x"): return 1
                        cagir(self.maas)

                    elif(secili_kolon=="K_Adi"):
                        if(self.__kad() == "x"): return 1
                        cagir(self.kad)
                        break
                    
                    elif(secili_kolon=="K_Sifre"):
                        if(self.__ksifre() == "x"): return 1
                        cagir(self.ksifre)
                        break
                    
                    elif(secili_kolon=="Ise_Baslangic"):
                        if(self.__istarih() == "x"): return 1
                        cagir(self.istarih)
                    
                    elif(secili_kolon=="Mail"):
                        if(self.__mail() == "x"): return 1
                        cagir(self.mail)
                        break


                except BaseException as error:
                    print('HATA: {}'.format(error))



    def veriSil(self):
        self.listele()
        s = self.__idkontrol()
        if (s == "x"):
            return 1
        try:
            self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
            self.imlec.execute("DELETE FROM Personel WHERE Personel_ID = %s;",(self.id,))
            self.mydb.commit()
            print("Personel Silme İşlemi Başarıyla Tamamlandı")

        except BaseException as error:
            print('HATA: {}'.format(error))


    def tümVerileriGetir(self):
        self.listele()


    def secilenSütunlarıGörüntüle(self):
        self.sutunGoruntule()
        s = self.sutunKontrol()
        if (s == "x"):
            return 1

        try:
            columns_str = ', '.join(self.selected_columns)

            self.imlec.execute(f"SELECT {columns_str} FROM Personel") 
            result = self.imlec.fetchall()

            for row in result:
                print(', '.join(str(value) for value in row))

        except BaseException as error:
                    print('HATA: {}'.format(error))

        
    def sorguSilme(self):
        self.sutunGoruntule()
        self.sutunKontrol()
        while True:
            try:
                sorgu_degerleri = {}
                for column in self.selected_columns:
                    deger = input(f"{column} Sütunu için sorgu değerini girin: ")
                    sorgu_degerleri[column] = deger

                sorgu_kosullari = ' AND '.join(f"{column}"+"= %s" for column in self.selected_columns)

                self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
                sql_sorgusu = f"DELETE FROM Personel WHERE {sorgu_kosullari}"
                self.imlec.execute(sql_sorgusu, tuple(sorgu_degerleri.values()))

                self.mydb.commit()
                islem_sayisi = self.imlec.rowcount
                print(islem_sayisi, "Adet Silme İşlemi Başarıyla Gerçekleştirildi")
                break
            except BaseException as error:
                print('HATA: {}'.format(error))

    def __tc2(self):
        while True:
            self.tcc = input("\n*TC: ")
            if(self.tcc == "x"): return "x"
            elif(self.tcc.isdigit() and len(self.tcc) == 11):
                break
            else:
                print("\033[1;31;40m Girdiğiniz TC Kimlik numarası yanlış. \033[0;0m\n")


    def TcPersonelSorgula(self):
        print("Lütfen Sorgulamak İstediğiniz Personel'in TC Kimlik Numarasını Giriniz\n")
        self.__tc2()
        try:
            self.imlec.execute("SELECT * FROM Personel WHERE TC = %s", (self.tcc,))
            members = self.imlec.fetchall()

            if members:
                 for index, row in enumerate(members, 1):
                    print(f"{index}- TC => '{row[1]}' AD => '{row[2]}' SOYAD => '{row[3]}' TELEFON => '{row[4]}' CİNSİYET => '{row[5]}' ÜNVAN => '{row[6]}' MAAŞ => '{row[7]}' K.ADİ => '{row[8]}' SİFRE => '{row[9]}' İSE_BASLANGİC => '{row[10]}' ADRES => '{row[11]}' MAİL => '{row[12]}'\n")

            else:
                print("\033[1;31;40m PERSONEL BULUNAMADI. \033[0;0m\n")

            self.mydb.commit()

        except BaseException as error:
            print('HATA: {}'.format(error))


           #Satis

class Sattis(): 

    def __init__(self):
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74",
            database="osman_db"
        )
            self.imlec = self.mydb.cursor()
            self.mydb.commit()

    def satisYap(self, musteri_ID, urun_ID, adet, p_ID):
        if(self.__musteriKontrol(musteri_ID) == "x"): return 1
        if(self.__urunKontrol(urun_ID) == "x"): return 1
        tarih = date.today()
        self.imlec.execute("INSERT INTO Satis (Satis_ID, Musteri_ID, Urun_ID, Adet, Toplam_Fiyat, Satis_Tarih) VALUES (null, %s, %s, %s, %s, %s)", (musteri_ID, urun_ID, adet, self.__hesaplaToplamFiyat(urun_ID, adet), tarih,))
        self.mydb.commit()
        print("Satış yapıldı.\n")

    def satisIptal(self):
        if(self.tumVerileriGetir() == "x"): return 1
        if(self.__idKontrol() == "x"): return 1
        self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
        try:
            self.imlec.execute("DELETE FROM Satis WHERE Satis_ID=%s", (self.id,))
            self.mydb.commit()
            print("Yapılan satış iptal edildi.\n")
        except BaseException as error:
            print('HATA: {}'.format(error))

    def tumVerileriGetir(self):
        self.imlec.execute("SELECT * FROM Satis")
        self.sonuc = self.imlec.fetchall()
        if(len(self.sonuc) > 0):
            for index, v in enumerate(self.sonuc, 1):
                print(f"{index}- MUSTERI ID => {v[1]} URUN ID => {v[2]} ADET => {v[3]} TOPLAM FIYAT => {v[4]} SATIS TARİHİ => {v[5]}\n")
        else:
            print("\033[1;31;40m Sistemde kayıtlı satış yok. \033[0;0m\n")
            return "x"

    def __idKontrol(self):
        while True:
            i = input("Lütfen işlem yapmak istediğiniz numarayı giriniz (Çıkmak için x giriniz)\n")
            if (i == "x"):
                return "x"
            elif (i.isdigit() and int(i) > 0):
                try:
                    self.id = self.sonuc[int(i)-1][0]
                    break
                except IndexError:
                    print("\033[1;31;40m Girdiğiniz sayı geçersiz. \033[0;0m\n")
            else:
                print("\033[1;31;40m Lütfen geçerli bir sayı giriniz. \033[0;0m\n")

    def __musteriKontrol(self, musteri_ID):
        self.imlec.execute("SELECT * FROM Musteriler WHERE Musteri_ID=%s", (musteri_ID,))
        sonuc = self.imlec.fetchall()
        count = self.imlec.rowcount
        if(count == 0):
            print("\033[1;31;40m Sistemde bu müşteri ID'si ile kayıtlı müşteri yok. \033[0;0m\n")
            return "x"
        return None

    def __urunKontrol(self, urun_ID):
        self.imlec.execute("SELECT * FROM Urunler WHERE Urun_ID=%s", (urun_ID,))
        sonuc = self.imlec.fetchall()
        count = self.imlec.rowcount
        if(count == 0):
            print("\033[1;31;40m Sistemde bu ürün ID'si ile kayıtlı ürün yok. \033[0;0m\n")
            return "x"
        return None

    def __hesaplaToplamFiyat(self, urun_ID, adet):
        self.imlec.execute("SELECT Fiyat FROM Urunler WHERE Urun_ID=%s", (urun_ID,))
        fiyat_sonuc = self.imlec.fetchone()

        if fiyat_sonuc:
            fiyat = fiyat_sonuc[0]
            toplam_fiyat = fiyat * adet
            return toplam_fiyat
        else:
            print("\033[1;31;40m Bu ürün ID'sine ait fiyat bulunamadı. \033[0;0m\n")
            return None

    def bağlantıyıKes(self):
        self.mydb.close()

    def satisIstenilenVerileriGetir(self):
        n = input("\n1-Musteri ID\n2-Urun ID\n3-Tarih\n")
        if(n == "1"): 
            if(self.__musteriGetir() == "x"): return 1
        elif(n == "2"):
            if(self.__urunGetir() == "x"): return 1
        elif(n == "3"):
            if(self.__tarihGetir() == "x"): return 1
        else:
            print("\033[1;31;40m Yalnış numara yazdınız. \033[0;0m\n")

    def __musteriGetir(self):
        musteri_ID = input("Sorgulamak istediğiniz müşterinin ID'sini yazınız.\n")
        if(musteri_ID == "x"): return "x"
        self.imlec.execute("SELECT * FROM Satis WHERE Musteri_ID=%s", (musteri_ID,))
        sonuc = self.imlec.fetchall()
        if(len(sonuc) > 0):
            for index, row in enumerate(sonuc, 1):
                print(f"{index}- MUSTERI ID => {row[1]} URUN ID => {row[2]} ADET => {row[3]} TOPLAM FIYAT => {row[4]} SATIS TARİHİ => {row[5]}\n")
        else:
            print("\033[1;31;40m Bu müşteri ID'sine kayıtlı satış bulunamadı. \033[0;0m\n")
    
    def __urunGetir(self):
        urun_ID = input("Sorgulamak istediğiniz ürünün ID'sini yazınız.\n")
        if(urun_ID == "x"): return "x"
        self.imlec.execute("SELECT * FROM Satis WHERE Urun_ID=%s", (urun_ID,))
        sonuc = self.imlec.fetchall()
        if(len(sonuc) > 0):
            for index, row in enumerate(sonuc, 1):
                print(f"{index}- MUSTERI ID => {row[1]} URUN ID => {row[2]} ADET => {row[3]} TOPLAM FIYAT => {row[4]} SATIS TARİHİ => {row[5]}\n")
        else:
            print("\033[1;31;40m Bu ürün ID'sine kayıtlı satış bulunamadı. \033[0;0m\n")

    def __tarihGetir(self):
        while True:
            tarih = input("Sorgulamak istediğiniz tarihi yazın (YYYY-MM-DD):\n")
            if(tarih == "x"): return "x"
            try:
                format = "%Y-%m-%d"
                datetime.strptime(tarih, format)
                self.imlec.execute("SELECT * FROM Satis WHERE Satis_Tarih=%s", (tarih,))
                sonuc = self.imlec.fetchall()
                if(len(sonuc) > 0):
                    for index, row in enumerate(sonuc, 1):
                        print(f"{index}- MUSTERI ID => {row[1]} URUN ID => {row[2]} ADET => {row[3]} TOPLAM FIYAT => {row[4]} SATIS TARİHİ => {row[5]}\n")
                else:
                    print("\033[1;31;40m Bu tarihte satış yok. \033[0;0m\n")
                break
            except ValueError:
                print("\033[1;31;40m Girdiğiniz tarih doğru formatta değil. \033[0;0m\n")


#iade crud
                

class Iade():

    def __init__(self):
                self.mydb = mysql.connector.connect(
            host="localhost",
            user="tester",
            password="Tester_74",
            database="osman_db"
        )
                self.imlec = self.mydb.cursor()
                self.mydb.commit()

    def iadeAlma(self, personel):
        if(self.__uyeKontrol() == "x"): return 1
        if(self.__urunKontrol() == "x"): return 1
        self.imlec.execute("SELECT * FROM Iade_Alma WHERE Musteri_ID=%s AND Urun_ID=%s", (self.tc, self.urun_id,))
        sonuc = self.imlec.fetchall()
        teslimTarih = date.today()
       
        
        durum = "Teslim Edildi"
       
        self.imlec.execute("""
            INSERT INTO Iade_Alma 
            (Iade_ID, Satis_ID, Musteri_ID, Urun_ID, Alis_Tarih, Teslim_Tarih, Iade_Durum, Personel_ID) 
            VALUES 
            (null, %s, %s, %s, %s, %s, %s, %s)
        """, (sonuc[0][0], sonuc[0][1], sonuc[0][2], sonuc[0][3], teslimTarih, durum, personel))
        self.mydb.commit()
        self.__oduncSil(sonuc[0][0])
    def __oduncSil(self, id):
        try:
            self.imlec.execute("SET FOREIGN_KEY_CHECKS=OFF;")
            self.imlec.execute("DELETE FROM Iade_Alma WHERE Iade_ID=%s", (id,))
            self.mydb.commit()
            print("Urun iade alındı.\n")
        except BaseException as error:
            print('HATA: {}'.format(error))

    def tumVerileriGetir(self):
        self.imlec.execute("SELECT * FROM Iade_Alma")
        sonuc = self.imlec.fetchall()
        if(len(sonuc) > 0):
            for index, row in enumerate(sonuc, 1):
                print(f"{index}- MUSTERI ADI => {row[2]} URUN ADI => {row[3]} ALIS TARİHİ => {row[4]} TESLIM TARİHİ  => {row[5]}  IADE DURUMU => {row[6]} PERSONEL => {row[7]} \n")
        else:
            print("\033[1;31;40m Sistemde kayıtlı iade yok. \033[0;0m\n")

    def istenilenVerileriGetir(self):
        n = input("\n1-İsim\n2-Ürün\n3-Tarih\n")
        if(n == "1"):
            if(self.__musteriVeri() == "x"): return 1
        elif(n == "2"):
            if(self.__urunVeri() == "x"): return 1
        elif(n == "3"):
            if(self.__tarihVeri() == "x"): return 1
        else:
            print("\033[1;31;40m Yalnış numara yazdınız. \033[0;0m\n")

    def __musteriVeri(self):
        musteri = input("Sorgulamak istediğiniz müşterinin adını yazın\n")
        if (musteri == "x"): return "x"
        self.imlec.execute("SELECT * FROM Iade_Alma WHERE Musteri_ID=%s", (musteri,))
        sonuc = self.imlec.fetchall()
        if(len(sonuc) > 0):
            for index, row in enumerate(sonuc, 1):
                print(f"{index}- MUSTERI ADI => {row[2]} URUN ADI => {row[3]} ALIS TARİHİ => {row[4]} TESLIM TARİHİ  => {row[5]}  IADE DURUMU => {row[6]} PERSONEL => {row[7]} \n")
        else:
            print("\033[1;31;40m Sistemde kayıtlı iade yok. \033[0;0m\n")

    def __urunVeri(self):
        urun = input("Sorgulamak istediğiniz ürünü yazın\n")
        if(urun == "x"): return "x"
        self.imlec.execute("SELECT * FROM Iade_Alma WHERE Urun_ID=%s", (urun,))
        sonuc = self.imlec.fetchall()
        if(len(sonuc) > 0):
            for index, row in enumerate(sonuc, 1):
                print(f"{index}- MUSTERI ADI => {row[2]} URUN ADI => {row[3]} ALIS TARİHİ => {row[4]} TESLIM TARİHİ  => {row[5]}  IADE DURUMU => {row[6]} PERSONEL => {row[7]} \n")
        else:
            print("\033[1;31;40m Sistemde kayıtlı iade yok. \033[0;0m\n")

    def __tarihVeri(self):
        while True:
            tarih = input("Sorgulamak istediğiniz tarihi yazın (YYYY-MM-DD):\n")
            if(tarih == "x"): return "x"
            try:
                format = "%Y-%m-%d"
                datetime.strptime(tarih, format)
                self.imlec.execute("SELECT * FROM Iade_Alma WHERE Alis_Tarih=%s OR Teslim_Tarih=%s", (tarih, tarih))
                sonuc = self.imlec.fetchall()
                if(len(sonuc) > 0):
                    for index, row in enumerate(sonuc, 1):
                        print(f"{index}- MUSTERI ADI => {row[2]} URUN ADI => {row[3]} ALIS TARİHİ => {row[4]} TESLIM TARİHİ  => {row[5]}  IADE DURUMU => {row[6]} PERSONEL => {row[7]} \n")
                else:
                    print("\033[1;31;40m Sistemde kayıtlı iade yok. \033[0;0m\n")
                break
            except ValueError:
                print("\033[1;31;40m Girdiğiniz tarih doğru formatta değil. \033[0;0m\n")

    def __uyeKontrol(self):
        while True:
            tc = input("Lütfen ürün alan müşterinin TC numarasını giriniz (Çıkmak için x giriniz)\n")
            if(tc == "x"):
                return "x"
            elif(tc.isdigit() and len(tc) == 11):
                self.imlec.execute("SELECT * FROM Musteriler WHERE TC=%s", (tc,))
                sonuc = self.imlec.fetchall()
                count = self.imlec.rowcount
                if(count == 0):
                    print("\033[1;31;40m Sistemde bu TC numarası ile kayıtlı müşteri yok. \033[0;0m\n")
                elif(count == 1):
                    self.tc = sonuc[0][0]
                    break
                else:
                    print("\033[1;31;40m Sistemde bu TC numarası ile kayıtlı birden fazla müşteri var. Kayıt düzeltilmeden işlem yapılamaz. \033[0;0m\n")
                    break
            else:
                print("\033[1;31;40m Girdiğiniz TC numarası yanlış. \033[0;0m\n")

    def __urunKontrol(self):
        while True:
            urun_id = input("Lütfen iade edilen ürünün ID numarasını giriniz (Çıkmak için x giriniz)\n")
            if(urun_id == "x"):
                return "x"
            elif(urun_id.isdigit()):
                self.imlec.execute("SELECT * FROM Urunler WHERE Urun_ID=%s", (urun_id,))
                sonuc = self.imlec.fetchall()
                count = self.imlec.rowcount
                if(count == 0):
                    print("\033[1;31;40m Sistemde bu ID numarası ile kayıtlı ürün yok. \033[0;0m\n")
                elif(count == 1):
                    self.urun_id = sonuc[0][0]
                    break
                else:
                    print("\033[1;31;40m Sistemde bu ID numarası ile kayıtlı birden fazla ürün var. Kayıt düzeltilmeden işlem yapılamaz. \033[0;0m\n")
            else:
                print("\033[1;31;40m Girdiğiniz ID numarası yanlış. \033[0;0m\n")

    def baglantiyiKes(self):
        self.mydb.close()