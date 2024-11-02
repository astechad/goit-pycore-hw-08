import pickle
import copy


class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite


class Contacts:
    def __init__(self, filename: str, contacts: list[Person] = None):
        if contacts is None:
            contacts = []
        self.filename = filename
        self.contacts = contacts
        self.is_unpacking = False
        self.count_save = 0

    def save_to_file(self):
        """Зберігає екземпляр класу Contacts у файл."""
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls, filename: str):
        """Завантажує екземпляр класу Contacts з файлу."""
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            # Повертаємо новий екземпляр Contacts, якщо файл не знайдено
            return cls(filename)

    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes["count_save"] += 1
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value
        self.is_unpacking = True


def main():
    # Завантаження даних з файлу або створення нової адресної книги
    address_book = Contacts.load_from_file("address_book.pkl")

    # Основний цикл програми
    while True:
        action = input(
            "Введіть 'додати' для додавання контакту, 'зберегти' для збереження та 'вийти' для виходу: ")

        if action.lower() == 'додати':
            name = input("Ім'я: ")
            email = input("Email: ")
            phone = input("Телефон: ")
            favorite = input(
                "Улюблений (True/False): ").strip().lower() == 'true'
            new_person = Person(name, email, phone, favorite)
            address_book.contacts.append(new_person)
            print("Контакт додано.")

        elif action.lower() == 'зберегти':
            address_book.save_to_file()
            print("Дані збережено.")

        elif action.lower() == 'вийти':
            address_book.save_to_file()  # Зберігаємо перед виходом
            print("Вихід з програми.")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
