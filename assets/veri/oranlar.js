/*
 * DESE Hukuk — hesaplama araçlarının parametre dosyası.
 * Tüm güncellemeler yalnızca bu dosyadan yapılır.
 *
 * AYLIK (TÜİK her ayın 3'ünde açıklar):
 *   tufe12 listesine yeni ayı ekle, tufeSonAy ve guncelleme alanlarını değiştir.
 *   Anahtar = kira artışının UYGULANDIĞI ay (verinin ait olduğu aydan bir sonraki ay).
 *   Örnek: Ekim 2026 TÜFE verisi (12 aylık ortalama %31,23) -> "2026-11": 31.23
 *
 * YILLIK (AAÜT her yıl Kasım civarı Resmî Gazete'de yayımlanır):
 *   aaut bloğundaki tutarları ve tarife künyesini güncelle.
 */
window.DESE_VERI = {
  guncelleme: "2026-11-19",

  // TÜFE 12 aylık ortalamalara göre değişim (%), TBK m.344 tavanı
  tufeSonAy: "2026-11",
  tufe12: {
    "2024-01": 53.86, "2024-02": 54.72, "2024-03": 55.91, "2024-04": 57.50,
    "2024-05": 59.64, "2024-06": 62.51, "2024-07": 65.07, "2024-08": 65.93,
    "2024-09": 64.91, "2024-10": 63.47, "2024-11": 62.02, "2024-12": 60.45,
    "2025-01": 58.51, "2025-02": 56.35, "2025-03": 53.83, "2025-04": 51.26,
    "2025-05": 48.73, "2025-06": 45.80, "2025-07": 43.23, "2025-08": 41.13,
    "2025-09": 39.62, "2025-10": 38.36, "2025-11": 37.15, "2025-12": 35.91,
    "2026-01": 34.88, "2026-02": 33.98, "2026-03": 33.39, "2026-04": 32.82,
    "2026-05": 32.43, "2026-06": 32.24, "2026-07": 32.03, "2026-08": 31.90,
    "2026-09": 31.79, "2026-10": 31.49, "2026-11": 31.23
  },

  // Konut kiralarında geçici %25 sınırı (TBK geçici m.1 ve 2): 11.06.2022 - 01.07.2024 (dahil)
  konut25: { bas: "2022-06-11", bit: "2024-07-01" },

  // Avukatlık Asgari Ücret Tarifesi
  aaut: {
    kunye: "2026-2027 Avukatlık Asgari Ücret Tarifesi (03.11.2026 tarihli ve 33419 sayılı Resmî Gazete)",
    yururluk: "2026-11-03",
    icraMaktu: 12500,          // İkinci kısım ikinci bölüm: icra dairelerinde yapılan takipler
    icraMaktuSinir: 78125,     // m.11/1: bu tutara kadar olan takiplerde maktu ücret
    tahliyeMaktu: 26000,       // tahliyeye ilişkin icra takipleri (m.11/5)
    icraMahkemesiIs: 15000,    // icra mahkemelerinde takip edilen işler
    icraMahkemesiDava: 23000,  // icra mahkemelerinde takip edilen dava ve duruşmalı işler
    // Üçüncü kısım nispi dilimler: [dilim tutarı, oran %]
    dilimler: [
      [800000, 16], [800000, 15], [1600000, 14], [1600000, 13], [2400000, 11],
      [3200000, 8], [4000000, 5], [4800000, 3], [5600000, 2], [Infinity, 1]
    ]
  },

  // İcra takibi açılış masrafları (2026)
  // Harçlar: 492 sayılı Harçlar Kanunu (1) sayılı tarife; baro pulu: TBB duyurusu
  // Tebligat tutarları: dosya başına borçlu sayısı kadar tebligat avansı
  icraMasraf: {
    yil: 2026,
    basvurma: 732,        // icraya başvurma harcı (Tarife B-I-1)
    pesinOran: 0.005,     // peşin harç, binde 5 (yalnız ilamsız takipte)
    suret: 104,           // vekaletname suret harcı
    pul: 164,             // vekalet (baro) pulu
    tebligat: { normal: 300, hizli: 600, mts: 350, e: 20 }   // borçlu başına
  }
};
