from django import forms

class AddEmployeeForm(forms.Form):
    employeeEmail = forms.EmailField(
        label="Son Email "
    )
