"""Sabitler. JVM bayrakları kodda sabit, kullanıcı değiştiremez."""
JVM_SABIT_BAYRAKLAR = ["-Dfile.encoding=UTF-8", "-Duser.language=en", "-Duser.country=US"]
HEAP_BAYRAKLARI = ["-Xms3G", "-Xmx3G"]
NOGUI_BAYRAGI = "--nogui"
BEKLENEN_JAVA_MAJOR = 25
OYUN_PORT = 25565
RCON_VARSAYILAN_PORT = 25575
SITE_VARSAYILAN_PORT = 8000
KALP_ATISI_SN = 60
KILIT_OLUM_ESIGI_SN = 600
KAPANMA_SAVE_BEKLEME_SN = 10
KAPANMA_UST_SINIR_SN = 90
TEHLIKELI_KOMUTLAR = ("stop", "op", "deop", "restart", "reload", "save-off")
SAHIP_DOSYASI = ".sahip"
GITHUB_REPO = "xpike-dgm/dgmcraft"
ESITLEME_DISLAMA = ["(?d)backups", "(?d)logs", "(?d)cache", "(?d).stversions", "*.tmp", "*.part", "(?d).sahip"]
KLASOR_ID = "dgmcraf-sunucu"
SYNCTHING_SURUM = "1.27.12"
TAILSCALE_SURUM = "1.62.0"
SYNCTHING_INDIRME_ADRESI = "https://github.com/syncthing/syncthing/releases/download/v1.27.12/syncthing-windows-amd64-v1.27.12.zip"
TAILSCALE_INDIRME_ADRESI = "https://pkgs.tailscale.com/stable/tailscale-setup-1.62.0-amd64.msi"
PAKET_SURUMU = "2026.09.23-1"
# Uygulamanın kendi sürümü: GitHub Release etiketiyle aynı dünyada olmalı,
# yoksa uygulama her açılışta "güncelleme var" der.
UYGULAMA_SURUMU = "v0.25.2"
JAVA_INDIRME_ADRESI = "https://api.adoptium.net/v3/binary/latest/25/ga/windows/x64/jdk/hotspot/normal/eclipse"
