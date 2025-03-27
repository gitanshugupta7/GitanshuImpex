from django import forms
from .models import Inquiry

# Sample list of country codes (extend as needed)
COUNTRY_CODES = [
    ('+1', 'United States (+1)'),
    ('+44', 'United Kingdom (+44)'),
    ('+61', 'Australia (+61)'),
    ('+91', 'India (+91)'),
    ('+81', 'Japan (+81)'),
    ('+86', 'China (+86)'),
    ('+49', 'Germany (+49)'),
    ('+33', 'France (+33)'),
    ('+39', 'Italy (+39)'),
    ('+971', 'United Arab Emirates (+971)'),
    # ... add additional country codes as required ...
]

class InquiryForm(forms.ModelForm):
    country_code = forms.ChoiceField(
        choices=COUNTRY_CODES,
        initial='+91',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
 
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'country_code', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your Message'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Default EmailField validation occurs here.
        return email
    
    def save(self, commit=True):
        inquiry = super().save(commit=False)
        # Combine country code with phone
        country_code = self.cleaned_data.get('country_code')
        phone = self.cleaned_data.get('phone')
        inquiry.phone = f"{country_code} {phone}".strip()
        if commit:
            inquiry.save()
        return inquiry
