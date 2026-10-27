from abc import ABC, abstractmethod
import logging
import random
import string

# Налаштовуємо логування (виправлено подвійний виклик basicConfig)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PasswordGenerator(ABC):
    """Абстрактний базовий клас для всіх генераторів паролів."""

    def __init__(self, length: int = 8):
        self.length = length

    @abstractmethod
    def generate_chars(self):
        """Кожен дочерній клас має реалізувати цей метод за допомогою yield,

        повертаючи випадкові символи по одному.
        """
        pass

    @abstractmethod
    def check_password(self, password: str) -> bool:
        """Кожен дочерній клас повинен реалізувати перевірку пароля

        на відповідність своїм правилам безпеки.
        """
        pass

    def create_password(self) -> str:
        """Послідовно збирає символи з генератора generate_chars

        і повертає готовий пароль.
        """
        logging.info(f"Починаємо створення пароля на {self.length} елементів")

        # Використовуємо генераторний метод класу для збору символів
        char_iterator = self.generate_chars()
        password_chars = [next(char_iterator) for _ in range(self.length)]

        password = "".join(password_chars)

        # Перевіряємо пароль за допомогою абстрактного методу
        if self.check_password(password):
            logging.info("Пароль успішно створено та перевірено.")
            return password
        else:
            logging.warning(
                "Згенерований пароль не пройшов валідацію! Спробуйте ще раз."
            )
            return self.create_password()  # Рекурсивний перезапуск у разі невдачі


class PasswordCreatorNumber(PasswordGenerator):
    """Дочерній клас, що спеціалізується на цифрових паролях (PIN-кодах)."""

    def __init__(self, length: int = 8):
        # Передаємо довжину в конструктор батьківського класу
        super().__init__(length)
        self.allowed_characters = string.digits

    def generate_chars(self):
        """Реалізація yield: нескінченно генерує випадкові символи (цифри)

        по запиту.
        """
        while True:
            yield random.choice(self.allowed_characters)

    def check_password(self, password: str) -> bool:
        """Приклад валідації: пароль не повинен складатися з однакових цифр

        або йти підряд (напр. '11111111' чи '12345678').
        """
        # Перевірка на унікальність символів (не всі однакові)
        if len(set(password)) <= 1:
            return False

        # Перевірка на просту послідовність чисел
        if password in "0123456789" or password in "9876543210":
            return False

        return True


# --- Перевірка роботи MVP ---
if __name__ == "__main__":
    # Створюємо об'єкт генератора суто цифрових паролів довжиною 8 символів
    numeric_generator = PasswordCreatorNumber(length=8)

    # Генеруємо пароль
    my_password = numeric_generator.create_password()
    print(f"\nРезультат: {my_password}")


    
    