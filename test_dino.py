#!/usr/bin/env python3
"""
Тестовый скрипт для проекта DINO.
Проверяет основную функциональность без использования реального API.
"""

import os
import sys
from PIL import Image
import tempfile


def test_imports():
    """Тестирует импорт всех модулей."""
    print("🔍 Тестируем импорты...")
    
    try:
        from models import DinosaurInfo
        print("✅ models.py - импорт успешен")
    except ImportError as e:
        print(f"❌ models.py - ошибка импорта: {e}")
        return False
    
    try:
        import utils
        print("✅ utils.py - импорт успешен")
    except ImportError as e:
        print(f"❌ utils.py - ошибка импорта: {e}")
        return False
    
    try:
        from dino_analyzer import DinosaurAnalyzer
        print("✅ dino_analyzer.py - импорт успешен")
    except ImportError as e:
        print(f"❌ dino_analyzer.py - ошибка импорта: {e}")
        return False
    
    return True


def test_models():
    """Тестирует работу Pydantic моделей."""
    print("\n📝 Тестируем модели...")
    
    try:
        from models import DinosaurInfo
        
        # Создаем тестовые данные
        test_data = {
            "species_name": "Тираннозавр Рекс",
            "color_description": "зеленый с коричневыми полосами",
            "geological_period": "Поздний меловой период",
            "brief_info": "Крупнейший наземный хищник"
        }
        
        # Создаем объект
        dino = DinosaurInfo(**test_data)
        print("✅ DinosaurInfo - создание объекта успешно")
        
        # Проверяем JSON сериализацию
        json_data = dino.model_dump_json()
        print("✅ DinosaurInfo - JSON сериализация успешна")
        
        # Проверяем валидацию
        restored = DinosaurInfo.model_validate_json(json_data)
        print("✅ DinosaurInfo - валидация JSON успешна")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании моделей: {e}")
        return False


def test_utils():
    """Тестирует утилиты для работы с изображениями."""
    print("\n🛠️ Тестируем утилиты...")
    
    try:
        from utils import (
            validate_image_file, 
            optimize_image_for_api, 
            format_file_size,
            save_temp_image,
            cleanup_temp_file
        )
        
        # Создаем тестовое изображение
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Тестируем оптимизацию
        optimized = optimize_image_for_api(test_image)
        print("✅ optimize_image_for_api - успешно")
        
        # Тестируем форматирование размера
        size_str = format_file_size(1024)
        assert "KB" in size_str
        print("✅ format_file_size - успешно")
        
        # Тестируем сохранение временного файла
        temp_path = save_temp_image(test_image)
        assert os.path.exists(temp_path)
        print("✅ save_temp_image - успешно")
        
        # Тестируем очистку
        success = cleanup_temp_file(temp_path)
        assert success
        assert not os.path.exists(temp_path)
        print("✅ cleanup_temp_file - успешно")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании утилит: {e}")
        return False


def test_analyzer_init():
    """Тестирует инициализацию анализатора без API ключа."""
    print("\n🤖 Тестируем анализатор...")
    
    try:
        from dino_analyzer import DinosaurAnalyzer
        
        # Тестируем без API ключа (должно выдать ошибку)
        try:
            analyzer = DinosaurAnalyzer()
            print("❌ DinosaurAnalyzer - не выдал ошибку без API ключа")
            return False
        except ValueError:
            print("✅ DinosaurAnalyzer - корректно требует API ключ")
        
        # Тестируем с фейковым API ключом
        try:
            analyzer = DinosaurAnalyzer(api_key="fake_key_for_testing")
            print("✅ DinosaurAnalyzer - инициализация с API ключом успешна")
        except Exception as e:
            print(f"❌ DinosaurAnalyzer - ошибка инициализации: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании анализатора: {e}")
        return False


def test_file_structure():
    """Проверяет структуру файлов проекта."""
    print("\n📁 Проверяем структуру проекта...")
    
    required_files = [
        "models.py",
        "dino_analyzer.py", 
        "streamlit_app.py",
        "utils.py",
        "requirements.txt",
        "README.md",
        "dino.md"
    ]
    
    missing_files = []
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - найден")
        else:
            print(f"❌ {file_name} - отсутствует")
            missing_files.append(file_name)
    
    return len(missing_files) == 0


def create_sample_image():
    """Создает образец изображения для тестирования."""
    print("\n🖼️ Создаем образец изображения...")
    
    try:
        # Создаем простое тестовое изображение
        img = Image.new('RGB', (300, 200), color='green')
        
        # Добавляем простую "фигурку динозавра" (прямоугольники)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Тело
        draw.rectangle([50, 100, 150, 160], fill='darkgreen')
        # Голова
        draw.rectangle([150, 80, 200, 120], fill='darkgreen')
        # Хвост
        draw.rectangle([20, 110, 50, 130], fill='darkgreen')
        # Ноги
        draw.rectangle([70, 160, 80, 180], fill='darkgreen')
        draw.rectangle([120, 160, 130, 180], fill='darkgreen')
        
        # Сохраняем
        sample_path = "sample_dino.jpg"
        img.save(sample_path, "JPEG")
        print(f"✅ Образец сохранен как {sample_path}")
        
        return sample_path
        
    except Exception as e:
        print(f"❌ Ошибка создания образца: {e}")
        return None


def main():
    """Основная функция тестирования."""
    print("🦕 DINO Project - Тестирование")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Запускаем тесты
    tests = [
        test_file_structure,
        test_imports,
        test_models,
        test_utils,
        test_analyzer_init
    ]
    
    for test_func in tests:
        if not test_func():
            all_tests_passed = False
    
    # Создаем образец изображения
    sample_path = create_sample_image()
    
    # Итог
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✅ Все тесты пройдены успешно!")
        print("\n🚀 Готово к запуску:")
        print("   streamlit run streamlit_app.py")
        if sample_path:
            print(f"   Используйте {sample_path} для тестирования")
    else:
        print("❌ Некоторые тесты не пройдены")
        print("   Проверьте ошибки выше")
    
    print("\n💡 Не забудьте:")
    print("   1. Установить зависимости: pip install -r requirements.txt")
    print("   2. Получить API ключ: https://ai.google.dev/")
    print("   3. Настроить переменную окружения GEMINI_API_KEY")


if __name__ == "__main__":
    main() 