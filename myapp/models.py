from django.db import models

class Avatar(models.Model):
    image = models.ImageField(upload_to='avatars/')  # Изображение будет сохраняться в папке `avatars`

    def __str__(self):
        return f"Avatar {self.id}"

class Brand(models.Model):
    country = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand} ({self.country})"

class Vehicle(models.Model):
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transmission = models.CharField(max_length=50)
    engine_volume = models.FloatField()
    drive = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    power_volume = models.FloatField()
    brand_country = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='vehicles', null=True, blank=True)
    avatar = models.ForeignKey('Avatar', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.model} ({self.year} {self.engine_volume} {self.price})"

class ParseCurrency():
    from bs4 import BeautifulSoup
    import requests

    url = 'https://bbr.ru/'
    page = requests.get(url)
    print(page.status_code)

    filteredCourse = []
    allCourse = []

    soup = BeautifulSoup(page.text, "html.parser")
    allCourse = soup.findAll('span', class_='css-11ctayd exmh6wy0')

    # это удаляет ненужные стоимости
    del allCourse[0:3]
    del allCourse[1]
    del allCourse[2]
    del allCourse[4]
    del allCourse[3]

    print(allCourse)

    for data in allCourse:
        filteredCourse.append(data.text)
    print(filteredCourse)
    cny_d = filteredCourse[1]
    jpy_d = filteredCourse[2]
    krw_d = filteredCourse[0]

    cny = float(cny_d.replace(',', '.'))
    jpy = float(jpy_d.replace(',', '.'))
    krw = float(krw_d.replace(',', '.'))
    def __str__(self):
        return f"{self.cny}, {self.jpy}, {self.krw}"


class Application(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    privacy_agreed = models.BooleanField(default=False, verbose_name='Согласие с политикой')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Заявка от {self.name} ({self.created_at})"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'