import numpy as np
from math import factorial, comb
from collections import defaultdict
import matplotlib.pyplot as plt

# Входни данни - твоят мултиномиален модел
print("=== МУЛТИНОМИАЛЕН MONTE CARLO ЗА ФУТБОЛЕН СЕЗОН ===")
n_matches = int(input("Брой мачове в сезона (38 за Висша лига): "))
win_p = float(input("Вероятност за победа (%): ")) / 100
draw_p = float(input("Вероятност за равен (%): ")) / 100
loss_p = float(input("Вероятност за загуба (%): ")) / 100
num_seasons = int(input("Брой симулирани сезони: "))

# Проверка за сумата на вероятностите
if abs(win_p + draw_p + loss_p - 1.0) > 0.01:
    print("-" * 80)
    print("ГРЕШКА: Сумата на вероятностите трябва да е 100%!")
    print(f"Текуща сума: {(win_p + draw_p + loss_p) * 100:.1f}%")
    print("-" * 80)
    exit()

print("-" * 80)
print(f"📊 МУЛТИНОМИАЛЕН МОДЕЛ:")
print(f"Победа: {win_p:.1%} | Равен: {draw_p:.1%} | Загуба: {loss_p:.1%}")
print(f"Очаквани точки на мач: {win_p * 3 + draw_p * 1:.2f}")

# Мултиномиален анализ (твоят код)
print("-" * 80)
print("🔢 МУЛТИНОМИАЛЕН АНАЛИЗ (най-вероятни комбинации):")

k = 3
d = defaultdict(float)
TOTAL_EVENTS_FACTORIAL = factorial(n_matches)

top_combinations = []
for wins in range(n_matches + 1):
    for draws in range(n_matches + 1):
        losses = n_matches - wins - draws
        if losses >= 0:
            coefficient = TOTAL_EVENTS_FACTORIAL // (factorial(wins) * factorial(draws) * factorial(losses))
            probability = (win_p ** wins) * (draw_p ** draws) * (loss_p ** losses) * coefficient
            points = wins * 3 + draws * 1
            top_combinations.append((wins, draws, losses, points, probability))

# Сортиране и показване на топ 10
top_combinations.sort(key=lambda x: -x[4])
print("Топ 10 най-вероятни комбинации:")
for i, (w, d, l, pts, prob) in enumerate(top_combinations[:10], 1):
    print(f"{i:2d}. {w} поб/{d} рав/{l} заг -> {pts} точки ({prob:.4%})")

# Monte Carlo симулация
print("-" * 80)
print("🎲 MONTE CARLO СИМУЛАЦИЯ:")
print(f"Симулиране на {num_seasons} сезона...")

points_per_season = []
wins_per_season = []

for season in range(num_seasons):
    total_points = 0
    total_wins = 0

    # Симулираме всеки мач в сезона
    for match in range(n_matches):
        result = np.random.choice(['победа', 'равен', 'загуба'], p=[win_p, draw_p, loss_p])

        if result == 'победа':
            total_points += 3
            total_wins += 1
        elif result == 'равен':
            total_points += 1

    points_per_season.append(total_points)
    wins_per_season.append(total_wins)

# Анализ на резултатите
points_array = np.array(points_per_season)
wins_array = np.array(wins_per_season)

print("-" * 80)
print("📊 СРАВНИТЕЛЕН АНАЛИЗ:")
print(f"{'МЕТОД':<25} {'МОНТЕ КАРЛО':<15} {'МУЛТИНОМИАЛЕН':<15}")
print(f"{'-' * 55}")

# Средни точки
mc_avg_points = np.mean(points_array)
multinom_avg_points = n_matches * (win_p * 3 + draw_p * 1)
print(f"{'Средни точки':<25} {mc_avg_points:<15.1f} {multinom_avg_points:<15.1f}")

# Средни победи
mc_avg_wins = np.mean(wins_array)
multinom_avg_wins = n_matches * win_p
print(f"{'Средни победи':<25} {mc_avg_wins:<15.1f} {multinom_avg_wins:<15.1f}")

# Статистики за класиране
champions = sum(1 for p in points_per_season if p >= 75)
europe = sum(1 for p in points_per_season if p >= 60)
relegation = sum(1 for p in points_per_season if p <= 30)

print("-" * 80)
print("🏆 СТАТИСТИКИ ЗА КЛАСИРАНЕ (Monte Carlo):")
print(f"Шампионски титли: {champions} ({(champions / num_seasons) * 100:.1f}%)")
print(f"Квалификации за Европа: {europe} ({(europe / num_seasons) * 100:.1f}%)")
print(f"Изпадания: {relegation} ({(relegation / num_seasons) * 100:.1f}%)")

print("-" * 80)
print("📈 РАЗПРЕДЕЛЕНИЕ НА ТОЧКИТЕ (Monte Carlo):")
for points_range in range(0, n_matches * 3 + 1, 10):
    count = len([p for p in points_per_season if points_range <= p < points_range + 10])
    percentage = (count / num_seasons) * 100
    if count > 0:
        bar = '█' * max(1, int(percentage / 2))
        print(f"{points_range:2d}-{points_range + 9:2d} точки: {count:4d} сезона ({percentage:5.1f}%) {bar}")

print("-" * 80)

# Намиране на най-вероятния резултат от Monte Carlo
points_counts = {}
for points in points_per_season:
    points_counts[points] = points_counts.get(points, 0) + 1

most_common_points = max(points_counts.items(), key=lambda x: x[1])
print(f"🎯 НАЙ-ЧЕСТ СЕЗОН ОТ МОНТЕ КАРЛО: {most_common_points[0]} точки ({most_common_points[1]} пъти)")

# Сравнение с мултиномиалния модел
multinom_most_likely = top_combinations[0]
print(f"🎯 НАЙ-ВЕРОЯТЕН СЕЗОН ОТ МУЛТИНОМИАЛ: {multinom_most_likely[3]} точки ({multinom_most_likely[4]:.4%})")

print("-" * 80)
print("💡 ЗАКЛЮЧЕНИЕ:")
print("Мултиномиалният модел дава ТОЧНИ вероятности")
print("Monte Carlo дава ПРАКТИЧЕСКИ резултати със симулации")
print("Двата метода се допълват перфектно! 🎯")

print("-" * 80)