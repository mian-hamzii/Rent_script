from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rent_car.forms import StepOneForm, CustomersForm
from rent_car.models import Reservation, TypeRate, Car, OfficeLocation, Extra, Customer


# Create your views here.
class IndexView(View):

    def get(self, request):
        form = StepOneForm
        office_location = OfficeLocation.objects.all()
        return render(request, 'index.html', context={
            'office_location': office_location,
            'form': form
        })

    def post(self, request):
        # Process the submitted form
        form = StepOneForm(request.POST)
        sort_option = request.POST.get('sort', 'default')  # Default to ascending order

        if sort_option == 'price_asc':
            cars = TypeRate.objects.all().order_by('price_per_day')
        else:
            cars = TypeRate.objects.all().order_by('?')
        if form.is_valid():
            # Extract cleaned form data
            pickup_date = form.cleaned_data['pickup_date']
            return_date = form.cleaned_data['return_date']
            pickup_location = form.cleaned_data['pickup_location']
            return_location = form.cleaned_data['return_location']

            # Calculate the number of days between pickup and return dates
            days = (return_date - pickup_date).days + 1

            # Update session variables
            request.session.update({
                'pickup_date': pickup_date.strftime('%Y-%m-%d'),
                'pickup_time': form.cleaned_data['pickup_time'],
                'return_date': return_date.strftime('%Y-%m-%d'),
                'return_time': form.cleaned_data['return_time'],
                'pickup_location': pickup_location,
                'return_location': return_location,
                'days': days,
            })

            # Prepare data for rendering the template
            step_one_data = {
                'pickup_date': pickup_date.strftime('%Y-%m-%d'),
                'pickup_time': form.cleaned_data['pickup_time'],
                'return_date': return_date.strftime('%Y-%m-%d'),
                'return_time': form.cleaned_data['return_time'],
                'pickup_location': pickup_location,
                'return_location': return_location,
                'days': days,
            }

            # Fetch TypeRate objects
            type_rate = TypeRate.objects.all()

            # Render the template with the form data and TypeRate objects
            return render(request, 'car_list_form.html', context={
                'form_data': step_one_data,
                'cars': cars,
                # 'type_rate': type_rate,
                'sort_option': sort_option,
            })

    def total_days(self, pickup_date, return_date):
        # Calculate the total number of days between pickup and return dates
        return (return_date - pickup_date).days + 1


class TypeRateList(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # Process the submitted form
        form = CustomersForm(request.POST)
        car_id = request.POST.get('car_id')

        # Fetch Extra objects
        extra = Extra.objects.all()

        # Fetch Car information based on the selected car_id
        car = TypeRate.objects.filter(type_rate=car_id).first()

        # Calculate the total cost for the selected car
        day = car.price_per_day * request.session.get('days')
        sub_total = day

        # Prepare data for rendering the template
        step_two_data = {
            'pickup_date': request.session.get('pickup_date'),
            'pickup_time': request.session.get('pickup_time'),
            'return_date': request.session.get('return_date'),
            'return_time': request.session.get('return_time'),
            'pickup_location': request.session.get('pickup_location'),
            'return_location': request.session.get('return_location'),
            'name': request.session.get('name'),
            'email': request.session.get('email'),
            'number': request.session.get('phone_number'),
            'days': request.session.get('days'),
            'sub_total': request.session.get('sub_total'),
        }

        # Update session variables
        request.session.update({
            'car_id': car_id,
            'sub_total': sub_total,
            'day': day,
        })
        # Render the template with the data
        return render(request, 'detail.html', context={
            'car': car,
            'form_data': step_two_data,
            'extra': extra,
            'day': day,
            'sub_total': sub_total,
            'form': form,
            # 'cars': cars,

        })


class DetailExtra(View):

    def get(self, request, *args, **kwargs):
        extra_id = kwargs.get('extra_id')
        extra = Extra.objects.filter(id=extra_id).first()
        car = TypeRate.objects.filter(type_rate=request.session.get('car_id')).first()
        day = request.session.get('day')
        data = {
            'total': extra.price + day,
            'extra': extra.price,
            'days': request.session.get('days'),
            'price': car.price_per_day,
            'day': day
        }
        return render(request, 'receipt.html', context={'receipt_data': data})


class SaveData(View):
    def post(self, request):
        form = CustomersForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            number = form.cleaned_data['phone_number']
            payment = form.cleaned_data['payment']

            request.session.update({
                'name': name,
                'email': email,
                'number': number,
                'payment': payment,
            })

        pickup_date = request.session.get('pickup_date')
        return_date = request.session.get('return_date')
        pickup_location = OfficeLocation.objects.get(address=request.session.get('pickup_location'))
        return_location = OfficeLocation.objects.get(address=request.session.get('return_location'))
        payment = request.session.get('payment')
        car_id = request.session.get('car_id')
        name = request.session.get('name')
        email = request.session.get('email')
        number = request.session.get('number')
        # Create a new Reservation instance and populate it

        car = TypeRate.objects.filter(type_rate=car_id).first()
        reservation = Reservation(
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=pickup_location,
            return_location=return_location,
            payment=payment,
            car_id=car.id,
            type_and_rate=car,
            # Populate other fields as needed
        )

        # Save the reservation to the database
        reservation.save()

        customer = Customer(
            name=name,
            email=email,
            phone_number=number,
            reservation_id=reservation.id,
        )
        customer.save()

        return render(request, 'final_page.html', context={
            'form': form,
        })


class AdjustPrice(View):
    def post(self, request):
        sort_option = request.POST.get('sort_option', 'default')  # Default to ascending order

        if sort_option == 'price_desc':
            cars = TypeRate.objects.all().order_by('-price_per_day')
        elif sort_option == '/price':
            cars = TypeRate.objects.all().order_by('price_per_day')
        else:
            cars = TypeRate.objects.all()

        return render(request, 'low_to_high_price.html', context={
            'cars': cars,
            'sort_option': sort_option,
        })
