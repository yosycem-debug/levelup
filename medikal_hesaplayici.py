#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
  TIPTA MATEMATİK - MEDİKAL HESAPLAYICI
=====================================================================
Lise matematik projesi için hazırlanmış, Türkçe menülü bir hesaplayıcı.

Bu programda tıpta kullanılan dört matematiksel model yer alır:
  1) Vücut Kitle İndeksi (VKİ)        -> İkinci dereceden ifade (boy²)
  2) Vücut Yüzey Alanı (Mosteller)    -> Karekök fonksiyonu
  3) İlaç Yarılanma Ömrü              -> Üstel (eksponansiyel) fonksiyon
  4) SIR Salgın Modeli                -> Diferansiyel denklemler

Çalıştırmak için:  python medikal_hesaplayici.py
Grafikler için gerekli kütüphane:  pip install matplotlib
=====================================================================
"""

import math
import sys

# matplotlib yüklü değilse program yine çalışsın, sadece grafik çizilmesin.
try:
    import matplotlib
    import matplotlib.pyplot as plt
    MATPLOTLIB_VAR = True
except ImportError:
    MATPLOTLIB_VAR = False


# ---------------------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------------------

def baslik_yaz(metin):
    """Ekrana çerçeveli bir başlık yazar."""
    print("\n" + "=" * 60)
    print(f"  {metin}")
    print("=" * 60)


def sayi_al(mesaj, en_az=None, en_cok=None, sifir_olabilir=False, tam_sayi=False):
    """
    Kullanıcıdan güvenli bir şekilde sayı alır.

    - Harf, boş giriş gibi hatalı girişlerde tekrar sorar.
    - Türkçe klavyedeki virgüllü yazımı da kabul eder (ör. 1,75).
    - Negatif sayıları, sıfırı (izin verilmediyse) ve
      belirtilen aralığın dışındaki değerleri reddeder.
    """
    while True:
        giris = input(mesaj).strip().replace(",", ".")

        if giris == "":
            print("  ⚠ Boş giriş yapılamaz. Lütfen bir sayı girin.")
            continue

        try:
            deger = int(giris) if tam_sayi else float(giris)
        except ValueError:
            tur = "tam sayı" if tam_sayi else "sayı"
            print(f"  ⚠ '{giris}' geçerli bir {tur} değil. Tekrar deneyin.")
            continue

        # float("nan") ve float("inf") gibi özel değerleri engelle
        if not math.isfinite(deger):
            print("  ⚠ Lütfen sonlu, gerçek bir sayı girin.")
            continue
        if deger < 0:
            print("  ⚠ Negatif değer girilemez.")
            continue
        if deger == 0 and not sifir_olabilir:
            print("  ⚠ Değer sıfır olamaz.")
            continue
        if en_az is not None and deger < en_az:
            print(f"  ⚠ Değer en az {en_az} olmalıdır.")
            continue
        if en_cok is not None and deger > en_cok:
            print(f"  ⚠ Değer en fazla {en_cok} olmalıdır.")
            continue

        return deger


def grafigi_goster(dosya_adi):
    """
    Çizilen grafiği PNG olarak kaydeder ve ekran varsa pencerede gösterir.
    (Ekransız ortamlarda, ör. sunucuda, sadece dosyaya kaydedilir.)
    """
    plt.tight_layout()
    plt.savefig(dosya_adi, dpi=120)
    print(f"\n  📊 Grafik '{dosya_adi}' dosyasına kaydedildi.")
    if matplotlib.get_backend().lower() != "agg":
        print("  (Devam etmek için grafik penceresini kapatın.)")
        plt.show()
    plt.close()


# ---------------------------------------------------------------------
# 1) VÜCUT KİTLE İNDEKSİ (VKİ)
# ---------------------------------------------------------------------

def vki_hesapla(kilo, boy_m):
    """VKİ = kilo / boy²   (kilo: kg, boy: metre)"""
    return kilo / (boy_m ** 2)


def vki_siniflandir(vki):
    """Dünya Sağlık Örgütü (DSÖ) sınıflandırmasına göre VKİ kategorisi."""
    if vki < 18.5:
        return "Zayıf"
    elif vki < 25:
        return "Normal"
    elif vki < 30:
        return "Fazla kilolu"
    else:
        return "Obez"


def vki_menusu():
    baslik_yaz("1) VÜCUT KİTLE İNDEKSİ (VKİ)")
    print("  Formül:  VKİ = kilo (kg) / boy² (m²)\n")

    kilo = sayi_al("  Kilonuzu girin (kg): ", en_az=2, en_cok=500)
    boy_cm = sayi_al("  Boyunuzu girin (cm): ", en_az=40, en_cok=260)

    boy_m = boy_cm / 100          # cm -> metre dönüşümü
    vki = vki_hesapla(kilo, boy_m)
    sinif = vki_siniflandir(vki)

    # Hesaplamanın adımlarını öğrenciye göstermek için yazdırıyoruz
    print("\n  --- Hesaplama Adımları ---")
    print(f"  Boy = {boy_cm:g} cm = {boy_m:g} m")
    print(f"  Boy² = {boy_m:g}² = {boy_m ** 2:.4f} m²")
    print(f"  VKİ = {kilo:g} / {boy_m ** 2:.4f} = {vki:.2f} kg/m²")

    print("\n  --- Sınıflandırma (DSÖ) ---")
    print("  VKİ < 18.5          : Zayıf")
    print("  18.5 ≤ VKİ < 25     : Normal")
    print("  25   ≤ VKİ < 30     : Fazla kilolu")
    print("  VKİ ≥ 30            : Obez")
    print(f"\n  ✅ Sonuç: VKİ = {vki:.2f}  →  {sinif}")


# ---------------------------------------------------------------------
# 2) VÜCUT YÜZEY ALANI (MOSTELLER FORMÜLÜ)
# ---------------------------------------------------------------------

def mosteller_vya(boy_cm, kilo):
    """VYA = √(boy (cm) × kilo (kg) / 3600)   sonuç: m²"""
    return math.sqrt(boy_cm * kilo / 3600)


def vya_menusu():
    baslik_yaz("2) VÜCUT YÜZEY ALANI (MOSTELLER)")
    print("  Formül:  VYA = √( boy (cm) × kilo (kg) / 3600 )   [m²]")
    print("  (Kemoterapi gibi ilaç dozlarının hesaplanmasında kullanılır.)\n")

    boy_cm = sayi_al("  Boyunuzu girin (cm): ", en_az=40, en_cok=260)
    kilo = sayi_al("  Kilonuzu girin (kg): ", en_az=2, en_cok=500)

    carpim = boy_cm * kilo
    bolum = carpim / 3600
    vya = mosteller_vya(boy_cm, kilo)

    print("\n  --- Hesaplama Adımları ---")
    print(f"  boy × kilo = {boy_cm:g} × {kilo:g} = {carpim:g}")
    print(f"  {carpim:g} / 3600 = {bolum:.4f}")
    print(f"  √{bolum:.4f} = {vya:.4f}")
    print(f"\n  ✅ Sonuç: Vücut Yüzey Alanı ≈ {vya:.2f} m²")
    print("  (Yetişkinlerde ortalama değer yaklaşık 1.7 - 1.9 m²'dir.)")


# ---------------------------------------------------------------------
# 3) İLAÇ YARILANMA ÖMRÜ (ÜSTEL AZALMA)
# ---------------------------------------------------------------------

def kalan_miktar(baslangic, yarilanma, t):
    """
    Üstel azalma formülü:
        N(t) = N₀ × (1/2)^(t / T½)
    N₀: başlangıç dozu, T½: yarılanma süresi, t: geçen süre
    """
    return baslangic * (0.5 ** (t / yarilanma))


def yarilanma_menusu():
    baslik_yaz("3) İLAÇ YARILANMA ÖMRÜ")
    print("  Formül:  N(t) = N₀ × (1/2)^(t / T½)")
    print("  N₀ = başlangıç dozu, T½ = yarılanma süresi, t = geçen süre\n")

    n0 = sayi_al("  Başlangıç dozu (mg): ")
    t_yari = sayi_al("  Yarılanma süresi (saat): ")
    t = sayi_al("  Geçen süre (saat): ", sifir_olabilir=True)

    kalan = kalan_miktar(n0, t_yari, t)
    us = t / t_yari
    yuzde = kalan / n0 * 100

    print("\n  --- Hesaplama Adımları ---")
    print(f"  t / T½ = {t:g} / {t_yari:g} = {us:.4f}  (geçen yarılanma sayısı)")
    print(f"  (1/2)^{us:.4f} = {0.5 ** us:.6f}")
    print(f"  N({t:g}) = {n0:g} × {0.5 ** us:.6f} = {kalan:.4f} mg")
    print(f"\n  ✅ Sonuç: {t:g} saat sonra vücutta {kalan:.4f} mg ilaç kalır "
          f"(başlangıcın %{yuzde:.2f}'i).")
    # Tıpta ilaç, yaklaşık 5 yarılanma ömrü sonunda vücuttan atılmış kabul edilir
    print(f"  ℹ İlaç yaklaşık 5 yarılanma ömrü ({5 * t_yari:g} saat) sonra "
          f"%{100 - 100 * 0.5 ** 5:.1f} oranında atılmış olur.")

    if not MATPLOTLIB_VAR:
        print("\n  ⚠ matplotlib yüklü değil, grafik çizilemiyor. "
              "(pip install matplotlib)")
        return

    # Grafik: 0'dan (en az 6 yarılanma süresi veya t'nin biraz fazlası) kadar
    t_son = max(6 * t_yari, t * 1.2)
    adim_sayisi = 300
    zamanlar = [t_son * i / adim_sayisi for i in range(adim_sayisi + 1)]
    miktarlar = [kalan_miktar(n0, t_yari, z) for z in zamanlar]

    plt.figure(figsize=(9, 5.5))
    plt.plot(zamanlar, miktarlar, color="tab:blue", linewidth=2,
             label=r"$N(t) = N_0 \cdot (1/2)^{t/T_{1/2}}$")

    # Her yarılanma noktasını işaretle (N₀/2, N₀/4, ...)
    k = 1
    while k * t_yari <= t_son:
        plt.plot(k * t_yari, n0 / 2 ** k, "o", color="gray", markersize=4)
        k += 1
    plt.axhline(n0 / 2, color="gray", linestyle=":", linewidth=1,
                label=f"Yarı doz ({n0 / 2:g} mg)")

    # Kullanıcının sorduğu zamanı kırmızı nokta ile göster
    plt.plot(t, kalan, "o", color="red", markersize=8,
             label=f"t = {t:g} sa → {kalan:.2f} mg")
    plt.axvline(t, color="red", linestyle="--", linewidth=1)

    plt.title("İlacın Vücuttan Üstel Azalması (Yarılanma Ömrü)")
    plt.xlabel("Zaman (saat)")
    plt.ylabel("Kalan ilaç miktarı (mg)")
    plt.grid(alpha=0.3)
    plt.legend()
    grafigi_goster("yarilanma_grafigi.png")


# ---------------------------------------------------------------------
# 4) SIR SALGIN SİMÜLASYONU
# ---------------------------------------------------------------------

def sir_simulasyonu(nufus, ilk_hasta, beta, gamma, gun, dt=0.1):
    """
    SIR modelini Euler yöntemiyle sayısal olarak çözer.

    S: Sağlıklı ama hastalanabilir (Susceptible)
    I: Enfekte / hasta (Infected)
    R: İyileşmiş / bağışık (Recovered)

    Diferansiyel denklemler:
        dS/dt = -β·S·I / N
        dI/dt =  β·S·I / N - γ·I
        dR/dt =  γ·I

    Euler yöntemi: yeni_değer = eski_değer + türev × Δt
    """
    S = nufus - ilk_hasta
    I = ilk_hasta
    R = 0.0
    zamanlar, S_liste, I_liste, R_liste = [0.0], [S], [I], [R]

    adim_sayisi = int(round(gun / dt))
    for adim in range(1, adim_sayisi + 1):
        yeni_hasta = beta * S * I / nufus * dt   # Δt sürede hastalananlar
        iyilesen = gamma * I * dt                # Δt sürede iyileşenler

        # Sayısal hata yüzünden negatife düşmeyi engelle
        yeni_hasta = min(yeni_hasta, S)
        iyilesen = min(iyilesen, I)

        S -= yeni_hasta
        I += yeni_hasta - iyilesen
        R += iyilesen

        zamanlar.append(adim * dt)
        S_liste.append(S)
        I_liste.append(I)
        R_liste.append(R)

    return zamanlar, S_liste, I_liste, R_liste


def sir_menusu():
    baslik_yaz("4) SIR SALGIN SİMÜLASYONU")
    print("  Formüller (diferansiyel denklemler):")
    print("    dS/dt = -β · S · I / N")
    print("    dI/dt =  β · S · I / N  -  γ · I")
    print("    dR/dt =  γ · I")
    print("  Temel üreme sayısı:  R₀ = β / γ")
    print("  S: hastalanabilir, I: hasta, R: iyileşmiş, N: toplam nüfus")
    print("  β: bulaşma oranı (1/gün), γ: iyileşme oranı (1/gün)\n")

    nufus = sayi_al("  Toplam nüfus (N): ", en_az=2, tam_sayi=True)
    ilk_hasta = sayi_al("  Başlangıçtaki hasta sayısı (I₀): ",
                        en_az=1, en_cok=nufus - 1, tam_sayi=True)
    beta = sayi_al("  Bulaşma oranı β (ör. 0.3): ", en_cok=10)
    gamma = sayi_al("  İyileşme oranı γ (ör. 0.1): ", en_cok=10)
    gun = sayi_al("  Simülasyon süresi (gün, ör. 160): ", en_az=1, en_cok=3650,
                  tam_sayi=True)

    zamanlar, S, I, R = sir_simulasyonu(nufus, ilk_hasta, beta, gamma, gun)

    r0 = beta / gamma
    zirve_indeks = I.index(max(I))       # hasta sayısının en yüksek olduğu an
    zirve_gun = zamanlar[zirve_indeks]
    zirve_hasta = I[zirve_indeks]

    print("\n  --- Sonuçlar ---")
    print(f"  R₀ = β / γ = {beta:g} / {gamma:g} = {r0:.2f}")
    if r0 > 1:
        print("  → R₀ > 1 olduğu için hastalık yayılarak salgına dönüşür.")
    else:
        print("  → R₀ ≤ 1 olduğu için hastalık yayılamadan söner.")
    print(f"  Ortalama hastalık süresi = 1 / γ = {1 / gamma:.1f} gün")
    print(f"  Hasta sayısının zirvesi : {zirve_gun:.1f}. gün, "
          f"yaklaşık {zirve_hasta:,.0f} kişi")
    print(f"  {gun}. gün sonunda      : S ≈ {S[-1]:,.0f}, "
          f"I ≈ {I[-1]:,.0f}, R ≈ {R[-1]:,.0f}")
    print(f"  Toplam hastalanan       : ≈ {nufus - S[-1]:,.0f} kişi "
          f"(nüfusun %{(nufus - S[-1]) / nufus * 100:.1f}'i)")

    if not MATPLOTLIB_VAR:
        print("\n  ⚠ matplotlib yüklü değil, grafik çizilemiyor. "
              "(pip install matplotlib)")
        return

    plt.figure(figsize=(9, 5.5))
    plt.plot(zamanlar, S, color="tab:blue", linewidth=2,
             label="S – Hastalanabilir")
    plt.plot(zamanlar, I, color="tab:red", linewidth=2, label="I – Hasta")
    plt.plot(zamanlar, R, color="tab:green", linewidth=2,
             label="R – İyileşmiş")
    plt.plot(zirve_gun, zirve_hasta, "o", color="darkred",
             label=f"Zirve: {zirve_gun:.0f}. gün, {zirve_hasta:,.0f} kişi")

    plt.title(f"SIR Salgın Modeli  (N={nufus:,}, β={beta:g}, γ={gamma:g}, "
              f"R₀={r0:.2f})")
    plt.xlabel("Zaman (gün)")
    plt.ylabel("Kişi sayısı")
    plt.grid(alpha=0.3)
    plt.legend()
    grafigi_goster("sir_grafigi.png")


# ---------------------------------------------------------------------
# ANA MENÜ
# ---------------------------------------------------------------------

def ana_menu():
    """Programın ana döngüsü: kullanıcı çıkış seçene kadar menüyü gösterir."""
    secenekler = {
        "1": vki_menusu,
        "2": vya_menusu,
        "3": yarilanma_menusu,
        "4": sir_menusu,
    }

    while True:
        baslik_yaz("TIPTA MATEMATİK - MEDİKAL HESAPLAYICI")
        print("  1) Vücut Kitle İndeksi (VKİ) hesapla")
        print("  2) Vücut Yüzey Alanı (Mosteller) hesapla")
        print("  3) İlaç yarılanma ömrü ve üstel azalma grafiği")
        print("  4) SIR salgın simülasyonu")
        print("  0) Çıkış")

        secim = input("\n  Seçiminiz (0-4): ").strip()

        if secim == "0":
            print("\n  Programdan çıkılıyor. Sağlıklı günler! 👋\n")
            break
        elif secim in secenekler:
            secenekler[secim]()
            input("\n  Ana menüye dönmek için Enter'a basın...")
        else:
            print("  ⚠ Geçersiz seçim! Lütfen 0 ile 4 arasında bir sayı girin.")


if __name__ == "__main__":
    try:
        ana_menu()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C veya Ctrl+D ile çıkışta hata mesajı yerine nazik bir mesaj
        print("\n\n  Program kullanıcı tarafından sonlandırıldı.\n")
        sys.exit(0)
