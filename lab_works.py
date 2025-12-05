"""
Лабораторні роботи з Python та Tkinter
Програма містить 5 лабораторних робіт для демонстрації різних функцій
"""

from tkinter import Tk, Frame, Label, Entry, Button, IntVar, StringVar, Scrollbar, Text, PhotoImage, Canvas
from tkinter import ttk
import random
import os
import math


class LabApp:
    """Головний клас програми з навігацією"""
    
    def __init__(self, root):
        self.root = root
        self.root.title('Лабораторні роботи')
        self.root.geometry('600x500')
        self.root.configure(bg='white')
        
        # Завантаження зображень
        script_dir = os.path.dirname(os.path.abspath(__file__))
        zstu_path = os.path.join(script_dir, 'zstu.png')
        tr12_path = os.path.join(script_dir, 'tr12.png')
        
        # Завантаження зображень з розміром 40x40
        try:
            self.zstu_image = PhotoImage(file=zstu_path)
        except Exception as e:
            print(f"Помилка завантаження zstu.png: {e}")
            self.zstu_image = None
        
        try:
            self.tr12_image = PhotoImage(file=tr12_path)
        except Exception as e:
            print(f"Помилка завантаження tr12.png: {e}")
            self.tr12_image = None
        
        # Головний контейнер
        self.main_frame = Frame(root, bg='white')
        self.main_frame.pack(fill='both', expand=True)
        
        # Поточний екран
        self.current_frame = None
        
        # Показати головне меню
        self.show_main_menu()
    
    def clear_frame(self):
        """Очищення поточного екрану з прокруткою"""
        # Очистити попередній canvas якщо він був
        if hasattr(self, 'canvas'):
            try:
                self.canvas.unbind_all("<MouseWheel>")
            except:
                pass
        
        # Очистити всі віджети з main_frame (крім футера)
        widgets_to_destroy = []
        for widget in self.main_frame.winfo_children():
            # Зберігаємо тільки футер (зелений)
            try:
                if widget.cget('bg') != '#10B981':
                    widgets_to_destroy.append(widget)
            except:
                widgets_to_destroy.append(widget)
        
        for widget in widgets_to_destroy:
            widget.destroy()
        
        # Створення Canvas з прокруткою
        canvas_container = Frame(self.main_frame, bg='white')
        canvas_container.pack(fill='both', expand=True)
        
        # Canvas для прокрутки
        self.canvas = Canvas(canvas_container, bg='white', highlightthickness=0)
        scrollbar = Scrollbar(canvas_container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Прив'язка прокрутки колесом миші
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.current_frame = self.scrollable_frame
    
    def show_main_menu(self):
        """Показ головного меню"""
        # Очистити весь main_frame (включаючи скрол контейнери)
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Очистити посилання на canvas якщо воно було
        if hasattr(self, 'canvas'):
            try:
                self.canvas.unbind_all("<MouseWheel>")
            except:
                pass
        
        self.current_frame = Frame(self.main_frame, bg='white')
        self.current_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Тайтл з синім фоном та білим текстом
        title_frame = Frame(self.current_frame, bg='#1E3A8A', height=80)
        title_frame.pack(fill='x', pady=0)
        title_frame.pack_propagate(False)
        
        # Заголовок по центру
        title_label = Label(title_frame, text='Лабораторні роботи', 
                           font=('Arial', 24, 'bold'),
                           bg='#1E3A8A', fg='white')
        title_label.pack(expand=True)
        
        # Жирна риска темнішого синього (як тінь)
        shadow_line = Frame(self.current_frame, bg='#0f266b', height=12)
        shadow_line.pack(fill='x', pady=0)
        
        # Контент з кнопками
        content_frame = Frame(self.current_frame, bg='white')
        content_frame.pack(fill='both', expand=True, pady=20)
        
        buttons = [
            ('Лабораторна №1', self.show_lab1),
            ('Лабораторна №2', self.show_lab2),
            ('Лабораторна №3', self.show_lab3),
            ('Лабораторна №4', self.show_lab4),
            ('Лабораторна №5', self.show_lab5),
        ]
        
        for text, command in buttons:
            btn = Button(content_frame, text=text, command=command, 
                        width=20, height=2,
                        font=('Arial', 11),
                        bg='#E5E7EB', fg='black',
                        activebackground='#D1D5DB',
                        relief='raised', bd=2)
            btn.pack(pady=5)
        
        # Зелений футер
        footer_frame = Frame(self.current_frame, bg='#10B981', height=90)
        footer_frame.pack(fill='x', side='bottom', pady=0)
        footer_frame.pack_propagate(False)
        
        # Контейнер для центрування зображень
        images_container = Frame(footer_frame, bg='#10B981')
        images_container.pack(expand=True, pady=5)
        
        # Зображення zstu
        if self.zstu_image:
            zstu_label = Label(images_container, image=self.zstu_image, bg='#10B981')
            zstu_label.pack(side='left', padx=(0, 10))
        
        # Зображення tr12
        if self.tr12_image:
            tr12_label = Label(images_container, image=self.tr12_image, bg='#10B981')
            tr12_label.pack(side='left', padx=(0, 0))
        
        # Текст під зображеннями
        footer_text = Label(footer_frame, text='Грудень 2016', 
                           font=('Arial', 9),
                           bg='#10B981', fg='white')
        footer_text.pack(pady=(0, 5))
    
    def add_back_button(self):
        """Додавання кнопки 'Назад'"""
        back_btn = Button(self.current_frame, text='← Назад', 
                         command=self.show_main_menu, width=10,
                         fg='black', bg='#E5E7EB')
        back_btn.pack(anchor='nw', pady=5)
    
    
    # ==================== Лабораторна робота №1 ====================
    def show_lab1(self):
        """Розрахунок залишку коштів для різних варіантів покупок"""
        self.clear_frame()
        self.add_back_button()
        
        Label(self.current_frame, text='Лабораторна робота №1', 
              font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Опис завдання
        desc_frame = Frame(self.current_frame, bg='#F3F4F6', relief='solid', bd=1)
        desc_frame.pack(fill='x', padx=20, pady=10)
        
        desc_text = """
Ця лабораторна робота допомагає розрахувати залишок коштів після покупки різних варіантів товарів.
Варіант 1: 1650 грн (100+250+200)*3
Варіант 2: 2310 грн (200+350+220)*3
Варіант 3: 3540 грн (500+400+280)*3

Введіть вашу суму коштів, і програма покаже, які варіанти вам підходять та скільки залишиться грошей.
        """
        Label(desc_frame, text=desc_text.strip(), 
              font=('Arial', 10), bg='#F3F4F6', justify='left', 
              wraplength=550).pack(padx=10, pady=10)
        
        self.var = IntVar()
        self.var1 = (100 + 250 + 200) * 3  # 1650
        self.var2 = (200 + 350 + 220) * 3  # 2310
        self.var3 = (500 + 400 + 280) * 3  # 3540
        
        Label(self.current_frame, text='Введіть суму коштів:', 
              font=('Arial', 11, 'bold')).pack(pady=10)
        entry = Entry(self.current_frame, textvariable=self.var, width=20, font=('Arial', 11))
        entry.pack(pady=5)
        
        Button(self.current_frame, text='Розрахувати', 
              command=self.calculate_lab1, font=('Arial', 11),
              bg='#3B82F6', fg='black', padx=20, pady=5).pack(pady=15)
        
        self.result_frame = Frame(self.current_frame)
        self.result_frame.pack(fill='both', expand=True, pady=10)
    
    def calculate_lab1(self):
        """Обробка натискання кнопки та розрахунок залишків"""
        # Очистити попередні результати
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        budget = self.var.get()
        ost1 = budget - self.var1
        ost2 = budget - self.var2
        ost3 = budget - self.var3
        
        if budget >= self.var3:
            Label(self.result_frame, text='Вам підходять усі варіанти!', 
                  font=('Arial', 12, 'bold')).pack(pady=5)
            Label(self.result_frame, text=f'1 залишок: {ost1}').pack()
            Label(self.result_frame, text=f'2 залишок: {ost2}').pack()
            Label(self.result_frame, text=f'3 залишок: {ost3}').pack()
        elif budget < self.var1:
            Label(self.result_frame, text='Мало коштів', 
                  font=('Arial', 12, 'bold')).pack(pady=5)
        elif budget < self.var2:
            Label(self.result_frame, text='Тільки перший варіант', 
                  font=('Arial', 12, 'bold')).pack(pady=5)
            Label(self.result_frame, text=f'Залишок: {ost1}').pack()
        elif budget < self.var3:
            Label(self.result_frame, 
                  text='Вам підходять тільки перший та другий варіанти', 
                  font=('Arial', 12, 'bold')).pack(pady=5)
            Label(self.result_frame, text=f'Залишок від першого варіанта: {ost1}').pack()
            Label(self.result_frame, text=f'Залишок від другого варіанта: {ost2}').pack()
    
    # ==================== Лабораторна робота №2 ====================
    def show_lab2(self):
        """Обчислення найбільшого спільного дільника (НСД)"""
        self.clear_frame()
        self.add_back_button()
        
        Label(self.current_frame, text='Лабораторна робота №2', 
              font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Опис завдання
        desc_frame = Frame(self.current_frame, bg='#F3F4F6', relief='solid', bd=1)
        desc_frame.pack(fill='x', padx=20, pady=10)
        
        desc_text = """
Найбільший спільний дільник (НСД) двох чисел - це найбільше число, яке ділить обидва числа без залишку.
Наприклад: НСД(48, 18) = 6

Програма використовує алгоритм Евкліда для обчислення НСД:
1. Беремо модулі обох чисел
2. Поки обидва числа не дорівнюють нулю, віднімаємо менше від більшого
3. Результат - сума залишків

Введіть два числа для обчислення їх НСД.
        """
        Label(desc_frame, text=desc_text.strip(), 
              font=('Arial', 10), bg='#F3F4F6', justify='left', 
              wraplength=550).pack(padx=10, pady=10)
        
        self.v21 = IntVar()
        self.v22 = IntVar()
        
        Label(self.current_frame, text='Введіть перше число:', 
              font=('Arial', 11, 'bold')).pack(pady=10)
        Entry(self.current_frame, textvariable=self.v21, width=20, font=('Arial', 11)).pack(pady=5)
        
        Label(self.current_frame, text='Введіть друге число:', 
              font=('Arial', 11, 'bold')).pack(pady=10)
        Entry(self.current_frame, textvariable=self.v22, width=20, font=('Arial', 11)).pack(pady=5)
        
        Button(self.current_frame, text='Обчислити НСД', 
              command=self.calculate_lab2, font=('Arial', 11),
              bg='#3B82F6', fg='black', padx=20, pady=5).pack(pady=15)
        
        self.result_frame = Frame(self.current_frame)
        self.result_frame.pack(fill='both', expand=True, pady=10)
    
    def calculate_lab2(self):
        """Обчислення НСД алгоритмом Евкліда"""
        # Очистити попередні результати
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        intv1 = self.v21.get()
        intv2 = self.v22.get()
        
        # Алгоритм Евкліда
        a, b = abs(intv1), abs(intv2)
        while a != 0 and b != 0:
            if a > b:
                a = a % b
            else:
                b = b % a
        
        nsd = a + b
        Label(self.result_frame, text=f'НСД({intv1}, {intv2}) = {nsd}', 
              font=('Arial', 12, 'bold')).pack(pady=5)
    
    # ==================== Лабораторна робота №3 ====================
    def show_lab3(self):
        """Виведення простих чисел у заданому діапазоні"""
        self.clear_frame()
        self.add_back_button()
        
        Label(self.current_frame, text='Лабораторна робота №3', 
              font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Опис завдання
        desc_frame = Frame(self.current_frame, bg='#F3F4F6', relief='solid', bd=1)
        desc_frame.pack(fill='x', padx=20, pady=10)
        
        desc_text = """
Просте число - це натуральне число, більше за 1, яке має тільки два дільники: 1 і саме число.
Наприклад: 2, 3, 5, 7, 11, 13, 17, 19, 23...

Програма знаходить всі прості числа у вказаному діапазоні, перевіряючи кожне число на наявність дільників.
Введіть початкове та кінцеве значення діапазону для пошуку простих чисел.
        """
        Label(desc_frame, text=desc_text.strip(), 
              font=('Arial', 10), bg='#F3F4F6', justify='left', 
              wraplength=550).pack(padx=10, pady=10)
        
        # Поля для введення діапазону
        input_frame = Frame(self.current_frame)
        input_frame.pack(pady=15)
        
        self.v31 = IntVar(value=2)
        self.v32 = IntVar(value=100)
        
        Label(input_frame, text='Від:', font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=5)
        Entry(input_frame, textvariable=self.v31, width=10, font=('Arial', 11)).grid(row=0, column=1, padx=5)
        
        Label(input_frame, text='До:', font=('Arial', 11, 'bold')).grid(row=0, column=2, padx=5)
        Entry(input_frame, textvariable=self.v32, width=10, font=('Arial', 11)).grid(row=0, column=3, padx=5)
        
        Button(self.current_frame, text='Знайти прості числа', 
              command=self.calculate_lab3, font=('Arial', 11),
              bg='#3B82F6', fg='black', padx=20, pady=5).pack(pady=10)
        
        # Створення прокручуваного текстового поля
        result_label = Label(self.current_frame, text='Результат:', 
                            font=('Arial', 11, 'bold'))
        result_label.pack(pady=(10, 5))
        
        scrollbar = Scrollbar(self.current_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.text_widget_lab3 = Text(self.current_frame, yscrollcommand=scrollbar.set, 
                          height=12, width=60, font=('Courier', 10))
        self.text_widget_lab3.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.config(command=self.text_widget_lab3.yview)
        
        # Початкове виведення
        self.calculate_lab3()
    
    def calculate_lab3(self):
        """Знаходження простих чисел у діапазоні"""
        self.text_widget_lab3.config(state='normal')
        self.text_widget_lab3.delete('1.0', 'end')
        
        start = self.v31.get()
        end = self.v32.get()
        
        if start < 2:
            start = 2
        if end < start:
            self.text_widget_lab3.insert('1.0', 'Помилка: кінцеве значення має бути більше за початкове')
            self.text_widget_lab3.config(state='disabled')
            return
        
        # Знаходження простих чисел
        primes = []
        for num in range(start, end + 1):
            is_prime = True
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(str(num))
        
        # Виведення простих чисел
        if primes:
            result_text = f'Прості числа від {start} до {end}:\n\n'
            result_text += ', '.join(primes)
            result_text += f'\n\nВсього знайдено: {len(primes)} простих чисел'
        else:
            result_text = f'У діапазоні від {start} до {end} простих чисел не знайдено.'
        
        self.text_widget_lab3.insert('1.0', result_text)
        self.text_widget_lab3.config(state='disabled')
    
    # ==================== Лабораторна робота №4 ====================
    def show_lab4(self):
        """Збереження даних користувача у файли"""
        self.clear_frame()
        self.add_back_button()
        
        Label(self.current_frame, text='Лабораторна робота №4', 
              font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Опис завдання
        desc_frame = Frame(self.current_frame, bg='#F3F4F6', relief='solid', bd=1)
        desc_frame.pack(fill='x', padx=20, pady=10)
        
        desc_text = """
Ця лабораторна робота демонструє роботу з файлами в Python.
Введіть ваше ім'я та дату народження, і програма:
1. Збереже обидва значення у файл Lab4.1.txt
2. Збереже тільки дату народження у файл Lab4.2.txt
3. Відобразить вміст обох файлів на екрані

Це демонструє операції читання та запису у файли.
        """
        Label(desc_frame, text=desc_text.strip(), 
              font=('Arial', 10), bg='#F3F4F6', justify='left', 
              wraplength=550).pack(padx=10, pady=10)
        
        self.v21 = StringVar()
        self.v22 = StringVar()
        
        input_frame = Frame(self.current_frame)
        input_frame.pack(pady=15)
        
        Label(input_frame, text="Ім'я:", font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        Entry(input_frame, textvariable=self.v21, width=25, font=('Arial', 11)).grid(row=0, column=1, padx=5, pady=5)
        
        Label(input_frame, text="Дата народження:", font=('Arial', 11, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        Entry(input_frame, textvariable=self.v22, width=25, font=('Arial', 11)).grid(row=1, column=1, padx=5, pady=5)
        
        Button(self.current_frame, text='Зберегти', 
              command=self.save_lab4, font=('Arial', 11),
              bg='#3B82F6', fg='black', padx=20, pady=5).pack(pady=15)
        
        # Область для виведення результатів
        Label(self.current_frame, text='Вміст файлів:', 
              font=('Arial', 12, 'bold')).pack(pady=(20, 5))
        
        self.result_frame = Frame(self.current_frame)
        self.result_frame.pack(fill='both', expand=True, pady=10)
    
    def save_lab4(self):
        """Збереження даних у файли та виведення на екран"""
        # Очистити попередні результати
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        name = self.v21.get()
        birth_date = self.v22.get()
        
        if not name or not birth_date:
            Label(self.result_frame, text='Будь ласка, заповніть усі поля!', 
                  fg='red').pack()
            return
        
        # Запис у перший файл
        with open('Lab4.1.txt', 'w', encoding='utf-8') as f:
            f.write(f"{name}\n{birth_date}")
        
        # Читання та запис у другий файл
        with open('Lab4.1.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 1:
                with open('Lab4.2.txt', 'w', encoding='utf-8') as f2:
                    f2.write(lines[1])
        
        # Виведення вмісту файлів на екран
        Label(self.result_frame, text='✅ Дані збережені!', 
              font=('Arial', 12, 'bold'), fg='green').pack(pady=5)
        
        # Вміст Lab4.1.txt
        Label(self.result_frame, text='Вміст Lab4.1.txt:', 
              font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        with open('Lab4.1.txt', 'r', encoding='utf-8') as f:
            content1 = f.read()
        text1 = Text(self.result_frame, height=2, width=50)
        text1.pack(pady=5)
        text1.insert('1.0', content1)
        text1.config(state='disabled')
        
        # Вміст Lab4.2.txt
        Label(self.result_frame, text='Вміст Lab4.2.txt:', 
              font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        try:
            with open('Lab4.2.txt', 'r', encoding='utf-8') as f:
                content2 = f.read()
            text2 = Text(self.result_frame, height=1, width=50)
            text2.pack(pady=5)
            text2.insert('1.0', content2)
            text2.config(state='disabled')
        except FileNotFoundError:
            Label(self.result_frame, text='Файл не знайдено', fg='red').pack()
    
    # ==================== Лабораторна робота №5 ====================
    def show_lab5(self):
        """Генерація та сортування комплексних чисел"""
        self.clear_frame()
        self.add_back_button()
        
        Label(self.current_frame, text='Лабораторна робота №5', 
              font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Опис завдання
        desc_frame = Frame(self.current_frame, bg='#F3F4F6', relief='solid', bd=1)
        desc_frame.pack(fill='x', padx=20, pady=10)
        
        desc_text = """
Комплексне число має вигляд a + bi, де:
- a - дійсна частина (Re)
- b - уявна частина (Im)
- i - уявна одиниця (i² = -1)

Програма:
1. Генерує 20 випадкових комплексних чисел
2. Сортує їх за модулем (відстань від початку координат)
3. Зберігає у файл Complex_Number.txt
4. Візуалізує на комплексній площині (дійсна вісь - X, уявна - Y)
5. Виводить список усіх комплексних чисел
        """
        Label(desc_frame, text=desc_text.strip(), 
              font=('Arial', 10), bg='#F3F4F6', justify='left', 
              wraplength=550).pack(padx=10, pady=10)
        
        Button(self.current_frame, text='Згенерувати комплексні числа', 
              command=self.generate_lab5, font=('Arial', 11),
              bg='#3B82F6', fg='black', padx=20, pady=5).pack(pady=15)
        
        # Область для виведення результатів
        self.result_frame = Frame(self.current_frame)
        self.result_frame.pack(fill='both', expand=True, pady=10)
    
    def generate_lab5(self):
        """Генерація та сортування комплексних чисел"""
        # Очистити попередні результати
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        comp = []
        
        # Генерація 20 комплексних чисел
        for _ in range(20):
            a = random.randint(-100, 100)
            b = random.randint(-100, 100)
            comp.append(complex(a, b))
        
        # Сортування за модулем (від більшого до меншого)
        comp.sort(key=abs, reverse=True)
        
        # Збереження у файл
        with open('Complex_Number.txt', 'w', encoding='utf-8') as f:
            f.write(str(comp))
        
        # Виведення на екран
        Label(self.result_frame, text='✅ Комплексні числа згенеровані та збережені!', 
              font=('Arial', 12, 'bold'), fg='green').pack(pady=5)
        
        # Візуалізація на координатній площині
        Label(self.result_frame, text='Візуалізація на комплексній площині:', 
              font=('Arial', 11, 'bold')).pack(pady=(15, 5))
        
        # Canvas для малювання
        canvas_frame = Frame(self.result_frame)
        canvas_frame.pack(pady=10)
        
        canvas_width = 500
        canvas_height = 500
        canvas = Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg='white', relief='solid', bd=1)
        canvas.pack()
        
        # Центр координат
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        scale = 2  # Масштаб для відображення
        
        # Малювання осей
        canvas.create_line(0, center_y, canvas_width, center_y, fill='gray', width=1)  # Горизонтальна вісь
        canvas.create_line(center_x, 0, center_x, canvas_height, fill='gray', width=1)  # Вертикальна вісь
        
        # Підписи осей
        canvas.create_text(center_x + 10, 10, text='Im', fill='black', font=('Arial', 10, 'bold'))
        canvas.create_text(canvas_width - 10, center_y - 10, text='Re', fill='black', font=('Arial', 10, 'bold'))
        canvas.create_text(center_x + 5, center_y + 15, text='0', fill='black', font=('Arial', 8))
        
        # Малювання комплексних чисел
        colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#EC4899']
        for i, num in enumerate(comp):
            x = center_x + num.real * scale
            y = center_y - num.imag * scale  # Інвертуємо Y для правильного відображення
            
            # Перевірка чи точка в межах canvas
            if 0 <= x <= canvas_width and 0 <= y <= canvas_height:
                color = colors[i % len(colors)]
                # Малюємо точку (коло)
                canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline=color)
                # Підпис числа (тільки для перших 10, щоб не перевантажувати)
                if i < 10:
                    canvas.create_text(x + 8, y - 8, text=f'{int(num.real)}+{int(num.imag)}i', 
                                     fill=color, font=('Arial', 7))
        
        # Виведення текстового списку
        Label(self.result_frame, text='Список комплексних чисел (відсортовані за модулем):', 
              font=('Arial', 10, 'bold')).pack(pady=(15, 5))
        
        scrollbar = Scrollbar(self.result_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = Text(self.result_frame, yscrollcommand=scrollbar.set, 
                          height=8, width=60, font=('Courier', 9))
        text_widget.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.config(command=text_widget.yview)
        
        # Виведення вмісту файлу
        with open('Complex_Number.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        text_widget.insert('1.0', content)
        text_widget.config(state='disabled')


# Запуск програми
if __name__ == '__main__':
    root = Tk()
    app = LabApp(root)
    root.mainloop()
