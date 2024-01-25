from rest_framework import serializers
from .. import models
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HelloWOrld():
    def __init__(self) -> None:
        pass

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ('__all__' )

class WechslerQustionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WechslerQuestion
        exclude = ['test',]


class WechslerTestSerializer(serializers.ModelSerializer):
    wechsler_qustions = WechslerQustionSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.WechslerTest
        exclude = ['general_test',]
        depth = 1


class GeneralTestSerializer(serializers.ModelSerializer):
    wechsler_general_test = WechslerTestSerializer(many=True, read_only=True)
    
    class Meta:
        fields = ('__all__')
        model = models.GeneralTest
        

class WechslerChildSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['child','id',]
        model = models.WechslerChild


class AddWechslerChildSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['vrebal_scal','practical_scale','IQ','diagnose',]
        model = models.WechslerChild


class PortageQustionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PortageQuestion
        exclude = ['block',]


class PortageBlockSerializer(serializers.ModelSerializer):
    portage_qustions = PortageQustionSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.PortageBlock
        exclude = ['test',]


class PortageTestSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()
    
    def get_blocks(self, instance):
        birthdate = self.context['view'].request.query_params['birthdate']
        test_type = self.context['view'].request.query_params['test-type']
        age = calculate_basal_age(birthdate, test_type)
        print(age)
        queryset = models.PortageBlock.objects.filter(basal_age__lte=age, test__name = test_type).order_by('-basal_age')
        return PortageBlockSerializer(queryset, many=True, read_only=True).data
    
    class Meta:
        model = models.PortageTest
        exclude = ['general_test',] 
        depth = 1

def calculate_basal_age(birthdate, test_type):
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        age = relativedelta(datetime.now(), birthdate)
        if (age.minutes < 0):
            raise serializers.ValidationError({"Error":"Invalid age"})
        age = age.months + (age.years * 12)
        if age in range(0,7):
            return 6
        elif age in range(7,13):
            return 12
        elif age in range(13,19):
            return 18
        elif age in range(19,25):
            return 24
        elif age in range(25,31):
            return 30
        elif age in range(31,37):
            return 36
        elif age in range(37,43):
            return 42
        elif age in range(43,49) and (test_type == 'اختبار البعد الاجتماعي' or 'اختبار البعد المعرفي'):##
            return 48##
        elif age in range(43,55) and (test_type == 'اختبار العناية بالذات' or 'اختبار البعد الحركي' or 'اختبار البعد الاتصالي'):
            return 54
        elif age in range(49,61) and (test_type == 'اختبار البعد الاجتماعي' or 'اختبار البعد المعرفي'):##
            return 60##
        elif age in range(55,67) and (test_type == 'اختبار العناية بالذات' or 'اختبار البعد الحركي' or 'اختبار البعد الاتصالي'):
            return 66
        elif age in range(61,73) and (test_type == 'اختبار البعد الاجتماعي' or 'اختبار البعد المعرفي'):##
            return 72##
        elif age in range(67,79) and (test_type == 'اختبار العناية بالذات' or 'اختبار البعد الحركي' or 'اختبار البعد الاتصالي'):
            return 78
        elif age in range(73,85) and (test_type == 'اختبار البعد الاجتماعي' or 'اختبار البعد المعرفي'):##
            return 84##
        elif age in range(79,91) and (test_type == 'اختبار العناية بالذات' or 'اختبار البعد الحركي' or 'اختبار البعد الاتصالي'):
            return 90
        elif age in range(85,97) and (test_type == 'اختبار البعد الاجتماعي' or 'اختبار البعد المعرفي'):##
            return 96##
        elif age in range(91,103) and (test_type == 'اختبار العناية بالذات' or 'اختبار البعد الحركي' or 'اختبار البعد الاتصالي'):
            return 102
        elif age >= 97 and (test_type == 'اختبار البعد الاجتماعي' or 'اختبار البعد المعرفي'):##
            return 108##
        elif age >= 103 and (test_type == 'اختبار العناية بالذات' or 'اختبار البعد الحركي' or 'اختبار البعد الاتصالي'):
            return 114
        
        
class PortageChildsTestsSerializer(serializers.ModelSerializer):
    child_name = serializers.StringRelatedField()
    test_name = serializers.StringRelatedField()
    non_aswered_questions = serializers.SerializerMethodField()
    
    def get_non_aswered_questions(self, instance):
        questions = models.NonAsweredPortageQuestion.objects.filter(child_name = instance.child_name, test_name = instance)
        non_answered_questions = NonAnswerdPortageQuestionSerializer(questions, many = True,  read_only=True).data
        queryset = []
        for question in non_answered_questions:
            queryset.append(question['question'])
        return queryset
    
    class Meta:
        model = models.PortageChildTest
        fields = ('__all__')
        depth = 1
        
        
class NonAnswerdPortageQuestionSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    
    class Meta:
        model = models.NonAsweredPortageQuestion
        exclude = ['id', 'test_name', 'child_name']   
        
class PortageChildTestsSerializer(serializers.ModelSerializer):
    test_name = serializers.StringRelatedField()
    child_name = serializers.StringRelatedField()
    non_aswered_questions = serializers.SerializerMethodField()
    
    def get_non_aswered_questions(self, instance):
        questions = models.NonAsweredPortageQuestion.objects.filter(child_name = instance.child_name, test_name = instance)
        non_answered_questions = NonAnswerdPortageQuestionSerializer(questions, many = True,  read_only=True).data
        queryset = []
        for question in non_answered_questions:
            queryset.append(question['question'])
        return queryset
        
        
    class Meta:
        model = models.PortageChildTest
        fields = ('__all__')
        depth = 1
        
        
class ChildInfoAnswerSerializer(serializers.ModelSerializer):
    qustion_id = serializers.StringRelatedField()
    
    class Meta:
        model = models.ChildInfoAnswer
        exclude = ['child_id',]


def get_portage_queryset_for_single_test(test_name, child):
    query = models.PortageChildTest.objects.filter(child_name=child, test_name__name = test_name)
    if query.exists():
        query_result = query.order_by('-id')[:2]
        if query_result[:1].exists():
            queryset = PortageChildTestsSerializer(query_result, many = True, read_only=True).data
    return queryset

def get_child_info_queryset(info_title, child_id):
    block = models.ChildInfoBlock.objects.get(name=info_title)
    child_answers = models.ChildInfoAnswer.objects.filter(child_id=child_id, qustion_id__block = block)
    queryset = ChildInfoAnswerSerializer(child_answers, many = True,  read_only=True).data
    return queryset

def get_lddrs_queryset(child_name, test_name):
        child = models.ChildPersonalInfo.objects.get(full_name=child_name)
        diagnose=models.LddrsChild.objects.filter(child=child,test=test_name)
        diagnose=diagnose.order_by('-id')[:2]
        if diagnose[:1].exists():
            diagnose_query=LddrsSerializers(diagnose,read_only=True,many=True).data
            return diagnose_query

class ChildPersonalInfoSerializer(serializers.ModelSerializer):
    family_history = serializers.SerializerMethodField()
    social_histoy = serializers.SerializerMethodField()
    medical_history = serializers.SerializerMethodField()
    pregnancy = serializers.SerializerMethodField()
    portage_results = serializers.SerializerMethodField()
    Wechsler_test=serializers.SerializerMethodField()
    Lddrs_listening=serializers.SerializerMethodField()
    Lddrs_writing=serializers.SerializerMethodField()
    Lddrs_seeing=serializers.SerializerMethodField()
    Lddrs_memory=serializers.SerializerMethodField()
    Lddrs_reading=serializers.SerializerMethodField()
    Lddrs_moving=serializers.SerializerMethodField()
    Lddrs_social=serializers.SerializerMethodField()
    Lddrs_attention=serializers.SerializerMethodField()
    Lddrs_math=serializers.SerializerMethodField()

    def get_family_history(self, instance):
        return get_child_info_queryset("تاريخ العائلة", instance.id)
    
    def get_pregnancy(self, instance):
        return get_child_info_queryset("الحمل", instance.id)
    
    def get_social_histoy(self, instance):
        return get_child_info_queryset("التاريخ الاجتماعي و السلوكي", instance.id)
    
    def get_medical_history(self, instance):
        return get_child_info_queryset("التاريخ الطبي", instance.id)
    
    def get_portage_results(self, instance):
        fullname = instance.full_name
        child = models.ChildPersonalInfo.objects.get(full_name=fullname)
        queryset = []
        queryset.append( get_portage_queryset_for_single_test('اختبار البعد الاجتماعي', child))
        queryset.append( get_portage_queryset_for_single_test('اختبار البعد المعرفي', child))
        queryset.append( get_portage_queryset_for_single_test('اختبار البعد الاتصالي', child))
        queryset.append( get_portage_queryset_for_single_test('اختبار البعد الحركي', child))
        queryset.append( get_portage_queryset_for_single_test('اختبار العناية بالذات', child))
        return queryset
    
    def get_Lddrs_listening(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات الاستماع')
    
    def get_Lddrs_writing(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات الكتابة')     
    
    def get_Lddrs_seeing(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات الإدراك البصري')

    def get_Lddrs_memory(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات الذاكرة')

    def get_Lddrs_reading(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات القراءة')        

    def get_Lddrs_moving(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات الإدراك الحركي')

    def get_Lddrs_social(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات السلوك الاجتماعي و الانفعالي')
    
    def get_Lddrs_attention(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات الانتباه')
    
    def get_Lddrs_math(self,instance):
        fullname = instance.full_name
        return get_lddrs_queryset(fullname, 'صعوبات تعلم الرياضيات')
                
    def get_Wechsler_test(self,instance):
        fullname = instance.full_name
        child = models.ChildPersonalInfo.objects.get(full_name=fullname)
        diagnose=models.WechslerChild.objects.filter(child=child)
        diagnose=diagnose.exclude(IQ=0)
        diagnose=diagnose.order_by('-id')[:2]
        
        if diagnose[:1].exists():
            query_set=WechslerChildSerializer(diagnose,read_only=True,many=True).data
            return query_set

    class Meta:
        model = models.ChildPersonalInfo
        exclude = ['parent',]
        

class ChildInfoQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChildInfoQuestion
        exclude = ['block',]


class ChildInfoBlockSerializer(serializers.ModelSerializer):
    block_qustions = ChildInfoQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ChildInfoBlock
        fields = ('__all__')
        
        
class ParentsQustionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ParentsQuestion
        exclude = ['block',]


class ParentsBlockSerializer(serializers.ModelSerializer):
    parents_qustions = ParentsQustionSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ParentsBlock
        exclude = ['test', 'age']


class ParentsTestSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()
    
    def get_blocks(self, instance):
        birthdate = self.context['view'].request.query_params['birthdate']
        age = models.calculate_parents_test_age(birthdate=birthdate)
        queryset = models.ParentsBlock.objects.filter(age__lte=age).order_by('-age')
        return ParentsBlockSerializer(queryset, many=True, read_only=True).data

    class Meta:
        model = models.ParentsTest
        exclude = ['general_test',]
        depth = 1
        
        
class ChildWechslerTest(serializers.ModelSerializer):
        Wechsler_test=WechslerChildSerializer(many=True, read_only=True)
        class Meta:
            model= models.ChildPersonalInfo
            fields= ['Wechsler_test',]

class LddrsQuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.LddrsQuestion
        exclude=['test_name',]
        depth=1
        

class LddrsSerializers(serializers.ModelSerializer):
        class Meta:
            model= models.LddrsChild
            exclude= ['id','child',]
            

class EventSerializers(serializers.ModelSerializer):
        class Meta:
            model= models.Event
            fields= ('__all__')


class AutismSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AutismQuestion
        exclude = []
        depth=1

  
def get_full_url(path):
    """Get full url with respect to current scheme"""
    url = 'https://127.0.0.1:8000' + str(path)
    return url        
        
class DyslexiaQuestionAnswersSerializer(serializers.ModelSerializer):
        class Meta:
            model= models.DyslexiaQuestionAnswers
            exclude = ['question']
            

class DyslexiaQuestionImagesSerializer(serializers.ModelSerializer):
        image = serializers.SerializerMethodField()
        
        def get_image(self, instance):
            return get_full_url(instance.image.url)   
        
        class Meta:
            model= models.DyslexiaQuestionImages
            exclude = ['question']
            
            
class DyslexiaQuestionSerializer(serializers.ModelSerializer):
        dyslexia_answers = DyslexiaQuestionAnswersSerializer(many=True, read_only=True)
        dyslexia_images = DyslexiaQuestionImagesSerializer(many=True, read_only=True)
        record = serializers.SerializerMethodField()
        
        def get_record(self, instance):
            try:
                return get_full_url(instance.record.url) 
            except:
                return None
            
        class Meta:
            model= models.DyslexiaQuestion
            fields = ('__all__')
            
            
class RavnQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    
    def get_answers(self, instance):
        images = models.RavnQuestionImages.objects.filter(question = instance)
        images = RavnQuestionImagesSerializer(images, many=True, read_only=True).data
        return images
    
    class Meta:
            model= models.RavnQuestion
            exclude = ['group']
            

class RavnQuestionImagesSerializer(serializers.ModelSerializer):
        image = serializers.SerializerMethodField()
        
        def get_image(self, instance):
            return get_full_url(instance.image.url)   
        
        class Meta:
            model= models.RavnQuestionImages
            exclude = ['question']
            
class RavnGroupSerializer(serializers.ModelSerializer):
        questions = RavnQuestionSerializer(many = True, read_only = True)
        
        class Meta:
            model= models.RavnGroup
            fields = ('__all__')

