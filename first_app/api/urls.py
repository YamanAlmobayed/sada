from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()

router.register('wechsler_qustions', views.WechslerTestView, basename='wechsler_qustions')#
router.register('wechsler_get', views.WechslerChildGet, basename='wechsler_get')

router.register('autism_question', views.AutismQustionView, basename='AutismQustionView')#  

router.register('portage_childs_tests', views.PortageChildTestView, basename = 'portage_childs_tests')#

router.register('child_info_questions', views.ChildInfoQustionsView, basename='child_info_questions')#
router.register('child_personal_info', views.ChildPersonalInfoView, basename='child_personal_info')#

router.register('lddrs_questions', views.LddrsQuestionsView, basename='LddrsQuestionsView') #
router.register('lddrs_child_results', views.LddrChildView, basename='LddrChildView') #

router.register('events', views.EventView)#

router.register('ravn', views.RavnTestView)




urlpatterns=[
     path('', include(router.urls)),
     path('scale_score/',views.WechslerScaleScore.as_view()),#
     path('wechsler_diagnose/',views.WechslerDiagnose.as_view()),#
     
     path('portage_qustions/', views.PortageView.as_view(), name = 'portage'),#
     path('portage_child_tests/', views.PortageSpecificChildTestsView.as_view(), name = 'portage_child_tests'),#
     path('portage_result/', views.calculate_portage_test_result, name = 'portage_result'),#
     path('portage_treatment/', views.add_portage_treatment_suggestion, name = 'portage_treatment_suggestion'),#
 
     path('add_child/', views.AddChildView.as_view(), name = 'add_child'),#
     path('child_submit_answers/', views.child_answer, name = 'child_submit_answers'),#
     
     path('parents_test/', views.ParentsView.as_view(), name = 'parents_test'),#
     path('parents_result/', views.calculate_parents_test_result, name = 'portage_result'),#
     
     path('lddrs_diagnose/', views.CalculateLddrs, name = 'CalculateLddrs'),#
     path('lddrs_suggestion/', views.LddrsSuggestion, name = 'CalculateLddrsSuggestion'),#
     
     path('login/', views.Login.as_view(), name='login'),#
     path('logout/',views.logout_view, name='logout'),#
     
     path('create_parent_account/', views.create_parent_account_view, name = 'create_parent_account'),#
     path('add_exciting_parent_to_child/', views.add_exciting_parent_view, name = 'add_exciting_parent_to_child'),#
     
     path('search_engine/', views.search_engine, name = 'search_engine'),#
     path('children_autism/', views.autism_children, name = 'children_autism'),
     path('toddler_autism/', views.autism_toddler, name = 'autism_toddler'),
     path('update_child/', views.update_chid_info, name = 'update_chid_info'),
     path('dyslexia/', views.DyslexiaView.as_view(), name = 'dyslexia'),
     path('add_wechsler/', views.AddWechslerChild, name = 'add_wechsler'),
     path('depression/', views.depression_detection_view),
]