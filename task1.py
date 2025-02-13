from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.

    Args:
        print_jobs: Список завдань на друк, де кожне завдання містить "id", "volume", "priority" та "print_time".
        constraints: Обмеження принтера, що містять "max_volume" та "max_items".

    Returns:
        Dict з ключами:
            "print_order": список ID завдань у оптимальному порядку друку,
            "total_time": загальний час друку (розраховується як сума максимальних часів друку для кожної групи).
    """
    # Перетворення словників у об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    # Перетворення словника обмежень у PrinterConstraints
    printer = PrinterConstraints(**constraints)

    # Сортуємо завдання за пріоритетом (низьке значення = вищий пріоритет)
    jobs.sort(key=lambda job: job.priority)

    print_order = []
    total_time = 0

    # Змінні для поточної групи (batch)
    current_batch = []
    current_volume = 0
    current_batch_time = 0

    for job in jobs:
        # Перевірка чи можемо додати завдання до поточної групи:
        # не перевищено обмеження по об'єму та кількості
        if (len(current_batch) < printer.max_items) and (
            current_volume + job.volume <= printer.max_volume
        ):
            current_batch.append(job)
            current_volume += job.volume
            # Час групи визначається як максимальний час серед завдань у групі
            current_batch_time = max(current_batch_time, job.print_time)
        else:
            # Завершуємо поточну групу та додаємо її до загального часу і порядку друку
            for bjob in current_batch:
                print_order.append(bjob.id)
            total_time += current_batch_time

            # Починаємо нову групу з поточним завданням
            current_batch = [job]
            current_volume = job.volume
            current_batch_time = job.print_time

    # Додаємо останню групу, якщо вона не порожня
    if current_batch:
        for bjob in current_batch:
            print_order.append(bjob.id)
        total_time += current_batch_time

    return {"print_order": print_order, "total_time": total_time}


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
