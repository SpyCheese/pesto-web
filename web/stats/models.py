from django.db import models

class Season(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    order = models.IntegerField()
    class Meta:
        ordering = ['year', 'order']
        
    def __str__(self):
        return self.name

class Parallel(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    class Meta:
        ordering = ['last_name', 'first_name']
    def __str__(self):
        return self.last_name + ' ' + self.first_name
    # user_id = models.IntegerField(null=True)

class Participation(models.Model):
    user = models.ForeignKey('User', null=True)
    season = models.ForeignKey('Season', null=True)
    parallel = models.ForeignKey('Parallel', null=True)
    def __str__(self):
        return str(self.season) + ' ' + str(self.parallel)

class Contest(models.Model):
    name = models.CharField(max_length=50, null=True)
    contest_id = models.IntegerField(null=True)
    season = models.ForeignKey('Season', null=True)
    parallel = models.ForeignKey('Parallel', null=True)
    day = models.IntegerField(null=True)
    theme = models.ForeignKey('Theme', null=True)
    class Meta:
        ordering = ['day']
    def __str__(self):
        return self.name or ''
    
class Problem(models.Model):
    name = models.CharField(max_length=30, blank=True)
    contest = models.ForeignKey('Contest', null=True)
    theme = models.ForeignKey('Theme', null=True)
    def __str__(self):
        return self.name or ''

class Language(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Submit(models.Model):
    problem = models.ForeignKey('Problem', null=True)
    participation = models.ForeignKey('Participation', null=True)
    outcome = models.CharField(max_length=2, choices=(
        ('OK', 'OK'),
        ('CE', 'Compilation Error'),
        ('RT', 'Runtime Error'),
        ('TL', 'Time-Limit Exceeded'),
        ('PE', 'Presentation Error'),
        ('WA', 'Wrong Answer'),
        ('CF', 'Check Failed'),
        ('PT', 'Partial Solution'),
        ('AC', 'Accepted for Testing'),
        ('IG', 'Ignored'),
        ('DQ', 'Disqualified'),
        ('PD', 'Pending'),
        ('ML', 'Memory Limit Exceeded'),
        ('SE', 'Secutity Violation'),
        ('SV', 'Style Violation'),
        ('WT', 'Wall Time Limit Exceeded'),
        ('PR', 'Pending Review'),
        ('RJ', 'Rejected'),
        ('SK', 'Skipped')))
    lang = models.ForeignKey('Language', null=True)
    # submit_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)

class Theme(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
