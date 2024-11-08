import requests
from bs4 import BeautifulSoup
import json

# Benzersiz ürünleri saklamak için bir liste oluşturun
urun_listesi = []

domain = "www.fidanburada.com"
# En az 5 sayfa verisi almak için döngü başlat
for sayfa in range(1, 15):  # 1'den başlayarak 5 sayfayı çekelim
    url = f"https://{domain}/bitkiler?ps={sayfa}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Tüm ürün kartlarını bul
    urun_kartlari = soup.find_all("div", class_="w-100 bg-white ease border-round")

    # Sayfada ürün kartı yoksa, döngüyü durdur
    if not urun_kartlari:
        print(f"Sayfa {sayfa} veri içermiyor. İşlem sonlandırıldı.")
        break

    for urun in urun_kartlari:
        # Ürün bilgilerini çekme
        urun_adi_element = urun.find("a", class_="col-12 product-title")
        urun_adi = urun_adi_element.get_text(strip=True) if urun_adi_element else "Ürün adı bulunamadı"

        fiyat_element = urun.find("strong", class_="fw-black product-price")
        fiyat = fiyat_element.get_text(strip=True) if fiyat_element else "Fiyat bulunamadı"

        resim_elementi = urun.find("picture", class_="image-inner").find("img")
        resim_url = resim_elementi.get("src") if resim_elementi else "Resim bulunamadı"

        # Ürün bilgilerini bir sözlük olarak saklayın
        urun_bilgisi = {
            "site_name": domain,
            "urun_adi": urun_adi,
            "fiyat": fiyat,
            "resim_url": resim_url
        }

        # Ürün zaten listede yoksa ekleyin
        if urun_bilgisi not in urun_listesi:
            urun_listesi.append(urun_bilgisi)

    print(f"Sayfa {sayfa} başarıyla işlendi.")

# Tüm ürün bilgilerini JSON dosyasına kaydedin
with open("tum_urunler.json", "w", encoding="utf-8") as f:
    json.dump(urun_listesi, f, ensure_ascii=False, indent=4)

print("Tüm ürün bilgileri 'tum_urunler.json' dosyasına kaydedildi.")
