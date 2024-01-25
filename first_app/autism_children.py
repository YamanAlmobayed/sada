import pickle
import pandas as pd


lr_loaded_model = pickle.load(open(r'first_app\LR_children_chisquared.sav', 'rb'))


def children_lr_predict(result_list):
    in_df = pd.DataFrame([result_list], columns=['A1_Score','A2_Score','A3_Score','A4_Score','A5_Score', 'A6_Score','A7_Score','A8_Score','A9_Score','A10_Score','age','gender','jaundice','family_member_with_asd'])
    result = lr_loaded_model.predict(in_df)
    print(result)
    if result == 0:
        ASD_Class = 'No Autism Traits but if you have doubt, please visit our center for further tests.'
    elif result == 1:
        ASD_Class = 'There are Autism Traits, please visit our center for further tests.'
    
    return ASD_Class



