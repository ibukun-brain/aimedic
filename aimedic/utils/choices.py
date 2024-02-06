from django.db import models


class Gender(models.TextChoices):
    Male = ("male", "Male")
    Female = ("female", "Female")
    Other = ("other", "Other")


class Profile(models.TextChoices):
    Patient = ("patient", "Patient")
    Practitioner = ("practitioner", "Practitioner")


class CropTypes(models.TextChoices):
    FoodCrop = ("food_crop", "Food Crop")
    FeedCrop = ("feed_crop", "Feed Crop")
    FiberCrop = ("fiber_crop", "Fiber Crop")
    ForageCrop = ("forage_crop", "Forage Crop")
    OilseedCrop = ("oilseed_crop", "Oilseed Crop")
    OrnamentalCrop = ("ornamental_crop", "Ornamental Crop")
    IndustrialCrop = ("industrial_crop", "Industrial Crop")


class SoilTypes(models.TextChoices):
    SandySoil = ("sandy_soil", "Sandy Soil")
    LoamySoil = ("loamy_soil", "Loamy Soil")
    ClaySoil = ("clay_soil", "Clay Soil")


class ArticleChoices(models.TextChoices):
    Draft = ("draft", "Draft")
    Published = ("published", "Published")
