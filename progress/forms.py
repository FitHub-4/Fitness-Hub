from django import forms
from exercises.models import ExerciseCompletion


class ExerciseCompletionForm(forms.ModelForm):
    class Meta:
        model = ExerciseCompletion
        fields = ('reps', 'hold_time_sec', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }

    def clean(self):
        cleaned_data = super().clean()
        reps = cleaned_data.get('reps')
        hold_time = cleaned_data.get('hold_time_sec')
        if not reps and not hold_time:
            raise forms.ValidationError('At least one of Reps or Hold Time must be provided.')
        return cleaned_data
