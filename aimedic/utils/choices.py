from django.db import models


class Gender(models.TextChoices):
    Male = ("male", "Male")
    Female = ("female", "Female")
    Other = ("other", "Other")


class AppointmentStatus(models.TextChoices):
    Pending = ("pending", "Pending")
    Active = ("active", "Active")
    Cancelled = ("cancelled", "Cancelled")


class AppointmentDurationStatus(models.IntegerChoices):
    one = 1
    two = 2
    three = 3


class SerializerGenderChoices(models.IntegerChoices):
    male = 1
    female = 0


class SerializerChestPainTypeChoices(models.IntegerChoices):
    typical_angina = 0
    atypical_angina = 1
    non_angina = 2
    asymptomatic = 3


class SerializerFastingBloodSugarChoices(models.IntegerChoices):
    true = 1
    false = 0


class SerializerECGChoices(models.IntegerChoices):
    normal = 0
    wave_abnormality = 1
    ventricular_hypertrophy = 2


class SerializerExangChoices(models.IntegerChoices):
    yes = 1
    no = 0


class SerializerSlopeChoices(models.IntegerChoices):
    unsloping = 0
    flat = 1
    downsloping = 2


class SerializerThalassemiaChoices(models.IntegerChoices):
    normal = 0
    fixed_defect = 1
    reversable_defect = 2


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
