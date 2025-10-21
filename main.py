import re
import os


class Node:
    # Узел однонаправленного линейного списка

    def __init__(self, coefficient=0, exponent=0, next_node=None):
        self.coefficient = coefficient
        self.exponent = exponent
        self.next = next_node  # ссылка на следующий узел


class Polynomial:

    def __init__(self):
        self.head = None

    def add_term(self, coefficient, exponent):
        if coefficient == 0:
            return

        new_node = Node(coefficient, exponent)

        # Если список пуст или добавляемый член имеет наибольшую степень
        if self.head is None or exponent > self.head.exponent:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            prev = None

            # Поиск позиции для вставки (упорядоченно по убыванию степени)
            while current is not None and current.exponent > exponent:
                prev = current
                current = current.next

            # Если член с такой степенью уже существует
            if current is not None and current.exponent == exponent:
                current.coefficient += coefficient
                if current.coefficient == 0:
                    # Удаляем узел, если коэффициент стал нулевым
                    if prev is None:
                        self.head = current.next
                    else:
                        prev.next = current.next
            else:
                # Вставляем новый узел
                if prev is None:
                    new_node.next = self.head
                    self.head = new_node
                else:
                    new_node.next = current
                    prev.next = new_node

    def parse_polynomial(self, poly_str):
        poly_str = poly_str.replace(' ', '').lower()

        pattern = r'([+-])?(\d*)([a-z])?(?:\^(\d+))?|(\d+)(?![a-z])'

        # Разбиваем строку на члены
        terms = re.findall(pattern, poly_str)

        current_sign = '+'

        for match in terms:
            sign, coeff_str, variable, exp_str, constant = match

            # Определяем текущий знак
            if sign:
                current_sign = sign
            elif not any(match[:-1]) and constant:
                coefficient = int(constant)
                if current_sign == '-':
                    coefficient = -coefficient
                self.add_term(coefficient, 0)
                current_sign = '+'
                continue

            # Пропускаем пустые совпадения
            if not coeff_str and not variable and not exp_str:
                continue

            # Определяем коэффициент
            if not coeff_str:
                if variable:
                    coefficient = 1
                else:
                    continue
            else:
                coefficient = int(coeff_str)

            if current_sign == '-':
                coefficient = -coefficient

            # Определяем степень
            if not variable:
                exponent = 0
            elif not exp_str:
                exponent = 1
            else:
                exponent = int(exp_str)

            # Добавляем член в многочлен
            if coefficient != 0:
                self.add_term(coefficient, exponent)

    def combine_like_terms(self):
        pass

    def to_string(self):
        if self.head is None:
            return "0"

        result = []
        current = self.head

        while current is not None:
            coeff = current.coefficient
            exp = current.exponent

            if coeff > 0 and result:
                sign = " + "
            elif coeff < 0:
                sign = " - "
                coeff = -coeff
            else:
                sign = ""

            if exp == 0:
                term = f"{coeff}"
            elif exp == 1:
                if coeff == 1:
                    term = "y"
                else:
                    term = f"{coeff}y"
            else:
                if coeff == 1:
                    term = f"y^{exp}"
                else:
                    term = f"{coeff}y^{exp}"

            result.append(sign + term)
            current = current.next

        return ''.join(result) if result else "0"

    def display(self):
        # Вывод многочлена на экран
        print(self.to_string())


def read_polynomial_from_file(filename):
    # Чтение многочлена из файла
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            lines = content.split('\n')
            for line in lines:
                # Ищем первую строку, которая выглядит как многочлен
                if any(c.isalpha() for c in line) and any(c in '+-^' or c.isdigit() for c in line):
                    clean_line = re.sub(r'^.*?:', '', line).strip()
                    if clean_line:
                        return clean_line
            # Если не нашли подходящую строку, возвращаем первую непустую
            for line in lines:
                if line.strip():
                    return line.strip()
            return content
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None


def write_polynomial_to_file(filename, polynomial_str, original_poly=None):
    try:
        original_content = ""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                original_content = file.read()
        except:
            pass

        found_original_poly = None
        if original_content:
            lines = original_content.split('\n')
            for line in lines:
                # Ищем строку с многочленом, но не результат
                if ("исходный" not in line.lower() and
                        "результат" not in line.lower() and
                        "упрощенный" not in line.lower() and
                        any(c.isalpha() for c in line) and
                        any(c in '+-^' or c.isdigit() for c in line)):
                    found_original_poly = line.strip()
                    break

        final_original_poly = original_poly or found_original_poly or original_content.strip()

        # Полностью перезаписываем файл
        with open(filename, 'w', encoding='utf-8') as file:
            if final_original_poly:
                file.write(f"{final_original_poly}\n")
            file.write(f"Результат приведения подобных членов: {polynomial_str}\n")
            # file.write("Члены упорядочены по убыванию степеней")

        print(f"Файл {filename} полностью перезаписан")

    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")


def main():
    filename = "text1.txt"

    # Чтение многочлена из файла
    original_poly_str = read_polynomial_from_file(filename)

    if original_poly_str:
        print(f"Исходный многочлен: {original_poly_str}")

        poly = Polynomial()
        poly.parse_polynomial(original_poly_str)

        # Приведение подобных слагаемых
        poly.combine_like_terms()

        # Получение результата
        result_str = poly.to_string()
        print(f"Упрощенный многочлен: {result_str}")

        write_polynomial_to_file(filename, result_str, original_poly_str)

    else:
        # Пример с тестовыми данными из задания
        test_poly = "52y^10 - 3y^8 + y"
        print(f"Тестовый многочлен: {test_poly}")

        poly = Polynomial()
        poly.parse_polynomial(test_poly)
        poly.combine_like_terms()

        result_str = poly.to_string()
        print(f"Упрощенный многочлен: {result_str}")

        # Создаем тестовый файл если его нет
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(test_poly)


if __name__ == "__main__":
    main()

