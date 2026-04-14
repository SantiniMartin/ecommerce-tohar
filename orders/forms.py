from django import forms

class CheckoutForm(forms.Form):
    # Datos de envío
    full_name = forms.CharField(max_length=100, label="Nombre Completo", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Pérez'}))
    address = forms.CharField(max_length=250, label="Dirección de Envío", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle Falsa 123'}))
    city = forms.CharField(max_length=100, label="Ciudad", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buenos Aires'}))
    zip_code = forms.CharField(max_length=20, label="Código Postal", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1000'}))
    
    # Datos de pago simulado
    card_number = forms.CharField(max_length=19, label="Número de Tarjeta", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 1234 5678'}))
    card_name = forms.CharField(max_length=100, label="Nombre en la Tarjeta", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'JUAN PEREZ'}))
    expiration_date = forms.CharField(max_length=5, label="Vencimiento", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AA'}))
    cvv = forms.CharField(max_length=4, label="CVV", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '123'}))
