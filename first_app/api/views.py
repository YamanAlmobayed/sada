import random
from .. import models
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import api_view, permission_classes
from . import serializers
from rest_framework.views import APIView
from rest_framework import status
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import check_password
from . import permissions
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import joblib
from django.core.exceptions import ObjectDoesNotExist
from random import randrange
import os



@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status.HTTP_200_OK)
    
class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if models.Account.objects.filter(user__username = username).exists():
            account = models.Account.objects.get(user__username = username)
        else: return Response({'message': 'Invalid username'})
        is_authinticated = check_password(password, account.user.password)
        if is_authinticated:
            token, created = Token.objects.get_or_create(user=account.user)
            childs = models.ChildPersonalInfo.objects.filter(parent = account) #parent may have more than one child
            if childs.exists():
                for child in childs:
                    child.save()
                childs = serializers.ChildPersonalInfoSerializer(childs, many = True).data
                return Response({
                        'Username': account.user.username,
                        'Account_type':account.account_type,
                        'Token':token.key,
                        'child':childs
                        })
            else: return Response({
                        'Username': account.user.username,
                        'Account_type':account.account_type,
                        'Token':token.key,
                        })
        else:  return Response({'message': 'Invalid password'})



        
        
@api_view(['POST',])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def create_parent_account_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    child_id = request.POST.get('child_id')
    user = models.User.objects.create(username = username)
    user.set_password(password)
    user.save()
    account = models.Account.objects.create(user = user, account_type = models.Account.AccountType.PARENT)
    child = models.ChildPersonalInfo.objects.get(id = child_id)
    child.parent = account
    child.save()
    return Response({"message":"Account Created Successfuly"}, status=status.HTTP_201_CREATED)


@api_view(['POST',])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def add_exciting_parent_view(request):
    username = request.POST.get('username')
    child_id = request.POST.get('child_id')
    parent = models.Account.objects.filter(user__username = username)
    child = models.ChildPersonalInfo.objects.get(id = child_id)
    if parent.exists():
        child.parent = parent[0]
        child.save()
        return Response({"message":"Parent added to child successfuly"}, status=status.HTTP_200_OK)
    else: return Response({"error":"Invalid parent name"}, status=status.HTTP_400_BAD_REQUEST)
         

class WechslerTestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.WechslerTestSerializer
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    
    def get_queryset(self):
        test_type = self.request.query_params['test-type']
        test = models.WechslerTest.objects.filter(name=test_type)
        return test
        
      

class WechslerScaleScore(APIView):
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        test=self.request.POST.get('test')
        score=self.request.POST.get('score')
        id=self.request.POST.get('id')
        if test == 'info_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,info_test=score)
                kid.vrebal_scal=x.scaled_score+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.vrebal_scal=randrange(10)+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done with randome values'})

        if test == 'similarity_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,similarity_test=score)
                kid.vrebal_scal=x.scaled_score+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.vrebal_scal=randrange(10)+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
            
        elif test == 'understanding_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,understanding_test=score)
                kid.vrebal_scal=x.scaled_score+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.vrebal_scal=randrange(10)+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
        
        elif test == 'compare_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,compare_test=score)
                kid.vrebal_scal=x.scaled_score+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.vrebal_scal=randrange(10)+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done with randome values'})


        
        elif test == 'math_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,math_test=score)
                kid.vrebal_scal=x.scaled_score+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.vrebal_scal=randrange(10)+kid.vrebal_scal
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
        
        elif test == 'complete_photo':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,complete_photo=score)
                kid.practical_scale=x.scaled_score+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.practical_scale=randrange(10)+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
        
        elif test == 'maze_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,maze_test=score)
                kid.practical_scale=x.scaled_score+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.practical_scale=randrange(10)+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
            
        
        elif test == 'collect_things':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,collect_things=score)
                kid.practical_scale=x.scaled_score+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.practical_scale=randrange(10)+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
        
        elif test == 'block_test':
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,block_test=score)
                kid.practical_scale=x.scaled_score+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.practical_scale=randrange(10)+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done with randome values'})
        else:
            try:
                kid=models.WechslerChild.objects.get(id=id)
                x= models.WechslerScaledScore.objects.get(age=kid.range,order_photo=score)
                kid.practical_scale=x.scaled_score+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done'})
            except ObjectDoesNotExist:
                kid=models.WechslerChild.objects.get(id=id)
                kid.practical_scale=randrange(10)+kid.practical_scale
                kid.save()
                return JsonResponse ({'status':'done with randome values'})


class WechslerDiagnose(APIView):
        permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
        def get(self, request, *args, **kwargs):
            vrebal_iq=0
            practi_iq=0
            id = self.request.headers.get('id')
            kid=models.WechslerChild.objects.get(id=id)
            if kid.vrebal_scal == 6:
                vrebal_iq=45
            elif kid.vrebal_scal ==7:
                vrebal_iq=46
            elif kid.vrebal_scal == 8:
                vrebal_iq=47
            elif kid.vrebal_scal ==9:
                vrebal_iq=48
            elif kid.vrebal_scal == 10:
                vrebal_iq=50
            elif kid.vrebal_scal ==11:
                vrebal_iq=51
            elif kid.vrebal_scal == 12:
                vrebal_iq=52
            elif kid.vrebal_scal ==13:
                vrebal_iq=53
            elif kid.vrebal_scal == 14:
                vrebal_iq=55
            elif kid.vrebal_scal ==15:
                vrebal_iq=56
            elif kid.vrebal_scal == 16:
                vrebal_iq=57
            elif kid.vrebal_scal ==17:
                vrebal_iq=58
            elif kid.vrebal_scal == 18:
                vrebal_iq=60
            elif kid.vrebal_scal ==19:
                vrebal_iq=51
            elif kid.vrebal_scal == 20:
                vrebal_iq=62
            elif kid.vrebal_scal ==21:
                vrebal_iq=63
            elif kid.vrebal_scal ==random.randint(26, 40):
                vrebal_iq=random.randint(70, 87)
            elif kid.vrebal_scal ==random.randint(41, 61):
                vrebal_iq=random.randint(87, 114)
            else:
                vrebal_iq=random.randint(114, 150)
####################
            if kid.practical_scale == 10:
                practi_iq=44
            elif kid.practical_scale ==11:
                practi_iq=46
            elif kid.practical_scale == 12:
                practi_iq=47
            elif kid.practical_scale ==13:
                practi_iq=48
            elif kid.practical_scale == 14:
                practi_iq=50
            elif kid.practical_scale ==15:
                practi_iq=51
            elif kid.practical_scale == 16:
                practi_iq=53
            elif kid.practical_scale ==17:
                practi_iq=54
            elif kid.practical_scale ==18:
                practi_iq=55
            elif kid.practical_scale == 19:
                practi_iq=57
            elif kid.practical_scale ==20:
                practi_iq=58
            elif kid.practical_scale == 21:
                practi_iq=60
            elif kid.practical_scale ==22:
                practi_iq=61
            elif kid.practical_scale == 23:
                practi_iq=62
            elif kid.practical_scale ==24:
                practi_iq=67
            elif kid.practical_scale ==25:
                practi_iq=69

            elif kid.practical_scale ==random.randint(26, 40):
                practi_iq=random.randint(67, 86)
            elif kid.practical_scale ==random.randint(41, 61):
                practi_iq=random.randint(87, 115)
            else:
                practi_iq=random.randint(114, 150)

            kid.IQ=(vrebal_iq+practi_iq)/2
            kid.IQ=int(round(kid.IQ))


            if kid.IQ in range(0,75):
                kid.diagnose='تاخر عقلي شديد'
            elif kid.IQ in range(76,125):
                kid.diagnose='بطء تعلم'
            elif kid.IQ in range(126,300):
                kid.diagnose='طبيعي'

            kid.save()
            return JsonResponse({"diagnose":kid.diagnose})
        
        
        def post(self, request, *args, **kwargs):
            id = self.request.headers.get('id')
            kid=models.WechslerChild.objects.get(id=id)
            treat=self.request.POST.get('suggestion')
            if treat is None:
                return Response({"message":"الحقل فارغ"})
            kid.treatment_suggestion=treat
            kid.save()
            return JsonResponse({'suggestion':treat})

        


class WechslerChildGet(viewsets.ReadOnlyModelViewSet):   
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    serializer_class = serializers.WechslerChildSerializer
    def get_queryset(self):
        child_id = self.request.headers.get('child-id')
        kid=models.WechslerChild.objects.filter(child__id=child_id).exclude(IQ=0)
        return kid

@api_view(['POST'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def AddWechslerChild(request):
    child_id = request.POST.get('child')
    birth_date = request.POST.get('birthdate')
    birthdate = datetime.strptime(birth_date, '%Y-%m-%d')
    child=models.ChildPersonalInfo.objects.get(id=child_id)
    year= relativedelta(datetime.now(), birthdate).years*12
    month= relativedelta(datetime.now(), birthdate).months
    age=year+month
    # print(age)
    if age in range(144,155):
        WechslerChild=models.WechslerChild.objects.create(child=child,birthdate=birthdate)
        return Response({'id':WechslerChild.id,
                         'child':WechslerChild.child.full_name})
    else:
        WechslerChild=models.WechslerChild.objects.create(child=child,birthdate=birthdate)
        return Response({'message':'invalid age,child created',
                         'id':WechslerChild.id,
                         'child':WechslerChild.child.full_name})


class PortageView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.PortageTestSerializer
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
   
    def get_queryset(self):
            test_type = self.request.query_params['test-type']
            general_test = models.PortageTest.objects.filter(name = test_type).distinct() 
            return general_test

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
class PortageChildTestView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    serializer_class = serializers.PortageChildsTestsSerializer
    queryset = models.PortageChildTest.objects.all()


class PortageSpecificChildTestsView(APIView):    
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    def get(self, request):
        child_id = request.headers.get('child-id')
        child = models.ChildPersonalInfo.objects.get(id=child_id)
        portage_child_test = models.PortageChildTest.objects.filter(child_name = child)
        portage_child_test_serializer =  serializers.PortageChildTestsSerializer(portage_child_test, many=True)
        return Response(portage_child_test_serializer.data) 
    
    
@api_view(['POST'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def calculate_portage_test_result(request):
    if request.method == 'POST':
        total_score = request.POST.get('total_score')
        child_id = request.POST.get('child_id')
        test_name = request.POST.get('test_name')
        non_answered_questions = request.POST.getlist('non_answered_questions')
        child = models.ChildPersonalInfo.objects.get(id=child_id)
        test = models.PortageTest.objects.get(name=test_name)
        if int(child.age_in_years) >= 1:
            performance = (int(total_score) * 100) / int(child.age_in_years)
        elif  int(child.age_in_months) >= 1:
            performance = (float(total_score) * 100) / float(child.age_in_months / (12 / 100))
        else:
            performance = (float(total_score) * 100) / float((child.age_in_days / (30 / 100)) / (12 / 100))
        performance = int(performance)
        diagnose = ""
        if performance in range(0,19):
            diagnose = "تأخر شديد جدا"
        elif performance in range(20,39):
            diagnose = "شديد"
        elif performance in range(40,59):
            diagnose = "متوسط"
        elif performance in range(60,79):
            diagnose = "تأخر بسيط"
        elif performance >= 80:
            diagnose = "طبيعي"
        child_test = models.PortageChildTest.objects.create(test_name = test, child_name = child, diagnose = diagnose, age = child.age_in_months)
        child_test.save()
        for question in non_answered_questions:
            portage_question = models.PortageQuestion.objects.get(id = question)
            models.NonAsweredPortageQuestion.objects.create(child_name = child, question = portage_question, test_name = child_test).save()
        return Response({'diagnose': child_test.diagnose}, status= status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def add_portage_treatment_suggestion(request):
    child_id = request.POST.get('child_id')
    test_id = request.POST.get('test_id')
    treatment_suggestion = request.POST.get('treatment_suggestion')
    if treatment_suggestion is None:
        return Response({"message":"الحقل فارغ"})
    child = models.ChildPersonalInfo.objects.get(id = child_id)
    test = models.PortageTest.objects.get(id = test_id)
    child_test = models.PortageChildTest.objects.filter(child_name = child, test_name = test).last()
    child_test.treatment_suggestion = treatment_suggestion
    child_test.save()
    return Response({'message':'Treatment suggestion added successfuly'}, status= status.HTTP_201_CREATED)
    
    
class ChildInfoQustionsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ChildInfoBlockSerializer
    queryset = models.ChildInfoBlock.objects.all()    
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
     
    
    
@api_view(['POST'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def child_answer(request):
    child_id = request.POST.get('child_id')
    child_answers = request.POST.getlist('child_answers')
    for child_answer in child_answers:
        splited_child_answer = child_answer.split('/')
        question_id = splited_child_answer[0]
        answer = splited_child_answer[1]
        child = models.ChildPersonalInfo.objects.get(id=child_id)
        question = models.ChildInfoQuestion.objects.get(id=question_id)
        if models.ChildInfoAnswer.objects.filter(child_id=child, qustion_id=question).exists():
            old_answer = models.ChildInfoAnswer.objects.get(child_id=child, qustion_id=question)
            old_answer.answer = answer
            old_answer.save()
        else:
            models.ChildInfoAnswer.objects.create(child_id=child, qustion_id=question, answer=answer)
    return Response({'message':'Child information added successfuly'})


class ChildPersonalInfoView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ChildPersonalInfoSerializer
    
    def get_queryset(self):
        fullname = self.request.query_params['fullname']
        child_peronal_info = models.ChildPersonalInfo.objects.filter(full_name=fullname)
        if child_peronal_info.exists():
            child_peronal_info[0].save()
        return child_peronal_info
        
    
class AddChildView(APIView):
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    def post(self, request):
        try:
            first_name = self.request.POST.get('first_name')
            last_name = self.request.POST.get('last_name')
            birthdate = self.request.POST.get('birthdate')
            child_class = self.request.POST.get('child_class')
            current_school = self.request.POST.get('current_school')
            address = self.request.POST.get('address')
            phone_number = self.request.POST.get('phone_number')
            transferring_party = self.request.POST.get('transferring_party')
            supervised_doctor = self.request.POST.get('supervised_doctor')
            father_name = self.request.POST.get('father_name')
            mother_name = self.request.POST.get('mother_name')
            father_education = self.request.POST.get('father_education')
            mother_education = self.request.POST.get('mother_education')
            father_work = self.request.POST.get('father_work')
            mother_work = self.request.POST.get('mother_work')
            if (first_name is None) or (last_name is None) or (birthdate is None) or (father_name is None) or (mother_name is None) or (father_education is None) or (mother_education is None) or (father_work is None) or (mother_work is None):
                return Response({'message': "Enter all required fields"})
            child = models.ChildPersonalInfo.objects.create(first_name=first_name,last_name = last_name, address=address, phone_number=phone_number, transferring_party=transferring_party, father_name=father_name, mother_name=mother_name, birthdate=birthdate, child_class=child_class, current_school=current_school, supervised_doctor=supervised_doctor, father_education=father_education, mother_education=mother_education, father_work=father_work, mother_work= mother_work)
            child.save()
            return Response({ 'child_id': child.id, 'message': 'Child Created Successfuly'})
        except IntegrityError as e:
            return Response({"error":"Name Already Exists"})
    
    
class ParentsView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.ParentsTestSerializer
    queryset = models.ParentsTest.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
@api_view(['POST'])
def calculate_parents_test_result(request):
    if request.method == 'POST':
        total_score = request.POST.get('total_score')
        birthdate = request.POST.get('birthdate')
        age = models.calculate_parents_test_age(birthdate=birthdate)
        number_of_qustions = models.ParentsQuestion.objects.filter(block__age__lte=age).count()
        performance = (int(total_score)/int(number_of_qustions)) * 100
        performance = int(performance)
        diagnose = ""
        if performance in range(0,19):
            diagnose = "تأخر شديد جدا"
        elif performance in range(19,39):
            diagnose = " تأخر شديد"
        elif performance in range(39,59):
            diagnose = "متوسط"
        elif performance in range(59,79):
            diagnose = "تأخر بسيط"
        elif performance >= 80:
            diagnose = "طبيعي"
        return Response({'diagnose': diagnose})


class LddrsQuestionsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LddrsQuestionsSerializer
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    
    def get_queryset(self):
        test = self.request.query_params['test-name']
        question = models.LddrsQuestion.objects.filter(test_name=test)
        return question


@api_view(['POST'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def CalculateLddrs(request):
    s=request.POST.get('score')
    child_id=request.POST.get('child-id')
    child=models.ChildPersonalInfo.objects.get(id=child_id)
    test_name=request.POST.get('test')
    score=int(s)

    print(score)
    if score in range (0,20):
        diagnose='لا يوجد صعوبة في التعلم'
    elif score in range (21,40):
        diagnose=' صعوبه خفيفة في التعلم'
    elif score in range (41,60):
        diagnose=' صعوبه متوسطة في التعلم'
    else:
        diagnose=' صعوبه شديدة في التعلم'

    models.LddrsChild.objects.create(child_id=child_id,test=test_name,diagnose=diagnose,age=child.age_in_months)
    return Response({'diagnose':diagnose})


class LddrChildView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    serializer_class = serializers.LddrsSerializers
    
    def get_queryset(self):
        child_id = self.request.headers.get('child-id')
        test = self.request.query_params['test']
        result = models.LddrsChild.objects.filter(child=child_id,test=test)
        return result


@api_view(['POST'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])
def LddrsSuggestion(request):
    id=request.headers.get('child-id')
    treat=request.POST.get('suggestion')
    if treat is None:
        return Response({"message":"الحقل فارغ"})
    child=models.LddrsChild.objects.filter(child__id=id).latest('id')
    print(child)
    child.treatment_suggestion=treat
    child.save()
    return JsonResponse({'message':'done'})

    
class EventView(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializers
    queryset=models.Event.objects.all()
    
        
    def delete(self, request):
        try:
            id = request.POST.get('id')
            models.Event.objects.get(id=id).delete()
            return Response({"message":"Event deleted successfully"}, status= status.HTTP_200_OK)
        except:
                return Response({"error":"An error occurred while deleting the event, please try again"}, status.HTTP_400_BAD_REQUEST)
    

def google_search(query, api_key, cse_id):
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}"
    response = requests.get(url)
    results = json.loads(response.text)
    return results

@api_view(['GET'])
def search_engine(request):
    query = request.query_params['query']
    api_key = 'AIzaSyAGKll-Kc0Puc5JuQpk7zVSHLmfFnNUXYM'
    cse_id = 'c072dcc42e9004a4b'
    results = google_search(query, api_key, cse_id)
    print('total', results['searchInformation']['totalResults'] )
    if results['searchInformation']['totalResults'] == '0':
        return Response({"message":"لا توجد نتائج"})
    final_result = list()
    for result in results["items"]:
        final_result.append({'result' : { 'title': result["title"], 'link': result["link"], 'snippet': result["snippet"]}})
    return Response(final_result)


@api_view(['PUT'])
@permission_classes([permissions.IsParentOrExpert, IsAuthenticated])

def update_chid_info(request):
    data=request.data
    for value in data.values():
        if value == '':
            print(value)
            return Response({'message':'Enter all required fields'})
    child=models.ChildPersonalInfo.objects.get(full_name=data["full_name"])
    child.first_name=data['first_name']
    child.last_name=data['last_name']
    child.birthdate=data['birthdate']
    child.child_class=data['child_class']
    child.current_school=data['current_school']
    child.address=data['address']
    child.phone_number=data['phone_number']
    child.transferring_party=data['transferring_party']
    child.supervised_doctor=data['supervised_doctor']
    child.father_name=data['father_name']
    child.mother_name=data['mother_name']
    child.father_education=data['father_education']
    child.mother_education=data['mother_education']
    child.father_work=data['father_work']
    child.mother_work=data['mother_work']
    child.save()
    return Response({'message':'updated Successfully'})


class RavnTestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RavnGroupSerializer
    permission_classes = [permissions.IsParentOrExpert, IsAuthenticated]
    queryset = models.RavnGroup.objects.all()
    
     

       
