from django import forms

from rent_car.models import OfficeLocation, Customer

pickup_choices = [(office_location.name, office_location.name.capitalize()) for office_location in
                  OfficeLocation.objects.all()]


class StepOneForm(forms.Form):
    pickup_date = forms.DateField()
    return_date = forms.DateField()
    pickup_time = forms.CharField(max_length=250)
    return_time = forms.CharField(max_length=250)
    pickup_location = forms.ChoiceField(choices=pickup_choices)
    return_location = forms.ChoiceField(choices=pickup_choices)

    def __init__(self, *args, **kwargs):
        super(StepOneForm, self).__init__(*args, **kwargs)
        self.fields['pickup_date'].widget.attrs["class"] = "form-control datepicker"
        self.fields['pickup_date'].widget.attrs["required"] = True
        self.fields['return_date'].widget.attrs["class"] = "form-control datepicker"
        self.fields['return_date'].widget.attrs["required"] = True
        self.fields['pickup_time'].widget.attrs["class"] = "form-control timepicker"
        self.fields['pickup_time'].widget.attrs["required"] = True
        self.fields['return_time'].widget.attrs["class"] = "form-control timepicker"
        self.fields['return_time'].widget.attrs["required"] = True
        self.fields['pickup_location'].widget.attrs["class"] = "form-select"
        self.fields['return_location'].widget.attrs["class"] = "form-select"
        self.fields['return_location'].widget.attrs["disabled"] = True


class StepTwoForm(forms.Form):
    car_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(StepTwoForm, self).__init__(*args, **kwargs)
        self.fields['car_id'].widget.attrs["type"] = "hidden"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def has_changed(self):
        return True


class CustomersForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    payment = forms.ChoiceField(
        choices=[
            ('Card', 'Card'),
            ('Cash', 'Cash'),
        ],
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(CustomersForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs["class"] = "form-control"
        self.fields['email'].widget.attrs["class"] = "form-control"
        self.fields['phone_number'].widget.attrs["class"] = "form-control"
        self.fields['payment'].widget.attrs["class"] = "form-select"
