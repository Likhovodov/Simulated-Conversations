from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Student, SubjectLabel, Researcher
import django_tables2 as tables
from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class NewStudentCreationForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        password1 = data["password1"]
        password2 = data["password2"]
        email = data["email"]

        if password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        if not Student.objects.filter(email=email, registered=False):
            if Student.objects.filter(email=email, registered=True):
                self.add_error('email', 'Account already created')
            else:
                self.add_error('email', 'Invalid email address, please enter the email address that'
                                        ' you received the email at.')
        return data


class StudentTable(tables.Table):
    class Meta:
        model = Student


class AddStudentForm(forms.Form):
    class Meta:
        model = Student
        fields = ['email']

class PassReset(forms.Form):
    email = forms.EmailField(max_length=254, required=True)


class LabelTable(tables.Table):
    class Meta:
        model = SubjectLabel


class AddToLabel(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Student email'}), label='')


class SendEmail(BSModalModelForm):
    student_email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Student email'}), label='')

    class Meta:
        model = Student
        fields = ('student_email',)

    def clean(self):
        data = self.cleaned_data
        email = data['student_email']
        if Student.objects.filter(email=email):
            self.add_error('student_email', 'Account already created')


"""
        if not (Student.objects.filter(email=email) and Researcher.objects.filter(email=email)):
            # creates a student with blank fist and last names, then the password is set to unusable
            first_name = ""
            last_name = ""
            password = ""

            user = Student.objects.create(email=email, first_name=first_name, last_name=last_name,
                                          password=password, added_by=added_by, )
            user.set_unusable_password()

            # adds a student to the "All Students" label
            label = SubjectLabel.objects.get(label_name="All Students", researcher=added_by)
            label.students.add(user)

            # collects the current domain of the website and the users uid
            current_site = get_current_site(self.request)
            site = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # creates the subject and message content for the emails
            subject = 'Activate your Simulated Conversations account'
            message = 'Hi, \nPlease register here: \nhttp://' + site + '/student/register/' \
                      + uid + '\n'

            # sends the email
            send_mail(subject, message, 'simulated.conversation@mail.com', [email], fail_silently=False)
            return True
        else:
            return False"""


class NewLabel(forms.Form):
    label_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Label name'}), label='')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UpdateTranscription(forms.Form):
    transcription = forms.CharField(help_text="Enter new transcription")


class NewResearcherCreationForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)


class AddResearcherForm(ModelForm):
    class Meta:
        model = Researcher
        fields = ('email',)
