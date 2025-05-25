import os
import json
from typing import Optional
from PIL import Image
import google.generativeai as genai

# Пытаемся импортировать dotenv, если доступен (для локальной разработки)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # На HF Spaces dotenv может быть недоступен, это нормально
    pass

from models import DinosaurInfo
from utils import optimize_image_for_api, save_temp_image, cleanup_temp_file, validate_image_file

class DinosaurAnalyzer:
    """Класс для анализа изображений динозавров с помощью Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация анализатора.
        
        Args:
            api_key: API ключ для Gemini. Если не указан, будет взят из переменной окружения.
        """
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
            
        if not api_key:
            raise ValueError(
                "API ключ не найден. Укажите его в параметре api_key или "
                "установите переменную окружения GEMINI_API_KEY"
            )
            
        genai.configure(api_key=api_key)
        
        # Инициализация модели с системной инструкцией
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": DinosaurInfo
            },
            system_instruction="""
            ВАЖНО: Отвечай ТОЛЬКО на РУССКОМ языке! Весь твой ответ должен быть на русском языке.
            
            Ты — эксперт-палеонтолог и ИИ для анализа изображений пластиковых фигурок динозавров. 
            Твоя задача — идентифицировать вид динозавра по фотографии игрушечной фигурки.
            
            ИНСТРУКЦИИ ПО АНАЛИЗУ:
            1. 🔍 ОПРЕДЕЛИ ВИД: Внимательно изучи форму тела, голову, конечности, хвост, характерные особенности для определения точного вида динозавра. Назови вид на РУССКОМ языке.
            
            2. 🎨 ОПИШИ ЦВЕТА: Опиши основные цвета именно этой пластиковой фигурки (как они выглядят на фото). НЕ описывай реальные цвета динозавра, а только то, что видишь на игрушке.
            
            3. ⏰ УКАЖИ ПЕРИОД: Определи геологический период, в котором жил этот вид динозавра. Ответ дай на РУССКОМ языке (например, "Юрский период", "Поздний меловой период").
            
            4. 📚 РАССКАЖИ ФАКТ: Поделись интересным фактом об этом виде динозавра. Факт должен быть познавательным и написан на РУССКОМ языке.
            
            ВАЖНЫЕ ТРЕБОВАНИЯ:
            - ВСЕ поля заполняй только на РУССКОМ языке
            - Если не можешь точно определить вид, напиши "Неопределенный вид" или опиши как "Динозавр семейства..."
            - Для цветов используй простые русские названия (зеленый, коричневый, желтый и т.д.)
            - Геологические периоды называй по-русски
            - Факты должны быть интересными и понятными
            
            Верни всю информацию в указанной JSON-схеме НА РУССКОМ ЯЗЫКЕ.
            """
        )
    
    def analyze_image(self, image_path: str) -> Optional[DinosaurInfo]:
        """
        Анализирует изображение динозавра и возвращает структурированную информацию.
        
        Args:
            image_path: Путь к файлу изображения
            
        Returns:
            DinosaurInfo объект с информацией о динозавре или None при ошибке
        """
        try:
            # Проверяем существование и валидность файла
            if not os.path.exists(image_path):
                print(f"Ошибка: файл {image_path} не найден")
                return None
                
            if not validate_image_file(image_path):
                print(f"Ошибка: файл {image_path} не является корректным изображением")
                return None
            
            # Загружаем и оптимизируем изображение
            img = Image.open(image_path)
            optimized_img = optimize_image_for_api(img)
            
            # Отправляем запрос к Gemini API
            response = self.model.generate_content([optimized_img])
            
            # Парсим JSON ответ в объект DinosaurInfo
            dino_data = DinosaurInfo.model_validate_json(response.text)
            return dino_data
            
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            print(f"Ответ модели: {response.text}")
            return None
        except Exception as e:
            print(f"Произошла ошибка при анализе изображения: {e}")
            if 'response' in locals() and hasattr(response, 'prompt_feedback'):
                print(f"Обратная связь: {response.prompt_feedback}")
            return None
    
    def analyze_image_from_pil(self, image: Image.Image) -> Optional[DinosaurInfo]:
        """
        Анализирует PIL изображение динозавра.
        
        Args:
            image: PIL изображение
            
        Returns:
            DinosaurInfo объект с информацией о динозавре или None при ошибке
        """
        temp_path = None
        try:
            # Сохраняем временный файл
            temp_path = save_temp_image(image)
            
            # Отправляем запрос к Gemini API с оптимизированным изображением
            optimized_img = optimize_image_for_api(image)
            response = self.model.generate_content([optimized_img])
            
            # Парсим JSON ответ в объект DinosaurInfo
            dino_data = DinosaurInfo.model_validate_json(response.text)
            return dino_data
            
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            if 'response' in locals():
                print(f"Ответ модели: {response.text}")
            return None
        except Exception as e:
            print(f"Произошла ошибка при анализе изображения: {e}")
            if 'response' in locals() and hasattr(response, 'prompt_feedback'):
                print(f"Обратная связь: {response.prompt_feedback}")
            return None
        finally:
            # Очищаем временный файл
            if temp_path:
                cleanup_temp_file(temp_path)
    
    def print_dinosaur_info(self, info: DinosaurInfo) -> None:
        """
        Красиво выводит информацию о динозавре.
        
        Args:
            info: Объект с информацией о динозавре
        """
        separator = "=" * 50
        print(f"\n{separator}")
        print("🦕 ИНФОРМАЦИЯ О ДИНОЗАВРЕ 🦕")
        print(f"{separator}")
        print(f"📛 Вид: {info.species_name}")
        print(f"🎨 Цвет фигурки: {info.color_description}")
        print(f"⏰ Период: {info.geological_period}")
        print(f"📚 Интересный факт: {info.brief_info}")
        print(f"{separator}\n")


def main():
    """Основная функция для демонстрации работы анализатора."""
    # Пример использования
    try:
        analyzer = DinosaurAnalyzer()
        
        # Замените на путь к вашему изображению динозавра
        image_path = input("Введите путь к изображению динозавра: ").strip()
        
        if not image_path:
            print("Путь к изображению не указан")
            return
        
        print("🔍 Анализируем изображение...")
        info = analyzer.analyze_image(image_path)
        
        if info:
            analyzer.print_dinosaur_info(info)
        else:
            print("❌ Не удалось проанализировать изображение")
            
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}")
        print("💡 Убедитесь, что у вас есть API ключ для Gemini")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main() 