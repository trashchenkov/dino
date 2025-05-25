import streamlit as st
import os
from PIL import Image
from dino_analyzer import DinosaurAnalyzer
from models import DinosaurInfo
from utils import format_file_size

def main():
    """Основная функция веб-приложения для Hugging Face Spaces."""
    
    # Настройка страницы
    st.set_page_config(
        page_title="🦕 DINO - Анализатор динозавров",
        page_icon="🦕",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Заголовок
    st.title("🦕 DINO - Анализатор динозавров")
    st.markdown("### Загрузите фотографию фигурки динозавра и получите подробную информацию!")
    
    # Информация о проекте в верхней части
    with st.expander("ℹ️ О проекте DINO", expanded=False):
        st.markdown("""
        **DINO (Dinosaur Image Neural Observer)** - это инновационный проект, демонстрирующий концепцию "Image ORM" 
        с использованием Gemini API.
        
        **Возможности:**
        - 🔍 **Идентификация вида динозавра** по изображению фигурки
        - 🎨 **Анализ цветов** пластиковой фигурки
        - ⏰ **Геологический период** обитания динозавра
        - 📚 **Интересные факты** о виде
        
        **🔗 Исходный код:** [GitHub Repository](https://github.com/trashchenkov/dino)
        """)
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Проверяем наличие API ключа в секретах HF
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        
        if api_key:
            st.success("✅ API ключ настроен администратором")
            st.info("💡 Вы можете сразу использовать приложение!")
        else:
            st.warning("⚠️ API ключ не настроен")
            # Ввод API ключа
            api_key = st.text_input(
                "🔑 Введите ваш Gemini API Key:",
                type="password",
                placeholder="Введите ваш API ключ здесь...",
                help="Получите API ключ на https://ai.google.dev/"
            )
            
            if not api_key:
                st.error("❌ Для работы приложения необходим API ключ Gemini")
                st.markdown("""
                **Как получить API ключ:**
                1. Перейдите на [Google AI Studio](https://ai.google.dev/)
                2. Войдите в аккаунт Google
                3. Создайте новый API ключ
                4. Введите его в поле выше
                """)
        
        st.markdown("---")
        
        # Информация о проекте
        st.markdown("""
        **Советы для лучших результатов:**
        - Используйте четкие фотографии
        - Хорошее освещение важно
        - Фигурка должна быть хорошо видна
        - Избегайте сильных теней
        
        **Поддерживаемые форматы:**
        - PNG, JPG, JPEG
        - Максимум 200MB
        """)
    
    # Основная область
    if api_key:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📸 Загрузка изображения")
            
            uploaded_file = st.file_uploader(
                "Выберите изображение фигурки динозавра",
                type=['png', 'jpg', 'jpeg'],
                help="Поддерживаемые форматы: PNG, JPG, JPEG"
            )
            
            if uploaded_file is not None:
                # Отображение загруженного изображения
                image = Image.open(uploaded_file)
                st.image(image, caption="Загруженное изображение", use_container_width=True)
                
                # Информация о файле
                file_size = len(uploaded_file.getvalue())
                st.info(f"📁 Размер файла: {format_file_size(file_size)}")
                st.info(f"📐 Размеры: {image.width} × {image.height} пикселей")
                
                # Кнопка анализа
                if st.button("🔍 Анализировать динозавра", type="primary", use_container_width=True):
                    analyze_dinosaur(image, api_key, col2)
        
        with col2:
            st.header("📊 Результаты анализа")
            st.info("👆 Загрузите изображение и нажмите 'Анализировать' для получения результатов")
    else:
        st.warning("⚠️ Для использования приложения необходим API ключ Gemini")


def analyze_dinosaur(image: Image.Image, api_key: str, result_column):
    """
    Анализирует изображение динозавра и отображает результаты.
    
    Args:
        image: PIL изображение
        api_key: API ключ для Gemini
        result_column: Столбец Streamlit для отображения результатов
    """
    with result_column:
        # Индикатор загрузки
        with st.spinner("🔍 Анализируем динозавра..."):
            try:
                # Создаем анализатор и анализируем изображение
                analyzer = DinosaurAnalyzer(api_key=api_key)
                result = analyzer.analyze_image_from_pil(image)
                
                if result:
                    display_results(result)
                else:
                    st.error("❌ Не удалось проанализировать изображение")
                    st.info("💡 Попробуйте другое изображение или проверьте качество фото")
                    
            except ValueError as e:
                st.error(f"❌ Ошибка конфигурации: {e}")
                st.info("💡 Убедитесь, что API ключ корректный")
            except Exception as e:
                st.error(f"❌ Произошла ошибка: {e}")
                st.info("💡 Попробуйте еще раз или проверьте подключение к интернету")


def display_results(info: DinosaurInfo):
    """
    Отображает результаты анализа в читаемом формате.
    
    Args:
        info: Информация о динозавре
    """
    # Основная информация
    st.success("✅ Анализ завершен!")
    
    # Используем более читаемый способ отображения данных
    st.subheader("📛 Вид динозавра")
    st.write(f"**{info.species_name}**")
    
    st.subheader("🎨 Цвет фигурки")
    st.write(f"{info.color_description}")
    
    st.subheader("⏰ Геологический период")
    st.write(f"{info.geological_period}")
    
    # Интересный факт в отдельном блоке
    st.subheader("📚 Интересный факт")
    st.info(info.brief_info)
    
    # Дополнительные действия
    st.markdown("---")
    st.subheader("💾 Экспорт данных")
    
    col_actions1, col_actions2 = st.columns(2)
    
    with col_actions1:
        if st.button("📋 Показать текстовые данные", use_container_width=True):
            data_text = f"""Вид: {info.species_name}
Цвет фигурки: {info.color_description}
Период: {info.geological_period}
Интересный факт: {info.brief_info}"""
            st.text_area("Данные для копирования:", data_text, height=150)
    
    with col_actions2:
        json_data = info.model_dump_json(indent=2)
        st.download_button(
            label="💾 Скачать JSON",
            data=json_data,
            file_name="dinosaur_info.json",
            mime="application/json",
            use_container_width=True
        )
    
    # JSON данные (сворачиваемые)
    with st.expander("🔧 Детальные данные (JSON)"):
        st.json(info.model_dump())


# Футер
def show_footer():
    """Отображает футер с дополнительной информацией."""
    st.markdown("---")
    
    # Статистика и дополнительная информация
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔬 Технологии:**
        - Gemini AI API
        - Streamlit
        - Python
        - Pydantic
        """)
    
    with col2:
        st.markdown("""
        **📊 Возможности:**
        - Распознавание видов
        - Анализ цветов
        - Исторические данные
        - Образовательные факты
        """)
    
    with col3:
        st.markdown("""
        **🚀 Ссылки:**
        - [GitHub](https://github.com/trashchenkov/dino)
        - [Документация](https://github.com/trashchenkov/dino#readme)
        - [Gemini API](https://ai.google.dev/)
        """)
    
    st.markdown("""
    <div style='text-align: center; margin-top: 2rem;'>
        <p>🦕 <strong>DINO Project</strong> - Image ORM для анализа динозавров</p>
        <p>Powered by <strong>Gemini API</strong> • Deployed on <strong>Hugging Face Spaces</strong> 🚀</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    show_footer() 