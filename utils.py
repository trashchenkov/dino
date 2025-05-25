import os
from typing import Tuple, Optional
from PIL import Image, ImageOps
import io


def validate_image_file(file_path: str) -> bool:
    """
    Проверяет, является ли файл корректным изображением.
    
    Args:
        file_path: Путь к файлу изображения
        
    Returns:
        True если файл является корректным изображением
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_image_info(file_path: str) -> Optional[dict]:
    """
    Получает информацию об изображении.
    
    Args:
        file_path: Путь к файлу изображения
        
    Returns:
        Словарь с информацией об изображении или None при ошибке
    """
    try:
        with Image.open(file_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": os.path.getsize(file_path)
            }
    except Exception:
        return None


def resize_image_if_needed(image: Image.Image, max_size: Tuple[int, int] = (1024, 1024)) -> Image.Image:
    """
    Изменяет размер изображения, если оно слишком большое.
    
    Args:
        image: PIL изображение
        max_size: Максимальный размер (ширина, высота)
        
    Returns:
        Изображение с измененным размером (если необходимо)
    """
    if image.width > max_size[0] or image.height > max_size[1]:
        # Сохраняем пропорции
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image


def optimize_image_for_api(image: Image.Image, quality: int = 85) -> Image.Image:
    """
    Оптимизирует изображение для отправки в API.
    
    Args:
        image: PIL изображение
        quality: Качество сжатия JPEG (1-100)
        
    Returns:
        Оптимизированное изображение
    """
    # Изменяем размер если нужно
    optimized = resize_image_if_needed(image)
    
    # Автоматически поворачиваем на основе EXIF данных
    optimized = ImageOps.exif_transpose(optimized)
    
    # Конвертируем в RGB если изображение в RGBA или другом формате
    if optimized.mode in ('RGBA', 'LA', 'P'):
        # Создаем белый фон для прозрачных изображений
        background = Image.new('RGB', optimized.size, (255, 255, 255))
        if optimized.mode == 'P':
            optimized = optimized.convert('RGBA')
        background.paste(optimized, mask=optimized.split()[-1] if optimized.mode == 'RGBA' else None)
        optimized = background
    elif optimized.mode != 'RGB':
        optimized = optimized.convert('RGB')
    
    return optimized


def save_temp_image(image: Image.Image, prefix: str = "temp_dino") -> str:
    """
    Сохраняет временное изображение и возвращает путь к нему.
    
    Args:
        image: PIL изображение
        prefix: Префикс для имени файла
        
    Returns:
        Путь к временному файлу
    """
    import tempfile
    import uuid
    
    # Создаем уникальное имя файла
    temp_name = f"{prefix}_{uuid.uuid4().hex[:8]}.jpg"
    temp_path = os.path.join(tempfile.gettempdir(), temp_name)
    
    # Оптимизируем и сохраняем
    optimized_image = optimize_image_for_api(image)
    optimized_image.save(temp_path, "JPEG", quality=85, optimize=True)
    
    return temp_path


def cleanup_temp_file(file_path: str) -> bool:
    """
    Удаляет временный файл.
    
    Args:
        file_path: Путь к файлу для удаления
        
    Returns:
        True если файл успешно удален
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def convert_bytes_to_image(image_bytes: bytes) -> Optional[Image.Image]:
    """
    Конвертирует байты в PIL изображение.
    
    Args:
        image_bytes: Байты изображения
        
    Returns:
        PIL изображение или None при ошибке
    """
    try:
        return Image.open(io.BytesIO(image_bytes))
    except Exception:
        return None


def get_supported_formats() -> list:
    """
    Возвращает список поддерживаемых форматов изображений.
    
    Returns:
        Список расширений файлов
    """
    return ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']


def format_file_size(size_bytes: int) -> str:
    """
    Форматирует размер файла в читаемый вид.
    
    Args:
        size_bytes: Размер в байтах
        
    Returns:
        Отформатированная строка размера
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB" 