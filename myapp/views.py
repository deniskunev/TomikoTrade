from django.shortcuts import render, get_object_or_404
from .models import Vehicle, Brand, ParseCurrency
from django.db.models import Q
import json
from django.http import JsonResponse
from .forms import ApplicationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



def tamozh_oform(currency):
    currency = float(currency)  # добавить преобразование
    if currency <= 200000:  # это в рублях
        nalog = 775  # это в рублях
    elif currency > 200000 and currency <= 450000:
        nalog = 1550
    elif currency > 450000 and currency <= 1200000:
        nalog = 3100
    elif currency > 1200000 and currency <= 2700000:
        nalog = 8530
    elif currency > 2700000 and currency <= 4200000:
        nalog = 12000
    elif currency > 4200000 and currency <= 5500000:
        nalog = 15000
    elif currency > 5500000 and currency <= 7000000:
        nalog = 20000
    elif currency > 7000000 and currency <= 8000000:
        nalog = 23000
    elif currency > 8000000 and currency <= 9000000:
        nalog = 25000
    elif currency > 9000000 and currency <= 10000000:
        nalog = 27000
    elif currency > 10000000:
        nalog = 30000

    return (nalog)


def edinaya_stavka(currency, engine_vol):
    currency = float(currency)  # добавить преобразование
    engine_vol_cm3 = engine_vol
    stavka_54 = currency * 0.54
    stavka_48 = currency * 0.48
    eur = ParseCurrency().krw

    if currency <= 8500 * eur:
        if stavka_54 >= engine_vol_cm3 * 2.5 * eur:  # это в евро
            nalog = stavka_54
        else:
            nalog = engine_vol_cm3 * 2.5 * eur
    elif currency > 8500 * eur and currency <= 16700 * eur:
        if stavka_48 >= engine_vol_cm3 * 3.5 * eur:  # это в евро
            nalog = stavka_48
        else:
            nalog = engine_vol_cm3 * 3.5 * eur
    elif currency > 16700 * eur and currency <= 42300 * eur:
        if stavka_48 >= engine_vol_cm3 * 5.5 * eur:  # это в евро
            nalog = stavka_48
        else:
            nalog = engine_vol_cm3 * 5.5 * eur
    elif currency > 42300 * eur and currency <= 845000 * eur:
        if stavka_48 >= engine_vol_cm3 * 7.5 * eur:  # это в евро
            nalog = stavka_48
        else:
            nalog = engine_vol_cm3 * 7.5 * eur
    elif currency > 845000 * eur and currency <= 169000 * eur:
        if stavka_48 >= engine_vol_cm3 * 15 * eur:  # это в евро
            nalog = stavka_48
        else:
            nalog = engine_vol_cm3 * 15 * eur
    elif currency > 169000 * eur:
        if stavka_48 >= engine_vol_cm3 * 20 * eur:  # это в евро
            nalog = stavka_48
        else:
            nalog = engine_vol_cm3 * 20 * eur
    return (nalog)


def utilizacionniy_sbor(year, engine_vol):
    engine_vol_cm3 = engine_vol
    eur = ParseCurrency().krw

    if year >= 3 and year < 5:
        if engine_vol_cm3 <= 1000:
            nalog = engine_vol_cm3 * 1.5 * eur
        elif engine_vol_cm3 > 1000 and engine_vol_cm3 <= 1500:
            nalog = engine_vol_cm3 * 1.7 * eur
        elif engine_vol_cm3 > 1500 and engine_vol_cm3 <= 1800:
            nalog = engine_vol_cm3 * 2.5 * eur
        elif engine_vol_cm3 > 1800 and engine_vol_cm3 <= 2300:
            nalog = engine_vol_cm3 * 2.7 * eur
        elif engine_vol_cm3 > 2300 and engine_vol_cm3 <= 3000:
            nalog = engine_vol_cm3 * 3 * eur
        elif engine_vol_cm3 > 3000:
            nalog = engine_vol_cm3 * 3.6 * eur

    elif year >= 5:
        if engine_vol_cm3 <= 1000:
            nalog = engine_vol_cm3 * 3 * eur
        elif (engine_vol_cm3 > 1000 and engine_vol_cm3 <= 1500):
            nalog = engine_vol_cm3 * 3.2 * eur
        elif engine_vol_cm3 > 1500 and engine_vol_cm3 <= 1800:
            nalog = engine_vol_cm3 * 3.5 * eur
        elif engine_vol_cm3 > 1800 and engine_vol_cm3 <= 2300:
            nalog = engine_vol_cm3 * 4.8 * eur
        elif engine_vol_cm3 > 2300 and engine_vol_cm3 <= 3000:
            nalog = engine_vol_cm3 * 5 * eur
        elif engine_vol_cm3 > 3000:
            nalog = engine_vol_cm3 * 5.7 * eur

    return (nalog)


def Poshlina(currency, engine_vol, year):
    return (utilizacionniy_sbor(year, engine_vol) + edinaya_stavka(currency, engine_vol) + tamozh_oform(currency))


def index(request):
    form = ApplicationForm()
    return render(request, "index.html", {'form': form})
def Actions(request):
    form = ApplicationForm()
    return render(request, "Actions.html", {'form': form})
def contact(request):
    form = ApplicationForm()
    return render(request, "contact.html", {'form': form})
def project(request):
    form = ApplicationForm()
    return render(request, "project.html", {'form': form})
def Send(request):
    data = {
        'val': {
            'cny': ParseCurrency().cny,
            'jpy': ParseCurrency().jpy,
            'krw': ParseCurrency().krw,
        }
    }
    return render(request, "Send.html", data)

def catalog(request):
    form = ApplicationForm()
    # Преобразование selected_brand в int
    selected_brand = request.GET.get('brand')
    try:
        selected_brand = int(selected_brand) if selected_brand else None
    except (ValueError, TypeError):
        selected_brand = None
    selected_model = request.GET.get('model')
    sort_field = request.GET.get('sort_field')
    sort_order = request.GET.get('sort_order', 'asc')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    mileage_min = request.GET.get('mileage_min')
    mileage_max = request.GET.get('mileage_max')
    engine_volume_min = request.GET.get('engine_volume_min')
    engine_volume_max = request.GET.get('engine_volume_max')
    selected_transmission = request.GET.get('transmission')
    selected_drive = request.GET.get('drive')
    selected_color = request.GET.get('color')
    try:
        selected_brand = int(selected_brand) if selected_brand else None
    except ValueError:
        selected_brand = None

    sort_mapping = {
        'mileage': 'mileage',
        'price': 'price',
        'engine_volume': 'engine_volume',
        'year': 'year'
    }

    models_queryset = Vehicle.objects.none()
    if selected_brand:
        models_queryset = Vehicle.objects.filter(
            brand_country_id=selected_brand
        ).values_list('model', flat=True).distinct().order_by('model')

    # Получение брендов
    brands = Brand.objects.order_by('brand')

    # Получение моделей только для выбранного бренда
    models = Vehicle.objects.all()
    if selected_brand:
        models = models.filter(brand_country_id=selected_brand)
    models = models.values_list('model', flat=True).distinct().order_by('model')

    # Get unique transmission types
    transmissions = Vehicle.objects.values_list('transmission', flat=True).distinct().order_by('transmission')

    # Get unique drive types
    drives = Vehicle.objects.values_list('drive', flat=True).distinct().order_by('drive')

    # Get unique colors
    colors = Vehicle.objects.values_list('color', flat=True).distinct().order_by('color')

    # Apply filters
    vehicles = Vehicle.objects.all()
    if selected_brand:
        vehicles = vehicles.filter(brand_country_id=selected_brand)
    if selected_model := request.GET.get('model'):
        vehicles = vehicles.filter(model=selected_model)
    if year_min:
        vehicles = vehicles.filter(year__gte=year_min)
    if year_max:
        vehicles = vehicles.filter(year__lte=year_max)
    if mileage_min:
        vehicles = vehicles.filter(mileage__gte=mileage_min)
    if mileage_max:
        vehicles = vehicles.filter(mileage__lte=mileage_max)
    if engine_volume_min:
        vehicles = vehicles.filter(engine_volume__gte=engine_volume_min)
    if engine_volume_max:
        vehicles = vehicles.filter(engine_volume__lte=engine_volume_max)
    if selected_transmission:
        vehicles = vehicles.filter(transmission=selected_transmission)
    if selected_drive:
        vehicles = vehicles.filter(drive=selected_drive)
    if selected_color:
        vehicles = vehicles.filter(color=selected_color)

    if sort_field in sort_mapping:
        field_name = sort_mapping[sort_field]
        if sort_order == 'desc':
            field_name = f'-{field_name}'
        vehicles = vehicles.order_by(field_name)
    else:
        # Сортировка по умолчанию если не выбрана
        vehicles = vehicles.order_by('-year')

    # Pagination
    paginator = CustomPaginator(vehicles, 16)  # Show 4 vehicles per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.page_range(page_obj, num_links=5)  # Adjust num_links as needed

    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    paginator = CustomPaginator(vehicles, 16)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.page_range(page_obj, num_links=5)
    # spisok_poshlin = []
    # for vehicle in Vehicle():
    #     print(spisok_poshlin.append(Poshlina(float(vehicle.price[-14:-2]), vehicle.engine_volume, vehicle.year)))
    # Calculate total price for each vehicle
    for vehicle in page_obj:
        vehicle.total_price = Poshlina(vehicle.price, vehicle.engine_volume, vehicle.year) + float(vehicle.price)
    context = {
        'form': form,
        'brands': Brand.objects.order_by('brand'),
        'models': models_queryset,
        'selected_brand': selected_brand,
        'selected_model': selected_model,
        'year_min': year_min,
        'year_max': year_max,
        'mileage_min': mileage_min,
        'mileage_max': mileage_max,
        'engine_volume_min': engine_volume_min,
        'engine_volume_max': engine_volume_max,
        'transmissions': transmissions,
        'selected_transmission': selected_transmission,
        'drives': drives,
        'selected_drive': selected_drive,
        'colors': colors,
        'selected_color': selected_color,
        'vehicles': page_obj,
        'sort_field': sort_field,
        'sort_order': sort_order,
        'get_params': get_params.urlencode(),
        'page_range': page_range,
        'page_obj': page_obj
    }
    return render(request, 'catalog.html', context)


def get_models(request):
    brand_id = request.GET.get('brand_id')
    if not brand_id or not Brand.objects.filter(id=brand_id).exists():
        return JsonResponse({'models': []})

    models = Vehicle.objects.filter(
        brand_country_id=brand_id
    ).values_list('model', flat=True).distinct().order_by('model')

    return JsonResponse({'models': list(models)})

from django.core.paginator import Paginator

class CustomPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def page_range(self, current_page, num_links=5):
        if current_page.number < 1 or current_page.number > self.num_pages:
            return []
        start = max(current_page.number - num_links // 2, 1)
        end = start + num_links
        if end > self.num_pages:
            end = self.num_pages
            start = end - num_links
            if start < 1:
                start = 1
        return list(range(start, end + 1))  # Include the end page

@require_POST
@csrf_exempt  # Для упрощения, лучше использовать CSRF правильно
def create_application(request):
    form = ApplicationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({
        'success': False,
        'errors': form.errors.as_json()
    }, status=400)

