from django.db import models
from apps.account.models import City, Account, Company


class JOBCategory(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class JobType(models.Model):
    title = models.CharField(max_length=235)

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=225)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    working_days = models.IntegerField()
    salary = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.ForeignKey(JOBCategory, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    type = models.ManyToManyField(JobType)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ApplyJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)


class LikedJobs(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return self.job
