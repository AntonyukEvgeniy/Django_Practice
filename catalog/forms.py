from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "purchase_price","owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            if field_name == "description":
                field.widget.attrs["rows"] = 3

    def clean(self):
        cleaned_data = super().clean()
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]

        name = cleaned_data.get("name", "").lower()
        description = cleaned_data.get("description", "").lower()
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

    def clean_purchase_price(self):
        price = self.cleaned_data.get("purchase_price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price
