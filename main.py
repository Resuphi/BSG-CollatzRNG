import time


class CollatzRNG:
    def __init__(self, seed=None):
        """
        RNG'yi bir tohum (seed) değeri ile başlatır.
        Eğer seed verilmezse sistem zamanını kullanır.
        """
        if seed is None:
            self.state = int(time.time() * 1000)
        else:
            self.state = seed

        # Orijinal tohumu sakla (döngüden kurtulmak için gerekebilir)
        self.original_seed = self.state
        self.counter = 0  # Entropi eklemek için sayaç

    def _step(self):
        """
        Collatz kuralına göre bir adım ilerler ve durumu günceller.
        """
        # 4-2-1 döngüsüne girerse (state 1, 2 veya 4 olduğunda)
        # Durumu "dürtmemiz" gerekir.
        if self.state <= 4:
            self.counter += 1
            # Basit bir karıştırma işlemi:
            # Eski seed, sayaç ve büyük bir asal sayı ile durumu yenile.
            self.state = (self.original_seed ^ self.counter) + 1299827

        if self.state % 2 == 0:
            self.state = self.state // 2
        else:
            # (3n + 1) her zaman çifttir, bu yüzden 2'ye bölerek
            # deterministik adımı atlıyor ve entropiyi artırıyoruz.
            self.state = (3 * self.state + 1) // 2

    def rand_int(self, min_val, max_val):
        """
        Belirtilen aralıkta (min_val dahil, max_val dahil) rastgele bir tamsayı döndürür.
        """
        range_size = max_val - min_val + 1

        # Yeterli karışıklığı sağlamak için Collatz adımını birkaç kez çalıştır
        # Bu, sayıların ardışık korelasyonunu azaltır.
        for _ in range(5):
            self._step()

        return min_val + (self.state % range_size)

    def rand_float(self):
        """
        0.0 ile 1.0 arasında rastgele bir ondalıklı sayı döndürür.
        """
        # Büyük bir sayı üretip normalize ediyoruz
        return self.rand_int(0, 1000000) / 1000000.0


# --- Kullanım Örneği ---

# 1. Üreteci başlat
rng = CollatzRNG()  # İsterseniz boş bırakın: CollatzRNG()

print("--- 0 ile 100 arası 10 rastgele sayı ---")
generated_numbers = []
for _ in range(10):
    num = rng.rand_int(0, 100)
    generated_numbers.append(num)

print(generated_numbers)

print("\n--- Yazı (0) Tura (1) Simülasyonu ---")
heads = 0
tails = 0
for _ in range(1000):
    if rng.rand_int(0, 1) == 0:
        tails += 1
    else:
        heads += 1
print(f"1000 atış sonucu: {heads} Yazı, {tails} Tura")