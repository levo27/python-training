import requests  # İnternet üzerinden veri çekmek için gerekli kütüphane

# Şehir adını alıp, koordinatlarını Open-Meteo'nun geocoding API'siyle bulur
def get_coordinates(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"  # Koordinat bulma API'si URL'si
    params = {"name": city, "count": 1, "language": "tr"}  # API'ye gönderilecek parametreler: şehir adı, 1 sonuç, Türkçe
    r = requests.get(geo_url, params=params)  # GET isteği atılır
    r.raise_for_status()  # Eğer istek başarısızsa hata fırlatır
    results = r.json().get("results")  # JSON'dan sonuçlar alınır
    if not results:  # Eğer sonuç yoksa
        raise Exception(f"Şehir bulunamadı: {city}")  # Hata ver
    loc = results[0]  # İlk sonucu al
    return loc["latitude"], loc["longitude"], loc["name"], loc.get("country", "")  # Enlem, boylam, şehir ismi, ülke

# Koordinatlar verildiğinde Open-Meteo'dan hava durumu verisini alır
def get_weather(lat, lon):
    weather_url = "https://api.open-meteo.com/v1/forecast"  # Hava durumu API URL'si
    params = {
        "latitude": lat,  # Enlem
        "longitude": lon,  # Boylam
        "current": "temperature_2m,wind_speed_10m,precipitation",  # İstediğimiz veriler: sıcaklık, rüzgar hızı, yağış
        "timezone": "auto"  # Yerel saat dilimine göre zamanlama
    }
    r = requests.get(weather_url, params=params)  # GET isteği atılır
    r.raise_for_status()  # Başarısızsa hata fırlatır
    return r.json()["current"]  # Güncel hava durumunu döndürür

def main():
    city = input("Hangi şehrin hava durumunu öğrenmek istiyorsunuz? : ")  # Kullanıcıdan şehir adı al
    try:
        # Şehirden koordinatları al
        lat, lon, name, country = get_coordinates(city)
        # Koordinatlarla hava durumu al
        weather = get_weather(lat, lon)
        # Sonuçları güzelce yazdır
        print(f"\n📍 {name}, {country}")
        print(f"🌡️ Sıcaklık: {weather['temperature_2m']} °C")
        print(f"🌬️ Rüzgar: {weather['wind_speed_10m']} km/s")
        print(f"🌧️ Yağış: {weather['precipitation']} mm")
    except Exception as e:  # Herhangi hata olursa yakala
        print(f"Hata: {e}")  # Hata mesajını göster

# Bu dosya doğrudan çalıştırıldığında main() fonksiyonunu başlat
if __name__ == "__main__":
    main()
