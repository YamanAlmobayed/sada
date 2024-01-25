from django.db import models 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date
from rest_framework import serializers



def upload_to(instance, filename):
    return 'files/{filename}'.format(filename=filename)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        

class Account(models.Model):
    class AccountType(models.TextChoices):
        PARENT = 'Parent', _('Parent')
        EXPERT = 'Expert', _('Expert')

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='user')
    account_type = models.CharField(max_length=6, choices=AccountType.choices, default=AccountType.EXPERT)
    def __str__(self):
         return self.user.username
    
    


class WechslerQuestion(models.Model):
    question = models.TextField()
    score = models.CharField(max_length=10)
    hint = models.TextField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    test = models.ForeignKey('WechslerTest', on_delete=models.CASCADE, related_name='wechsler_qustions')
    image=models.ImageField(upload_to=upload_to,blank=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = "أسئلة ويكسلر"


class WechslerTest(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    errors_allowed = models.IntegerField(null=True, blank=True)
    general_test = models.ForeignKey('GeneralTest', on_delete=models.CASCADE, null=True, related_name='wechsler_general_test')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "اختبارات ويكسلر"
        
        
class WechslerScaledScore(models.Model):
    age=models.TextField()
    scaled_score=models.IntegerField()
    info_test=models.IntegerField(null=True,blank=True)
    compare_test=models.IntegerField(null=True,blank=True)
    math_test=models.IntegerField(null=True,blank=True)
    similarity_test=models.IntegerField(null=True,blank=True)
    understanding_test=models.IntegerField(null=True,blank=True)
    complete_photo=models.IntegerField(null=True,blank=True)
    order_photo=models.IntegerField(null=True,blank=True)
    block_test=models.IntegerField(null=True,blank=True)
    collect_things=models.IntegerField(null=True,blank=True)
    maze_test=models.IntegerField(null=True,blank=True)

    class Meta:
             verbose_name_plural = "تثقيل اختبارات وكسلر"

    
    
class WechslerChild(models.Model):
    child = models.ForeignKey('ChildPersonalInfo', on_delete=models.CASCADE, related_name='Wechsler_test', null=True, blank=True)
    vrebal_scal=models.IntegerField(default=0)
    practical_scale=models.IntegerField(default=0)
    IQ=models.IntegerField(default=0)
    diagnose=models.TextField(null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    birthdate=models.DateField(null=True)
    range=models.CharField(editable=False,max_length=20)
    treatment_suggestion=models.TextField(null=True,blank=True)
    age=models.IntegerField(null=True,blank=True,editable=False)


    def __str__(self):
        return f'{self.child} | {self.id}'
    
    class Meta:
        verbose_name_plural = "طفل وكسلر"
        ordering=['-date']
    
    @property
    def get_age(self):
             year= relativedelta(datetime.now(), self.birthdate).years*12
             month= relativedelta(datetime.now(), self.birthdate).months
             print(year+month)
             return (year+month)


         

    @property
    def get_range(self):
        if type(self.birthdate) is str:
            birthdate = datetime.strptime(self.birthdate, '%Y-%m-%d').date()
            return relativedelta(datetime.now(), birthdate).years*12
        else:
             year= relativedelta(datetime.now(), self.birthdate).years*12
             month= relativedelta(datetime.now(), self.birthdate).months
             x=year+month
             if x in range (88,91):
                  return '7-4/7-7'
             elif x in range (180,183):
                  return '15/15-3'
             elif x in range (184,187):
                  return '15-4/15-7'
             elif x in range (188,191):
                  return '15-8/15-11'
             elif x in range (168,171):
                  return '14/14-3'
             elif x in range (172,175):
                  return '14-4/14-7'
             elif x in range (176,179):
                  return '14-8/14-11'
             elif x in range (156,159):
                  return '13/13-3'
             elif x in range (162,165):
                  return '13-4/13-7'
             elif x in range (168,171):
                  return '13-8/13-11'
             elif x in range (144,147):
                  return '12/12-3'
             elif x in range (148,151):
                  return '12-4/12-7'
             elif x in range (152,155):
                  return '12-8/12-11'
             else:
                  return 'None'


            

    
    
    def save(self, *args, **kwargs):
          self.range = self.get_range
          self.age=self.get_age
          super(WechslerChild, self).save(*args, **kwargs)

class PortageQuestion(models.Model):
    question = models.TextField()
    score = models.CharField(max_length=10)
    block = models.ForeignKey('PortageBlock', on_delete=models.CASCADE, related_name='portage_qustions',blank=True,null=True)
    
    def __str__(self):
        return  f"{self.question}"
    
    class Meta:
        verbose_name_plural = "أسئلة بورتيج"
    
        
class PortageBlock(models.Model):
    basal_age = models.IntegerField()
    test = models.ForeignKey('PortageTest', on_delete=models.CASCADE, related_name='blocks')
    
    def __str__(self):
        return f"Test: {self.test.name} | Basal age: {self.basal_age}"
    
    class Meta:
        verbose_name_plural = "بلوكات بورتيج"
    
    
class PortageTest(models.Model):
    name = models.TextField(null=True, blank=True)
    general_test = models.ForeignKey('GeneralTest', on_delete=models.CASCADE, null=True, related_name='protage_general_test')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "اختبارات بورتيج"
    
    
class PortageChildTest(models.Model):
    date = models.DateField(auto_now_add=True)
    diagnose = models.TextField(null=True, blank=True)
    treatment_suggestion = models.TextField(null=True, blank=True)
    test_name = models.ForeignKey(PortageTest, on_delete=models.CASCADE, related_name="portage_test")
    child_name = models.ForeignKey('ChildPersonalInfo', on_delete=models.CASCADE, related_name="portage_results")
    age = models.IntegerField()

    
    class Meta:
        verbose_name_plural = "نتائج اختبارات بورتيج"
        
    def __str__(self):
        return  f"ChildID: {self.child_name.id} | Child Name: {self.child_name.full_name} | Test: {self.test_name.name} | Level: {self.diagnose}"
    
class NonAsweredPortageQuestion(models.Model):
    child_name = models.ForeignKey('ChildPersonalInfo', on_delete=models.CASCADE, related_name="child_non_aswered_question")
    test_name = models.ForeignKey(PortageChildTest, on_delete=models.CASCADE, related_name="non_aswered_question_test")
    question = models.ForeignKey(PortageQuestion, on_delete=models.CASCADE, related_name="non_aswered_question")


class GeneralTest(models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "الاختبارات العامة"
        
    
class ChildPersonalInfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50, editable=False, unique=True, null=True)
    birthdate = models.DateField()
    age_in_years = models.IntegerField(editable=False)
    age_in_months = models.IntegerField(editable=False)
    age_in_days = models.IntegerField(editable=False)
    child_class = models.CharField(max_length=20, null=True, blank=True)
    current_school = models.CharField(max_length=70, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    transferring_party = models.CharField(max_length=50, null=True, blank=True)
    supervised_doctor = models.CharField(max_length=50, null=True, blank=True)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    father_education = models.TextField()
    mother_education = models.TextField()
    father_work = models.TextField()
    mother_work = models.TextField()
    parent = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    
    
    def __str__(self):
        return f'{self.full_name} || {self.id}'
    
    class Meta:
        verbose_name_plural = "الاطفال"
    
    @property
    def get_age_in_years(self):
        if type(self.birthdate) is str:
            birthdate = datetime.strptime(self.birthdate, '%Y-%m-%d').date()
            return relativedelta(datetime.now(), birthdate).years
        else:
            return relativedelta(datetime.now(), self.birthdate).years
        
    @property
    def get_age_in_months(self):
        if type(self.birthdate) is str:
            birthdate = datetime.strptime(self.birthdate, '%Y-%m-%d').date()
            years = (relativedelta(datetime.now(), birthdate).years * 12)
            return years + relativedelta(datetime.now(), birthdate).months
        else:
            years = (relativedelta(datetime.now(), self.birthdate).years * 12)
            return years + relativedelta(datetime.now(), self.birthdate).months
        
    @property
    def get_age_in_days(self):
        if type(self.birthdate) is str:
            birthdate = datetime.strptime(self.birthdate, '%Y-%m-%d').date()
            years = (relativedelta(datetime.now(), birthdate).years * 12) * 30
            months = (relativedelta(datetime.now(), birthdate).months * 30)
            return relativedelta(datetime.now(), birthdate).days + years + months
        else:
            years = (relativedelta(datetime.now(), self.birthdate).years * 12) * 30
            months = (relativedelta(datetime.now(), self.birthdate).months * 30)
            return relativedelta(datetime.now(), self.birthdate).days + years + months
    
    @property
    def get_full_name(self):
         fullname = self.first_name + " " + self.father_name + " " + self.last_name
         return fullname

    def save(self, *args, **kwargs):
            self.age_in_days = self.get_age_in_days
            self.age_in_months = self.get_age_in_months
            self.age_in_years = self.get_age_in_years
            self.full_name = self.get_full_name
            super(ChildPersonalInfo, self).save(*args, **kwargs)
     
          
class ChildInfoQuestion(models.Model):
    qustion = models.TextField()
    block = models.ForeignKey('ChildInfoBlock', on_delete=models.SET_NULL, related_name="block_qustions", null=True)
    
    def __str__(self):
        return f'{self.qustion} | {self.id}'
    
    class Meta:
        verbose_name_plural = "أسئلة معلومات الطفل"
    
    
class ChildInfoBlock(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} | {self.id}" 
    
    class Meta:
        verbose_name_plural = "بلوكات معلومات الطفل"
    
    
class ChildInfoAnswer(models.Model):
    child_id = models.ForeignKey(ChildPersonalInfo, on_delete=models.SET_NULL, related_name="child_id", null=True)
    qustion_id = models.ForeignKey(ChildInfoQuestion, on_delete=models.SET_NULL, related_name="qustion_id", null=True)
    answer = models.TextField(null=True, blank=True)    
    
    class Meta:
        verbose_name_plural = "معلومات الطفل" 
        
    def __str__(self):
        return f'Child_ID: {self.child_id.full_name} | Question {self.qustion_id.qustion}'
    
    
class ParentsQuestion(models.Model):
    question = models.TextField()
    score = models.CharField(max_length=10)
    block = models.ForeignKey('ParentsBlock', on_delete=models.CASCADE, related_name='parents_qustions')
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = "أسئلة الأهل"
    
        
class ParentsBlock(models.Model):
    age_range = models.CharField(max_length=50)
    test = models.ForeignKey('ParentsTest', on_delete=models.CASCADE, related_name='blocks')
    age = models.IntegerField(editable=False)
    
    def __str__(self):
        return str(self.age_range) 
    
    @property
    def get_age(self):
        return calculate_parents_test_age(age_range=self.age_range)
        
    def save(self, *args, **kwargs):
          self.age = self.get_age
          super(ParentsBlock, self).save(*args, **kwargs)
          
    class Meta:
        verbose_name_plural = "بلوكات اختبار الاهل"
    
        
def calculate_parents_test_age(birthdate = None, age_range =None):
    age = None
    if birthdate is not None:    
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        age = relativedelta(datetime.now(), birthdate)
        if (age.minutes < 0):
            raise serializers.ValidationError({"Error":"Invalid age"})
        age = int((((age.months) + (age.years * 12)) * 4) + (age.days/7))
    if age in range(0,3) or age_range == 'من الولادة و حتى 3 اسابيع':
        return 0
    elif age in range(3,12) or age_range == 'من 3 اسابيع و حتى 3 اشهر':
            return 3
    elif age in range(12,24) or age_range == 'من 3 اشهر حتى 6 اشهر':
            return 12
    elif age in range(24,48) or age_range == 'من 6 اشهر حتى سنة':
            return 24
    elif age in range(48,72) or age_range == 'من سنة الى سنة و نصف':
            return 48
    elif age in range(72,96) or age_range == 'من سنة و نصف حتى سنتين':
            return 72
    elif age in range(96,144) or age_range == 'من سنتين حتى 3 سنوات':
            return 96
    elif age in range(144,192) or age_range == 'من 3 سنوات حتى 4 سنوات':
            return 144
    elif age in range(192,240) or age_range == 'من 4 سنوات حتى 5 سنوات':
            return 192
    elif age >= 240 or age_range == 'من 5 سنوات حتى 6 سنوات':
            return 240


    
class ParentsTest(models.Model):
    name = models.TextField(null=True, blank=True)
    general_test = models.ForeignKey(GeneralTest, on_delete=models.CASCADE, null=True, related_name='parents_general_test')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "اختبارات الأهل" 


class LddrsQuestion(models.Model):
    test_name=models.CharField(max_length=50,null=True)
    question=models.TextField()


    def __str__(self):
        return self.question
    class Meta:

        verbose_name_plural = "اسئلة مقاييس التقدير التشخيصية"


class LddrsChild(models.Model):
    test=models.CharField(max_length=50)
    child=models.ForeignKey(ChildPersonalInfo,on_delete=models.CASCADE)
    diagnose=models.TextField()
    date=models.DateField(auto_now_add=True)
    treatment_suggestion=models.TextField(null=True,blank=True)
    age=models.IntegerField(null=True)

    def __str__(self):
        return self.child.full_name

    class Meta:
        ordering=['date']
        verbose_name_plural = "نتائج مقاييس التقدير التشخيصية"
    



class Event(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    date = models.DateTimeField()


class AutismAnswer(models.Model):
     answer=models.TextField()
     score=models.IntegerField()
     def __str__(self):
          return f'{self.answer}| {self.score}'


class AutismQuestion(models.Model):
     age=models.CharField(max_length=20)
     question=models.TextField()
     answer=models.ManyToManyField(AutismAnswer,blank=True)

     
class DyslexiaQuestion(models.Model):
    question = models.TextField()
    record = models.FileField(upload_to=upload_to, blank=True, null=True)
    hint = models.CharField(max_length=50)

    

class DyslexiaQuestionAnswers(models.Model):
    answer = models.CharField(max_length=50)
    score = models.CharField(max_length=20)
    question = models.ForeignKey(DyslexiaQuestion, blank=True, null=True, on_delete=models.SET_NULL, related_name='dyslexia_answers')
    
    def __str__(self) -> str:
         return self.answer
    
class DyslexiaQuestionImages(models.Model):
    image = models.ImageField(upload_to=upload_to)
    question = models.ForeignKey(DyslexiaQuestion, blank=True, null=True, on_delete=models.SET_NULL, related_name='dyslexia_images')
    
    
class RavnQuestion(models.Model):
    question_image = models.ImageField(upload_to=upload_to)
    group = models.ForeignKey('RavnGroup', on_delete=models.SET_NULL,  blank=True, null=True, related_name = "questions")


class RavnQuestionImages(models.Model):
    image = models.ImageField(upload_to=upload_to)
    question = models.ForeignKey(RavnQuestion, blank=True, null=True, on_delete=models.SET_NULL, related_name='asnwers')
    score = models.CharField(max_length= 20)

class RavnGroup(models.Model):
    name = models.CharField(max_length=10)
    