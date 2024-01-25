import pickle
import pandas as pd

svm_loaded_model1 = pickle.load(open(r'first_app\SVM_toddlers_chisquared.sav', 'rb')) 




def toddlers_svm_predict(result_list):
    in_df = pd.DataFrame([result_list], columns=['a1','a2','a3','a4','a5', 'a6','a7','a8','a9','a10','age_mons','ethnicity','jaundice','gender'])
    result = svm_loaded_model1.predict(in_df)
    print(result)
    if result == 0:
        ASD_Class = 'No Autism Traits but if you have doubt, please visit our center for further tests.'
    elif result == 1:
        ASD_Class = 'There are Autism Traits, please visit our center for further tests.'
    
    return ASD_Class