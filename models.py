from pydantic import BaseModel, Field
from typing import Optional


class DinosaurInfo(BaseModel):
    """Модель для структурированной информации о динозавре."""
    
    species_name: str = Field(
        description="Научное или общепринятое название вида динозавра"
    )
    color_description: str = Field(
        description="Описание основных цветов фигурки динозавра"
    )
    geological_period: str = Field(
        description="Геологический период, в котором обитал этот вид динозавра (например, Юрский, Меловой)"
    )
    brief_info: str = Field(
        description="Краткая интересная информация о динозавре (1-2 предложения)"
    ) 