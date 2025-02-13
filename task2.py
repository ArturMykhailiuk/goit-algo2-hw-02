from typing import List, Dict, Tuple


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком довжин відрізків та кількістю розрізів.
    """
    # Мемоізація: ключ — довжина, значення — (max_profit, cuts_list)
    memo = {}

    def helper(n: int) -> Tuple[int, List[int]]:
        # Якщо довжина 0, прибуток 0, немає розрізів
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = -float("inf")
        best_cuts = None
        # Для кожного можливого першого розрізу (i від 1 до n)
        for i in range(1, n + 1):
            # Прибуток за розрізання першої частини довжиною i
            current_profit = prices[i - 1]
            # Прибуток за залишок стрижня
            remaining_profit, remaining_cuts = helper(n - i)
            total_profit = current_profit + remaining_profit

            if total_profit > max_profit:
                max_profit = total_profit
                best_cuts = [i] + remaining_cuts

        memo[n] = (max_profit, best_cuts)
        return memo[n]

    max_profit, cuts = helper(length)
    # Кількість розрізів — кількість частин мінус 1 (якщо стрижень не зрізався, розрізів 0)
    number_of_cuts = len(cuts) - 1 if cuts and len(cuts) > 0 else 0
    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": number_of_cuts}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком довжин відрізків та кількістю розрізів.
    """
    # dp[j] — максимальний прибуток для стрижня довжиною j
    dp = [0] * (length + 1)
    # cuts[j] — оптимальний набір розрізів для довжини j
    cuts = [[] for _ in range(length + 1)]

    for j in range(1, length + 1):
        max_profit = -float("inf")
        best_cut = None
        # Розглядаємо кожне можливе перше розрізання (i від 1 до j)
        for i in range(1, j + 1):
            current_profit = prices[i - 1] + dp[j - i]
            if current_profit > max_profit:
                max_profit = current_profit
                best_cut = [i] + cuts[j - i]
        dp[j] = max_profit
        cuts[j] = best_cut

    # Кількість розрізів — кількість частин мінус 1 (якщо немає розрізів, то 0)
    number_of_cuts = (
        len(cuts[length]) - 1 if cuts[length] and len(cuts[length]) > 0 else 0
    )
    return {
        "max_profit": dp[length],
        "cuts": cuts[length],
        "number_of_cuts": number_of_cuts,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        # Тест 2: Оптимально не різати
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        # Тест 3: Всі розрізи по 1
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
