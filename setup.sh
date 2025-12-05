#!/bin/bash

# Скрипт для ініціалізації середовища для запуску лабораторних робіт
# Працює на macOS та Linux

set -e  # Зупинити виконання при помилці

echo "🚀 Ініціалізація середовища для лабораторних робіт..."
echo ""

# Перевірка операційної системи
OS="$(uname -s)"
echo "📋 Операційна система: $OS"

# Перевірка наявності Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не знайдено!"
    echo "📦 Встановлення Python3..."
    
    if [[ "$OS" == "Darwin" ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew не знайдено. Будь ласка, встановіть Homebrew спочатку:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        brew install python@3.14
    elif [[ "$OS" == "Linux" ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-tk
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python python-pip tk
        else
            echo "❌ Не вдалося визначити менеджер пакетів. Встановіть Python3 вручну."
            exit 1
        fi
    else
        echo "❌ Непідтримувана операційна система"
        exit 1
    fi
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python знайдено: $PYTHON_VERSION"
fi

# Перевірка та встановлення tkinter
echo ""
echo "📦 Перевірка наявності tkinter..."

if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ tkinter вже встановлено"
else
    echo "⚠️  tkinter не знайдено. Встановлення..."
    
    if [[ "$OS" == "Darwin" ]]; then
        # macOS - встановлення через Homebrew
        if command -v brew &> /dev/null; then
            brew install python-tk@3.14 || brew install python-tk
        else
            echo "❌ Homebrew не знайдено. Встановіть tkinter вручну:"
            echo "   brew install python-tk@3.14"
            exit 1
        fi
    elif [[ "$OS" == "Linux" ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-tk
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm tk
        fi
    fi
fi

# Перевірка після встановлення
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ tkinter успішно встановлено"
else
    echo "❌ Помилка: tkinter не вдалося встановити автоматично"
    echo "📝 Спробуйте встановити вручну:"
    if [[ "$OS" == "Darwin" ]]; then
        echo "   brew install python-tk@3.14"
    elif [[ "$OS" == "Linux" ]]; then
        echo "   sudo apt-get install python3-tk  # для Debian/Ubuntu"
        echo "   sudo yum install python3-tkinter  # для CentOS/RHEL"
    fi
    exit 1
fi

# Перевірка наявності всіх необхідних файлів
echo ""
echo "📁 Перевірка файлів проекту..."

REQUIRED_FILES=("lab_works.py" "zstu.png" "tr12.png")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file знайдено"
    else
        echo "❌ $file не знайдено"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo "⚠️  Відсутні файли: ${MISSING_FILES[*]}"
    echo "   Переконайтеся, що всі файли присутні в директорії"
fi

# Фінальна перевірка
echo ""
echo "🧪 Тестовий запуск програми..."

if python3 -c "
import tkinter
import os
import sys

# Перевірка наявності файлів
files = ['lab_works.py', 'zstu.png', 'tr12.png']
for f in files:
    if not os.path.exists(f):
        print(f'❌ Файл {f} не знайдено')
        sys.exit(1)

print('✅ Всі перевірки пройдено успішно!')
" 2>/dev/null; then
    echo "✅ Середовище готове до використання!"
    echo ""
    echo "🎉 Ініціалізація завершена успішно!"
    echo ""
    echo "📝 Для запуску програми виконайте:"
    echo "   python3 lab_works.py"
    echo ""
else
    echo "⚠️  Деякі перевірки не пройдено, але основне середовище налаштовано"
    echo "   Спробуйте запустити програму: python3 lab_works.py"
fi

