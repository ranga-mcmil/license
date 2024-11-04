from django import forms

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'val',
            'id': 'search-input01',

        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        phone_number = cl_data.get('phone_number')
        return phone_number

