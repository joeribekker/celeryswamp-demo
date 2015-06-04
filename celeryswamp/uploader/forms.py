from django import forms


class UploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        data = self.cleaned_data['file']

        if not data.name.endswith('.csv'):
            raise forms.ValidationError('Your file should be a CSV file.')

        return data
