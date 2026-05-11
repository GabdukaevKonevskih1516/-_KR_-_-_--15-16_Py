"""
<summary>
Модуль "Математический помощник".

Предоставляет графическое приложение для решения математических задач,
включая квадратные уравнения, построение графиков, поиск пересечений
функций и конвертацию систем счисления.
</summary>
<remarks>
Требует установки библиотек: numpy, matplotlib.
Поддерживает Python версии 3.7 и выше.
</remarks>
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
from typing import List, Tuple, Optional, Any


class MathApp:
    """
    <summary>
    Главный класс приложения "Математический Помощник".
    </summary>
    <remarks>
    Реализует графический интерфейс пользователя (GUI) и логику вычислений.
    Приложение состоит из 4 вкладок для различных математических задач:
    - Квадратное уравнение
    - График функции
    - Пересечение функций
    - Системы счисления
    </remarks>
    """

    # ==================== КОНСТРУКТОР ====================

    def __init__(self, root: tk.Tk) -> None:
        """
        <summary>
        Конструктор класса MathApp.
        </summary>
        <param name="root">
        Корневой объект окна Tkinter, в котором размещается приложение.
        </param>
        <returns>None</returns>
        <remarks>
        Выполняет настройку главного окна, создает вкладки
        и инициализирует интерфейс каждой вкладки.
        </remarks>
        """
        self.root = root
        self.root.title("Математический Помощник")
        self.root.geometry("800x850")
        self.root.resizable(True, True)

        # Создаем виджет Notebook для организации вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Создаем контейнеры (фреймы) для каждой вкладки
        self.tab_quadratic = ttk.Frame(self.notebook)
        self.tab_plot = ttk.Frame(self.notebook)
        self.tab_intersect = ttk.Frame(self.notebook)
        self.tab_systems = ttk.Frame(self.notebook)

        # Добавляем фреймы в Notebook с соответствующими заголовками
        self.notebook.add(self.tab_quadratic, text="Квадратное уравнение")
        self.notebook.add(self.tab_plot, text="График функции")
        self.notebook.add(self.tab_intersect, text="Пересечение функций")
        self.notebook.add(self.tab_systems, text="Системы счисления")

        # Вызываем методы инициализации интерфейса для каждой вкладки
        self._setup_quadratic_tab()
        self._setup_plot_tab()
        self._setup_intersection_tab()
        self._setup_numeral_system_tab()

    # ==================== ВКЛАДКА 1: КВАДРАТНОЕ УРАВНЕНИЕ ====================

    def _setup_quadratic_tab(self) -> None:
        """
        <summary>
        Настройка графических элементов вкладки решения квадратных уравнений.
        </summary>
        <returns>None</returns>
        <remarks>
        Создает поля ввода для коэффициентов a, b, c,
        кнопку вычисления и метку для отображения результата.
        </remarks>
        """
        tk.Label(
            self.tab_quadratic,
            text="Решение уравнения ax² + bx + c = 0",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Фрейм для группировки полей ввода
        input_frame = tk.Frame(self.tab_quadratic)
        input_frame.pack(pady=10)

        # Создание текстовых полей ввода коэффициентов
        self.entry_a = tk.Entry(input_frame, width=5)
        self.entry_b = tk.Entry(input_frame, width=5)
        self.entry_c = tk.Entry(input_frame, width=5)

        # Размещение элементов в сетке (Grid)
        tk.Label(input_frame, text="a:").grid(row=0, column=0)
        self.entry_a.grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="b:").grid(row=0, column=2)
        self.entry_b.grid(row=0, column=3, padx=5)
        tk.Label(input_frame, text="c:").grid(row=0, column=4)
        self.entry_c.grid(row=0, column=5, padx=5)

        # Кнопка запуска расчета
        tk.Button(
            self.tab_quadratic,
            text="Найти корни",
            command=self._solve_quadratic
        ).pack(pady=10)

        # Метка для вывода результата
        self.label_quadratic_result = tk.Label(
            self.tab_quadratic,
            text="",
            font=("Arial", 10)
        )
        self.label_quadratic_result.pack()

    def _solve_quadratic(self) -> None:
        """
        <summary>
        Алгоритм решения квадратного уравнения.
        </summary>
        <returns>None</returns>
        <exception cref="ValueError">
        Возникает, если пользователь ввел нечисловое значение.
        </exception>
        <exception cref="ZeroDivisionError">
        Возникает при делении на ноль (не используется в текущей реализации).
        </exception>
        <remarks>
        Вычисляет дискриминант и находит корни уравнения ax² + bx + c = 0.
        Обрабатывает случаи:
        - D > 0: два действительных корня
        - D = 0: один корень (кратный)
        - D < 0: действительных корней нет
        - a = 0: линейное уравнение
        </remarks>
        """
        try:
            # Преобразование введенного текста в вещественные числа
            coefficient_a = float(self.entry_a.get())
            coefficient_b = float(self.entry_b.get())
            coefficient_c = float(self.entry_c.get())

            # Проверка на линейное уравнение
            if coefficient_a == 0:
                if coefficient_b == 0:
                    result_text = "Уравнение не имеет смысла (0 = 0)"
                else:
                    # Линейное уравнение bx + c = 0
                    root_x = -coefficient_c / coefficient_b
                    result_text = f"Линейное уравнение: x = {root_x:.3f}"
            else:
                # Расчет дискриминанта
                discriminant = coefficient_b ** 2 - 4 * coefficient_a * coefficient_c

                if discriminant > 0:
                    # Случай двух корней
                    sqrt_discriminant = discriminant ** 0.5
                    root_x1 = (-coefficient_b + sqrt_discriminant) / (2 * coefficient_a)
                    root_x2 = (-coefficient_b - sqrt_discriminant) / (2 * coefficient_a)
                    result_text = f"x1 = {root_x1:.3f}\nx2 = {root_x2:.3f}"
                elif discriminant == 0:
                    # Случай одного корня
                    root_x = -coefficient_b / (2 * coefficient_a)
                    result_text = f"x = {root_x:.3f}"
                else:
                    # Действительных корней нет
                    result_text = "Корней нет (D < 0)"

            self.label_quadratic_result.config(text=result_text)

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа!")

    # ==================== ВКЛАДКА 2: ГРАФИК ФУНКЦИИ ====================

    def _setup_plot_tab(self) -> None:
        """
        <summary>
        Настройка графических элементов вкладки визуализации функций.
        </summary>
        <returns>None</returns>
        <remarks>
        Создает поле ввода формулы, поля для диапазона X,
        кнопку построения и холст для отображения графика.
        </remarks>
        """
        tk.Label(
            self.tab_plot,
            text="Построение графика f(x)",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Поле ввода формулы
        function_frame = tk.Frame(self.tab_plot)
        function_frame.pack()

        tk.Label(function_frame, text="f(x) =").pack(side=tk.LEFT)
        self.entry_function = tk.Entry(function_frame, width=30)
        self.entry_function.pack(side=tk.LEFT, padx=5)
        self.entry_function.insert(0, "x**2")

        # Поля ввода диапазона X
        range_frame = tk.Frame(self.tab_plot)
        range_frame.pack(pady=5)

        self.entry_xmin = tk.Entry(range_frame, width=5)
        self.entry_xmin.insert(0, "-10")
        self.entry_xmax = tk.Entry(range_frame, width=5)
        self.entry_xmax.insert(0, "10")

        tk.Label(range_frame, text="x от:").pack(side=tk.LEFT)
        self.entry_xmin.pack(side=tk.LEFT, padx=5)
        tk.Label(range_frame, text="до:").pack(side=tk.LEFT)
        self.entry_xmax.pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.tab_plot,
            text="Построить",
            command=self._plot_function
        ).pack(pady=5)

        # Создание объекта фигуры Matplotlib и привязка к Tkinter
        self.figure_plot, _ = plt.subplots(figsize=(5, 4))
        self.canvas_plot = FigureCanvasTkAgg(self.figure_plot, self.tab_plot)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _plot_function(self) -> None:
        """
        <summary>
        Генерация данных и отрисовка графика функции.
        </summary>
        <returns>None</returns>
        <exception cref="Exception">
        Возникает при синтаксической ошибке в формуле или недопустимых значениях.
        </exception>
        <remarks>
        Строит график функции на заданном интервале с использованием
        библиотеки matplotlib. Поддерживает математические функции:
        sin, cos, sqrt, abs, tan, exp, log.
        Поддерживается оператор ** для возведения в степень.
        </remarks>
        """
        try:
            # Заменяем ^ на ** для корректной работы eval в Python
            function_string = self.entry_function.get().replace("^", "**")
            original_formula = self.entry_function.get()
            x_min = float(self.entry_xmin.get())
            x_max = float(self.entry_xmax.get())

            # Проверка корректности диапазона
            if x_min >= x_max:
                messagebox.showerror("Ошибка", "x_min должен быть меньше x_max!")
                return

            # Генерируем 1000 точек для плавности линии
            x_values = np.linspace(x_min, x_max, 1000)

            # Разрешенные функции для использования в вводе
            safe_namespace = {
                "x": x_values,
                "np": np,
                "sin": np.sin,
                "cos": np.cos,
                "sqrt": np.sqrt,
                "abs": np.abs,
                "tan": np.tan,
                "exp": np.exp,
                "log": np.log,
                "pi": np.pi
            }

            # Вычисляем значения Y
            y_values = eval(function_string, safe_namespace)

            # Очищаем и перерисовываем график
            self.figure_plot.clear()
            axes = self.figure_plot.add_subplot(111)
            axes.plot(x_values, y_values, color='#2c3e50', linewidth=2.5)

            # Установка сетки с шагом 1.0
            axes.xaxis.set_major_locator(MultipleLocator(1.0))

            # Отрисовка главных осей координат
            axes.axhline(0, color='black', linewidth=1.2)
            axes.axvline(0, color='black', linewidth=1.2)
            axes.grid(True, which='both', linestyle='--', alpha=0.5)

            # Отображение формулы в заголовке
            display_formula = original_formula.replace("**", "^")
            axes.set_title(f"График функции f(x) = {display_formula}", fontsize=10)
            axes.set_xlabel("x")
            axes.set_ylabel("f(x)")

            self.canvas_plot.draw()

        except SyntaxError:
            messagebox.showerror("Ошибка", "Синтаксическая ошибка в формуле!")
        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка ввода функции: {error}")

    # ==================== ВКЛАДКА 3: ПЕРЕСЕЧЕНИЕ ФУНКЦИЙ ====================

    def _setup_intersection_tab(self) -> None:
        """
        <summary>
        Настройка элементов вкладки поиска точек пересечения функций.
        </summary>
        <returns>None</returns>
        <remarks>
        Создает поля ввода для двух функций, кнопку поиска,
        метку для вывода результата и холст для отображения графиков.
        </remarks>
        """
        tk.Label(
            self.tab_intersect,
            text="Поиск пересечений f(x) и g(x)",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Фрейм для ввода функций
        function_frame = tk.Frame(self.tab_intersect)
        function_frame.pack()

        self.entry_function_f = tk.Entry(function_frame, width=15)
        self.entry_function_f.insert(0, "x**2")
        self.entry_function_g = tk.Entry(function_frame, width=15)
        self.entry_function_g.insert(0, "x+2")

        tk.Label(function_frame, text="f(x):").pack(side=tk.LEFT)
        self.entry_function_f.pack(side=tk.LEFT, padx=5)
        tk.Label(function_frame, text="g(x):").pack(side=tk.LEFT)
        self.entry_function_g.pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.tab_intersect,
            text="Найти точки",
            command=self._find_intersections
        ).pack(pady=10)

        self.label_intersection_result = tk.Label(
            self.tab_intersect,
            text="",
            font=("Arial", 9)
        )
        self.label_intersection_result.pack()

        # Холст для графика пересечений
        self.figure_intersection, _ = plt.subplots(figsize=(5, 4))
        self.canvas_intersection = FigureCanvasTkAgg(
            self.figure_intersection,
            self.tab_intersect
        )
        self.canvas_intersection.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _find_intersections(self) -> None:
        """
        <summary>
        Математический поиск точек пересечения графиков функций.
        </summary>
        <returns>None</returns>
        <exception cref="Exception">
        Возникает при ошибках в математических выражениях.
        </exception>
        <remarks>
        Использует метод поиска нулей разности функций f(x) - g(x)
        на интервале [-10, 10] с последующей линейной интерполяцией
        для уточнения координат.
        </remarks>
        """
        try:
            function_f_expr = self.entry_function_f.get().replace("^", "**")
            function_g_expr = self.entry_function_g.get().replace("^", "**")

            # Анализируем диапазон [-10, 10] для поиска
            x_range = np.linspace(-10, 10, 2000)

            # Безопасное пространство имен для eval
            safe_namespace = {"x": x_range, "np": np, "sin": np.sin}

            # Вычисляем значения обеих функций
            f_values = eval(function_f_expr, safe_namespace)
            g_values = eval(function_g_expr, safe_namespace)

            # Разность функций для поиска нулей (точек пересечения)
            difference = f_values - g_values
            intersection_points = []

            for i in range(len(x_range) - 1):
                # Если произведение значений в соседних точках <= 0,
                # значит график пересек ноль
                if difference[i] * difference[i + 1] <= 0:
                    # Линейная интерполяция для точности координаты X
                    x_intersect = (
                            x_range[i] - difference[i] *
                            (x_range[i + 1] - x_range[i]) /
                            (difference[i + 1] - difference[i])
                    )
                    y_intersect = eval(
                        function_f_expr,
                        {"x": x_intersect, "np": np, "sin": np.sin}
                    )
                    intersection_points.append((x_intersect, y_intersect))

            # Обновление визуализации
            self.figure_intersection.clear()
            axes = self.figure_intersection.add_subplot(111)
            axes.plot(x_range, f_values, label=f"f(x) = {function_f_expr}")
            axes.plot(x_range, g_values, label=f"g(x) = {function_g_expr}")

            if intersection_points:
                x_coords, y_coords = zip(*intersection_points)
                axes.scatter(x_coords, y_coords, color='red', s=50, zorder=5)

                # Формируем текст с координатами точек
                points_text = "\n".join(
                    [f"({x:.3f}, {y:.3f})" for x, y in intersection_points]
                )
                self.label_intersection_result.config(
                    text=f"Найдено пересечений: {len(intersection_points)}\n{points_text}"
                )
            else:
                self.label_intersection_result.config(text="Пересечений не найдено")

            axes.grid(True, alpha=0.3)
            axes.legend()
            axes.axhline(0, color='black', linewidth=0.5)
            axes.axvline(0, color='black', linewidth=0.5)
            self.canvas_intersection.draw()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка в математических выражениях: {error}")

    # ==================== ВКЛАДКА 4: СИСТЕМЫ СЧИСЛЕНИЯ ====================

    def _setup_numeral_system_tab(self) -> None:
        """
        <summary>
        Настройка интерфейса конвертера систем счисления.
        </summary>
        <returns>None</returns>
        <remarks>
        Создает поля ввода для числа, исходного и целевого оснований,
        кнопку конвертации и метку для вывода результата.
        Поддерживаются системы от 2 до 16 включительно.
        </remarks>
        """
        tk.Label(
            self.tab_systems,
            text="Конвертер систем счисления (2-16)",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        input_frame = tk.Frame(self.tab_systems)
        input_frame.pack()

        self.entry_number = tk.Entry(input_frame)
        self.entry_base_from = tk.Entry(input_frame, width=5)
        self.entry_base_from.insert(0, "10")
        self.entry_base_to = tk.Entry(input_frame, width=5)
        self.entry_base_to.insert(0, "2")

        tk.Label(input_frame, text="Число:").grid(row=0, column=0, padx=5)
        self.entry_number.grid(row=0, column=1, pady=5)
        tk.Label(input_frame, text="Из системы:").grid(row=1, column=0, padx=5)
        self.entry_base_from.grid(row=1, column=1, pady=5)
        tk.Label(input_frame, text="В систему:").grid(row=2, column=0, padx=5)
        self.entry_base_to.grid(row=2, column=1, pady=5)

        tk.Button(
            self.tab_systems,
            text="Перевести",
            command=self._convert_base
        ).pack(pady=10)

        self.label_conversion_result = tk.Label(
            self.tab_systems,
            text="",
            font=("Arial", 12, "bold")
        )
        self.label_conversion_result.pack()

    def _convert_base(self) -> None:
        """
        <summary>
        Логика перевода числа между различными системами счисления.
        </summary>
        <returns>None</returns>
        <exception cref="ValueError">
        Возникает, если число не соответствует указанному основанию
        или основание выходит за пределы допустимого диапазона 2-16.
        </exception>
        <remarks>
        Поддерживает системы с основаниями от 2 до 16.
        Сначала переводит число из исходной системы в десятичную,
        затем из десятичной в целевую систему.
        Используются цифры 0-9 и буквы A-F.
        </remarks>
        <example>
        Вход: число "FF", из системы 16 в систему 2
        Выход: "11111111"
        </example>
        """
        try:
            # Чтение входных данных
            number_string = self.entry_number.get().strip().upper()
            base_from = int(self.entry_base_from.get())
            base_to = int(self.entry_base_to.get())

            # Проверка допустимости оснований
            if base_from < 2 or base_from > 16:
                messagebox.showerror("Ошибка", "Исходное основание должно быть от 2 до 16!")
                return
            if base_to < 2 or base_to > 16:
                messagebox.showerror("Ошибка", "Целевое основание должно быть от 2 до 16!")
                return

            # 1. Перевод из исходной системы в десятичную
            decimal_number = int(number_string, base_from)

            # 2. Перевод из десятичной в целевую систему
            digits = "0123456789ABCDEF"
            result = ""

            if decimal_number == 0:
                result = "0"
            else:
                temp_number = decimal_number
                while temp_number > 0:
                    result = digits[temp_number % base_to] + result
                    temp_number //= base_to

            self.label_conversion_result.config(
                text=f"Результат: {result} (в {base_to}-ичной системе)"
            )

        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Некорректное число или основание системы!\n"
                "Убедитесь, что число соответствует указанному основанию."
            )
        except Exception as error:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка: {error}")


def main() -> None:
    """
    <summary>
    Главная функция запуска приложения.
    </summary>
    <returns>None</returns>
    <remarks>
    Создает главное окно Tkinter, инициализирует приложение MathApp
    и запускает главный цикл обработки событий GUI.
    </remarks>
    """
    # Создание главного объекта окна
    root_window = tk.Tk()

    # Инициализация нашего приложения
    math_application = MathApp(root_window)  # noqa: F841

    # Запуск бесконечного цикла обработки событий GUI
    root_window.mainloop()


# Точка входа в программу
if __name__ == "__main__":
    """
    <summary>
    Точка входа в программу.
    </summary>
    <remarks>
    Вызывает функцию main() при запуске скрипта напрямую.
    </remarks>
    """
    main()
