from datetime import timedelta

from django.contrib import admin
from django.utils.html import format_html

from rent_car.forms import CustomerForm
from rent_car.models import Reservation, TypeRate, Car, Extra, OfficeLocation, Customer, Availability


# Register your models here.
class AdminCustomer(admin.TabularInline):
    model = Customer
    extra = 1
    form = CustomerForm


class AdminReservation(admin.ModelAdmin):
    list_display = (
        'display_pickup_return_date', 'type_and_rate', 'display_car', 'get_total_price',
        'edit_button',
        'delete_button')

    inlines = [AdminCustomer]

    def display_pickup_return_date(self, obj):
        return f"{obj.pickup_date} - {obj.return_date}"

    display_pickup_return_date.short_description = 'Pickup/Return'

    def display_car(self, obj):
        return f"{obj.car.make} - {obj.car.registration_number}"

    display_car.short_description = 'Car'

    def get_total_price(self, obj):
        days = (obj.return_date - obj.pickup_date).days
        total_price = days * obj.type_and_rate.price_per_day
        return total_price

    get_total_price.short_description = 'Total Price'

    def edit_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/reservation/{obj.id}/change/">'
            f'Edit</a>')

    edit_button.allow_tags = True
    edit_button.short_description = 'Edit'

    def delete_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/reservation/{obj.id}/delete/">'
            f'Delete</a>')

    delete_button.allow_tags = True
    delete_button.short_description = 'Delete'


class AdminTypeRate(admin.ModelAdmin):
    list_display = ('display_image', 'type', 'display_model', 'get_number_of_cars', 'edit_button', 'delete_button')

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    display_image.short_description = 'Image'

    def display_model(self, obj):
        # passenger_icon = '<i class="fa fa-user"></i>'
        # bag_icon = '<i class="fa fa-suitcase"></i>'
        # car_icon = '<i class="fa fa-taxi"></i>'
        # set_icon = '<i class="fa fa-cog"></i>'
        return format_html(
            f"{obj.num_of_passenger} - {obj.piece_of_bag} - {obj.num_of_door} - "
            f"{obj.transmission}")

    display_model.short_description = 'Car Models'

    def get_number_of_cars(self, obj):
        cars_with_same_model = Car.objects.filter(type_and_rate=obj)
        count_of_cars = cars_with_same_model.count()
        return count_of_cars

    get_number_of_cars.short_description = 'Number of Cars'

    def edit_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/typerate/{obj.id}/change/">'
            f'Edit</a>')

    edit_button.allow_tags = True
    edit_button.short_description = 'Edit'

    def delete_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/typerate/{obj.id}/delete/">'
            f'Delete</a>')

    delete_button.allow_tags = True
    delete_button.short_description = 'Delete'


class AdminCar(admin.ModelAdmin):
    list_display = (
        'registration_number', 'make', 'model', 'office_location', 'type_and_rate', 'edit_button', 'delete_button')

    def edit_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/car/{obj.id}/change/">'
            f'Edit</a>')

    edit_button.allow_tags = True
    edit_button.short_description = 'Edit'

    def delete_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/car/{obj.id}/delete/">'
            f'Delete</a>')

    delete_button.allow_tags = True
    delete_button.short_description = 'Delete'


class AdminLocation(admin.ModelAdmin):
    list_display = ('name', 'address', 'get_available_cars', 'edit_button', 'delete_button')

    def get_available_cars(self, obj):
        car = TypeRate.objects.all().count()
        return car

    get_available_cars.short_description = 'Available Cars'

    def edit_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/officelocation/{obj.id}/change/">'
            f'Edit</a>')

    edit_button.allow_tags = True
    edit_button.short_description = 'Edit'

    def delete_button(self, obj):
        return format_html(
            f'<a href="/admin/rent_car/officelocation/{obj.id}/delete/">'
            f'Delete</a>')

    delete_button.allow_tags = True
    delete_button.short_description = 'Delete'


class AdminAvailability(admin.ModelAdmin):
    list_display = ('pickup_date', 'return_date', 'type_and_rate', 'car', 'list_of_days')

    def list_of_days(self, obj):
        # Generate a list of all the dates between pickup_date and return_date
        days = [obj.pickup_date + timedelta(days=i) for i in range((obj.return_date - obj.pickup_date).days + 1)]
        day_names = []

        # Get the day name for each date and append it to the list
        for day in days:
            day_names.append(day.strftime('%A'))

        return ", ".join(f"{day} ({day_name})" for day, day_name in zip(days, day_names))

    list_of_days.short_description = 'List of Days'


admin.site.register(Reservation, AdminReservation)
admin.site.register(TypeRate, AdminTypeRate)
admin.site.register(Car, AdminCar)
admin.site.register(Extra)
admin.site.register(OfficeLocation, AdminLocation)
admin.site.register(Customer)
admin.site.register(Availability, AdminAvailability)
