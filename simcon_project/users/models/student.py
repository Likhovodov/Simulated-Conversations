from django.db import models
from .custom_user import CustomUser
from .subject_label import SubjectLabel
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
#from django.contrib.sites.models import Site


class Student(CustomUser):
    added_by = models.ForeignKey('users.Researcher', default=0, related_name='students', on_delete=models.CASCADE)

    def save(self):
        super(Student, self).save()
        self.set_unusable_password()

        # adds a student to the "All Students" label
        label = SubjectLabel.objects.get(label_name="All Students", researcher=self.added_by)
        print(self)
        user = Student.objects.get(email=self)
        #print(self.objects)
        label.students.add(user)

        #curr_site = Site.objects.get_current()
        #current_site = curr_site.domain
        # collects the current domain of the website and the users uid
        current_site = get_current_site(user.request)
        site = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # creates the subject and message content for the emails
        subject = 'Activate your Simulated Conversations account'
        message = 'Hi, \nPlease register here: \nhttp://' + site + '/student/register/' \
                  + uid + '\n'

        # sends the email
        send_mail(subject, message, 'simulated.conversation@mail.com', [user.email], fail_silently=False)
