# DgmCraft Başlatıcı — Genel Yönetici Kurulum Notu

Teknoloji: Python 3.12 + Tkinter (stdlib) + PyInstaller. Harici pip paketi yok. Arayüz `ui/theme.py` içinde (siteyle aynı dil: warm-dark + amber, saf siyah yok).

## Bootstrapper (arkadaş yolu)
- `launcher/stub/kurulum_stub.py` tek dosya derlenir (`DgmCraft-Kurulum.exe`): latest zip + SHA256 indirir, doğrular, AppData'ya kurar, kısayol koyar, başlatır.
- Yarım/bozuk indirme çöpe atılır, doğrulamasız paket çalıştırılmaz.
- Release'te 3 dosya olur: `DgmCraft-windows.zip`, `.sha256`, `DgmCraft-Kurulum.exe`.

## AI Yardım (sınırlı)
- Komut satırındaki "AI Yardım" düğmesi: sorunu yazarsın, durum özeti + son konsol ile birlikte ucuz modele sorar, Türkçe teşhis verir.
- AI komut çalıştırmaz, dosya yazmaz, ayar değiştirmez.
- Anahtar koda/repoya gömülmez: Ayarlar > AI anahtarı alanına yapıştırılır, `%LOCALAPPDATA%\DgmCraft\openai.key` dosyasında saklanır (kullanıcıya özel izinli).
- Varsayılan model: `gpt-4o-mini` (`core/ai.py`). Anahtar limitli tutulur.

## Derleme
1. Python 3.12 64-bit kur (derleme makinesine).
2. `launcher/build/build_onefile.ps1` çalıştır.
3. Çıktı `dist/DgmCraft/` klasörünü sunucu köküne (`purpur.jar` yanına) kopyala.

## İlk dağıtım
- `kurulum-anahtari.txt` dosyasını sunucu köküne koy (Tailscale pre-auth key, tek satır). Sihirbaz ilk açılışta okur veya kullanıcı 1. ekrana yapıştırır. Sonra dosyayı sil.
- Kullanıcı uygulamayı açar: Ad + anahtarı girer -> 2. ekranda anlatılan Syncthing ve Tailscale kurulumlarını kendisi yapar -> Kontrol Et (üçü yeşil olmalı) -> Eşleştir -> Hazır.
- Uygulama indirme/kurulum yapmaz; sadece kurulu mu, çalışıyor mu, bağlı mı diye doğrular. VPN bağlantısı Ayarlar > VPN Bağlan ile (saklanan anahtarla) yapılır.
- JVM bayrakları `core/constants.py` içinde sabit: `-Dfile.encoding=UTF-8 -Duser.language=en -Duser.country=US -Xms3G -Xmx3G --nogui`. Kullanıcı değiştiremez. dogrulanmadi: Purpur 26.2 build 2633 ile yük testi genel yönetici yapmalıdır.

## Sözleşmeler (site yöneticisi için)
- Site klasörü: göreli `site/`, yayın yalnızca VPN IP üzerinde, varsayılan port 8000.
- `GET /api/log`: `logs/latest.log` son 200 satır JSON.
- `POST /api/cmd`: `{"komut":"...","onayKodu":"..."}`. `stop,op,deop,restart,reload,save-off` önce onay sorusu döndürür.
- `site-link.txt`: `http://<vpn-ip>:<port>`. VPN kapalıysa yazılmaz, Skript "site şu an kapalı" der.

## Test
1. İlk kurulum: 3 PC'de sihirbaz, eşitleme %100, site açılıyor mu.
2. Host değişimi: A güvenli kapat (kilit silinir), B başlat (dünya devam).
3. Çökme: kilit kalp atışı 10 dk eskiyse B devralır, "önceki kilit ölü bulundu" yazar.

## Sınırlamalar (dogrulanmadi)
- Syncthing/Tailscale indirme URL ve sürümleri örnek, güncellenmelidir.
- SmartScreen ilk açılışta "Yine de çalıştır" ister (ücretsiz imza yok).
- ZeroTier alternatifi: panel onayı gerekir, bu yüzden varsayılan Tailscale.
