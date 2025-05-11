# IoT Dashboard

Kişisel Bulut Tabanlı IoT Dashboard Projesi

**Teknolojiler:** Mosquitto (MQTT Broker), InfluxDB (Time‑Series Database), Grafana (Görselleştirme), Python (paho‑mqtt, pandas), Docker Compose

---

## İçindekiler

* [Proje Hakkında](#proje-hakkında)
* [Özellikler](#özellikler)
* [Mimari](#mimari)
* [Gereksinimler](#gereksinimler)
* [Ön Koşullar](#ön-koşullar)
* [Kurulum & Çalıştırma](#kurulum--çalıştırma)
* [Uygulama Akışı](#uygulama-akışı)
* [Testler](#testler)
* [Örnek Kullanım](#örnek-kullanım)
* [Özelleştirme](#özelleştirme)

---

## Proje Hakkında

Bu proje, IoT cihazlardan telemetri verilerini MQTT üzerinden alır, Python servisi ile işler, InfluxDB’ye kaydeder ve Grafana ile gerçek zamanlı ile geçmişe dönük görselleştirmesini sunar.

Tamamen Docker Compose ile orkestre edilmiş, "free-tier" bulut servislerine kolay entegrasyon sağlayan maliyetsiz bir altyapıdır.

## Özellikler

* **Uçtan Uca Veri Akışı:** MQTT → Python Service → InfluxDB → Grafana
* **Gerçek Zamanlı Dashboard:** Anlık değerler ve zaman serisi görselleştirmesi
* **Veri Ön İşleme:** Pandas ile filtreleme ve agregasyon
* **Hata Yönetimi:** Yeniden bağlanma (retry) ve istikrar
* **Modüler Ölçeklenebilirlik:** Docker Compose ile yeni bileşen eklenebilir
* **Free-Tier Uyumlu:** Kişisel projeler için maliyetsiz kullanım

## Mimari

```text
[IoT Cihazlar] → Mosquitto (MQTT Broker) → Python Service → InfluxDB → Grafana → Kullanıcı
```

* **Mosquitto:** MQTT mesaj alış‑verişi için açık kaynak broker
* **Python Service:** paho-mqtt ile veri alır, pandas ile ön işler, influxdb-client ile yazar
* **InfluxDB:** Zaman serisi veritabanı
* **Grafana:** Dashboard ve grafikler

## Gereksinimler

* **MQTT Broker**: Eclipse Mosquitto v2.0 veya üzeri
* **InfluxDB**: v2.6 veya üzeri (HTTP API & Flux desteği)
* **Grafana**: v9.5.21 veya üzeri (OSS sürümü)
* **Python**: v3.10 veya üzeri

  * `paho-mqtt`
  * `pandas`
  * `influxdb-client`
* **Docker Engine**: v20.10 veya üzeri
* **Docker Compose**: v2 (CLI plugin)
* **Git**: son sürüm
* **Opsiyonel CLI Araçları**:

  * `mosquitto-clients` (MQTT testleri için)

## Kurulum & Çalıştırma & Çalıştırma

1. Repo’yu klonlayın:

   ```bash
   git clone https://github.com/<kullanici_adiniz>/IoT_Dashboard.git
   cd IoT_Dashboard
   ```

2. Ortam değişkenlerini tanımlayın (opsiyonel, `.env` dosyası):

   ```ini
   MQTT_BROKER=mosquitto
   MQTT_PORT=1883
   INFLUX_URL=http://influxdb:8086
   INFLUX_TOKEN=admin123
   INFLUX_ORG=my_org
   INFLUX_BUCKET=iot_data
   ```

3. Servisleri başlatın:

   ```bash
   docker compose up -d --build
   ```

4. Durumu kontrol edin:

   ```bash
   docker compose ps
   ```

## Uygulama Akışı

1. IoT cihazı veya test script’i `test/topic` konusuna değer mesajı gönderir.
2. Python Service, mesajı alır ve pandas ile işleyerek InfluxDB’ye yazar.
3. Grafana, InfluxDB’den veriyi çeker ve dashboard’da sunar.

## Testler

* **Birim Test (pytest):** Python modülleri için örnek testler yazılabilir.
* **MQTT Test:**

  ```bash
  docker compose exec mosquitto mosquitto_pub -t test/topic -m "23.4"
  docker compose exec mosquitto mosquitto_sub -t test/topic -v
  ```
* **Yük Test:** Basit Python script ile saniyede 100 mesaj simülasyonu.
* **Servis Logları:**

  ```bash
  docker compose logs -f python-service
  ```

## Örnek Kullanım

1. MQTT üzerinden değer gönderin:

   ```bash
   docker compose exec mosquitto mosquitto_pub -t test/topic -m "55.7"
   ```
2. Python Servis log’unda çıktıyı ve InfluxDB UI’da kaydı doğrulayın.
3. Grafana dashboard’unda yeni veri noktasını izleyin.

## Özelleştirme

* **Yeni Ölçümler:** `python-service/app.py` içinde Point tanımını güncelleyin.
* **Dashboard Provision:** `grafana/provisioning` klasörüne JSON dosyaları ekleyin.
* **Güvenlik:** Mosquitto TLS/SSL veya Grafana OAuth entegrasyonu ekleyin.
