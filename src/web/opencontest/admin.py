from django.contrib import admin

from opencontest.models import *

admin.site.register(Contest)
admin.site.register(Person)
admin.site.register(Problem)
admin.site.register(Result)
admin.site.register(SubmissionCase)
admin.site.register(Submission)
admin.site.register(TestCase)
