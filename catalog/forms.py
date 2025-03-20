from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'purchase_price']

    def clean(self):
        cleaned_data = super().clean()
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа',
            'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]

        name = cleaned_data.get('name', '').lower()
        description = cleaned_data.get('description', '').lower()
        for word in forbidden_words:
            if word in name:
                raise forms.ValidationError(
                    f'Название не может содержать слово "{word}"'
                )
            if word in description:
                raise forms.ValidationError(
                    f'Описание не может содержать слово "{word}"'
                )
        return cleaned_data