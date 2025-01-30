from django.contrib import admin
from .models import Avatar, Vehicle, Brand, Application
import os
from django.core.files import File
from django.conf import settings

# Функция для создания Avatar из изображений
def create_avatars_from_images():
    avatars_dir = os.path.join(settings.BASE_DIR, 'myproject', 'media', 'avatars')
    avatar_images = [f for f in os.listdir(avatars_dir) if f.endswith('.webp')]

    for image_name in avatar_images:
        image_path = os.path.join(avatars_dir, image_name)
        if not Avatar.objects.filter(image=f'avatars/{image_name}').exists():  # Проверка на дублирование
            with open(image_path, 'rb') as f:
                avatar = Avatar(image=File(f, name=image_name))
                avatar.save()

# Действие для админки: присвоить Avatar выбранным Vehicle
def assign_avatars(modeladmin, request, queryset):
    create_avatars_from_images()  # Создаем Avatar, если их еще нет
    avatars = Avatar.objects.all()

    for vehicle, avatar in zip(queryset, avatars):
        vehicle.avatar = avatar
        vehicle.save()

assign_avatars.short_description = "Assign avatars to selected vehicles"

# Регистрация моделей в админке
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model', 'year', 'brand_country')  # Поля для отображения в списке
    actions = [assign_avatars]  # Добавляем действие в админку

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand', 'country')  # Поля для отображения в списке

@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')  # Поля для отображения в списке

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at', 'privacy_agreed')
    search_fields = ('name', 'phone')
    list_filter = ('created_at',)