---
title: DINO - Dinosaur Analyzer
emoji: 🦕
colorFrom: green
colorTo: brown
sdk: streamlit
sdk_version: 1.45.1
app_file: app.py
pinned: false
license: mit
---

# 🦕 DINO - Dinosaur Image Neural Observer

An innovative **Image ORM** project that uses **Gemini API** to analyze plastic dinosaur figurines and extract structured information including species identification, color analysis, geological periods, and educational facts.

## 🚀 Try it Live!

Upload a photo of your dinosaur figurine and get instant analysis with:
- 🔍 **Species identification** - Scientific name and classification
- 🎨 **Color analysis** - Description of the figurine's colors
- ⏰ **Geological period** - When this dinosaur lived
- 📚 **Educational facts** - Interesting information about the species

## 🔑 API Key Required

This app requires a **Gemini API key** to function. You can:
1. Get your free API key at [Google AI Studio](https://ai.google.dev/)
2. Enter it in the sidebar when using the app

## 🛠️ Technology Stack

- **AI Model**: Google Gemini API for image analysis
- **Framework**: Streamlit for web interface
- **Language**: Python with Pydantic for data validation
- **Image Processing**: PIL/Pillow for image optimization

## 📊 Features

- ✅ **Real-time analysis** of dinosaur figurines
- ✅ **Structured JSON output** with consistent data format
- ✅ **Russian language support** for AI responses
- ✅ **Modern web interface** with drag-and-drop upload
- ✅ **Export functionality** for analysis results
- ✅ **Error handling** and validation

## 🔗 Source Code

Full source code, documentation, and local setup instructions available on GitHub:
[https://github.com/trashchenkov/dino](https://github.com/trashchenkov/dino)

## 📝 Example Output

```json
{
  "species_name": "Тираннозавр Рекс",
  "color_description": "зеленый с коричневыми полосами",
  "geological_period": "Поздний меловой период",
  "brief_info": "Один из крупнейших наземных хищников всех времен"
}
```

## 💡 Tips for Best Results

- Use clear, well-lit photos
- Ensure the dinosaur figurine is clearly visible
- Avoid strong shadows or reflections
- Supported formats: PNG, JPG, JPEG

---

**Made with ❤️ for dinosaur enthusiasts and AI technology lovers!** 