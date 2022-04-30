from django import forms

from .models import Post, EducationYear, SubjectTopic

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].queryset = EducationYear.objects.none()
        self.fields['topic'].queryset = SubjectTopic.objects.none()

        # define lits of years based on group (in POST or if there's an instance for update)
        if 'group' in self.data:
            try:
                group_id = int(self.data.get('group'))
                self.fields['year'].queryset = EducationYear.objects.filter(group_id=group_id).order_by('year')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['year'].queryset = self.instance.group.years.order_by('year')

        # define lits of years based on group (in POST or if there's an instance for update)
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['topic'].queryset = SubjectTopic.objects.filter(subject_id=subject_id).order_by('topic')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['topic'].queryset = self.instance.subject.topics.order_by('topic')

    class Meta:
        model = Post
        fields = ['title', 'group', 'year', 'subject', 'topic', 'draft', 'tags']
