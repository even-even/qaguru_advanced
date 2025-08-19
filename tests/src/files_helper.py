from pathlib import Path


def get_root_path() -> Path:
    # Получаем текущий рабочий каталог
    current_dir = Path(__file__).resolve()
    max_steps = 10
    count = 0

    # Поднимаемся на уровень выше, пока не достигнем корня проекта
    while current_dir.name != "qaguru_advanced" and count < max_steps:
        current_dir = current_dir.parent
        count += 1

    if count >= max_steps:
        message = f"Превышено максимальное количество подъемов ({max_steps}). Корень проекта не найден"
        raise ValueError(message)

    return current_dir
