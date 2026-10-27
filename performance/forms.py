from django import forms


NUMBER_INPUT_CLASS = "number-input"


class StudentPredictionForm(forms.Form):
    student_name = forms.CharField(
        label="Student Name",
        max_length=100,
        help_text="Use the name that should appear in saved records.",
        widget=forms.TextInput(attrs={"placeholder": "Enter student name"}),
    )
    attendance = forms.FloatField(
        label="Attendance (%)",
        min_value=0,
        max_value=100,
        help_text="Enter a percentage between 0 and 100.",
        widget=forms.NumberInput(
            attrs={"class": NUMBER_INPUT_CLASS, "placeholder": "Example: 82", "step": "0.1"}
        ),
    )
    study_hours = forms.FloatField(
        label="Study Hours per Day",
        min_value=0,
        max_value=24,
        help_text="Average daily study time outside class.",
        widget=forms.NumberInput(
            attrs={"class": NUMBER_INPUT_CLASS, "placeholder": "Example: 4", "step": "0.1"}
        ),
    )
    previous_marks = forms.FloatField(
        label="Previous Marks (%)",
        min_value=0,
        max_value=100,
        help_text="Previous exam or semester percentage.",
        widget=forms.NumberInput(
            attrs={"class": NUMBER_INPUT_CLASS, "placeholder": "Example: 74", "step": "0.1"}
        ),
    )
    assignment_score = forms.FloatField(
        label="Assignment Score (%)",
        min_value=0,
        max_value=100,
        help_text="Current assignment or coursework percentage.",
        widget=forms.NumberInput(
            attrs={"class": NUMBER_INPUT_CLASS, "placeholder": "Example: 80", "step": "0.1"}
        ),
    )
    sleep_hours = forms.FloatField(
        label="Sleep Hours per Day",
        min_value=0,
        max_value=24,
        help_text="Average daily sleep hours.",
        widget=forms.NumberInput(
            attrs={"class": NUMBER_INPUT_CLASS, "placeholder": "Example: 7", "step": "0.1"}
        ),
    )

    def clean_student_name(self):
        return self.cleaned_data["student_name"].strip()
