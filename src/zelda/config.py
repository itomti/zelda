from __future__ import annotations
import json
import logging
from pydantic import BaseModel


class Config(BaseModel):
    fps: int
    tile_size: int
    user_interface: UserInterfaceSettings

    @staticmethod
    def make() -> Config:
        cfg = {}
        with open("config.json", "r") as f:
            cfg = json.load(f)

        logging.info(json.dumps(cfg))
        return Config(**cfg)

class HealthBar(BaseModel):
    height: int
    width: int
    color: str

class EnergyBar(BaseModel):
    height: int
    width: int
    color: str

class Font(BaseModel):
    path: str
    size: int

class UIColor(BaseModel):
    water: str
    background: str
    border: str
    active: str
    text: str

class UserInterfaceSettings(BaseModel):
    width: int
    height: int
    healthBar: HealthBar
    energyBar: EnergyBar
    item_box_size: int
    font: Font
    ui_color: UIColor
