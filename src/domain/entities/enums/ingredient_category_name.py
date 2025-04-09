from enum import StrEnum


class IngredientCategoryName(StrEnum):
    INGREDIENT = "Ingredient"
    SEMI_FINISHED_PRODUCT = "SemiFinishedProduct"
    FINISHED_PRODUCT = "FinishedProduct"
    INVENTORY = "Inventory"
    PACKING = "Packing"
    CONSUMABLES = "Consumables"
