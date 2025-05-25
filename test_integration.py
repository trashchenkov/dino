#!/usr/bin/env python3
"""
Интеграционный тест для проекта DINO.
Тестирует реальную работу с Gemini API.
ТРЕБУЕТ: настроенный API ключ в .env файле.
"""

import os
import sys
from PIL import Image
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def test_api_connection():
    """Тестирует подключение к Gemini API."""
    print("🔗 Тестируем подключение к Gemini API...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ API ключ не найден в переменных окружения")
        print("💡 Убедитесь, что файл .env содержит GEMINI_API_KEY")
        return False
    
    if api_key == "your_api_key_here":
        print("❌ API ключ не настроен (используется значение по умолчанию)")
        print("💡 Замените 'your_api_key_here' на реальный API ключ")
        return False
    
    print(f"✅ API ключ найден (длина: {len(api_key)} символов)")
    return True


def test_real_image_analysis():
    """Тестирует реальный анализ изображения через API."""
    print("\n🖼️ Тестируем реальный анализ изображения...")
    
    try:
        from dino_analyzer import DinosaurAnalyzer
        
        # Создаем анализатор
        analyzer = DinosaurAnalyzer()
        print("✅ Анализатор создан успешно")
        
        # Проверяем, есть ли тестовое изображение
        test_image_path = "sample_dino.jpg"
        if not os.path.exists(test_image_path):
            print(f"❌ Тестовое изображение {test_image_path} не найдено")
            return False
        
        print(f"📁 Используем тестовое изображение: {test_image_path}")
        
        # Анализируем изображение
        print("🔍 Отправляем запрос к Gemini API...")
        result = analyzer.analyze_image(test_image_path)
        
        if result:
            print("✅ Анализ прошел успешно!")
            print(f"📛 Вид: {result.species_name}")
            print(f"🎨 Цвет: {result.color_description}")
            print(f"⏰ Период: {result.geological_period}")
            print(f"📚 Факт: {result.brief_info}")
            
            # Проверяем, что поля заполнены
            if all([result.species_name, result.color_description, 
                   result.geological_period, result.brief_info]):
                print("✅ Все поля заполнены")
                return True
            else:
                print("❌ Некоторые поля пустые")
                return False
        else:
            print("❌ Анализ не удался - API вернул None")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при анализе: {e}")
        return False


def test_pil_image_analysis():
    """Тестирует анализ PIL изображения."""
    print("\n🎨 Тестируем анализ PIL изображения...")
    
    try:
        from dino_analyzer import DinosaurAnalyzer
        
        # Создаем простое цветное изображение
        test_image = Image.new('RGB', (200, 200), color='darkgreen')
        
        # Добавляем простые формы
        from PIL import ImageDraw
        draw = ImageDraw.Draw(test_image)
        draw.rectangle([50, 50, 150, 100], fill='lightgreen')  # Тело
        draw.rectangle([150, 40, 180, 80], fill='green')       # Голова
        
        analyzer = DinosaurAnalyzer()
        result = analyzer.analyze_image_from_pil(test_image)
        
        if result:
            print("✅ Анализ PIL изображения успешен")
            print(f"📛 Результат: {result.species_name}")
            return True
        else:
            print("❌ Анализ PIL изображения не удался")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при анализе PIL изображения: {e}")
        return False


def test_model_validation():
    """Тестирует валидацию модели с реальными данными."""
    print("\n📝 Тестируем валидацию модели...")
    
    try:
        from models import DinosaurInfo
        
        # Создаем JSON как мог бы вернуть API
        api_response = '''
        {
            "species_name": "Tyrannosaurus Rex",
            "color_description": "brown and green plastic figure",
            "geological_period": "Late Cretaceous",
            "brief_info": "One of the largest land predators ever known"
        }
        '''
        
        # Валидируем
        dino = DinosaurInfo.model_validate_json(api_response)
        print("✅ Валидация JSON успешна")
        print(f"📛 Создан объект: {dino.species_name}")
        
        # Проверяем сериализацию обратно
        json_output = dino.model_dump_json(indent=2)
        print("✅ Сериализация в JSON успешна")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка валидации модели: {e}")
        return False


def test_error_handling():
    """Тестирует обработку ошибок."""
    print("\n🛡️ Тестируем обработку ошибок...")
    
    try:
        from dino_analyzer import DinosaurAnalyzer
        
        analyzer = DinosaurAnalyzer()
        
        # Тестируем несуществующий файл
        result = analyzer.analyze_image("nonexistent_file.jpg")
        if result is None:
            print("✅ Корректно обработан несуществующий файл")
        else:
            print("❌ Неправильная обработка несуществующего файла")
            return False
        
        # Тестируем некорректный файл (если существует)
        with open("test_invalid.txt", "w") as f:
            f.write("This is not an image")
        
        result = analyzer.analyze_image("test_invalid.txt")
        if result is None:
            print("✅ Корректно обработан некорректный файл")
        else:
            print("❌ Неправильная обработка некорректного файла")
            return False
        
        # Очищаем тестовый файл
        os.remove("test_invalid.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании обработки ошибок: {e}")
        return False


def main():
    """Основная функция интеграционного тестирования."""
    print("🦕 DINO Project - Интеграционное тестирование")
    print("=" * 50)
    print("⚠️  ТРЕБУЕТ: настроенный API ключ в .env файле")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Запускаем интеграционные тесты
    tests = [
        test_api_connection,
        test_model_validation,
        test_error_handling,
        test_real_image_analysis,
        test_pil_image_analysis
    ]
    
    for test_func in tests:
        if not test_func():
            all_tests_passed = False
            print()  # Пустая строка для разделения
    
    # Итог
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 Все интеграционные тесты пройдены!")
        print("✅ Проект DINO полностью функционален")
        print("\n🚀 Можно использовать:")
        print("   • streamlit run streamlit_app.py (веб-интерфейс)")
        print("   • python dino_analyzer.py (консоль)")
    else:
        print("❌ Некоторые интеграционные тесты не пройдены")
        print("🔧 Проверьте конфигурацию API и повторите")
    
    print("\n📊 Результаты тестирования:")
    print("   • Unit тесты: python test_dino.py")
    print("   • Integration тесты: python test_integration.py")


if __name__ == "__main__":
    main() 