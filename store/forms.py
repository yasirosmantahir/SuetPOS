from django import forms
from .models import Product , ProductDetail ,Category

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            field = self.fields[f]
            field.widget.attrs['class'] = 'form-control'

            if (f == "category"):
                field.widget.attrs['onchange'] = 'categoryChanged(this);'

    class Meta:
        model = Product
        exclude=['is_active', 'created_at' , 'updated_at']

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Category
        exclude=['created_at' , 'updated_at']

class ProductDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductDetailForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductDetail
        exclude=['created_at' , 'updated_at']
