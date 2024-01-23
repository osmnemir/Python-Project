import bil_proje as fd


def VeritabaniHazirlama():
    try:
        ilk_kurulum = fd.VT_olustur()
        ilk_kurulum.tablolariOlustur()
        ilk_kurulum.verileriGir()
        ilk_kurulum.baglantiyiKapat()
    except:
        print("\n\nHata var\n\n")
#---------------------------------------------------
fd.VT_Kontrol()
p_id = fd.Login().login()

while True:
    
    print("\n\n","-"*50)


    print("\033[1;32;40mYonca Kütüphanesi\033[0;0m\033[1;33;40m'ne Hoşgeldiniz! İşlem yapmak istediğiniz tabloyu lütfen seçiniz\033[0;0m")


    Secenekler=["Üyeler","Kitap","Personel","Ödünç Alma","İade Alma"]
    for i , sec in enumerate(Secenekler,1):
            print(i,"-",sec)

    secim=input("Kullanmak istediğiniz menüyü seçiniz (çıkmak için x giriniz)\n")

    if secim == "0":
        VeritabaniHazirlama()
        print("")

    

       

###################################### ÜYE ARAYÜZ #################################################
            
    elif secim=="1":



        print("\033[1;32;40mÜye Arayüzüne Hoşgeldiniz Lütfen Yapmak İstediğiniz İşlemi Seçiniz \033[0;0m")

        Secenekler=["Veri Ekleme","Tüm Verileri Göster","ID İle Silme","Bilgi Güncelleme","Seçilen Sütunları Göster","Sorgu İle Silme","TC ile Üye Sorgulama"]
        for i , sec in enumerate(Secenekler,1):
            print(i,"-",sec)

        icsecim=input("\n Lütfen İşlem Yapmak İstediğiniz Menüyü Sayı İle Tuşlayınız: ")

        if icsecim=="1":
            fd.Uye().veriEkle()

        elif icsecim=="2":
            fd.Uye().tümVerileriGetir()
        
        elif icsecim=="3":
            fd.Uye().veriSil()
        
        elif icsecim=="4":
            fd.Uye().veriGuncelle()       

        elif icsecim=="5":
            fd.Uye().secilenSütunlarıGörüntüle()     

        elif icsecim=="6":
            fd.Uye().sorguSilme()
        elif icsecim=="7":
            fd.Uye().TcUyeSorgula()

 
 ####################################################### ÜRÜN ARAYÜZ ##################################
    elif secim=="2":

            print("\033[1;33;40mÜrünArayüzüne Hoşgeldiniz! Lütfen Yapmak İstediğiniz İşlemi Seçiniz\033[0;0m")


            Secenekler=["Veri Ekleme","Tüm Verileri Göster","ID İle Silme","Bilgi Güncelleme","Seçilen Sütunları Göster","Sorgu İle Silme","ISBN ile Kitap Sorgulama"]
            for i , sec in enumerate(Secenekler,1):
                print(i,"-",sec)

            icsecim=input("\n Lütfen İşlem Yapmak İstediğiniz Menüyü Sayı İle Tuşlayınız: ")

            if icsecim=="1":
                fd.Urun().veriEkle()

            elif icsecim=="2":
                fd.Urun().tümVerileriGetir()
            
            elif icsecim=="3":
                fd.Urun().veriSil()
            
            elif icsecim=="4":
                fd.Urun().veriGuncelle()       

            elif icsecim=="5":
                fd.Urun().secilenSütunlarıGörüntüle()     

            elif icsecim=="6":
                fd.Urun().sorguSilme()
            elif icsecim=="7":
                fd.Urun().ISBNkitapSorgula()
                

 ####################################################### PERSONEL ARAYÜZ ##################################


    elif secim=="3":
            
            print("\033[1;35;40mPersonel Arayüzüne Hoşgeldiniz! Lütfen Yapmak İstediğiniz İşlemi Seçiniz\033[0;0m")


            Secenekler=["Veri Ekleme","Tüm Verileri Göster","ID İle Silme","Bilgi Güncelleme","Seçilen Sütunları Göster","Sorgu İle Silme","TC ile Personel Sorgulama"]
            for i , sec in enumerate(Secenekler,1):
                print(i,"-",sec)

            icsecim=input("\n Lütfen İşlem Yapmak İstediğiniz Menüyü Sayı İle Tuşlayınız: ")

            if icsecim=="1":
                fd.Personel().veriEkle()

            elif icsecim=="2":
                fd.Personel().tümVerileriGetir()
            
            elif icsecim=="3":
                fd.Personel().veriSil()
            
            elif icsecim=="4":
                fd.Personel().veriGuncelle()       

            elif icsecim=="5":
                fd.Personel().secilenSütunlarıGörüntüle()     

            elif icsecim=="6":
                fd.Personel().sorguSilme()
            elif icsecim=="7":
                fd.Personel().TcPersonelSorgula()

 
            
####################################################### SATIŞ ARAYÜZ ##################################  
              
    elif secim=="4":
            print("\033[1;33;40mÖdünç Alma Arayüzüne Hoşgeldiniz! Lütfen Yapmak İstediğiniz İşlemi Seçiniz\033[0;0m")



            Secenekler=["Ödünç Al Kayıt İşlemi","Tüm Verileri Göster","Ödünç Kayıt Silme İşlemi","İstenilen Verileri Getir"]
            for i , sec in enumerate(Secenekler,1):
                print(i,"-",sec)

            icsecim=input("\n Lütfen İşlem Yapmak İstediğiniz Menüyü Sayı İle Tuşlayınız: ")

            if icsecim=="1":
                fd.Sattis().oduncAl(p_id)

            elif icsecim=="2":
                fd.Sattis().tumVerileriGetir()
            
            elif icsecim=="3":
                fd.Sattis().oduncSil()
            
            elif icsecim=="4":
                fd.Sattis().istenilenVerileriGetir()      
           

    
    elif secim == "x" or secim == "X":
        print("Uygulama sonlandırıldı\n")
        break

####################################################### İADE ARAYÜZ ##################################  

    elif secim=="5":
            print("\033[1;32;40mİade Etme Arayüzüne Hoşgeldiniz! Lütfen Yapmak İstediğiniz İşlemi Seçiniz\033[0;0m")

            Secenekler=["İade Alma İşlemi","Tüm Verileri Göster","İstenilen Verileri Getir"]
            for i , sec in enumerate(Secenekler,1):
                print(i,"-",sec)

            icsecim=input("\n Lütfen İşlem Yapmak İstediğiniz Menüyü Sayı İle Tuşlayınız: ")

            if icsecim=="1":
                fd.Iade().iadeAl(p_id)

            elif icsecim=="2":
                fd.Iade().tümVerileriGetir()
            
            elif icsecim=="3":
                fd.Iade().istenilenVerileriGetir()       

    
    elif secim == "x" or secim == "X":
        print("Uygulama sonlandırıldı\n")
        break



