import pandas as pd
import numpy as np
import streamlit as st
import re
from datetime import date

# Files used later (set up)
crosswalk_file = '/Users/canluser/Library/CloudStorage/Box-Box/VUMC Secondary QC Check/Crosswalk.xlsx'

def convert_df(df):
    return df.to_csv().encode('utf-8') 

today = date.today()

st.write("# VUMC QC Check")
full_data = st.file_uploader("Upload full RC database export", type='csv')

if full_data is None:
    st.write("To get started, please upload the full RC database export above.")
    st.write("Make sure the file is a CSV as the file uploaded will not accept any other format.")

############################################################################## Making a full discrepancy db ##############################################################################
if full_data is not None:
    # Opening needed files
    full_db = pd.read_csv(full_data)
    crosswalk_db = pd.read_excel(crosswalk_file, sheet_name='Everything')
    full_db = full_db.fillna(0)
    filtered_full_db = full_db[(full_db['scid_iscomplete'] == 'Yes') & (full_db['dx1'] != 47)]
    
    ####################################################################### Creating lists that will do most of the work ###################################################################

    # Criterion names and syndrome names
    syndrome_names_list = crosswalk_db.syndrome_names.values.tolist() # Full syndrome names (e.g., Current Major Depressive Episode, etc.)
    syndrome_names_list_cleaned = [x for x in syndrome_names_list if str(x) != 'nan']

    short_syndrome_names_list = crosswalk_db.syndrome_acronyms.values.tolist() # Acronym of syndrome names (e.g., CMDE)
    short_syndrome_names_list_cleaned = [x for x in short_syndrome_names_list if str(x) != 'nan']

    all_criteria_items = crosswalk_db.all_syndrome_criteria.values.tolist()
    all_criteria_items_cleaned = [x for x in all_criteria_items if str(x) != 'nan']
    
    criterion_w_one_item = crosswalk_db.criterions_w_one_item.values.tolist() # Criterions that only have one assessed item (e.g., A6 (CMDE))
    criterion_w_one_item_cleaned = [x for x in criterion_w_one_item if str(x) != 'nan']
    
    criterion_w_two_items = crosswalk_db.criterions_w_two_items.values.tolist() # Criterions that have two assessed items (e.g., A1 (CMDE))
    criterion_w_two_items_cleaned = [x for x in criterion_w_two_items if str(x) != 'nan']
    
    criterion_w_three_items = crosswalk_db.criterions_w_three_items.values.tolist() # Criterions that have three assessed items (e.g., A3 (CMDE))
    criterion_w_three_items_cleaned = [x for x in criterion_w_three_items if str(x) != 'nan']

    criterion_w_four_items = crosswalk_db.criterions_w_four_items.values.tolist() # Criterions that have four assessed items (e.g., A2 (CMDE))
    criterion_w_four_items_cleaned = [x for x in criterion_w_four_items if str(x) != 'nan']

    criterion_w_exceptions = crosswalk_db.exception_criteria.values.tolist() # ME Criteria that have the length and checkbox requirement
    criterion_w_exceptions_cleaned = [x for x in criterion_w_exceptions if str(x) != 'nan']

    impairment_criteria = crosswalk_db.impairment_criteria.values.tolist()
    impairment_criteria_cleaned = [x for x in impairment_criteria if str(x) != 'nan']
    
    criterion_count_exceptions = crosswalk_db.criterion_count_exceptions.values.tolist()
    criterion_count_exceptions_cleaned = [x for x in criterion_count_exceptions if str(x) != 'nan']

    criterion_w_cnt_items = crosswalk_db.criterion_w_cnt_items.values.tolist()
    criterion_w_cnt_items_cleaned = [x for x in criterion_w_cnt_items if str(x) != 'nan']

    criterion_w_validation = crosswalk_db.criterion_cnt_validation.values.tolist()
    criterion_w_validation_cleaned = [x for x in criterion_w_validation if str(x) != 'nan']

    criterion_w_one_validation = crosswalk_db.criteria_cnt_valid_1it.values.tolist()
    criterion_w_one_validation_cleaned = [x for x in criterion_w_one_validation if str(x) != 'nan']

    criterion_w_two_validations = crosswalk_db.criteria_cnt_valid_2it.values.tolist()
    criterion_w_two_validations_cleaned = [x for x in criterion_w_two_validations if str(x) != 'nan']

    criterion_w_three_validations = crosswalk_db.criteria_cnt_valid_3it.values.tolist()
    criterion_w_three_validations_cleaned = [x for x in criterion_w_three_validations if str(x) != 'nan']

    criterion_w_special_validations = crosswalk_db.criteria_cnt_valid_sit.values.tolist()
    criterion_w_special_validations_cleaned = [x for x in criterion_w_special_validations if str(x) != 'nan']

    criterion_w_no_cnt_validations = crosswalk_db.criteria_cnt_valid_only_my_it.values.tolist()
    criterion_w_no_cnt_validations_cleaned = [x for x in criterion_w_no_cnt_validations if str(x) != 'nan']

    diagnosis_names = crosswalk_db.diagnosis_names.values.tolist()
    diagnosis_names_cleaned = [x for x in diagnosis_names if str(x)!= 'nan']

    syndromes_for_diag_check = crosswalk_db.syndrome_for_diag_count.values.tolist()
    syndromes_for_diag_check_cleaned = [x for x in syndromes_for_diag_check if str(x) != 'nan']

    diags_w_2_scid = crosswalk_db.diags_w_2_criteria.values.tolist()
    diags_w_2_scid_cleaned = [x for x in diags_w_2_scid if str(x) != 'nan']

    diags_w_3_scid = crosswalk_db.diags_w_3_criteria.values.tolist()
    diags_w_3_scid_cleaned = [x for x in diags_w_3_scid if str(x) != 'nan']

    diags_w_4_scid = crosswalk_db.diags_w_4_criteria.values.tolist()
    diags_w_4_scid_cleaned = [x for x in diags_w_4_scid if str(x) != 'nan']

    diags_w_5_scid = crosswalk_db.diags_w_5_criteria.values.tolist()
    diags_w_5_scid_cleaned = [x for x in diags_w_5_scid if str(x) != 'nan']

    diags_w_6_scid = crosswalk_db.diags_w_6_criteria.values.tolist()
    diags_w_6_scid_cleaned = [x for x in diags_w_6_scid if str(x) != 'nan']

    diags_w_7_scid = crosswalk_db.diags_w_7_criteria.values.tolist()
    diags_w_7_scid_cleaned = [x for x in diags_w_7_scid if str(x) != 'nan']

    diags_w_9_scid = crosswalk_db.diags_w_9_criteria.values.tolist()
    diags_w_9_scid_cleaned = [x for x in diags_w_9_scid if str(x) != 'nan']

    diags_w_10_scid = crosswalk_db.diags_w_10_criteria.values.tolist()
    diags_w_10_scid_cleaned = [x for x in diags_w_10_scid if str(x) != 'nan']

    criteria_w_multi_items = crosswalk_db.criteria_cnt_multiple_items.values.tolist()
    criteria_w_multi_items_cleaned = [x for x in criteria_w_multi_items if str(x) != 'nan']

    criteria_w_cnt_items = crosswalk_db.criteria_cnt_cnt_items.values.tolist()
    criteria_w_cnt_items_cleaned = [x for x in criteria_w_cnt_items if str(x) != 'nan']

    # SCID ITEMS that correspond to the criterion names/syndrome names
    one_criterion_items = crosswalk_db.one_item_items.values.tolist() # Items that are used by the 
    one_criterion_items_cleaned = [x for x in one_criterion_items if str(x) != 'nan']

    two_criteria_items = crosswalk_db.two_item_items.values.tolist()
    two_criteria_items_cleaned = [x for x in two_criteria_items if str(x) != 'nan']

    three_criteria_items = crosswalk_db.three_item_items.values.tolist()
    three_criteria_items_cleaned = [x for x in three_criteria_items if str(x) != 'nan']

    four_criteria_items = crosswalk_db.four_item_items.values.tolist()
    four_criteria_items_cleaned = [x for x in four_criteria_items if str(x) != 'nan']

    exclusion_criteria_items = crosswalk_db.exception_items.values.tolist()
    exclusion_criteria_items_cleaned = [x for x in exclusion_criteria_items if str(x) != 'nan']

    impairment_items = crosswalk_db.impairment_items.values.tolist()
    impairment_items_cleaned = [x for x in impairment_items if str(x) != 'nan']

    rc_criterion_w_cnt_items = crosswalk_db.redcap_cnt_item.values.tolist()
    rc_criterion_w_cnt_items_cleaned = [x for x in rc_criterion_w_cnt_items if str(x) != 'nan']

    rc_items_for_criterion_validation = crosswalk_db.rc_criterion_validation_items.values.tolist()
    rc_items_for_criterion_validation_cleaned = [x for x in rc_items_for_criterion_validation if str(x) != 'nan']

    my_cnt_items_for_criterion_validation = crosswalk_db.my_criterion_validation_items.values.tolist()
    my_cnt_items_for_criterion_validation_cleaned = [x for x in my_cnt_items_for_criterion_validation if str(x) != 'nan']

    diagnosis_items = crosswalk_db.diagnosis_items.values.tolist()
    diagnosis_items_cleaned = [x for x in diagnosis_items if str(x) != 'nan']

    all_scid_items = crosswalk_db.all_scid_items.values.tolist()
    all_scid_items_cleaned = [x for x in all_scid_items if str(x) != 'nan']

    two_criteria_diag_items_scid = crosswalk_db.two_criteria_diag_items_scid.values.tolist()
    two_criteria_diag_items_scid_cleaned = [x for x in two_criteria_diag_items_scid if str(x) != 'nan']

    three_criteria_diag_items_scid = crosswalk_db.three_criteria_diag_items_scid.values.tolist()
    three_criteria_diag_items_scid_cleaned = [x for x in three_criteria_diag_items_scid if str(x) != 'nan']

    four_criteria_diag_items_scid = crosswalk_db.four_criteria_diag_items_scid.values.tolist()
    four_criteria_diag_items_scid_cleaned = [x for x in four_criteria_diag_items_scid if str(x) != 'nan']

    five_criteria_diag_items_scid = crosswalk_db.five_criteria_diag_items_scid.values.tolist()
    five_criteria_diag_items_scid_cleaned = [x for x in five_criteria_diag_items_scid if str(x) != 'nan']

    six_criteria_diag_items_scid = crosswalk_db.six_criteria_diag_items_scid.values.tolist()
    six_criteria_diag_items_scid_cleaned = [x for x in six_criteria_diag_items_scid if str(x) != 'nan']

    seven_criteria_diag_items_scid = crosswalk_db.seven_criteria_diag_items_scid.values.tolist()
    seven_criteria_diag_items_scid_cleaned = [x for x in seven_criteria_diag_items_scid if str(x) != 'nan']
    
    nine_criteria_diag_items_scid = crosswalk_db.nine_criteria_diag_items_scid.values.tolist()
    nine_criteria_diag_items_scid_cleaned = [x for x in nine_criteria_diag_items_scid if str(x) != 'nan']

    ten_criteria_diag_items_scid = crosswalk_db.ten_criteria_diag_items_scid.values.tolist()
    ten_criteria_diag_items_scid_cleaned = [x for x in ten_criteria_diag_items_scid if str(x) != 'nan']

    two_criteria_diag_items_mine = crosswalk_db.two_criteria_diag_items_mine.values.tolist()
    two_criteria_diag_items_mine_cleaned = [x for x in two_criteria_diag_items_mine if str(x) != 'nan']

    three_criteria_diag_items_mine = crosswalk_db.three_criteria_diag_items_mine.values.tolist()
    three_criteria_diag_items_mine_cleaned = [x for x in three_criteria_diag_items_mine if str(x) != 'nan']

    four_criteria_diag_items_mine = crosswalk_db.four_criteria_diag_items_mine.values.tolist()
    four_criteria_diag_items_mine_cleaned = [x for x in four_criteria_diag_items_mine if str(x) != 'nan']

    five_criteria_diag_items_mine = crosswalk_db.five_criteria_diag_items_mine.values.tolist()
    five_criteria_diag_items_mine_cleaned = [x for x in five_criteria_diag_items_mine if str(x) != 'nan']

    six_criteria_diag_items_mine = crosswalk_db.six_criteria_diag_items_mine.values.tolist()
    six_criteria_diag_items_mine_cleaned = [x for x in six_criteria_diag_items_mine if str(x) != 'nan']

    seven_criteria_diag_items_mine = crosswalk_db.seven_criteria_diag_items_mine.values.tolist()
    seven_criteria_diag_items_mine_cleaned = [x for x in seven_criteria_diag_items_mine if str(x) != 'nan']
    
    nine_criteria_diag_items_mine = crosswalk_db.nine_criteria_diag_items_mine.values.tolist()
    nine_criteria_diag_items_mine_cleaned = [x for x in nine_criteria_diag_items_mine if str(x) != 'nan']

    ten_criteria_diag_items_mine = crosswalk_db.ten_criteria_diag_items_mine.values.tolist()
    ten_criteria_diag_items_mine_cleaned = [x for x in ten_criteria_diag_items_mine if str(x) != 'nan']

    ####################################################################### While Loops that creates Desired Columns #######################################################################

    # Creating a function that converts month and week string items in length columns to days (numeric)
    def convert_to_days(x):
        try:
            return int(x)
        except ValueError:
            if 'month' in x:
                return int(x.split()[0]) * 30
            elif 'week' in x:
                return int(x.split()[0]) * 7
            else:
                return None
    
    # Converting 3u to just 3 (scid_e5, scid_e25, )
    filtered_full_db = filtered_full_db.replace('3u', '3')

    # Turning all scid items into integers to prevent some symptoms not being counted for
    filtered_full_db = filtered_full_db.astype({all_scid_items_cleaned[i]:'int' for i in range(len(all_scid_items_cleaned))})

    # Count items for the criterion while loop
    initial_count = 0
    criterion_one_count = 0
    criterion_two_count_1 = 0
    criterion_two_count_2 = 0
    criterion_three_count_1 = 0
    criterion_three_count_2 = 0
    criterion_four_count_1 = 0
    criterion_four_count_2 = 0
    exclusion_criteria_count_1 = 0
    exclusion_criteria_count_2 = 0
    impairment_criteria_count_1 = 0
    impairment_criteria_count_2 = 0
    
    # Loop is creating the criterion count items based on five different sub-types
    while initial_count < len(all_criteria_items_cleaned):
        if all_criteria_items_cleaned[initial_count] in criterion_w_one_item_cleaned:
            if "C (SCHIZOPHRENIFORM)" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_one_item_cleaned[criterion_one_count]] = np.where(((filtered_full_db[one_criterion_items_cleaned[criterion_one_count]] != 3) & 
                                                                                       (filtered_full_db[one_criterion_items_cleaned[criterion_one_count]] != 0)), 1, 0)
                initial_count += 1
                criterion_one_count += 1
            elif "C (CME)" in all_criteria_items_cleaned[initial_count] or "C (PME)" in all_criteria_items_cleaned[initial_count] or "D (ADHD)" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_one_item_cleaned[criterion_one_count]] = np.where(((filtered_full_db[one_criterion_items_cleaned[criterion_one_count]] >= 3)), 1, 0)
                initial_count += 1
                criterion_one_count += 1
            else:
                filtered_full_db[criterion_w_one_item_cleaned[criterion_one_count]] = np.where(((filtered_full_db[one_criterion_items_cleaned[criterion_one_count]] == 3)), 1, 0)
                initial_count += 1
                criterion_one_count += 1
        elif all_criteria_items_cleaned[initial_count] in criterion_w_two_items_cleaned:
            if "BN" in all_criteria_items_cleaned[initial_count] or "BE" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_two_items_cleaned[criterion_two_count_1]] = np.where(((filtered_full_db[two_criteria_items_cleaned[criterion_two_count_2]] == 3) & 
                (filtered_full_db[two_criteria_items_cleaned[criterion_two_count_2 + 1]] == 3)), 1, 0)
                initial_count += 1
                criterion_two_count_1 += 1
                criterion_two_count_2 += 2
            elif "OB (LOCD)" in all_criteria_items_cleaned[initial_count] or "CO (LOCD)" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_two_items_cleaned[criterion_two_count_1]] = np.where(((filtered_full_db[two_criteria_items_cleaned[criterion_two_count_2]] == 3) & 
                (filtered_full_db[two_criteria_items_cleaned[criterion_two_count_2 + 1]] == 3)), 1, 0)
                initial_count += 1
                criterion_two_count_1 += 1
                criterion_two_count_2 += 2
            else:
                filtered_full_db[criterion_w_two_items_cleaned[criterion_two_count_1]] = np.where(((filtered_full_db[two_criteria_items_cleaned[criterion_two_count_2]] == 3) | 
                (filtered_full_db[two_criteria_items_cleaned[criterion_two_count_2 + 1]] == 3)), 1, 0)
                initial_count += 1
                criterion_two_count_1 += 1
                criterion_two_count_2 += 2
        elif all_criteria_items_cleaned[initial_count] in criterion_w_three_items_cleaned:
            if "OCD" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_three_items_cleaned[criterion_three_count_1]] = np.where(((filtered_full_db[three_criteria_items_cleaned[criterion_three_count_2]] == 3) |
                (filtered_full_db[three_criteria_items_cleaned[criterion_three_count_2 + 1]] >= 3) | (filtered_full_db[three_criteria_items_cleaned[criterion_three_count_2 + 2]] == 3)), 1, 0)
                initial_count += 1
                criterion_three_count_1 += 1
                criterion_three_count_2 += 3
            else:
                filtered_full_db[criterion_w_three_items_cleaned[criterion_three_count_1]] = np.where(((filtered_full_db[three_criteria_items_cleaned[criterion_three_count_2]] == 3) |
                (filtered_full_db[three_criteria_items_cleaned[criterion_three_count_2 + 1]] == 3) | (filtered_full_db[three_criteria_items_cleaned[criterion_three_count_2 + 2]] == 3)), 1, 0)
                initial_count += 1
                criterion_three_count_1 += 1
                criterion_three_count_2 += 3
        elif all_criteria_items_cleaned[initial_count] in criterion_w_four_items_cleaned:
            if "ME" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_four_items_cleaned[criterion_four_count_1]] = np.where((((filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2]] == 3) & 
                (filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2 + 1]] == 3)) | ((filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2 + 2]] == 3) &
                (filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2 + 3]] == 3))), 1, 0)
                initial_count += 1
                criterion_four_count_1 += 1
                criterion_four_count_2 += 4
            else:
                filtered_full_db[criterion_w_four_items_cleaned[criterion_four_count_1]] = np.where(((filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2]] == 3) | 
                (filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2 + 1]] == 3) | (filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2 + 2]] == 3) |
                (filtered_full_db[four_criteria_items_cleaned[criterion_four_count_2 + 3]] == 3)), 1, 0)
                initial_count += 1
                criterion_four_count_1 += 1
                criterion_four_count_2 += 4
        elif all_criteria_items_cleaned[initial_count] in criterion_w_exceptions_cleaned:
            filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2]] = filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2]].apply(convert_to_days)
            if "CHME" in all_criteria_items_cleaned[initial_count] or "PHME" in all_criteria_items_cleaned[initial_count]:
                filtered_full_db[criterion_w_exceptions_cleaned[exclusion_criteria_count_1]] = np.where(((filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2]] >= 4) & 
                (filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2 + 1]] == 0) & (filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2]] < 7)), 1, 0)
                initial_count += 1
                exclusion_criteria_count_1 += 1
                exclusion_criteria_count_2 += 2
            else:
                filtered_full_db[criterion_w_exceptions_cleaned[exclusion_criteria_count_1]] = np.where(((filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2]] >= 7) | 
                (filtered_full_db[exclusion_criteria_items_cleaned[exclusion_criteria_count_2 + 1]] == 1)), 1, 0)
                initial_count += 1
                exclusion_criteria_count_1 += 1
                exclusion_criteria_count_2 += 2
        elif all_criteria_items_cleaned[initial_count] in impairment_criteria_cleaned:
            filtered_full_db[impairment_criteria_cleaned[impairment_criteria_count_1]] = np.where(((filtered_full_db[impairment_items_cleaned[impairment_criteria_count_2]] >= 3) | 
            (filtered_full_db[impairment_items_cleaned[impairment_criteria_count_2 + 1]] >= 3)), 1, 0)
            initial_count += 1
            impairment_criteria_count_1 += 1
            impairment_criteria_count_2 += 2 
        else:
            initial_count +=1

    # Creating Criterion A for ME as it works a bit different than others.
    filtered_full_db['A (CME) [MINE]'] = np.where(((filtered_full_db['A1 (CME)'] == 1) & (filtered_full_db['A2 (CME)'] == 1)), 1, 0)
    filtered_full_db['A (PME) [MINE]'] = np.where(((filtered_full_db['A1 (PME)'] == 1) & (filtered_full_db['A2 (PME)'] == 1)), 1, 0)
    filtered_full_db['A (CHME) [MINE]'] = np.where(((filtered_full_db['A1 (CHME)'] == 1) & (filtered_full_db['A2 (CHME)'] == 1)), 1, 0)
    filtered_full_db['A (PHME) [MINE]'] = np.where(((filtered_full_db['A1 (PHME)'] == 1) & (filtered_full_db['A2 (PHME)'] == 1)), 1, 0)

    # Creating Criterion Counts where applicable
    criterion_count_pattern = re.compile(r'\(([^()]+)\)')
    desired_criterion_colummns = []
    criterion_counts = {}

    # Creating a dictionary for only the desired criterion that need count items
    for col in all_criteria_items_cleaned:
        if col not in criterion_count_exceptions_cleaned:
            desired_criterion_colummns.append(col)
        else:
            pass
    
    # Getting new column names
    for col in desired_criterion_colummns:
        disorder_match = criterion_count_pattern.search(col)
        if disorder_match is not None:
            disorder = disorder_match.group(1)
            criterion = f'Criterion {col[0]} ({disorder}) Count [MINE]'
            criterion_counts.setdefault(criterion, []).append(col)
        else:
            pass
    
    # The actual summation of criterion items
    for new_col, old_cols in criterion_counts.items():
       filtered_full_db[new_col] = filtered_full_db[old_cols].sum(axis = 1)

    # Adding special B+C (PDD) Count Item
    filtered_full_db['Criterion B+C (PDD) Count [MINE]'] = filtered_full_db['Criterion B (PDD) Count [MINE]'] + filtered_full_db['Criterion C (PDD) Count [MINE]']

    # Checking Criterion Counts where applicable
    for item in criterion_w_cnt_items_cleaned:
        if 'Criterion ' + item + ' Count [MINE]' in filtered_full_db.columns:
            if 'Criterion ' + item + ' Count' == 'Criterion C (PDD) Count':
                new_col_name = 'B+C (PDD) Count Comparison'
                filtered_full_db[new_col_name] = np.where((filtered_full_db['Criterion B+C (PDD) Count [MINE]'] == filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]), "Same", "Problem")
            else:    
                new_col_name = item + ' Count Comparison'
                filtered_full_db[new_col_name] = np.where((filtered_full_db['Criterion ' + item + ' Count [MINE]'] == filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]), "Same", "Problem")
        elif item == 'CATA (SCHIZOPHRENIA)':
            new_col_name = 'Schizophrenia (Catatonia) Count Comparison'
            filtered_full_db['Schizophrenia Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c10'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = np.where((filtered_full_db['Schizophrenia Catatonia Count [MINE]'] == filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]), "Same", "Problem")
        elif item == 'CATA (SCHIZOPHRENIFORM)':
            new_col_name = 'Schizophreniform (Catatonia) Count Comparison'
            filtered_full_db['Schizophreniform Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c14'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = np.where((filtered_full_db['Schizophreniform Catatonia Count [MINE]'] == filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]), "Same", "Problem")
        elif item == 'CATA (SCHIZOAFFECTIVE)':
            new_col_name = 'Schizoaffective (Catatonia) Count Comparison'
            filtered_full_db['Schizoaffective Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c26'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = np.where((filtered_full_db['Schizoaffective Catatonia Count [MINE]'] == filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]), "Same", "Problem")    
        elif item == 'CATA (BRIEF PSYCHOTIC DISORDER)':
            new_col_name = 'Brief Psychotic Disorder (Catatonia) Count Comparison'
            filtered_full_db['Brief Psychotic Disorder Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c44'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = np.where((filtered_full_db['Brief Psychotic Disorder Catatonia Count [MINE]'] == filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]), "Same", "Problem")

    # Creating Criterion Count Discrepancy Values (scid - mine)
    for item in criterion_w_cnt_items_cleaned:
        if 'Criterion ' + item + ' Count [MINE]' in filtered_full_db.columns:
            if 'Criterion ' + item + ' Count' == 'Criterion C (PDD) Count':
                new_col_name = 'B+C (PDD) Count Discrepancy'
                filtered_full_db[new_col_name] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]] - filtered_full_db['Criterion B+C (PDD) Count [MINE]']
            else:    
                new_col_name = item + ' Count Discrepancy'
                filtered_full_db[new_col_name] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]] - filtered_full_db['Criterion ' + item + ' Count [MINE]']
        elif item == 'CATA (SCHIZOPHRENIA)':
            new_col_name = 'Schizophrenia (Catatonia) Count Discrepancy'
            filtered_full_db['Schizophrenia Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c10'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]] - filtered_full_db['Schizophrenia Catatonia Count [MINE]']
            filtered_full_db['Schizophrenia Catatonia Count [SCID]'] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]
        elif item == 'CATA (SCHIZOPHRENIFORM)':
            new_col_name = 'Schizophreniform (Catatonia) Count Discrepancy'
            filtered_full_db['Schizophreniform Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c14'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]] - filtered_full_db['Schizophreniform Catatonia Count [MINE]']
            filtered_full_db['Schizophreniform Catatonia Count [SCID]'] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]
        elif item == 'CATA (SCHIZOAFFECTIVE)':
            new_col_name = 'Schizoaffective (Catatonia) Count Discrepancy'
            filtered_full_db['Schizoaffective Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c26'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]] - filtered_full_db['Schizoaffective Catatonia Count [MINE]']
            filtered_full_db['Schizoaffective Catatonia Count [SCID]'] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]
        elif item == 'CATA (BRIEF PSYCHOTIC DISORDER)':
            new_col_name = 'Brief Psychotic Disorder (Catatonia) Count Discrepancy'
            filtered_full_db['Brief Psychotic Disorder Catatonia Count [MINE]'] = np.where(((filtered_full_db['scid_c44'] == 3)), filtered_full_db['Criterion A (CATATONIA) Count [MINE]'], 0)
            filtered_full_db[new_col_name] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]] - filtered_full_db['Brief Psychotic Disorder Catatonia Count [MINE]']
            filtered_full_db['Brief Psychotic Disorder Catatonia Count [SCID]'] = filtered_full_db[rc_criterion_w_cnt_items_cleaned[criterion_w_cnt_items_cleaned.index(item)]]

    # Checking Criterion Validity where applicable (SCID info)
    initial_count_crit_val = 0

    while initial_count_crit_val < len(criterion_w_validation_cleaned):
        if criterion_w_validation_cleaned[initial_count_crit_val] in criterion_w_one_validation_cleaned:
            new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
            cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
            filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] >= 1)) |
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0) & (filtered_full_db[cnt_item] == 0)) | 
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & (filtered_full_db[cnt_item] < 1))), "No Problem",
            np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 1)), "Problem", "Should be coded"))
            initial_count_crit_val += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val] in criterion_w_two_validations_cleaned:
            new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
            cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
            filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] >= 2)) |
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0) & (filtered_full_db[cnt_item] == 0)) | 
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & (filtered_full_db[cnt_item] < 2))), "No Problem",
            np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 2)), "Problem", "Should be coded"))
            initial_count_crit_val += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val] in criterion_w_three_validations_cleaned:
            if "CATA" in criterion_w_validation_cleaned[initial_count_crit_val]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & (filtered_full_db[cnt_item] >= 3)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0) & (filtered_full_db[cnt_item] == 0)) | 
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0) & (filtered_full_db[cnt_item] < 3))), "No Problem",
                np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & (filtered_full_db[cnt_item] < 3)), "Problem", "Should be coded"))
                initial_count_crit_val += 1
            else:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] >= 3)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0) & (filtered_full_db[cnt_item] == 0)) | 
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & (filtered_full_db[cnt_item] < 3))), "No Problem",
                np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 3)), "Problem", "Should be coded"))
                initial_count_crit_val += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val] in criterion_w_special_validations_cleaned:
            if "CMDE" in criterion_w_validation_cleaned[initial_count_crit_val]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where(((((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & (filtered_full_db[cnt_item] >= 5) &
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) |
                (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[cnt_item] == 0) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0)) | 
                (((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & (filtered_full_db[cnt_item] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & ((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[cnt_item] >= 5))|
                (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[cnt_item] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1))),
                "No Problem", np.where(((((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & (filtered_full_db[cnt_item] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) | (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[cnt_item] >= 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) | (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[cnt_item] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3))), "Problem", "Should be coded"))
                initial_count_crit_val += 1
            elif "PMDE" in criterion_w_validation_cleaned[initial_count_crit_val]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where(((((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & (filtered_full_db[cnt_item] >= 5) &
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) |
                (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[cnt_item] == 0) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 0)) | 
                (((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & (filtered_full_db[cnt_item] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1) & ((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[cnt_item] >= 5))|
                (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[cnt_item] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 1))),
                "No Problem", np.where(((((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & (filtered_full_db[cnt_item] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) | (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[cnt_item] >= 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) | (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[cnt_item] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3))), "Problem", "Should be coded"))
                initial_count_crit_val += 1
            elif "CME" in criterion_w_validation_cleaned[initial_count_crit_val]:
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db['A (CME) [MINE]'] == 1) & (filtered_full_db['scid_a57'] == 3)) | ((filtered_full_db['A (CME) [MINE]'] == 0) & (filtered_full_db['scid_a57'] != 3))), "No Problem",
                    np.where(((filtered_full_db['A (CME) [MINE]'] == 0) & (filtered_full_db['scid_a57'] == 3)), "Problem", "Should be Coded"))
                    initial_count_crit_val += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 3) &
                    ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & 
                    (filtered_full_db[cnt_item] < 4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >= 3) & ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >=4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & 
                    ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val += 1
                else:
                    initial_count_crit_val += 1
            elif "PME" in criterion_w_validation_cleaned[initial_count_crit_val]:
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db['A (PME) [MINE]'] == 1) & (filtered_full_db['scid_a95'] == 3)) | ((filtered_full_db['A (PME) [MINE]'] == 0) & (filtered_full_db['scid_a95'] != 3))), "No Problem",
                    np.where(((filtered_full_db['A (PME) [MINE]'] == 0) & (filtered_full_db['scid_a95'] == 3)), "Problem", "Should be Coded"))
                    initial_count_crit_val += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 3) &
                    ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & 
                    (filtered_full_db[cnt_item] < 4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >= 3) & ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >=4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & 
                    ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val += 1
                else:
                    initial_count_crit_val += 1
            elif "CHME" in criterion_w_validation_cleaned[initial_count_crit_val]:
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db['A (CHME) [MINE]'] == 0) & (filtered_full_db['scid_a72'] == 3)), "Problem", 
                                                                       np.where(((filtered_full_db['A (CHME) [MINE]'] == 1) & (filtered_full_db['scid_a72'] != 3)), "Should be Coded", "No Problem"))
                    initial_count_crit_val += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 3) &
                    ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & 
                    (filtered_full_db[cnt_item] < 4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >= 3) & ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >=4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & 
                    ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val += 1
                else:
                    initial_count_crit_val += 1
            elif "PHME" in criterion_w_validation_cleaned[initial_count_crit_val]: 
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db['A (PHME) [MINE]'] == 0) & (filtered_full_db['scid_a110'] == 3)), "Problem", 
                                                                       np.where(((filtered_full_db['A (PHME) [MINE]'] == 1) & (filtered_full_db['scid_a110'] != 3)), "Should be Coded", "No Problem"))
                    initial_count_crit_val += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                    cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 3) &
                    ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & 
                    (filtered_full_db[cnt_item] < 4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >= 3) & ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >=4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & 
                    ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val += 1  
                else:
                    initial_count_crit_val += 1
            elif "B+C" in criterion_w_validation_cleaned[initial_count_crit_val]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[cnt_item] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)), "Problem", 
                np.where(((filtered_full_db[cnt_item] > 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3)), "Should be Coded", "No Problem"))  
                initial_count_crit_val += 1
            elif "P (LPD)" in criterion_w_validation_cleaned[initial_count_crit_val]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[cnt_item] < 4) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3)) | 
                ((filtered_full_db[cnt_item] >= 4) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db['scid_f2'] != 3))), "Problem", 
                np.where(((filtered_full_db[cnt_item] >= 4) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db['scid_f2'] == 3)), "Should be Coded", "No Problem"))
                initial_count_crit_val += 1
            elif "ADHD" in criterion_w_validation_cleaned[initial_count_crit_val]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val] + ' Validation [SCID]'
                cnt_item = rc_items_for_criterion_validation_cleaned[initial_count_crit_val] + "cnt"
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] == 3) & (filtered_full_db[cnt_item] < 5)), "Problem",
                np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val]] != 3) & (filtered_full_db[cnt_item] >= 5)), "Should be Coded", "No Problem"))
                initial_count_crit_val += 1
            else:
                initial_count_crit_val += 1
        else:
           initial_count_crit_val += 1

    # Creating an A/B/C (MDD) Validation + A (ADHD) Validation (SCID) + B (LPD) Validation (SCID) + A (BID) Validation (SCID) + A (BIID) Validation (SCID)
    filtered_full_db['Criterion A/B/C (MDD) Validation [SCID]'] = np.where(((((filtered_full_db['scid_a25'] != 3) & (filtered_full_db['scid_a51'] != 3)) & (filtered_full_db['scid_d26'] == 3))), "Problem", 
                                                                  np.where(((((filtered_full_db['scid_a25'] == 3) | (filtered_full_db['scid_a51'] == 3)) & (filtered_full_db['scid_d26'] != 3))), "Should be Coded", "No Problem"))
    filtered_full_db['Criterion A (ADHD) Validation [SCID]'] = np.where((((filtered_full_db['scid_k13'] != 3) & (filtered_full_db['scid_k23'] != 3)) & (filtered_full_db['scid_k24'] == 3)), "Problem", 
                                                               np.where((((filtered_full_db['scid_k13'] == 3) | (filtered_full_db['scid_k23'] == 3)) & (filtered_full_db['scid_k24'] != 3)), "Should be coded", "No Problem"))
    filtered_full_db['Criterion B (LPD) Validation [SCID]'] = np.where((((filtered_full_db['scid_f18'] != 3) & (filtered_full_db['scid_f19'] != 3)) & (filtered_full_db['scid_f20'] == 3)), "Problem", 
                                                            np.where((((filtered_full_db['scid_f18'] == 3) | (filtered_full_db['scid_f19'] == 3)) & (filtered_full_db['scid_f20'] != 3)), "Should be coded", "No Problem"))
    filtered_full_db['Criterion A (BID) Validation [SCID]'] = np.where(((filtered_full_db['scid_a70'] != 3) & (filtered_full_db['scid_a108'] != 3) & (filtered_full_db['scid_d2'] == 3)), "Problem", 
                                                                       np.where((((filtered_full_db['scid_a70'] == 3) | (filtered_full_db['scid_a108'] == 3)) & (filtered_full_db['scid_d2'] != 3)), "Should be Coded", "No Problem"))
    filtered_full_db['Criterion A (BIID) Validation [SCID]'] = np.where(((filtered_full_db['scid_a25'] != 3) & (filtered_full_db['scid_a51'] != 3) & (filtered_full_db['scid_a91'] != 3) & (filtered_full_db['scid_a129'] != 3) & (filtered_full_db['scid_d5'] == 3)), "Problem", 
                                                                        np.where(((((filtered_full_db['scid_a25'] == 3) | (filtered_full_db['scid_a51'] == 3)) & ((filtered_full_db['scid_a91'] == 3) | (filtered_full_db['scid_a129'] == 3))) & (filtered_full_db['scid_d5'] != 3)), "Should be Coded", "No Problem"))

    # Checking Criterion Validity where applicable (My counts)
    initial_count_crit_val_my = 0

    while initial_count_crit_val_my < len(criterion_w_validation_cleaned):
        if criterion_w_validation_cleaned[initial_count_crit_val_my] in criterion_w_one_validation_cleaned:
            new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
            filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 1)) |
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1)) | 
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1))), "No Problem",
            np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1)), "Problem", "Should be coded"))
            initial_count_crit_val_my += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val_my] in criterion_w_two_validations_cleaned:
            new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
            filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 2)) |
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 2)) | 
            ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 2))), "No Problem",
            np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 2)), "Problem", "Should be coded"))
            initial_count_crit_val_my += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val_my] in criterion_w_three_validations_cleaned:
            if "CATA" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3)) | 
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3))), "No Problem",
                np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3)), "Problem", "Should be coded"))
                initial_count_crit_val_my += 1
            else:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3)) | 
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3))), "No Problem",
                np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3)), "Problem", "Should be coded"))
                initial_count_crit_val_my += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val_my] in criterion_w_special_validations_cleaned:
            if "CMDE" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5) &
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)) |
                (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] == 0) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0)) | 
                (((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & ((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5))|
                (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1))),
                "No Problem", np.where(((((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)) | (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)) | (((filtered_full_db['A1 (CMDE)'] == 0) & (filtered_full_db['A2 (CMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3))), "Problem", "Should be coded"))
                initial_count_crit_val_my += 1
            elif "PMDE" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5) &
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)) |
                (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] == 0) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0)) | 
                (((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1)) |
                ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & ((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5))|
                (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1))),
                "No Problem", np.where(((((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)) | (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)) | (((filtered_full_db['A1 (PMDE)'] == 0) & (filtered_full_db['A2 (PMDE)'] == 0)) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & 
                (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3))), "Problem", "Should be coded"))
                initial_count_crit_val_my += 1
            elif "CME" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db['A (CME) [MINE]'] == 1) & (filtered_full_db['scid_a57'] == 3)) | ((filtered_full_db['A (CME) [MINE]'] == 0) & (filtered_full_db['scid_a57'] != 3))), "No Problem",
                    np.where(((filtered_full_db['A (CME) [MINE]'] == 0) & (filtered_full_db['scid_a57'] == 3)), "Problem", "Should be Coded"))
                    initial_count_crit_val_my += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3) &
                    ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3) & ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >=4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & 
                    ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val_my += 1
                else:
                    initial_count_crit_val_my += 1
            elif "PME" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db['A (PME) [MINE]'] == 1) & (filtered_full_db['scid_a95'] == 3)) | ((filtered_full_db['A (PME) [MINE]'] == 0) & (filtered_full_db['scid_a95'] != 3))), "No Problem",
                    np.where(((filtered_full_db['A (PME) [MINE]'] == 0) & (filtered_full_db['scid_a95'] == 3)), "Problem", "Should be Coded"))
                    initial_count_crit_val_my += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3) &
                    ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3) & ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >=4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & 
                    ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val_my += 1
                else:
                    initial_count_crit_val_my += 1
            elif "CHME" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db['A (CHME) [MINE]'] == 0) & (filtered_full_db['scid_a72'] == 3)), "Problem", 
                                                                       np.where(((filtered_full_db['A (CHME) [MINE]'] == 1) & (filtered_full_db['scid_a72'] != 3)), "Should be Coded", "No Problem"))
                    initial_count_crit_val_my += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3) &
                    ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3) & ((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >=4) & ((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3) & 
                    ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val_my += 1
                else:
                    initial_count_crit_val_my += 1 
            elif "PHME" in criterion_w_validation_cleaned[initial_count_crit_val_my]: 
                if "A" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db['A (PHME) [MINE]'] == 0) & (filtered_full_db['scid_a110'] == 3)), "Problem", 
                                                                       np.where(((filtered_full_db['A (PHME) [MINE]'] == 1) & (filtered_full_db['scid_a110'] != 3)), "Should be Coded", "No Problem"))
                    initial_count_crit_val_my += 1
                elif "B" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where((((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3) &
                    ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3))) | ((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3))))), "Problem", 
                    np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3) & ((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3)) |
                    (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >=4) & ((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3) & 
                    ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3)))), "Should be coded", "No Problem"))
                    initial_count_crit_val_my += 1     
                else:
                    initial_count_crit_val_my += 1 
            elif "B+C" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3)), "Problem", 
                np.where(((filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] > 5) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3)), "Should be Coded", "No Problem"))  
                initial_count_crit_val_my += 1
            elif "P (LPD)" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 4) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) | 
                ((filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 4) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db['scid_f2'] != 3))), "Problem", 
                np.where(((filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 4) & (filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db['scid_f2'] == 3)), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            elif "ADHD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5)), "Problem",
                np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5)), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            else:
                st.write(criterion_w_validation_cleaned[initial_count_crit_val_my], " Count Item:", initial_count_crit_val_my)
                initial_count_crit_val_my += 1
        elif criterion_w_validation_cleaned[initial_count_crit_val_my] in criterion_w_no_cnt_validations_cleaned:
            if "PDD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 1)), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            elif "OB/CO" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 1) & 
                (filtered_full_db['OB (LOCD)'] != 1) & (filtered_full_db['CO (LOCD)'] != 1)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 0) & 
                ((filtered_full_db['OB (LOCD)'] == 1) | (filtered_full_db['CO (LOCD)'] == 1))), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            elif "BE" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "APD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 3)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 3)), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            elif "ASD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                if "B" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 9)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 9)), "Should be Coded", "No Problem"))
                    initial_count_crit_val_my += 1
                else:
                    new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                    filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                    (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 1)), "Should be Coded", "No Problem"))
                    initial_count_crit_val_my += 1
            elif "PPD" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "SdPD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 4)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 4)), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            elif "SPD" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "BoPD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 5)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 5)), "Should be Coded", "No Problem"))
                initial_count_crit_val_my += 1
            elif "PTSD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                if "LPTSD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    if "A" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "B" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "C" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                        new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                        filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 1)), "Should be Coded", "No Problem"))
                        initial_count_crit_val_my += 1
                    elif "D" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "E" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                        new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                        filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 2)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 2)), "Should be Coded", "No Problem"))
                        initial_count_crit_val_my += 1
                elif "CPTSD" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                    if "D (CPTSD)" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "E" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                        new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                        filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 2)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 2)), "Should be Coded", "No Problem"))
                        initial_count_crit_val_my += 1
                    elif "A" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "B" in criterion_w_validation_cleaned[initial_count_crit_val_my] or "C" in criterion_w_validation_cleaned[initial_count_crit_val_my]:
                        new_col_name_crit_val = "Criterion " + criterion_w_validation_cleaned[initial_count_crit_val_my] + ' Validation [MINE]'
                        filtered_full_db[new_col_name_crit_val] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] == 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] < 1)), "Problem", np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[initial_count_crit_val_my]] != 3) & 
                        (filtered_full_db[my_cnt_items_for_criterion_validation[initial_count_crit_val_my] + " [MINE]"] >= 1)), "Should be Coded", "No Problem"))
                        initial_count_crit_val_my += 1
                else:
                    pass
            else:
                initial_count_crit_val_my += 1
        else:
           initial_count_crit_val_my += 1 

    # Creating general Criterion Item for ones that were composed of many sub-parts (SCID) # Going to be used later to create syndrome criteria counts to then check diagnosis validity
    for item in criterion_w_validation_cleaned:
        if "CATA" in item or "OB/CO" in item:
            new_col_name_scid = item + " [SCID]"
            filtered_full_db[new_col_name_scid] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)]] == 1)), 1, 0)
        else:
            new_col_name_scid = item + " [SCID]"
            filtered_full_db[new_col_name_scid] = np.where(((filtered_full_db[rc_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)]] == 3)), 1, 0)

    # Creating general Criterion Item for ones that were composed of many sub-parts (MINE)
    for item in criterion_w_validation_cleaned:
        if item in criterion_w_one_validation_cleaned:
            new_col_name_mine = item + " [MINE]"
            filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 1)), 1, 0)
        elif item in criterion_w_two_validations_cleaned:
            new_col_name_mine = item + " [MINE]"
            filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 2)), 1, 0)
        elif item in criterion_w_three_validations_cleaned:
            new_col_name_mine = item + " [MINE]"
            filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 3)), 1, 0)
        elif item in criterion_w_special_validations_cleaned:
            if "CMDE" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where((((filtered_full_db['A1 (CMDE)'] == 1) | (filtered_full_db['A2 (CMDE)'] == 1)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 5)), 1, 0)
            elif "PMDE" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where((((filtered_full_db['A1 (PMDE)'] == 1) | (filtered_full_db['A2 (PMDE)'] == 1)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 5)), 1, 0)
            elif "B (CME)" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where((((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 3)), 1, 
                np.where((((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3)) & ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 4)), 1, 0))
            elif "B (PME)" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where((((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 3)), 1, 
                np.where((((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3)) & ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 4)), 1, 0))
            elif "B (CHME)" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where((((filtered_full_db['scid_a54a'] == 3) | (filtered_full_db['scid_a54c1'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 3)), 1, 
                np.where((((filtered_full_db['scid_a54a'] != 3) & (filtered_full_db['scid_a54c1'] != 3)) & ((filtered_full_db['scid_a54b'] == 3) | (filtered_full_db['scid_a54c2'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 4)), 1, 0))
            elif "B (PHME)" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where((((filtered_full_db['scid_a92a'] == 3) | (filtered_full_db['scid_a92c1'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 3)), 1, 
                np.where((((filtered_full_db['scid_a92a'] != 3) & (filtered_full_db['scid_a92c1'] != 3)) & ((filtered_full_db['scid_a92b'] == 3) | (filtered_full_db['scid_a92c2'] == 3)) & 
                (filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 4)), 1, 0))
            elif "B+C" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 5)), 1, 0)
            elif "P (LPD)" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 4) &
                (filtered_full_db['scid_f2'] == 3)), 1, 0)
            elif "ADHD" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 5)), 1, 0)
        elif item in criterion_w_no_cnt_validations_cleaned:
            if "PDD" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 1)), 1, 0)
            elif "OCD" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db['CO (LOCD)'] == 1) | (filtered_full_db['OB (LOCD)'] == 1)), 1, 0)
            elif "BE" in item or "APD" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 3)), 1, 0)
            elif "ASD" in item:
                if "B" in item:
                    new_col_name_mine = item + " [MINE]"
                    filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 9)), 1, 0)
                else:
                    new_col_name_mine = item + " [MINE]"
                    filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 1)), 1, 0)
            elif "PPD" in item or "SdPD" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 4)), 1, 0)
            elif "SPD" in item or "BoPD" in item:
                new_col_name_mine = item + " [MINE]"
                filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"] >= 5)), 1, 0)
            elif "LPTSD" in item:
                if "A" in item or "B" in item or "C" in item:
                    new_col_name_mine = item + " [MINE]"
                    filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"]) >= 1), 1, 0)
                elif "D" in item or "E" in item:
                    new_col_name_mine = item + " [MINE]"
                    filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"]) >= 2), 1, 0)
                else:
                    st.write(item)
            elif "CPTSD" in item:
                if "D " in item or "E" in item:
                    new_col_name_mine = item + " [MINE]"
                    filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"]) >= 2), 1, 0)
                elif "A" in item or "B" in item or "C" in item:
                    new_col_name_mine = item + " [MINE]"
                    filtered_full_db[new_col_name_mine] = np.where(((filtered_full_db[my_cnt_items_for_criterion_validation_cleaned[criterion_w_validation_cleaned.index(item)] + " [MINE]"]) >= 1), 1, 0)
                else:
                    st.write(item)
        else:
            st.write(item)

    # Creating both [SCID] and [MINE] items for A of ADHD
    filtered_full_db['A (ADHD) [SCID]'] = np.where(((filtered_full_db['scid_k24'] == 3)), 1, 0)
    filtered_full_db['A (ADHD) [MINE]'] = np.where(((filtered_full_db['A1 (ADHD [Inattention]) [MINE]'] == 1) | (filtered_full_db['A2 (ADHD [Hyperactivity]) [MINE]'] == 1)), 1, 0)

    # Creating an A (ADHD) Validation (MINE) [would do an A/B/C (MDD) validation but will need to do the diagnosis validation first]
    filtered_full_db['Criterion A (ADHD) Validation [MINE]'] = np.where((((filtered_full_db['A1 (ADHD [Inattention]) [MINE]'] == 0) & (filtered_full_db['A2 (ADHD [Hyperactivity]) [MINE]'] == 0)) & (filtered_full_db['scid_k24'] == 3)),
                                                                "Problem", np.where((((filtered_full_db['A1 (ADHD [Inattention]) [MINE]'] == 1) | (filtered_full_db['A2 (ADHD [Hyperactivity]) [MINE]'] == 1)) & 
                                                                                    (filtered_full_db['scid_k24'] != 3)), "Should be coded", "No Problem"))

    ########### Changing the name of the SCID count items to look more like mine in order to query more easily # As well as Diagnosis Items

    # SCID Items
    scid_count_item_name_change = ["Criterion " + item + " Count [SCID]"  for item in criterion_w_cnt_items_cleaned]
    scid_count_name_dict = {rc_criterion_w_cnt_items_cleaned[i]:scid_count_item_name_change[i] for i in range(len(scid_count_item_name_change))}
    filtered_full_db = filtered_full_db.astype({rc_criterion_w_cnt_items_cleaned[i]:'int' for i in range(len(rc_criterion_w_cnt_items_cleaned))})
    filtered_full_db = filtered_full_db.rename(columns=scid_count_name_dict)

    # Diagnosis Items
    diagnosis_change_dict = {diagnosis_items_cleaned[i]:diagnosis_names_cleaned[i] for i in range(len(diagnosis_items_cleaned))}
    filtered_full_db = filtered_full_db.astype({diagnosis_items_cleaned[i]:'int' for i in range(len(diagnosis_items_cleaned))})
    filtered_full_db = filtered_full_db.rename(columns = diagnosis_change_dict)

    # Creating Diagnosis Checks (based on SCID info) # 2 steps. 1. Create summation of criteria. 2. Compare summation to number needed for diag
    
    # Step 1: Creating criteria counts
    scid_2_count = 0
    scid_3_count = 0
    scid_4_count = 0
    scid_5_count = 0
    scid_6_count = 0
    scid_7_count = 0
    scid_9_count = 0
    scid_10_count = 0

    for item in syndromes_for_diag_check_cleaned:
        if item in diags_w_2_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            column_list_scid = []
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[two_criteria_diag_items_scid_cleaned[scid_2_count], two_criteria_diag_items_scid_cleaned[scid_2_count + 1]]].sum(axis = 1)
            scid_2_count += 2
        elif item in diags_w_3_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[three_criteria_diag_items_scid_cleaned[scid_3_count], three_criteria_diag_items_scid_cleaned[scid_3_count + 1],
                                                             three_criteria_diag_items_scid_cleaned[scid_3_count + 2]]].sum(axis = 1)
            scid_3_count += 3
        elif item in diags_w_4_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[four_criteria_diag_items_scid_cleaned[scid_4_count], four_criteria_diag_items_scid_cleaned[scid_4_count + 1], 
                                                             four_criteria_diag_items_scid_cleaned[scid_4_count + 2], four_criteria_diag_items_scid_cleaned[scid_4_count + 3]]].sum(axis = 1)
            scid_4_count += 4
        elif item in diags_w_5_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[five_criteria_diag_items_scid_cleaned[scid_5_count], five_criteria_diag_items_scid_cleaned[scid_5_count + 1], 
                                                             five_criteria_diag_items_scid_cleaned[scid_5_count + 2], five_criteria_diag_items_scid_cleaned[scid_5_count + 3],
                                                             five_criteria_diag_items_scid_cleaned[scid_5_count + 4]]].sum(axis = 1)
            scid_5_count += 5
        elif item in diags_w_6_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[six_criteria_diag_items_scid_cleaned[scid_6_count], six_criteria_diag_items_scid_cleaned[scid_6_count + 1],
                                                             six_criteria_diag_items_scid_cleaned[scid_6_count + 2], six_criteria_diag_items_scid_cleaned[scid_6_count + 3],
                                                             six_criteria_diag_items_scid_cleaned[scid_6_count + 4], six_criteria_diag_items_scid_cleaned[scid_6_count + 5]]].sum(axis = 1)
            scid_6_count += 6
        elif item in diags_w_7_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[seven_criteria_diag_items_scid_cleaned[scid_7_count], seven_criteria_diag_items_scid_cleaned[scid_7_count + 1],
                                                             seven_criteria_diag_items_scid_cleaned[scid_7_count + 2], seven_criteria_diag_items_scid_cleaned[scid_7_count + 3], 
                                                             seven_criteria_diag_items_scid_cleaned[scid_7_count + 4], seven_criteria_diag_items_scid_cleaned[scid_7_count + 5], 
                                                             seven_criteria_diag_items_scid_cleaned[scid_7_count + 6]]].sum(axis = 1)
            scid_7_count += 7
        elif item in diags_w_9_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[nine_criteria_diag_items_scid_cleaned[scid_9_count], nine_criteria_diag_items_scid_cleaned[scid_9_count + 1],
                                                             nine_criteria_diag_items_scid_cleaned[scid_9_count + 2], nine_criteria_diag_items_scid_cleaned[scid_9_count + 3],
                                                             nine_criteria_diag_items_scid_cleaned[scid_9_count + 4], nine_criteria_diag_items_scid_cleaned[scid_9_count + 5],
                                                             nine_criteria_diag_items_scid_cleaned[scid_9_count + 6], nine_criteria_diag_items_scid_cleaned[scid_9_count + 7],
                                                             nine_criteria_diag_items_scid_cleaned[scid_9_count + 8]]].sum(axis = 1)
        elif item in diags_w_10_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            filtered_full_db[diagnosis_criteria_scid_name] = filtered_full_db[[ten_criteria_diag_items_scid_cleaned[scid_10_count], ten_criteria_diag_items_scid_cleaned[scid_10_count + 1],
                                                             ten_criteria_diag_items_scid_cleaned[scid_10_count + 2], ten_criteria_diag_items_scid_cleaned[scid_10_count + 3],
                                                             ten_criteria_diag_items_scid_cleaned[scid_10_count + 4], ten_criteria_diag_items_scid_cleaned[scid_10_count + 5],
                                                             ten_criteria_diag_items_scid_cleaned[scid_10_count + 6], ten_criteria_diag_items_scid_cleaned[scid_10_count + 7],
                                                             ten_criteria_diag_items_scid_cleaned[scid_10_count + 8], ten_criteria_diag_items_scid_cleaned[scid_10_count + 9]]].sum(axis = 1)

    # Step 2: Checking if criterion counts meet criteria for a diagnosis
    for item in syndromes_for_diag_check_cleaned:
        if item in diags_w_2_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 2) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 2) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_3_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 3) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 3) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_4_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 4) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 4) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_5_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 5) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 5) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_6_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 6) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 6) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_7_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 7) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 7) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_9_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 9) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 9) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_10_scid_cleaned:
            diagnosis_criteria_scid_name = item + " Criteria Count [SCID]"
            diagnosis_scid_validation_name = item + " Diagnosis Validation [SCID]"
            filtered_full_db[diagnosis_scid_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_scid_name] < 10) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_scid_name] >= 10) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))

    # Creating Diagnosis Checks (based on my counts) # 2 steps. 1. Create summation of criteria. 2. Compare summation to number needed for diag
    
    # Step 1: Creating Criteria Counts
    mine_2_count = 0
    mine_3_count = 0
    mine_4_count = 0
    mine_5_count = 0
    mine_6_count = 0
    mine_7_count = 0
    mine_9_count = 0
    mine_10_count = 0

    for item in syndromes_for_diag_check_cleaned:
        if item in diags_w_2_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            column_list_scid = []
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[two_criteria_diag_items_mine_cleaned[mine_2_count], two_criteria_diag_items_mine_cleaned[mine_2_count + 1]]].sum(axis = 1)
            mine_2_count += 2
        elif item in diags_w_3_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[three_criteria_diag_items_mine_cleaned[mine_3_count], three_criteria_diag_items_mine_cleaned[mine_3_count + 1],
                                                             three_criteria_diag_items_mine_cleaned[mine_3_count + 2]]].sum(axis = 1)
            mine_3_count += 3
        elif item in diags_w_4_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[four_criteria_diag_items_mine_cleaned[mine_4_count], four_criteria_diag_items_mine_cleaned[mine_4_count + 1], 
                                                             four_criteria_diag_items_mine_cleaned[mine_4_count + 2], four_criteria_diag_items_mine_cleaned[mine_4_count + 3]]].sum(axis = 1)
            mine_4_count += 4
        elif item in diags_w_5_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[five_criteria_diag_items_mine_cleaned[mine_5_count], five_criteria_diag_items_mine_cleaned[mine_5_count + 1], 
                                                             five_criteria_diag_items_mine_cleaned[mine_5_count + 2], five_criteria_diag_items_mine_cleaned[mine_5_count + 3],
                                                             five_criteria_diag_items_mine_cleaned[mine_5_count + 4]]].sum(axis = 1)
            mine_5_count += 5
        elif item in diags_w_6_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[six_criteria_diag_items_mine_cleaned[mine_6_count], six_criteria_diag_items_mine_cleaned[mine_6_count + 1],
                                                             six_criteria_diag_items_mine_cleaned[mine_6_count + 2], six_criteria_diag_items_mine_cleaned[mine_6_count + 3],
                                                             six_criteria_diag_items_mine_cleaned[mine_6_count + 4], six_criteria_diag_items_mine_cleaned[mine_6_count + 5]]].sum(axis = 1)
            mine_6_count += 6
        elif item in diags_w_7_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[seven_criteria_diag_items_mine_cleaned[mine_7_count], seven_criteria_diag_items_mine_cleaned[mine_7_count + 1],
                                                             seven_criteria_diag_items_mine_cleaned[mine_7_count + 2], seven_criteria_diag_items_mine_cleaned[mine_7_count + 3], 
                                                             seven_criteria_diag_items_mine_cleaned[mine_7_count + 4], seven_criteria_diag_items_mine_cleaned[mine_7_count + 5], 
                                                             seven_criteria_diag_items_mine_cleaned[mine_7_count + 6]]].sum(axis = 1)
            mine_7_count += 7
        elif item in diags_w_9_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[nine_criteria_diag_items_mine_cleaned[mine_9_count], nine_criteria_diag_items_mine_cleaned[mine_9_count + 1],
                                                             nine_criteria_diag_items_mine_cleaned[mine_9_count + 2], nine_criteria_diag_items_mine_cleaned[mine_9_count + 3],
                                                             nine_criteria_diag_items_mine_cleaned[mine_9_count + 4], nine_criteria_diag_items_mine_cleaned[mine_9_count + 5],
                                                             nine_criteria_diag_items_mine_cleaned[mine_9_count + 6], nine_criteria_diag_items_mine_cleaned[mine_9_count + 7],
                                                             nine_criteria_diag_items_mine_cleaned[mine_9_count + 8]]].sum(axis = 1)
        elif item in diags_w_10_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            filtered_full_db[diagnosis_criteria_mine_name] = filtered_full_db[[ten_criteria_diag_items_mine_cleaned[mine_10_count], ten_criteria_diag_items_mine_cleaned[mine_10_count + 1],
                                                             ten_criteria_diag_items_mine_cleaned[mine_10_count + 2], ten_criteria_diag_items_mine_cleaned[mine_10_count + 3],
                                                             ten_criteria_diag_items_mine_cleaned[mine_10_count + 4], ten_criteria_diag_items_mine_cleaned[mine_10_count + 5],
                                                             ten_criteria_diag_items_mine_cleaned[mine_10_count + 6], ten_criteria_diag_items_mine_cleaned[mine_10_count + 7],
                                                             ten_criteria_diag_items_mine_cleaned[mine_10_count + 8], ten_criteria_diag_items_mine_cleaned[mine_10_count + 9]]].sum(axis = 1)

    # Step 2: Checking if criterion counts meet criteria for a diagnosis
    for item in syndromes_for_diag_check_cleaned:
        if item in diags_w_2_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 2) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 2) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_3_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 3) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 3) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_4_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 4) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 4) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_5_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 5) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 5) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_6_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 6) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 6) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_7_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 7) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 7) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_9_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 9) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 9) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))
        elif item in diags_w_10_scid_cleaned:
            diagnosis_criteria_mine_name = item + " Criteria Count [MINE]"
            diagnosis_mine_validation_name = item + " Diagnosis Validation [MINE]"
            filtered_full_db[diagnosis_mine_validation_name] = np.where(((filtered_full_db[diagnosis_criteria_mine_name] < 10) & (filtered_full_db[item + " Diagnosis"] == 3)), "Problem", 
                                                               np.where(((filtered_full_db[diagnosis_criteria_mine_name] >= 10) & (filtered_full_db[item + " Diagnosis"] != 3)), "Should be Coded", "No Problem"))

    # Creating an A/B/C (MDD) Validation Item # Also creating BID/BIID validation items # Using Criteria Counts to see if diagnosis is met
    filtered_full_db['Criterion A/B/C (MDD) Validation [MINE]'] = np.where(((((filtered_full_db['CMDE Criteria Count [MINE]'] < 3) & (filtered_full_db['PMDE Criteria Count [MINE]'] < 3)) & (filtered_full_db['A/B/C (MDD)'] == 1))), "Problem", 
                                                                  np.where(((((filtered_full_db['CMDE Criteria Count [MINE]'] >= 3) | (filtered_full_db['PMDE Criteria Count [MINE]'] >= 3)) & (filtered_full_db['A/B/C (MDD)'] == 0))), "Should be Coded", "No Problem"))
    filtered_full_db['Criterion A (BID) Validation [MINE]'] = np.where((((filtered_full_db['CME Criteria Count [MINE]'] < 4) & (filtered_full_db['PME Criteria Count [MINE]'] < 4) & (filtered_full_db['A (BID)'] == 1))), "Problem",
                                                                       np.where((((filtered_full_db['CME Criteria Count [MINE]'] >= 4) | (filtered_full_db['PME Criteria Count [MINE]'] >= 4)) & (filtered_full_db['A (BID)'] == 0)), "Should be Coded", "No Problem"))
    filtered_full_db['Criterion A (BIID) Validation [MINE]'] = np.where(((((filtered_full_db['CMDE Criteria Count [MINE]'] < 3) & (filtered_full_db['PMDE Criteria Count [MINE]'] < 3)) | ((filtered_full_db['CHME Criteria Count [MINE]'] < 6) & (filtered_full_db['PHME Criteria Count [MINE]'] < 6))) & (filtered_full_db['A (BIID)'] == 1)), "Problem",
                                                                         np.where(((((filtered_full_db['CMDE Criteria Count [MINE]'] >= 3) | (filtered_full_db['PMDE Criteria Count [MINE]'] >= 3)) & ((filtered_full_db['CHME Criteria Count [MINE]'] >= 6) | (filtered_full_db['PHME Criteria Count [MINE]'] >= 6))) & (filtered_full_db['A (BIID)'] == 0)), "Should be Coded", "No Problem"))

######################################################################### Creating Master Discrepant DBs #######################################################################################
    # Diagnosis Master DB
    filtered_full_db = filtered_full_db.set_index('subject_id')
    personality_disorder_list = ["Criterion A (PPD) Validation [MINE]", "Criterion A (SPD) Validation [MINE]", "Criterion A (SdPD) Validation [MINE]", "Criterion A (BoPD) Validation [MINE]", "Criterion A (APD) Validation [MINE]"]
    discrepant_columns_diag = [col for col in filtered_full_db.columns if "Diagnosis Validation" in col] + [col for col in filtered_full_db.columns if "SUD" in col and "Validation" in col] + personality_disorder_list + [col for col in filtered_full_db.columns if "AUD" in col and "Validation" in col]
    diagnosis_discrepany_db = filtered_full_db[discrepant_columns_diag]
    diagnosis_validation_columns = diagnosis_discrepany_db.columns.tolist()
    diag_validation_count = 0
    Master_list_diag = []
    while diag_validation_count < len(diagnosis_validation_columns):
        needed_ids = diagnosis_discrepany_db.index[diagnosis_discrepany_db[diagnosis_validation_columns[diag_validation_count]] != 'No Problem'].tolist()
        Master_list_diag.append(needed_ids)
        diag_validation_count += 1

    maxLen_diag = max(len(item) for item in Master_list_diag)
    for item in Master_list_diag:
        while len(item) < maxLen_diag:
            item.append(None)

    master_dictionary_diag = dict(zip(diagnosis_validation_columns, Master_list_diag))
    master_db_diag = pd.DataFrame.from_dict(master_dictionary_diag)
    filtered_master_db_diag = master_db_diag.dropna(axis = 1, how = 'all')
    
    # Count Master DB
    discrepant_columns_count =  [col for col in filtered_full_db.columns if "Count Comparison" in col]
    count_discrepany_db = filtered_full_db[discrepant_columns_count]
    count_validation_columns = count_discrepany_db.columns.tolist()

    count_validation_count = 0
    Master_list_count = []
    while count_validation_count < len(count_validation_columns):
        needed_ids = count_discrepany_db.index[count_discrepany_db[count_validation_columns[count_validation_count]] != 'Same'].tolist()
        Master_list_count.append(needed_ids)
        count_validation_count += 1

    maxLen_count = max(len(item) for item in Master_list_count)
    for item in Master_list_count:
        while len(item) < maxLen_count:
            item.append(None)

    master_dictionary_count = dict(zip(count_validation_columns, Master_list_count))
    master_db_count = pd.DataFrame.from_dict(master_dictionary_count)
    filtered_master_db_count = master_db_count.dropna(axis = 1, how = 'all')

    # Criterion Master DB
    discrepant_columns_criteria =  [col for col in filtered_full_db.columns if "Criterion" in col and "Validation" in col]
    criteria_discrepany_db = filtered_full_db[discrepant_columns_criteria]
    criteria_validation_columns = criteria_discrepany_db.columns.tolist()

    criteria_validation_count = 0
    Master_list_criteria = []
    while criteria_validation_count < len(criteria_validation_columns):
        needed_ids = criteria_discrepany_db.index[criteria_discrepany_db[criteria_validation_columns[criteria_validation_count]] != 'No Problem'].tolist()
        Master_list_criteria.append(needed_ids)
        criteria_validation_count += 1

    maxLen_criteria = max(len(item) for item in Master_list_criteria)
    for item in Master_list_criteria:
        while len(item) < maxLen_criteria:
            item.append(None)

    master_dictionary_criteria = dict(zip(criteria_validation_columns, Master_list_criteria))
    master_db_criteria = pd.DataFrame.from_dict(master_dictionary_criteria)
    filtered_master_db_criteria = master_db_criteria.dropna(axis = 1, how = 'all')

####################################################################### Creating a Slimmed Comparison DB ########################################################################################
    # Just having the Validation items and count discrepancy items
    slim_columns = [col for col in filtered_full_db.columns if "Count Comparison" in col] + [col for col in filtered_full_db.columns if "Validation" in col]
    slim_comparison_db = filtered_full_db[slim_columns]

################################################################################ Dashboard Components ##########################################################################################
    individual_data_files = st.sidebar.checkbox("Individual Data Files")
    first_selection = st.sidebar.selectbox("What would you like to look at?", ["", "Specific Disorder", "Interviewer", "Subject_id"])

    if individual_data_files:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Full Database', 'Filtered Database', 'Discrepancy Database', 'Only Discrepant IDs', 'Just the Facts'])
        with tab1:
            st.write("This is the complete data set before anything was done to it.")
            full_db = full_db.set_index('subject_id')
            st.write(full_db)
            csv = convert_df(full_db)
            st.download_button("Download Data as a CSV", data=csv, file_name = f'full_vumc_dataset_{today}.csv', mime = 'text/csv')
            st.write("Number of subjects:", len(full_db.index))
        with tab2:
            st.write("This is the filtered data set using the parameters: dx1 != 47 and scid_iscomplete == yes. Unlike the previous dashboard, the reliability subjects are included.")
            full_db = full_db[(full_db['scid_iscomplete'] == 'Yes') & (full_db['dx1'] != 47)]
            st.write(full_db)
            st.download_button("Download Data as a CSV", data=csv, file_name = f'filtered_vumc_dataset_{today}.csv', mime = 'text/csv')
            st.write("Number of subjects:", len(full_db.index))
        with tab4:
            discrepancy_filter = st.selectbox("Which discrepancy would you like to explore?", ['', "Count Discrepancies", "Criterion Validation", "Diagnostic Problems"])
            if discrepancy_filter == 'Count Discrepancies':
                st.write("The table below shows the IDs that have count discrepancies between the count item in the SCID and the actual symptom count.")
                st.write(filtered_master_db_count)
                csv = convert_df(filtered_master_db_count)
                st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_count_vumc_id_dataset_mine_{today}.csv', mime = 'text/csv')
                subject_count_disc = filtered_master_db_count.count()
                subject_count_disc = subject_count_disc.rename('Number of Subjects')
                st.write(subject_count_disc)
                csv = convert_df(subject_count_disc)
                st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_counts_id_diag_count_{today}.csv', mime = 'text/csv')
                st.write("Number of Discrepant Disorders: ", len(filtered_master_db_count.columns.tolist()))
            elif discrepancy_filter == "Criterion Validation":
                st.write("For this dashboard, I created a validation based on the info provided in the interview as marked and then with my own criteria using the actual counts of symptoms.")
                st.write("Using the toggle below, you can decide which set you would like to look at.")
                criterion_discrepancy_filter = st.selectbox("Which Validations would you like to look at?", ['', 'Mine', 'SCID', 'Both'])
                if criterion_discrepancy_filter == 'Mine':
                    # Selecting only the "MINE" columns
                    my_cols_criteria = [col for col in filtered_master_db_criteria.columns if "[MINE]" in col]
                    filtered_master_db_mine_criteria = filtered_master_db_criteria[my_cols_criteria]
                    st.write(filtered_master_db_mine_criteria)
                    csv = convert_df(filtered_master_db_mine_criteria)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_criteria_vumc_id_dataset_mine_{today}.csv', mime = 'text/csv')
                    subject_count_mine_criteria = filtered_master_db_mine_criteria.count()
                    subject_count_mine_criteria = subject_count_mine_criteria.rename("Number of Subjects")
                    st.write(subject_count_mine_criteria)
                    csv = convert_df(subject_count_mine_criteria)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_criteria_mine_id_diag_count_{today}.csv', mime = 'text/csv')
                    st.write("Number of Discrepant Disorders: ",len(filtered_master_db_mine_criteria.columns.tolist()))
                elif criterion_discrepancy_filter == 'SCID':
                    scid_cols_criteria = [col for col in filtered_master_db_criteria.columns if "[SCID]" in col]
                    filtered_master_db_scid_criteria = filtered_master_db_criteria[scid_cols_criteria]
                    st.write(filtered_master_db_scid_criteria)
                    csv = convert_df(filtered_master_db_scid_criteria)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_criteria_vumc_id_dataset_scid_{today}.csv', mime = 'text/csv')
                    subject_count_scid_criteria = filtered_master_db_scid_criteria.count()
                    subject_count_scid_criteria = subject_count_scid_criteria.rename("Number of Subjects")
                    st.write(subject_count_scid_criteria)
                    csv = convert_df(subject_count_scid_criteria)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_criteria_scid_id_diag_count_{today}.csv', mime = 'text/csv')
                    st.write("Number of Discrepant Disorders: ",len(filtered_master_db_scid_criteria.columns.tolist()))
                elif criterion_discrepancy_filter == 'Both':
                    st.write(filtered_master_db_criteria)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_criteria_vumc_id_dataset_both_{today}.csv', mime = 'text/csv')
                    subject_count_both_criteria = filtered_master_db_criteria.count()
                    subject_count_both_criteria = subject_count_both_criteria.rename("Number of Subjects")
                    st.write(subject_count_both_criteria)
                    csv = convert_df(subject_count_both_criteria)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_criteria_both_id_diag_count_{today}.csv', mime = 'text/csv')
                    st.write("Number of Discrepant Disorders: ", (len(filtered_master_db_diag.columns.tolist()))/2)
            elif discrepancy_filter == "Diagnostic Problems":
                st.write("For this dashboard, I created a validation based on the info provided in the interview as marked and then with my own criteria using the actual counts of symptoms.")
                st.write("Using the toggle below, you can decide which set you would like to look at.")
                diagnosis_discrepancy_filter = st.selectbox("Which Validations would you like to look at?", ['', 'Mine', 'SCID', 'Both'])
                if diagnosis_discrepancy_filter == 'Mine':
                    # Creating a file that only returns discrepant ids
                    my_cols = [col for col in filtered_master_db_diag.columns if "[MINE]" in col]
                    filtered_master_db_mine = filtered_master_db_diag[my_cols]
                    st.write(filtered_master_db_mine)
                    csv = convert_df(filtered_master_db_mine)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_diag_vumc_id_dataset_mine_{today}.csv', mime = 'text/csv')
                    subject_count_mine_diag = filtered_master_db_mine.count()
                    subject_count_mine_diag = subject_count_mine_diag.rename("Number of Subjects")
                    st.write(subject_count_mine_diag)
                    csv = convert_df(subject_count_mine_diag)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_diag_mine_id_diag_count_{today}.csv', mime = 'text/csv')
                    st.write("Number of Discrepant Disorders: ",len(filtered_master_db_mine.columns.tolist()))
                elif diagnosis_discrepancy_filter == 'SCID':
                    scid_cols = [col for col in filtered_master_db_diag.columns if "[SCID]" in col]
                    filtered_master_db_scid = filtered_master_db_diag[scid_cols]
                    st.write(filtered_master_db_scid)
                    csv = convert_df(filtered_master_db_scid)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_vumc_id_dataset_scid_{today}.csv', mime = 'text/csv')
                    subject_count_scid_diag = filtered_master_db_scid.count()
                    subject_count_scid_diag = subject_count_scid_diag.rename("Number of Subjects")
                    st.write(subject_count_scid_diag)
                    csv = convert_df(subject_count_scid_diag)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_scid_id_diag_count_{today}.csv', mime = 'text/csv')
                    st.write("Number of Discrepant Disorders: ",len(filtered_master_db_scid.columns.tolist()))
                elif diagnosis_discrepancy_filter == 'Both':
                    st.write(filtered_master_db_diag)
                    csv = convert_df(filtered_master_db_diag)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_diags_vumc_id_dataset_both_{today}.csv', mime = 'text/csv')
                    subject_count_both_diag = filtered_master_db_diag.count()
                    subject_count_both_diag = subject_count_both_diag.rename("Number of Subjects")
                    st.write(subject_count_both_diag)
                    csv = convert_df(subject_count_both_diag)
                    st.download_button("Download Data as a CSV", data=csv, file_name = f'discrepant_diags_both_id_diag_count_{today}.csv', mime = 'text/csv')
                    st.write("Number of Discrepant Disorders: ", (len(filtered_master_db_diag.columns.tolist()))/2)
                else:
                    st.write("Please select a filter criteria to get data export!")
            else:
                st.write("In this tab you can select which problems you would like to look at.")
                st.write("- There are three options:")
                st.write("1. Count Discrepancies")
                st.write("2. Criterion Validation Discrepancies")
                st.write("3. Diagnostic Problems")
                st.write("Use the toggle above to select which discrepancy you would like to look at.")
                st.write("For this dashboard, I created a validation based on the info provided in the interview as marked and then with my own criteria using the actual counts of symptoms.")
                st.write("Using the toggle above, you can decide which set you would like to look at.")
        with tab3:
            st.write("Below is the database that contains all of the items and validation columns created to form this dashboard.")
            st.write("If you'd like to see only discrepant IDs and/or their associated interviewers select the boxes below.")
            st.markdown("- Discrepant IDs are only associated with diagnostic discrepancies and may or may not include subjects with count problems or criterion validation.")
            only_ids = st.checkbox("Only Discrepant IDs?")
            associated_ints = st.checkbox("See Associated Interviewers?")
            if associated_ints:
                if only_ids:
                    count = 0
                    subject_id_list = []
                    columns = filtered_master_db_diag.columns.tolist()
                    while count < len(columns):
                        subject_id_list.append(filtered_master_db_diag[columns[count]].values)
                        count += 1
                    subject_id_list_1 = [x for x in subject_id_list if str(x) != None]
                    flat_list = [item for sublist in subject_id_list_1 for item in sublist]
                    cleaned_flat_list = [x for x in flat_list if x != None]
                    only_wanted_ids = []
                    for x in cleaned_flat_list:
                        if x not in only_wanted_ids:
                            only_wanted_ids.append(x)
                    Interviewer_data = filtered_full_db.loc[only_wanted_ids, "scid_interviewername"]
                    refined_data_2 = slim_comparison_db.loc[only_wanted_ids, :]
                    final_data = pd.concat([Interviewer_data, refined_data_2], axis = 1)
                    st.write("Only Discrepant Diagnoses IDs: ")
                    st.dataframe(final_data)
                    csv = convert_df(final_data)
                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'VUMC_Discrepant_ids_and_ints_{today}.csv', mime = 'text/csv')
                    st.write("Number of discrepant subjects:", len(final_data.index))
            elif only_ids:
                count = 0
                subject_id_list = []
                columns = filtered_master_db_diag.columns.tolist()
                while count < len(columns):
                    subject_id_list.append(filtered_master_db_diag[columns[count]].values)
                    count += 1
                subject_id_list_1 = [x for x in subject_id_list if str(x) != None]
                flat_list = [item for sublist in subject_id_list_1 for item in sublist]
                cleaned_flat_list = [x for x in flat_list if x != None]
                only_wanted_ids = []
                for x in cleaned_flat_list:
                    if x not in only_wanted_ids:
                        only_wanted_ids.append(x)
                refined_data = slim_comparison_db.loc[only_wanted_ids, :]
                st.write("Only Discrepant Diagnoses IDs: ")
                st.dataframe(refined_data)
                csv = convert_df(refined_data)
                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'VUMC_Discrepant_ids_{today}.csv', mime = 'text/csv')
                st.write("Number of Discrepant IDs: ", len(refined_data.index))
            else:
                st.write("Everything:")
                st.dataframe(slim_comparison_db)
                csv = convert_df(slim_comparison_db)
                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'VUMC_slim_db_{today}.csv', mime = 'text/csv')
        with tab5:
            st.write("Below is a database that just has the discrepant subject_ids, their interviewer, and a list of their associated problems.")
            st.write("If you want more info on where these discrepancies lie, you will need to dive into the problem toggle in the sidebar.")
            problem_list_db = pd.DataFrame(columns=['subject_id', "QC_Problems"])
            for subject_id in slim_comparison_db.index:
                problem_columns = slim_comparison_db.loc[subject_id][(slim_comparison_db.loc[subject_id] == 'Problem') | (slim_comparison_db.loc[subject_id] == 'Should be Coded')].index.tolist()
                if problem_columns:
                    problem_list_db = problem_list_db.append({'subject_id':subject_id, 'QC_Problems': problem_columns}, ignore_index = True)
            problem_subject_list = problem_list_db['subject_id'].values.tolist()
            scid_interviewer_list = filtered_full_db.loc[problem_subject_list, 'scid_interviewername']
            problem_list_db = problem_list_db.set_index('subject_id')
            final_problem_list_db = pd.concat([scid_interviewer_list, problem_list_db], axis = 1)
            st.write(final_problem_list_db)
            st.write("Number of Problem Subjects", len(problem_subject_list))
            csv = convert_df(final_problem_list_db)
            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'VUMC_problem_subjects_{today}.csv', mime = 'text/csv')

    if first_selection == "" and not individual_data_files:
        st.markdown("## General Info")
        st.markdown("---")
        st.markdown("- This dashboard was created to do a comprehensive second level QC of the VUMC RC data.")
        st.markdown("- There are three types of common problems checked by this dashboard.")
        st.markdown("1. Criterion Count Check.")
        st.markdown("2. Criterion Validation.")
        st.markdown("3. Diagnosis Validation.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.write("")
    elif first_selection == "Specific Disorder":
        specific_disorder_scope = st.sidebar.selectbox("Which type of problem would you like to look at?", ['', 'Criterion Counts', 'Criterion Validations', 'Diagnoses', 'All'])
        if specific_disorder_scope == 'Criterion Counts':
            disorder_list = []
            refined_count_validation_columns = filtered_master_db_count.columns.tolist()
            for syndrome in refined_count_validation_columns:
                short_item = re.search(r'\((.*?)\)', syndrome).group(1)
                if "Catatonia" in short_item:
                    short_item = re.search(r'(.*?)\s\(', syndrome).group(1)
                    disorder_list.append(short_item)
                else:
                    if "ADHD" in short_item:
                        disorder_list.append(short_item)
                    else:
                        item = syndrome_names_list_cleaned[short_syndrome_names_list_cleaned.index(short_item)]
                        if item in disorder_list:
                            pass
                        else:
                            disorder_list.append(item)
            specific_disorder = st.sidebar.selectbox("What disorder would you like to look at?", [''] + disorder_list)
            interviewers = st.sidebar.checkbox("See Associated Interviewer?")
            specific_problem = st.sidebar.checkbox("See Specific Problem?")
            if specific_disorder == '':
                st.write("## Please select a disorder to look at using the sidebar drop down menu.")
            elif any(short_syndrome_names_list_cleaned[syndrome_names_list_cleaned.index(specific_disorder)] in col for col in refined_count_validation_columns):
                st.markdown('# Data Outputs')
                st.markdown("---")
                st.markdown(f"## {specific_disorder}")
                data = filtered_master_db_count.filter(like = short_syndrome_names_list_cleaned[syndrome_names_list_cleaned.index(specific_disorder)])
                abreviated_name = short_syndrome_names_list_cleaned[syndrome_names_list_cleaned.index(specific_disorder)]
                if interviewers:
                    if specific_problem:
                        data = filtered_master_db_count.filter(like = abreviated_name)
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        else:
                            if "PDD" in abreviated_name:
                                if "CPDD" in abreviated_name or "PPDD" in abreviated_name:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if abreviated_name in new_cols:
                                            count_columns.append(old_cols)
                                    flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                    my_count_problem = data.iloc[:, 0].dropna()
                                    my_count_problem_ids = my_count_problem.values.tolist()
                                    interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                    filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(final_new_data)
                                    csv = convert_df(final_new_data)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                    st.write("Here's a breakdown of the interviewers:")
                                    st.write(interviewers_mine_count.value_counts())
                                else:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if abreviated_name in new_cols:
                                            count_columns.append(old_cols)
                                    flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                    final_flat_count_column_list = [x for x in flat_count_column_list if "(CPDD)" not in x and "(PPDD)" not in x]
                                    column_one_count_problem = data.iloc[:, 2].dropna()
                                    column_two_count_problem = data.iloc[:, 3].dropna()
                                    my_count_problem_ids = column_one_count_problem.values.tolist() + column_two_count_problem.values.tolist()
                                    interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                    filter_columns_count = final_flat_count_column_list + [x for x in filtered_full_db.columns if "(PDD)" in x and "Count" in x and "Criteria" not in x and "(CPDD)" not in x and "(PPDD)" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(final_new_data)
                                    csv = convert_df(final_new_data)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                    st.write("Here's a breakdown of the interviewers:")
                                    st.write(interviewers_mine_count.value_counts())
                            elif "ADHD" in abreviated_name:
                                data = filtered_master_db_count.filter(like = specific_disorder)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if specific_disorder in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if specific_disorder in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{specific_disorder}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                            elif "Schizo" in abreviated_name or "Delusional" in abreviated_name or "Brief" in abreviated_name:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if "CATATONIA" in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                            else:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if abreviated_name in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                    else:
                        data = filtered_master_db_count.filter(like = abreviated_name)
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        else:
                            if "PDD" in abreviated_name:
                                if "CPDD" in abreviated_name or "PPDD" in abreviated_name:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    my_count_problem = data.iloc[:, 0].dropna()
                                    my_count_problem_ids = my_count_problem.values.tolist()
                                    interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                    filter_columns_count = [x for x in filtered_full_db.columns if abreviated_name in x and "Count Comparison" in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(final_new_data)
                                    csv = convert_df(final_new_data)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                    st.write("Here's a breakdown of the interviewers:")
                                    st.write(interviewers_mine_count.value_counts())
                                else:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    column_one_count_problem = data.iloc[:, 2].dropna()
                                    column_two_count_problem = data.iloc[:, 3].dropna()
                                    my_count_problem_ids = column_one_count_problem.values.tolist() + column_two_count_problem.values.tolist()
                                    interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                    filter_columns_count = [x for x in filtered_full_db.columns if "(PDD)" in x and "Count Comparison" in x and "(CPDD)" not in x and "(PPDD)" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(final_new_data)
                                    csv = convert_df(final_new_data)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                    st.write("Here's a breakdown of the interviewers:")
                                    st.write(interviewers_mine_count.value_counts())
                            elif "ADHD" in abreviated_name:
                                data = filtered_master_db_count.filter(like = specific_disorder)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = [x for x in filtered_full_db.columns if specific_disorder in x and "Count Comparison" in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                            else:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = [x for x in filtered_full_db.columns if abreviated_name in x and "Count Comparison" in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                else:
                    if specific_problem:
                        data = filtered_master_db_count.filter(like = abreviated_name)
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        else:
                            if "PDD" in abreviated_name:
                                if "CPDD" in abreviated_name or "PPDD" in abreviated_name:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if abreviated_name in new_cols:
                                            count_columns.append(old_cols)
                                    flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                    my_count_problem = data.iloc[:, 0].dropna()
                                    my_count_problem_ids = my_count_problem.values.tolist()
                                    filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(new_data_count)
                                    csv = convert_df(new_data_count)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                                else:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if abreviated_name in new_cols:
                                            count_columns.append(old_cols)
                                    flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                    final_flat_count_column_list = [x for x in flat_count_column_list if "(CPDD)" not in x and "(PPDD)" not in x]
                                    column_one_count_problem = data.iloc[:, 2].dropna()
                                    column_two_count_problem = data.iloc[:, 3].dropna()
                                    my_count_problem_ids = column_one_count_problem.values.tolist() + column_two_count_problem.values.tolist()
                                    filter_columns_count = final_flat_count_column_list + [x for x in filtered_full_db.columns if "(PDD)" in x and "Count" in x and "Criteria" not in x and "(CPDD)" not in x and "(PPDD)" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(new_data_count)
                                    csv = convert_df(new_data_count)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                            elif "ADHD" in abreviated_name:
                                data = filtered_master_db_count.filter(like = specific_disorder)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if specific_disorder in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if specific_disorder in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(new_data_count)
                                csv = convert_df(new_data_count)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{specific_disorder}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                            else:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if abreviated_name in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(new_data_count)
                                csv = convert_df(new_data_count)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                    else:
                        if "ADHD" in abreviated_name:
                            data = filtered_master_db_count.filter(like = specific_disorder)
                            final_data = data.dropna(axis = 0)
                            st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with {specific_disorder}")
                            st.dataframe(final_data)
                            st.write("The number of discrepant subjects is", len(final_data.index))
                            csv = convert_df(data)
                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{specific_disorder}_count_problem_ids_{today}.csv', mime= 'text/csv')
                        else:
                            data = filtered_master_db_count.filter(like = abreviated_name)
                            if len(data.columns) == 4:
                                col1 = data.iloc[:, 2]
                                col2 = data.iloc[:, 3]
                                if col1.count() == col2.count():
                                    new_data = pd.DataFrame({
                                        col1.name: col1.dropna(),
                                        col2.name: col2.dropna()
                                    })
                                    col1_ids = col1.values.tolist()
                                    col2_ids = col2.values.tolist()
                                    full_ids = col1_ids + col2_ids
                                    unique_ids = [*set(full_ids)]
                                    filtered_unique_ids_1 = [x for x in unique_ids if str(x) != 'nan']
                                    filtered_unique_ids = list(filter(None, filtered_unique_ids_1))
                                else:
                                    max_len = max(col1.count(), col2.count())
                                    new_col1 = col1.reindex(range(max_len)).fillna(np.nan)
                                    new_col2 = col2.reindex(range(max_len)).fillna(np.nan)
                                    new_data = pd.DataFrame({
                                        col1.name: new_col1.dropna(),
                                        col2.name: new_col2.dropna()
                                    })
                                    col1_ids = new_col1.values.tolist()
                                    col2_ids = new_col2.values.tolist()
                                    full_ids = col1_ids + col2_ids
                                    unique_ids = [*set(full_ids)]
                                    filtered_unique_ids = [x for x in unique_ids if str(x) != 'nan']
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                st.write(new_data)
                                csv = convert_df(new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(filtered_unique_ids))
                            elif len(data.columns) == 1:
                                final_data = data.dropna(axis = 0)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with {specific_disorder}")
                                st.dataframe(final_data)
                                st.write("The number of discrepant subjects is", len(final_data.index))
                                csv = convert_df(data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                            else:
                                st.write("### No problems in this syndrome!")
        elif specific_disorder_scope == 'Criterion Validations':
            disorder_list = []
            refined_criteria_validation_columns = filtered_master_db_criteria.columns.tolist()
            for syndrome in refined_criteria_validation_columns: # Created a dynamic syndrome list # Excluding criterion validations that doubled as diagnostic checks
                short_item = re.search(r'\((.*?)\)', syndrome).group(1)
                if "ADHD" in short_item:
                    adhd_check = short_item[0:4]
                    if adhd_check in disorder_list: # to prevent repeats!
                        pass
                    else:
                        disorder_list.append(adhd_check)
                # Removing the below items as the criterion validation is equivalent to the diagnosis validation
                elif "CSUD" in short_item or "PSUD" in short_item or "PPD" in short_item or "SdPD" in short_item or "SPD" in short_item or "BoPD" in short_item or "APD" in short_item or "AUD" in short_item:
                    continue
                else:
                    if "SCHIZO" in short_item or "BRIEF" in short_item:
                        transformed_short = short_item.title() # Had to change form of short_item to properly index
                        item = syndrome_names_list_cleaned[short_syndrome_names_list_cleaned.index(transformed_short)]
                        if item in disorder_list:
                            continue
                        else:
                            disorder_list.append(item)
                    else:
                        item = syndrome_names_list_cleaned[short_syndrome_names_list_cleaned.index(short_item)]
                        if item in disorder_list:
                            continue
                        else:
                            disorder_list.append(item)
            specific_disorder = st.sidebar.selectbox("What disorder would you like to look at?", [''] + disorder_list)
            if specific_disorder == '':
                st.write("## Please select a disorder to look at using the sidebar drop down menu.")
            elif specific_disorder == 'Schizophrenia':
                st.markdown('# Data Outputs')
                st.markdown("---")
                st.markdown(f"## {specific_disorder}")
                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with criteria validation problems with **{specific_disorder}**")
                abreviated_name = 'CATA (SCHIZOPHRENIA)'
                interviewers = st.sidebar.checkbox("See Associated Interviewer?")
                specific_problem = st.sidebar.checkbox("See Specific Problem?")
                if interviewers:
                    if specific_problem:
                        data = filtered_master_db_criteria.filter(like = abreviated_name) # Filtering criteria validation db by the abreviated disorder name!
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        elif len(data.columns) == 2: # need to account for potential discrepancies between SCID validation and MINE validation
                            column_one = data.columns.tolist()[0][:-7] # Getting just the criteria validation name and stripping "[SCID]" or "[MINE]"
                            column_two = data.columns.tolist()[1][:-7] # Takes the second item in the list and removes the last 7 characters in the string.
                            if column_one == column_two: # Makes sure that it fits the SCID/MINE paradigm and not combining two different criteria
                                scid_criteria_problem = data.iloc[:, 0].dropna() # The paradigm usually follows that the scid column comes first and then the "MINE" column
                                my_criteria_problem = data.iloc[:, 1].dropna()
                                scid_criteria_problem_ids = scid_criteria_problem.values.tolist() # Creating two seperate lists on the off chance that the IDs are different
                                my_criteria_problem_ids = my_criteria_problem.values.tolist()
                                interviewers_scid_criteria = filtered_full_db.loc[scid_criteria_problem_ids, 'scid_interviewername']
                                interviewers_mine_criteria = filtered_full_db.loc[my_criteria_problem_ids, 'scid_interviewername']
                                specific_scid_items_diag = st.checkbox("See the specific SCID Items?")
                                if specific_scid_items_diag:
                                    st.write("you masochistic little freak")
                                else:
                                    workable_name_1 = [x for x in criterion_w_validation_cleaned if x in column_one] # Pulls the correct criterion item from the list of criterion check syndromes
                                    workable_name = workable_name_1[0]
                                    desired_count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if "CATATONIA" in new_cols:
                                            desired_count_columns.append(old_cols)
                                    flat_desired_count_columns = [item for sublist in desired_count_columns for item in sublist]
                                    desired_columns = (flat_desired_count_columns + [workable_name + ' [MINE]', workable_name + ' [SCID]'] + ['Schizophrenia Diagnosis'] +
                                                        [x for x in filtered_full_db.columns if workable_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    my_desired_columns = [x for x in desired_columns if "[SCID]" not in x] + [workable_name + ' [SCID]']
                                    scid_desired_columns = [x for x in desired_columns if "[MINE]" not in x] + [workable_name + ' [MINE]']
                                    my_desired_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                    scid_desired_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        scid_final_db = pd.concat([interviewers_scid_criteria, scid_desired_db], axis = 1)
                                        st.markdown("### SCID Problems")
                                        st.write("---")
                                        st.write(scid_final_db)
                                        csv = convert_df(scid_final_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                    with col2:
                                        my_final_db = pd.concat([interviewers_mine_criteria, my_desired_db], axis = 1)
                                        st.markdown("### MY Problems")
                                        st.write("---")
                                        st.write(my_final_db)
                                        csv = convert_df(my_final_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                        else:
                            st.write(data)
            elif specific_disorder != '':
                st.markdown('# Data Outputs')
                st.markdown("---")
                st.markdown(f"## {specific_disorder}")
                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with criteria validation problems with **{specific_disorder}**")
                abreviated_name = short_syndrome_names_list_cleaned[syndrome_names_list_cleaned.index(specific_disorder)] # Getting the abbreviation of the specific disorder e.g. cmde, cme, etc.
                interviewers = st.sidebar.checkbox("See Associated Interviewer?")
                specific_problem = st.sidebar.checkbox("See Specific Problem?")
                if interviewers:
                    if specific_problem:
                        data = filtered_master_db_criteria.filter(like = abreviated_name) # Filtering criteria validation db by the abreviated disorder name!
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        elif len(data.columns) > 2: # This is for cases where syndrome have more than one criteria validation
                            if "ADHD" in abreviated_name:
                                refined_adhd = st.selectbox("What Problem Would You Like to Look at?", ['', 'Overall Criteria A', 'Sub-Criterion A items'])
                                if refined_adhd == '':
                                    st.write("Please select which aspect of ADHD Criterion validation you would like to examine.")
                                    st.write("Options are just Criterion A or the A1 and A2 sub-parts of criterion A.")
                                elif refined_adhd == 'Overall Criteria A':
                                    refined_adhd_data = data.filter(like = "Criterion A (ADHD)")
                                    scid_adhd_db = refined_adhd_data.iloc[:,0].dropna()
                                    my_adhd_db = refined_adhd_data.iloc[:,1].dropna()
                                    scid_adhd_problem_ids = scid_adhd_db.values.tolist()
                                    my_adhd_problem_ids = my_adhd_db.values.tolist()
                                    scid_adhd_interviewers = filtered_full_db.loc[scid_adhd_problem_ids, 'scid_interviewername']
                                    my_adhd_interviewers = filtered_full_db.loc[my_adhd_problem_ids, 'scid_interviewername']
                                    scid_desired_adhd_columns = ["A1 (ADHD [Inattention]) [SCID]", "A2 (ADHD [Hyperactivity]) [SCID]", 'A (ADHD) [SCID]', 'Criterion A (ADHD) Validation [SCID]']
                                    my_desired_adhd_columns = ["A1 (ADHD [Inattention]) [MINE]", "A2 (ADHD [Hyperactivity]) [MINE]", 'A (ADHD) [SCID]',  "Criterion A (ADHD) Validation [MINE]"]
                                    my_desired_adhd_db = filtered_full_db.loc[my_adhd_problem_ids, my_desired_adhd_columns]
                                    scid_desired_adhd_db = filtered_full_db.loc[scid_adhd_problem_ids, scid_desired_adhd_columns]
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        scid_final_adhd_db = pd.concat([scid_adhd_interviewers, scid_desired_adhd_db], axis = 1)
                                        st.markdown("### SCID Problems")
                                        st.write("---")
                                        st.write(scid_final_adhd_db)
                                        csv = convert_df(scid_final_adhd_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'adhd_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(scid_adhd_problem_ids))
                                        st.write("Here's a breakdown of the interviewers:")
                                        st.write(scid_adhd_interviewers.value_counts())
                                    with col2:
                                        my_final_adhd_db = pd.concat([my_adhd_interviewers, my_desired_adhd_db], axis = 1)
                                        st.markdown("### MY Problems")
                                        st.write("---")
                                        st.write(my_final_adhd_db)
                                        csv = convert_df(my_final_adhd_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'adhd_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(my_adhd_problem_ids))
                                        st.write("Here's a breakdown of the interviewers:")
                                        st.write(my_adhd_interviewers.value_counts())
                                elif refined_adhd == "Sub-Criterion A items":
                                    refined_adhd_data = data.filter(regex= r'A\d') # Selects for columns with A1 or A2 (or any A + number combo)
                                    inattention_db = refined_adhd_data.iloc[:, 0].dropna()
                                    hyper_db = refined_adhd_data.iloc[:, 1].dropna()
                                    inattention_db_problem_ids = inattention_db.values.tolist()
                                    hyper_db_problem_ids = hyper_db.values.tolist()
                                    inattention_db_criterion = filtered_full_db.loc[inattention_db_problem_ids, 'scid_interviewername'] # Just the desired interviewer names
                                    hyper_db_criterion = filtered_full_db.loc[hyper_db_problem_ids, 'scid_interviewername'] # Just the desired interviewer names
                                    inattention_columns = ([col for col in filtered_full_db.columns if abreviated_name in col and "Inattention" in col and '[SCID]' not in col and '[MINE]' not in col and "Discrepancy" not in col] + 
                                                           [col for col in filtered_full_db.columns if abreviated_name in col and "Inattention" in col and ('[SCID]' in col or '[MINE]' in col) and "Comparison" not in col])
                                    hyperactivity_columns = ([col for col in filtered_full_db.columns if abreviated_name in col and "Hyperactivity" in col and '[SCID]' not in col and '[MINE]' not in col and "Discrepancy" not in col] + 
                                                           [col for col in filtered_full_db.columns if abreviated_name in col and "Hyperactivity" in col and ('[SCID]' in col or '[MINE]' in col) and "Comparison" not in col])
                                    col1, col2 = st.columns(2)
                                    with col1: # Inattentive Column
                                        st.markdown("## A1 [INATTENTION]")
                                        st.markdown(f"The table below is of the Discrepant ID dbs for subjects with criterion validation problems with **Inattention**")
                                        desired_ina_db = filtered_full_db.loc[inattention_db_problem_ids, inattention_columns]
                                        final_ina_db = pd.concat([inattention_db_criterion, desired_ina_db], axis = 1)
                                        st.write(final_ina_db)
                                        csv = convert_df(final_ina_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'adhd_ina_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(inattention_db_problem_ids))
                                        st.write("Here's a breakdown of the interviewers:")
                                        st.write(inattention_db_criterion.value_counts())
                                    with col2: # Hyperactivity column
                                        st.markdown("## A1 [HYPERACTIVITY]")
                                        st.markdown(f"The table below is of the Discrepant ID dbs for subjects with criterion validation problems with **Hyperactivity**")
                                        desired_hyp_db = filtered_full_db.loc[hyper_db_problem_ids, hyperactivity_columns]
                                        final_hyp_db = pd.concat([hyper_db_criterion, desired_hyp_db], axis = 1)
                                        st.write(final_hyp_db)
                                        csv = convert_df(final_hyp_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'adhd_hyp_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(hyper_db_problem_ids))
                                        st.write("Here's a breakdown of the interviewers:")
                                        st.write(hyper_db_criterion.value_counts())
                            elif "PTSD" in abreviated_name:
                                if len(data.columns) == 4:
                                    # Getting criterion type in PTSD (B, C, D, E)
                                    crit1_name = data.columns.tolist()[0][10:19]
                                    crit2_name = data.columns.tolist()[1][10:19]
                                    crit3_name = data.columns.tolist()[2][10:19]
                                    crit4_name = data.columns.tolist()[3][10:19]
                                    # Getting the desired dbs
                                    crit_1 = data.iloc[:, 0].dropna()
                                    crit_2 = data.iloc[:, 1].dropna()
                                    crit_3 = data.iloc[:, 2].dropna()
                                    crit_4 = data.iloc[:, 3].dropna()
                                    # List of problem IDs for each criteria 
                                    crit1_problem_ids = crit_1.values.tolist()
                                    crit2_problem_ids = crit_2.values.tolist()
                                    crit3_problem_ids = crit_3.values.tolist()
                                    crit4_problem_ids = crit_4.values.tolist()
                                    # Getting the associated interviewers for each criteria
                                    crit1_interviewers = filtered_full_db.loc[crit1_problem_ids, 'scid_interviewername']
                                    crit2_interviewers = filtered_full_db.loc[crit2_problem_ids, 'scid_interviewername']
                                    crit3_interviewers = filtered_full_db.loc[crit3_problem_ids, 'scid_interviewername']
                                    crit4_interviewers = filtered_full_db.loc[crit4_problem_ids, 'scid_interviewername']
                                    # Getting the desired count columns for each criteria
                                    desired_count_columns_crit1 = []
                                    desired_count_columns_crit2 = []
                                    desired_count_columns_crit3 = []
                                    desired_count_columns_crit4 = []
                                    for new_cols, old_cols in criterion_counts.items(): # Appending the correct criterion columns to each list
                                        if crit1_name in new_cols:
                                            desired_count_columns_crit1.append(old_cols)
                                        elif crit2_name in new_cols:
                                            desired_count_columns_crit2.append(old_cols)
                                        elif crit3_name in new_cols:
                                            desired_count_columns_crit3.append(old_cols)
                                        elif crit4_name in new_cols:
                                            desired_count_columns_crit4.append(old_cols)
                                    flat_crit1_desired_count_columns = [item for sublist in desired_count_columns_crit1 for item in sublist]
                                    flat_crit2_desired_count_columns = [item for sublist in desired_count_columns_crit2 for item in sublist]
                                    flat_crit3_desired_count_columns = [item for sublist in desired_count_columns_crit3 for item in sublist]
                                    flat_crit4_desired_count_columns = [item for sublist in desired_count_columns_crit4 for item in sublist]
                                    crit1_desired_columns = (flat_crit1_desired_count_columns + [crit1_name + " [SCID]"] +
                                                             [x for x in filtered_full_db.columns if crit1_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    crit2_desired_columns = (flat_crit2_desired_count_columns + [crit2_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit2_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    crit3_desired_columns = (flat_crit3_desired_count_columns + [crit3_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit3_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    crit4_desired_columns = (flat_crit4_desired_count_columns + [crit4_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit4_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"## {crit1_name}")
                                        st.write("---")
                                        filtered_crit_1 = filtered_full_db.loc[crit1_problem_ids, crit1_desired_columns]
                                        final_crit1_db = pd.concat([crit1_interviewers, filtered_crit_1], axis = 1)
                                        st.write(final_crit1_db)
                                        csv = convert_df(final_crit1_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit1_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit1_problem_ids))
                                        # Doing two in one column for clutter reasons
                                        st.write(f"## {crit2_name}")
                                        st.write("---")
                                        filtered_crit_2 = filtered_full_db.loc[crit2_problem_ids, crit2_desired_columns]
                                        final_crit2_db = pd.concat([crit2_interviewers, filtered_crit_2], axis = 1)
                                        st.write(final_crit2_db)
                                        csv = convert_df(final_crit2_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit2_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit2_problem_ids))
                                    with col2:
                                        st.write(f"## {crit3_name}")
                                        st.write("---")
                                        filtered_crit_3 = filtered_full_db.loc[crit3_problem_ids, crit3_desired_columns]
                                        final_crit3_db = pd.concat([crit3_interviewers, filtered_crit_3], axis = 1)
                                        st.write(final_crit3_db)
                                        csv = convert_df(final_crit3_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit3_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit3_problem_ids))
                                        # Doing two in one column for clutter reasons
                                        st.write(f"## {crit4_name}")
                                        st.write("---")
                                        filtered_crit_4 = filtered_full_db.loc[crit4_problem_ids, crit4_desired_columns]
                                        final_crit4_db = pd.concat([crit4_interviewers, filtered_crit_4], axis = 1)
                                        st.write(final_crit4_db)
                                        csv = convert_df(final_crit4_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit4_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit4_problem_ids))
                                elif len(data.columns) == 3:
                                    # Getting criterion type in PTSD (B, C, D, E)
                                    crit1_name = data.columns.tolist()[0][10:19]
                                    crit2_name = data.columns.tolist()[1][10:19]
                                    crit3_name = data.columns.tolist()[2][10:19]
                                    # Getting the desired dbs
                                    crit_1 = data.iloc[:, 0].dropna()
                                    crit_2 = data.iloc[:, 1].dropna()
                                    crit_3 = data.iloc[:, 2].dropna()
                                    # List of problem IDs for each criteria 
                                    crit1_problem_ids = crit_1.values.tolist()
                                    crit2_problem_ids = crit_2.values.tolist()
                                    crit3_problem_ids = crit_3.values.tolist()
                                    # Getting the associated interviewers for each criteria
                                    crit1_interviewers = filtered_full_db.loc[crit1_problem_ids, 'scid_interviewername']
                                    crit2_interviewers = filtered_full_db.loc[crit2_problem_ids, 'scid_interviewername']
                                    crit3_interviewers = filtered_full_db.loc[crit3_problem_ids, 'scid_interviewername']
                                    # Getting the desired count columns for each criteria
                                    desired_count_columns_crit1 = []
                                    desired_count_columns_crit2 = []
                                    desired_count_columns_crit3 = []
                                    for new_cols, old_cols in criterion_counts.items(): # Appending the correct columns to each list
                                        if crit1_name in new_cols:
                                            desired_count_columns_crit1.append(old_cols)
                                        elif crit2_name in new_cols:
                                            desired_count_columns_crit2.append(old_cols)
                                        elif crit3_name in new_cols:
                                            desired_count_columns_crit3.append(old_cols)
                                    flat_crit1_desired_count_columns = [item for sublist in desired_count_columns_crit1 for item in sublist]
                                    flat_crit2_desired_count_columns = [item for sublist in desired_count_columns_crit2 for item in sublist]
                                    flat_crit3_desired_count_columns = [item for sublist in desired_count_columns_crit3 for item in sublist]
                                    crit1_desired_columns = (flat_crit1_desired_count_columns + [crit1_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit1_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    crit2_desired_columns = (flat_crit2_desired_count_columns + [crit2_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit2_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    crit3_desired_columns = (flat_crit3_desired_count_columns + [crit3_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit3_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x]) 
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"## {crit1_name}")
                                        st.write("---")
                                        filtered_crit_1 = filtered_full_db.loc[crit1_problem_ids, crit1_desired_columns]
                                        final_crit1_db = pd.concat([crit1_interviewers, filtered_crit_1], axis = 1)
                                        st.write(final_crit1_db)
                                        csv = convert_df(final_crit1_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit1_problem_ids}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit1_problem_ids))
                                        # Doing two in one column for clutter reasons
                                        st.write(f"## {crit2_name}")
                                        st.write("---")
                                        filtered_crit_2 = filtered_full_db.loc[crit2_problem_ids, crit2_desired_columns]
                                        final_crit2_db = pd.concat([crit2_interviewers, filtered_crit_2], axis = 1)
                                        st.write(final_crit2_db)
                                        csv = convert_df(final_crit2_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit2_problem_ids}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit2_problem_ids))
                                    with col2:
                                        st.write(f"## {crit3_name}")
                                        st.write("---")
                                        filtered_crit_3 = filtered_full_db.loc[crit3_problem_ids, crit3_desired_columns]
                                        final_crit3_db = pd.concat([crit3_interviewers, filtered_crit_3], axis = 1)
                                        st.write(final_crit3_db)
                                        csv = convert_df(final_crit3_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit3_problem_ids}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit3_problem_ids))
                                elif len(data.columns) == 2:
                                    # Getting criterion type in PTSD (B, C, D, E)
                                    crit1_name = data.columns.tolist()[0][10:19]
                                    crit2_name = data.columns.tolist()[1][10:19]
                                    # Getting the desired dbs
                                    crit_1 = data.iloc[:, 0].dropna()
                                    crit_2 = data.iloc[:, 1].dropna()
                                    # List of problem IDs for each criteria 
                                    crit1_problem_ids = crit_1.values.tolist()
                                    crit2_problem_ids = crit_2.values.tolist()
                                    # Getting the associated interviewers for each criteria
                                    crit1_interviewers = filtered_full_db.loc[crit1_problem_ids, 'scid_interviewername']
                                    crit2_interviewers = filtered_full_db.loc[crit2_problem_ids, 'scid_interviewername']
                                    # Getting the desired count columns for each criteria
                                    desired_count_columns_crit1 = []
                                    desired_count_columns_crit2 = []
                                    for new_cols, old_cols in criterion_counts.items(): # Appending the correct columns to each list
                                        if crit1_name in new_cols:
                                            desired_count_columns_crit1.append(old_cols)
                                        elif crit2_name in new_cols:
                                            desired_count_columns_crit2.append(old_cols)
                                    flat_crit1_desired_count_columns = [item for sublist in desired_count_columns_crit1 for item in sublist]
                                    flat_crit2_desired_count_columns = [item for sublist in desired_count_columns_crit2 for item in sublist]
                                    crit1_desired_columns = (flat_crit1_desired_count_columns + [crit1_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit1_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    crit2_desired_columns = (flat_crit2_desired_count_columns + [crit2_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit2_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"## {crit1_name}")
                                        st.write("---")
                                        filtered_crit_1 = filtered_full_db.loc[crit1_problem_ids, crit1_desired_columns]
                                        final_crit1_db = pd.concat([crit1_interviewers, filtered_crit_1], axis = 1)
                                        st.write(final_crit1_db)
                                        csv = convert_df(final_crit1_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit1_problem_ids}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit1_problem_ids))
                                    with col2:
                                        st.write(f"## {crit2_name}")
                                        st.write("---")
                                        filtered_crit_2 = filtered_full_db.loc[crit2_problem_ids, crit2_desired_columns]
                                        final_crit2_db = pd.concat([crit2_interviewers, filtered_crit_2], axis = 1)
                                        st.write(final_crit2_db)
                                        csv = convert_df(final_crit2_db)
                                        st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit2_problem_ids}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                        st.write("The number of **unique** discrepant subjects is:", len(crit2_problem_ids))
                                elif len(data.columns) == 1:
                                    # Getting criterion type in PTSD (B, C, D, E)
                                    crit1_name = data.columns.tolist()[0][10:19]
                                    # Getting the desired dbs
                                    crit_1 = data.iloc[:, 0].dropna()
                                    # List of problem IDs for the criterion
                                    crit1_problem_ids = crit_1.values.tolist()
                                    # Getting the associated interviewers for each criteria
                                    crit1_interviewers = filtered_full_db.loc[crit1_problem_ids, 'scid_interviewername']
                                    # Getting the desired count columns for the criterion
                                    desired_count_columns_crit1 = []
                                    for new_cols, old_cols in criterion_counts.items(): # Appending the correct columns to each list
                                        if crit1_name in new_cols:
                                            desired_count_columns_crit1.append(old_cols)
                                    flat_crit1_desired_count_columns = [item for sublist in desired_count_columns_crit1 for item in sublist]
                                    crit1_desired_columns = (flat_crit1_desired_count_columns + [crit1_name + " [SCID]"] +
                                                            [x for x in filtered_full_db.columns if crit1_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                    st.write(f"## {crit1_name}")
                                    st.write("---")
                                    filtered_crit_1 = filtered_full_db.loc[crit1_problem_ids, crit1_desired_columns]
                                    final_crit1_db = pd.concat([crit1_interviewers, filtered_crit_1], axis = 1)
                                    st.write(final_crit1_db)
                                    csv = convert_df(final_crit1_db)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'ptsd_{crit1_problem_ids}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of **unique** discrepant subjects is:", len(crit1_problem_ids))
                                else:
                                    st.write("## NO PROBLEMS IN THIS SYNDROME!")
                            elif "PDD" in abreviated_name:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with criterion validation problems with **{specific_disorder}**")
                                column_list = data.columns.tolist() #using this to get correct column index (in case this changes overtime)
                                desired_column_name = [x for x in column_list if "(PDD)" in x]
                                needed_index = data.columns.get_loc(*desired_column_name)
                                workable_name_v1 = data.columns.tolist()[needed_index]
                                st.write()
                                if "[MINE]" in workable_name_v1:
                                    workable_name = workable_name_v1.replace("Criterion ", '').replace(" Validation [MINE]", '')
                                elif "[SCID]" in workable_name_v1:
                                    workable_name = workable_name_v1.replace("Criterion ", '').replace(" Validation [SCID]", '')
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if workable_name in new_cols and "CPDD" not in new_cols and "PPDD" not in new_cols: 
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_crit_problem = data.iloc[:, needed_index].dropna()
                                my_crit_problem_ids = my_crit_problem.values.tolist()
                                interviewers_mine_crit = filtered_full_db.loc[my_crit_problem_ids, 'scid_interviewername']
                                filter_columns_crit = (flat_count_column_list + [workable_name + " [SCID]"] +
                                                       [x for x in filtered_full_db.columns if workable_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                new_data_crit = filtered_full_db.loc[my_crit_problem_ids, filter_columns_crit]
                                final_new_data = pd.concat([interviewers_mine_crit, new_data_crit], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_crit))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_crit.value_counts())
                            elif "PHME" in abreviated_name or "PME" in abreviated_name:
                                if len(data.columns) == 3:
                                    column1 = data.iloc[:, 0].dropna()
                                    column2 = data.iloc[:, 1].dropna()
                                    column3 = data.iloc[:, 2].dropna()
                                    column1_subjects = column1.values.tolist()
                                    column2_subjects = column2.values.tolist()
                                    column3_subjects = column3.values.tolist()
                                    column1_interviewers = filtered_full_db.loc[column1_subjects, 'scid_interviewername']
                                    column2_interviewers = filtered_full_db.loc[column2_subjects, 'scid_interviewername']
                                    column3_interviewers = filtered_full_db.loc[column3_subjects, 'scid_interviewername']
                                    if column1.name[:-7] == column2.name[:-7]: # Making sure the first two are both criterion A
                                        my_criterion_a_columns = ['scid_a92a', 'scid_a92c1', 'scid_a92b', 'scid_a92c2', 'scid_a95l', 'scid_pme_a2_cb03___a95h', 'scid_a95', 'scid_a110', f'Criterion A ({abreviated_name}) Validation [MINE]']
                                        scid_criterion_a_columns = ['scid_a92a', 'scid_a92c1', 'scid_a92b', 'scid_a92c2', 'scid_a95l', 'scid_pme_a2_cb03___a95h', 'scid_a95', 'scid_a110', f'Criterion A ({abreviated_name}) Validation [SCID]']
                                        criterion_b_columns = ['scid_a92a', 'scid_a92c1', 'scid_a92b', 'scid_a92c2']
                                        criterion_b_count_columns = []
                                        for new_cols, old_cols in criterion_counts.items():
                                                    if abreviated_name in new_cols and "Criterion B" in new_cols:
                                                        criterion_b_count_columns.append(old_cols)
                                        flat_criterion_b_count_columns = [item for sublist in criterion_b_count_columns for item in sublist]
                                        final_criterion_b_columns = (criterion_b_columns + flat_criterion_b_count_columns + [f"Criterion B ({abreviated_name}) Count{column3.name[-7:]}", f"Criterion B ({abreviated_name}) Validation{column3.name[-7:]}"] + [f"Criterion B ({abreviated_name}) Count [SCID]"])
                                        desired_column1_db = filtered_full_db.loc[column1_subjects, scid_criterion_a_columns]
                                        desired_column2_db = filtered_full_db.loc[column2_subjects, my_criterion_a_columns]
                                        desired_column3_db = filtered_full_db.loc[column3_subjects, final_criterion_b_columns]
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            final_column1_db = pd.concat([column1_interviewers, desired_column1_db], axis =1)
                                            st.markdown("### SCID Problems")
                                            st.write("---")
                                            st.write(final_column1_db)
                                            csv = convert_df(final_column1_db)
                                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                            st.write("The number of **unique** discrepant subjects is:", len(column1_subjects))
                                            st.write("Here's a breakdown of the interviewers:")
                                            st.write(column1_interviewers.value_counts())
                                            st.write("---")
                                            st.write("### Criterion B Problems")
                                            st.write("---")
                                            final_column3_db = pd.concat([column3_interviewers, desired_column3_db], axis = 1)
                                            st.write(final_column3_db)
                                            csv = convert_df(final_column3_db)
                                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                            st.write("The number of **unique** discrepant subjects is:", len(column3_subjects))
                                            st.write("Here's a breakdown of the interviewers:")
                                            st.write(column3_interviewers.value_counts())
                                        with col2:
                                            final_column2_db = pd.concat([column2_interviewers, desired_column2_db], axis =1)
                                            st.markdown("### MY Problems")
                                            st.write("---")
                                            st.write(final_column2_db)
                                            csv = convert_df(final_column2_db)
                                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                            st.write("The number of **unique** discrepant subjects is:", len(column2_subjects))
                                            st.write("Here's a breakdown of the interviewers:")
                                            st.write(column2_interviewers.value_counts())
                            else:
                                st.write(data.dropna(how = "all"))
                                st.write("Need to flesh out.")
                        elif len(data.columns) == 2: # need to account for potential discrepancies between SCID validation and MINE validation
                            column_one = data.columns.tolist()[0][:-7] # Getting just the criteria validation name and stripping "[SCID]" or "[MINE]"
                            column_two = data.columns.tolist()[1][:-7] # Takes the second item in the list and removes the last 7 characters in the string.
                            if column_one == column_two: # Makes sure that it fits the SCID/MINE paradigm and not combining two different criteria
                                scid_criteria_problem = data.iloc[:, 0].dropna() # The paradigm usually follows that the scid column comes first and then the "MINE" column
                                my_criteria_problem = data.iloc[:, 1].dropna()
                                scid_criteria_problem_ids = scid_criteria_problem.values.tolist() # Creating two seperate lists on the off chance that the IDs are different
                                my_criteria_problem_ids = my_criteria_problem.values.tolist()
                                interviewers_scid_criteria = filtered_full_db.loc[scid_criteria_problem_ids, 'scid_interviewername']
                                interviewers_mine_criteria = filtered_full_db.loc[my_criteria_problem_ids, 'scid_interviewername']
                                specific_scid_items_diag = st.checkbox("See the specific SCID Items?")
                                if specific_scid_items_diag:
                                    st.write("you masochistic little freak")
                                else:
                                    if any(abreviated_name in item for item in criteria_w_multi_items_cleaned): # Checking if multiple items needed to understand validation decision
                                        workable_name_1 = [x for x in criterion_w_validation_cleaned if x in column_one]
                                        workable_name = workable_name_1[0]
                                        if "CME" in workable_name or "CHME" in workable_name:
                                            scid_desired_columns = ['scid_a54a', 'scid_a54c1', 'scid_a54b', 'scid_a54c2', 'scid_a57l', 'scid_cme_a2_cb03___a57h', 'scid_a57', 'scid_a72', f'Criterion A ({abreviated_name}) Validation [SCID]']
                                            my_desired_columns = ['scid_a54a', 'scid_a54c1', 'scid_a54b', 'scid_a54c2', 'scid_a57l', 'scid_cme_a2_cb03___a57h', 'scid_a57', 'scid_a72', f'Criterion A ({abreviated_name}) Validation [MINE]']
                                            scid_filtered_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                            my_filtered_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                            final_scid_db_bid = pd.concat([interviewers_scid_criteria, scid_filtered_db], axis = 1)
                                            final_my_db_bid = pd.concat([interviewers_mine_criteria, my_filtered_db], axis = 1)
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.write("## SCID PROBLEMS")
                                                st.write(final_scid_db_bid)
                                                csv = convert_df(final_scid_db_bid)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_scid_criteria.value_counts())
                                            with col2:
                                                st.write("## MY PROBLEMS")
                                                st.write(final_my_db_bid)
                                                csv = convert_df(final_my_db_bid)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_mine_criteria.value_counts())
                                        elif "PME" in workable_name or "PHME" in workable_name:
                                            st.write('Need to flesh out')
                                            st.write('data')
                                        elif "LPD" in workable_name:
                                            desired_count_columns = []
                                            for new_cols, old_cols in criterion_counts.items():
                                                    if abreviated_name in new_cols:
                                                        desired_count_columns.append(old_cols)
                                            flat_desired_count_columns = [item for sublist in desired_count_columns for item in sublist] # Unpacking the list of lists into one list
                                            desired_columns = (['scid_f2'] + flat_desired_count_columns + [workable_name + ' [MINE]', workable_name + ' [SCID]'] +
                                                                [x for x in filtered_full_db.columns if workable_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                            my_desired_columns = [x for x in desired_columns if "[SCID]" not in x] + [workable_name + ' [SCID]'] + [f"Criterion P ({abreviated_name}) Count [SCID]"]
                                            scid_desired_columns = [x for x in desired_columns if "[MINE]" not in x] + [workable_name + ' [MINE]'] + [f"Criterion P ({abreviated_name}) Count [MINE]"]
                                            my_desired_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                            scid_desired_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                scid_final_db = pd.concat([interviewers_scid_criteria, scid_desired_db], axis = 1)
                                                st.markdown("### SCID Problems")
                                                st.write("---")
                                                st.write(scid_final_db)
                                                csv = convert_df(scid_final_db)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_scid_criteria.value_counts())
                                            with col2:
                                                my_final_db = pd.concat([interviewers_mine_criteria, my_desired_db], axis = 1)
                                                st.markdown("### MY Problems")
                                                st.write("---")
                                                st.write(my_final_db)
                                                csv = convert_df(my_final_db)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_mine_criteria.value_counts())
                                        else:
                                            desired_count_columns = []
                                            for new_cols, old_cols in criterion_counts.items():
                                                    if abreviated_name in new_cols:
                                                        desired_count_columns.append(old_cols)
                                            flat_desired_count_columns = [item for sublist in desired_count_columns for item in sublist] # Unpacking the list of lists into one list
                                            desired_columns = (flat_desired_count_columns + [workable_name + ' [MINE]', workable_name + ' [SCID]'] +
                                                                [x for x in filtered_full_db.columns if workable_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                            my_desired_columns = [x for x in desired_columns if "[SCID]" not in x] + [x for x in desired_columns if 'Count' in x and '[SCID]' in x] + [workable_name + ' [SCID]']
                                            scid_desired_columns = [x for x in desired_columns if "[MINE]" not in x] + [x for x in desired_columns if 'Count' in x and '[MINE]' in x] + [workable_name + ' [MINE]']
                                            my_desired_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                            scid_desired_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                scid_final_db = pd.concat([interviewers_scid_criteria, scid_desired_db], axis = 1)
                                                st.markdown("### SCID Problems")
                                                st.write("---")
                                                st.write(scid_final_db)
                                                csv = convert_df(scid_final_db)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_scid_criteria.value_counts())
                                            with col2:
                                                my_final_db = pd.concat([interviewers_mine_criteria, my_desired_db], axis = 1)
                                                st.markdown("### MY Problems")
                                                st.write("---")
                                                st.write(my_final_db)
                                                csv = convert_df(my_final_db)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_mine_criteria.value_counts())
                                    else: # Items where only the count is needed to validate.
                                        if "BID" not in abreviated_name and "MDD" not in abreviated_name and "BIID" not in abreviated_name:
                                            workable_name_1 = [x for x in criterion_w_validation_cleaned if x in column_one] # Pulls the correct criterion item from the list of criterion check syndromes
                                            workable_name = workable_name_1[0]
                                            desired_count_columns = []
                                            for new_cols, old_cols in criterion_counts.items():
                                                if abreviated_name in new_cols:
                                                    desired_count_columns.append(old_cols)
                                            flat_desired_count_columns = [item for sublist in desired_count_columns for item in sublist]
                                            desired_columns = (flat_desired_count_columns + [workable_name + ' [MINE]', workable_name + ' [SCID]'] +
                                                                [x for x in filtered_full_db.columns if workable_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                            my_desired_columns = [x for x in desired_columns if "[SCID]" not in x] + [workable_name + ' [SCID]'] + [f"Criterion {workable_name} Count [SCID]"]
                                            scid_desired_columns = [x for x in desired_columns if "[MINE]" not in x] + [workable_name + ' [MINE]'] + [f"Criterion {workable_name} Count [MINE]"]
                                            my_desired_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                            scid_desired_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                scid_final_db = pd.concat([interviewers_scid_criteria, scid_desired_db], axis = 1)
                                                st.markdown("### SCID Problems")
                                                st.write("---")
                                                st.write(scid_final_db)
                                                csv = convert_df(scid_final_db)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_scid_criteria.value_counts())
                                            with col2:
                                                my_final_db = pd.concat([interviewers_mine_criteria, my_desired_db], axis = 1)
                                                st.markdown("### MY Problems")
                                                st.write("---")
                                                st.write(my_final_db)
                                                csv = convert_df(my_final_db)
                                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                st.write("Here's a breakdown of the interviewers:")
                                                st.write(interviewers_mine_criteria.value_counts())
                                        else:
                                            if "BID" in abreviated_name:
                                                scid_desired_columns = ['CME Diagnosis', 'PME Diagnosis', 'A (BID)', 'Criterion A (BID) Validation [SCID]']
                                                my_desired_columns = ['CME Criteria Count [MINE]', 'PME Criteria Count [MINE]', 'A (BID)', 'Criterion A (BID) Validation [MINE]']
                                                scid_filtered_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                                my_filtered_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                                final_scid_db_bid = pd.concat([interviewers_scid_criteria, scid_filtered_db], axis = 1)
                                                final_my_db_bid = pd.concat([interviewers_mine_criteria, my_filtered_db], axis = 1)
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    st.write("## SCID PROBLEMS")
                                                    st.write(final_scid_db_bid)
                                                    csv = convert_df(final_scid_db_bid)
                                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                    st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                    st.write("Here's a breakdown of the interviewers:")
                                                    st.write(interviewers_scid_criteria.value_counts())
                                                with col2:
                                                    st.write("## MY PROBLEMS")
                                                    st.write(final_my_db_bid)
                                                    csv = convert_df(final_my_db_bid)
                                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                    st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                    st.write("Here's a breakdown of the interviewers:")
                                                    st.write(interviewers_mine_criteria.value_counts())
                                            elif "BIID" in abreviated_name:
                                                scid_desired_columns = ['CMDE Diagnosis', 'PMDE Diagnosis', 'CHME Diagnosis', 'PHME Diagnosis', 'A (BIID)', 'Criterion A (BIID) Validation [SCID]']
                                                my_desired_columns = ['CMDE Criteria Count [MINE]', 'PMDE Criteria Count [MINE]', 'CHME Criteria Count [MINE]', 'PHME Criteria Count [MINE]', 'A (BIID)', 'Criterion A (BIID) Validation [MINE]']
                                                scid_filtered_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                                my_filtered_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                                final_scid_db_biid = pd.concat([interviewers_scid_criteria, scid_filtered_db], axis = 1)
                                                final_my_db_biid = pd.concat([interviewers_mine_criteria, my_filtered_db], axis = 1)
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    st.write("## SCID PROBLEMS")
                                                    st.write(final_scid_db_biid)
                                                    csv = convert_df(final_scid_db_biid)
                                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                    st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                    st.write("Here's a breakdown of the interviewers:")
                                                    st.write(interviewers_scid_criteria.value_counts())
                                                with col2:
                                                    st.write("## MY PROBLEMS")
                                                    st.write(final_my_db_biid)
                                                    csv = convert_df(final_my_db_biid)
                                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                    st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                    st.write("Here's a breakdown of the interviewers:")
                                                    st.write(interviewers_mine_criteria.value_counts())
                                            elif "MDD" in abreviated_name:
                                                scid_desired_columns = ['CMDE Diagnosis', 'PMDE Diagnosis', 'A/B/C (MDD)', 'Criterion A/B/C (MDD) Validation [SCID]']
                                                my_desired_columns = ['CMDE Criteria Count [MINE]', 'PMDE Criteria Count [MINE]', 'A/B/C (MDD)', 'Criterion A/B/C (MDD) Validation [MINE]']
                                                scid_filtered_db = filtered_full_db.loc[scid_criteria_problem_ids, scid_desired_columns]
                                                my_filtered_db = filtered_full_db.loc[my_criteria_problem_ids, my_desired_columns]
                                                final_scid_db_mdd = pd.concat([interviewers_scid_criteria, scid_filtered_db], axis = 1)
                                                final_my_db_mdd = pd.concat([interviewers_mine_criteria, my_filtered_db], axis = 1)
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    st.write("## SCID PROBLEMS")
                                                    st.write(final_scid_db_mdd)
                                                    csv = convert_df(final_scid_db_mdd)
                                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                    st.write("The number of **unique** discrepant subjects is:", len(scid_criteria_problem_ids))
                                                    st.write("Here's a breakdown of the interviewers:")
                                                    st.write(interviewers_scid_criteria.value_counts())
                                                with col2:
                                                    st.write("## MY PROBLEMS")
                                                    st.write(final_my_db_mdd)
                                                    csv = convert_df(final_my_db_mdd)
                                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                                    st.write("The number of **unique** discrepant subjects is:", len(my_criteria_problem_ids))
                                                    st.write("Here's a breakdown of the interviewers:")
                                                    st.write(interviewers_mine_criteria.value_counts())
                                            else:
                                                st.write(data.dropna(how = "all"))
                            else: # For instances where a syndrome has more than one criteria validation in the same syndrome
                                st.write("Need to flesh out")
                        else: # For instances where it's just a SCID problem or just a MINE problem
                            if "LOCD" in abreviated_name:
                                desired_columns = ['OB (LOCD)', 'CO (LOCD)', 'OB/CO (LOCD) [SCID]', 'Criterion OB/CO (LOCD) Validation [MINE]']
                                ocd_db = data.iloc[:, 0].dropna()
                                ocd_problem_ids = ocd_db.values.tolist()
                                ocd_interviewers = filtered_full_db.loc[ocd_problem_ids, 'scid_interviewername']
                                filtered_ocd_db = filtered_full_db.loc[ocd_problem_ids, desired_columns]
                                final_ocd_db = pd.concat([ocd_interviewers, filtered_ocd_db], axis = 1)
                                st.write(final_ocd_db)
                                csv = convert_df(final_ocd_db)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(ocd_problem_ids))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(ocd_interviewers.value_counts())
                            else:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with criterion validation problems with **{specific_disorder}**")
                                workable_name_v1 = data.columns.tolist()[0]
                                if "[MINE]" in workable_name_v1:
                                    workable_name = workable_name_v1.replace("Criterion ", '').replace(" Validation [MINE]", '')
                                elif "[SCID]" in workable_name_v1:
                                    workable_name = workable_name_v1.replace("Criterion ", '').replace(" Validation [SCID]", '')
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if workable_name in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_crit_problem = data.iloc[:, 0].dropna()
                                my_crit_problem_ids = my_crit_problem.values.tolist()
                                interviewers_mine_crit = filtered_full_db.loc[my_crit_problem_ids, 'scid_interviewername']
                                filter_columns_crit = (flat_count_column_list + [workable_name + " [SCID]"] +
                                                       [x for x in filtered_full_db.columns if workable_name in x and ("Count" in x or "Validation" in x) and "Discrepancy" not in x])
                                new_data_crit = filtered_full_db.loc[my_crit_problem_ids, filter_columns_crit]
                                final_new_data = pd.concat([interviewers_mine_crit, new_data_crit], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_criterion_validation_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_crit))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_crit.value_counts())
                    else:
                        data = filtered_master_db_count.filter(like = abreviated_name)
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        else:
                            if "PDD" in abreviated_name:
                                if "CPDD" in abreviated_name or "PPDD" in abreviated_name:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    my_count_problem = data.iloc[:, 0].dropna()
                                    my_count_problem_ids = my_count_problem.values.tolist()
                                    interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                    filter_columns_count = [x for x in filtered_full_db.columns if abreviated_name in x and "Count Comparison" in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(final_new_data)
                                    csv = convert_df(final_new_data)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                    st.write("Here's a breakdown of the interviewers:")
                                    st.write(interviewers_mine_count.value_counts())
                                else:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    column_one_count_problem = data.iloc[:, 2].dropna()
                                    column_two_count_problem = data.iloc[:, 3].dropna()
                                    my_count_problem_ids = column_one_count_problem.values.tolist() + column_two_count_problem.values.tolist()
                                    interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                    filter_columns_count = [x for x in filtered_full_db.columns if "(PDD)" in x and "Count Comparison" in x and "(CPDD)" not in x and "(PPDD)" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(final_new_data)
                                    csv = convert_df(final_new_data)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                    st.write("Here's a breakdown of the interviewers:")
                                    st.write(interviewers_mine_count.value_counts())
                            elif "ADHD" in abreviated_name:
                                data = filtered_master_db_count.filter(like = specific_disorder)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = [x for x in filtered_full_db.columns if specific_disorder in x and "Count Comparison" in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                            else:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                interviewers_mine_count = filtered_full_db.loc[my_count_problem_ids, 'scid_interviewername']
                                filter_columns_count = [x for x in filtered_full_db.columns if abreviated_name in x and "Count Comparison" in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                final_new_data = pd.concat([interviewers_mine_count, new_data_count], axis = 1)
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_count))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_count.value_counts())
                else:
                    if specific_problem:
                        data = filtered_master_db_count.filter(like = abreviated_name)
                        if data.empty:
                            st.write("### No Problems with this Syndrome!")
                        else:
                            if "PDD" in abreviated_name:
                                if "CPDD" in abreviated_name or "PPDD" in abreviated_name:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if abreviated_name in new_cols:
                                            count_columns.append(old_cols)
                                    flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                    my_count_problem = data.iloc[:, 0].dropna()
                                    my_count_problem_ids = my_count_problem.values.tolist()
                                    filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(new_data_count)
                                    csv = convert_df(new_data_count)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                                else:
                                    st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                    count_columns = []
                                    for new_cols, old_cols in criterion_counts.items():
                                        if abreviated_name in new_cols:
                                            count_columns.append(old_cols)
                                    flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                    final_flat_count_column_list = [x for x in flat_count_column_list if "(CPDD)" not in x and "(PPDD)" not in x]
                                    column_one_count_problem = data.iloc[:, 2].dropna()
                                    column_two_count_problem = data.iloc[:, 3].dropna()
                                    my_count_problem_ids = column_one_count_problem.values.tolist() + column_two_count_problem.values.tolist()
                                    filter_columns_count = final_flat_count_column_list + [x for x in filtered_full_db.columns if "(PDD)" in x and "Count" in x and "Criteria" not in x and "(CPDD)" not in x and "(PPDD)" not in x]
                                    new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                    st.write("### Count Problems")
                                    st.write("---")
                                    st.write(new_data_count)
                                    csv = convert_df(new_data_count)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                            elif "ADHD" in abreviated_name:
                                data = filtered_master_db_count.filter(like = specific_disorder)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if specific_disorder in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if specific_disorder in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(new_data_count)
                                csv = convert_df(new_data_count)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{specific_disorder}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                            else:
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                count_columns = []
                                for new_cols, old_cols in criterion_counts.items():
                                    if abreviated_name in new_cols:
                                        count_columns.append(old_cols)
                                flat_count_column_list = [item for sublist in count_columns for item in sublist]
                                my_count_problem = data.iloc[:, 0].dropna()
                                my_count_problem_ids = my_count_problem.values.tolist()
                                filter_columns_count = flat_count_column_list + [x for x in filtered_full_db.columns if abreviated_name in x and "Count" in x and "Criteria" not in x]
                                new_data_count = filtered_full_db.loc[my_count_problem_ids, filter_columns_count]
                                st.write("### Count Problems")
                                st.write("---")
                                st.write(new_data_count)
                                csv = convert_df(new_data_count)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(my_count_problem_ids))
                    else:
                        if "ADHD" in abreviated_name:
                            data = filtered_master_db_criteria.filter(like = specific_disorder)
                            final_data = data.dropna(how = 'all')
                            st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with {specific_disorder}")
                            st.dataframe(final_data)
                            st.write("The number of discrepant subjects is", len(final_data.index))
                            csv = convert_df(data)
                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{specific_disorder}_count_problem_ids_{today}.csv', mime= 'text/csv')
                        else:
                            data = filtered_master_db_criteria.filter(like = abreviated_name)
                            if len(data.columns) == 2:
                                col1 = data.iloc[:, 0]
                                col2 = data.iloc[:, 1]
                                if col1.count() == col2.count():
                                    new_data = pd.DataFrame({
                                        col1.name: col1.dropna(),
                                        col2.name: col2.dropna()
                                    })
                                    col1_ids = col1.values.tolist()
                                    col2_ids = col2.values.tolist()
                                    full_ids = col1_ids + col2_ids
                                    unique_ids = [*set(full_ids)]
                                    filtered_unique_ids_1 = [x for x in unique_ids if str(x) != 'nan']
                                    filtered_unique_ids = list(filter(None, filtered_unique_ids_1))
                                else:
                                    max_len = max(col1.count(), col2.count())
                                    new_col1 = col1.reindex(range(max_len)).fillna(np.nan)
                                    new_col2 = col2.reindex(range(max_len)).fillna(np.nan)
                                    new_data = pd.DataFrame({
                                        col1.name: new_col1.dropna(),
                                        col2.name: new_col2.dropna()
                                    })
                                    col1_ids = new_col1.values.tolist()
                                    col2_ids = new_col2.values.tolist()
                                    full_ids = col1_ids + col2_ids
                                    unique_ids = [*set(full_ids)]
                                    filtered_unique_ids = [x for x in unique_ids if str(x) != 'nan']
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with **{specific_disorder}**")
                                st.write(new_data)
                                csv = convert_df(new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(filtered_unique_ids))
                            elif len(data.columns) == 1:
                                final_data = data.dropna(axis = 0)
                                st.markdown(f"The table below is of the Discrepant ID dbs for subjects with count problems with {specific_disorder}")
                                st.dataframe(final_data)
                                st.write("The number of discrepant subjects is", len(final_data.index))
                                csv = convert_df(data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_count_problem_ids_{today}.csv', mime= 'text/csv')
                            else:
                                st.write("### No problems in this syndrome!")
        elif specific_disorder_scope == 'Diagnoses':
            disorder_list = []
            refined_diag_validation_columns = filtered_master_db_diag.columns.tolist()
            for syndrome in refined_diag_validation_columns:
                short_item = syndrome.split(" ", 1)[0]
                if "Criterion" in short_item:
                    short_item = re.search(r'\((.*?)\)', syndrome).group(1)
                    item = syndrome_names_list_cleaned[short_syndrome_names_list_cleaned.index(short_item)]
                    if item in disorder_list:
                        continue
                    else:
                        disorder_list.append(item)
                else:
                    item = syndrome_names_list_cleaned[short_syndrome_names_list_cleaned.index(short_item)]
                    if item in disorder_list:
                        continue
                    else:
                        disorder_list.append(item)
            specific_disorder = st.sidebar.selectbox("What disorder would you like to look at?", disorder_list)
            interviewers = st.sidebar.checkbox("See Associated Interviewer?")
            specific_problem = st.sidebar.checkbox("See Specific Problem?")
            if specific_disorder == '':
                st.write("## Please select a disorder to look at using the sidebar drop down menu.")
            elif any(short_syndrome_names_list_cleaned[syndrome_names_list_cleaned.index(specific_disorder)] in col for col in diagnosis_validation_columns):
                st.markdown('# Data Outputs')
                st.markdown("---")
                st.markdown(f"## {specific_disorder}")
                abreviated_name = short_syndrome_names_list_cleaned[syndrome_names_list_cleaned.index(specific_disorder)]
                data = filtered_master_db_diag.filter(like = abreviated_name)
                if interviewers:
                    if specific_problem:
                        st.markdown(f"The tables below are the Discrepant ID dbs for subjects with problems with **{specific_disorder}**")
                        specific_scid_items_diag = st.checkbox("See the specific SCID Items?")
                        data = filtered_master_db_diag.filter(like = abreviated_name)
                        if len(data.columns) == 2:
                            scid_diag_problem = data.iloc[:, 0].dropna()
                            my_diag_problem = data.iloc[:, 1].dropna()
                            scid_diag_problem_ids = scid_diag_problem.values.tolist()
                            my_diag_problem_ids = my_diag_problem.values.tolist()
                            interviewers_scid_diag = filtered_full_db.loc[scid_diag_problem_ids, 'scid_interviewername']
                            interviewers_mine_diag = filtered_full_db.loc[my_diag_problem_ids, 'scid_interviewername']
                            if specific_scid_items_diag:
                                st.write("Why did you do this to yourself?")
                            else:
                                # First getting the needed criteria items in a DB # Will have to break it down by criteria counts
                                if abreviated_name in diags_w_2_scid_cleaned:
                                    scid_criteria_columns = [x for x in two_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in two_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_3_scid_cleaned:
                                    if "CAN" in abreviated_name:
                                        scid_criteria_columns = [x for x in three_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x and "CANNABIS" not in x]
                                        my_criteria_columns = [x for x in three_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                        scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                    else:
                                        scid_criteria_columns = [x for x in three_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                        my_criteria_columns = [x for x in three_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                        scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_4_scid_cleaned:
                                    scid_criteria_columns = [x for x in four_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in four_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_5_scid_cleaned:
                                    scid_criteria_columns = [x for x in five_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in five_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_6_scid_cleaned:
                                    scid_criteria_columns = [x for x in six_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in six_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_7_scid_cleaned:
                                    scid_criteria_columns = [x for x in seven_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in seven_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_9_scid_cleaned:
                                    scid_criteria_columns = [x for x in nine_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in nine_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_10_scid_cleaned:
                                    scid_criteria_columns = [x for x in ten_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in ten_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                            col1, col2 = st.columns(2)
                            with col1:
                                final_scid_new_data = pd.concat([interviewers_scid_diag, scid_new_data], axis = 1)
                                st.write("### SCID Problems")
                                st.write("---")
                                st.write(final_scid_new_data)
                                csv = convert_df(final_scid_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(interviewers_scid_diag))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_scid_diag.value_counts())
                            with col2:
                                final_my_new_data = pd.concat([interviewers_mine_diag, my_new_data], axis = 1)
                                st.write("### My Problems")
                                st.write("---")
                                st.write(final_my_new_data)
                                csv = convert_df(final_my_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(interviewers_mine_diag))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_diag.value_counts())
                        elif len(data.columns) == 1:
                            one_column =  data.columns.values.tolist()
                            if any("[SCID]" in x for x in one_column):
                                scid_diag_problem = data.iloc[:, 0].dropna()
                                scid_diag_problem_ids = scid_diag_problem.values.tolist()
                                interviewers_scid_diag = filtered_full_db.loc[scid_diag_problem_ids, 'scid_interviewername']
                                if abreviated_name in diags_w_2_scid_cleaned:
                                    scid_criteria_columns = [x for x in two_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_3_scid_cleaned:
                                    if "CAN" in abreviated_name:
                                        scid_criteria_columns = [x for x in three_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x and "CANNABIS" not in x]
                                        scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    else:
                                        scid_criteria_columns = [x for x in three_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                        scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_4_scid_cleaned:
                                    scid_criteria_columns = [x for x in four_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_5_scid_cleaned:
                                    scid_criteria_columns = [x for x in five_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_6_scid_cleaned:
                                    scid_criteria_columns = [x for x in six_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_7_scid_cleaned:
                                    scid_criteria_columns = [x for x in seven_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_9_scid_cleaned:
                                    scid_criteria_columns = [x for x in nine_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_10_scid_cleaned:
                                    scid_criteria_columns = [x for x in ten_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                final_scid_new_data = pd.concat([interviewers_scid_diag, scid_new_data], axis = 1)
                                st.write("### SCID Problems")
                                st.write("---")
                                st.write(final_scid_new_data)
                                csv = convert_df(final_scid_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_scid_diag))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_scid_diag.value_counts())
                            elif any("[MINE]" in x for x in one_column):
                                my_diag_problem = data.iloc[:, 0].dropna()
                                my_diag_problem_ids = my_diag_problem.values.tolist()
                                interviewers_mine_diag = filtered_full_db.loc[my_diag_problem_ids, 'scid_interviewername']
                                if abreviated_name in diags_w_2_scid_cleaned:
                                    my_criteria_columns = [x for x in two_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_3_scid_cleaned:
                                    if "CAN" in abreviated_name:
                                        my_criteria_columns = [x for x in three_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x and "CANNABIS" not in x]
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                    else:
                                        my_criteria_columns = [x for x in three_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_4_scid_cleaned:
                                    my_criteria_columns = [x for x in four_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_5_scid_cleaned:
                                    my_criteria_columns = [x for x in five_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_6_scid_cleaned:
                                    my_criteria_columns = [x for x in six_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_7_scid_cleaned:
                                    my_criteria_columns = [x for x in seven_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_9_scid_cleaned:
                                    my_criteria_columns = [x for x in nine_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_10_scid_cleaned:
                                    my_criteria_columns = [x for x in ten_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif "CSUD" in abreviated_name or "PSUD" in abreviated_name:
                                    if "CSUD" in abreviated_name:
                                        pure_drug = specific_disorder.split(" ")[1]
                                        upper_drug = pure_drug.upper()
                                        my_criteria_columns = ([x for x in filtered_full_db.columns if abreviated_name in x and "Count [SCID]" in x] + 
                                                            [x for x in filtered_full_db.columns if abreviated_name in x and "[SCID]" not in x and "Comparison" not in x and "Discrepancy" not in x] +
                                                            [x for x in filtered_full_db.columns if "Diagnosis" in x and "CSUD" in x and pure_drug in x])
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                    else:
                                        pure_drug = specific_disorder.split(" ")[1]
                                        upper_drug = pure_drug.upper()
                                        my_criteria_columns = ([x for x in filtered_full_db.columns if abreviated_name in x and "Count [SCID]" in x] + 
                                                            [x for x in filtered_full_db.columns if abreviated_name in x and "[SCID]" not in x and "Comparison" not in x and "Discrepancy" not in x] +
                                                            [x for x in filtered_full_db.columns if "Diagnosis" in x and "PSUD" in x and pure_drug in x])
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif "PD" in abreviated_name:
                                    my_criteria_columns = [x for x in filtered_full_db.columns if abreviated_name in x and "Validation" not in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Validation" in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif "CAUD" in abreviated_name or "PAUD" in abreviated_name:
                                    my_criteria_columns = [x for x in filtered_full_db.columns if abreviated_name in x and "Validation" not in x and "Count Comparison" not in x and "Count Discrepancy" not in x and "[SCID]" not in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Validation" in x and "[MINE]" in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                final_my_new_data = pd.concat([interviewers_mine_diag, my_new_data], axis = 1)
                                st.write("### My Problems")
                                st.write("---")
                                st.write(final_my_new_data)
                                csv = convert_df(final_my_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_mine_diag))
                                st.write("Here's a breakdown of the interviewers:")
                                st.write(interviewers_mine_diag.value_counts())
                        else:
                            st.write("### No problems in this syndrome!")
                            st.write(len(data.columns))
                    else:
                        st.markdown(f"The tables below are the Discrepant ID dbs for subjects with problems with **{specific_disorder}**")
                        data = filtered_master_db_diag.filter(like = abreviated_name)
                        if len(data.columns) == 2:
                            scid_diag_problem = data.iloc[:, 0].dropna()
                            my_diag_problem = data.iloc[:, 1].dropna()
                            scid_diag_problem_ids = scid_diag_problem.values.tolist()
                            my_diag_problem_ids = my_diag_problem.values.tolist()
                            interviewers_scid_diag = filtered_full_db.loc[scid_diag_problem_ids, 'scid_interviewername']
                            interviewers_mine_diag = filtered_full_db.loc[my_diag_problem_ids, 'scid_interviewername']
                            if scid_diag_problem.count() == my_diag_problem.count():
                                new_data = pd.DataFrame({
                                    scid_diag_problem.name: scid_diag_problem.dropna(),
                                    my_diag_problem.name: my_diag_problem.dropna()
                                })
                                col1_ids = scid_diag_problem.values.tolist()
                                col2_ids = my_diag_problem.values.tolist()
                                full_ids = col1_ids + col2_ids
                                unique_ids = [*set(full_ids)]
                                filtered_unique_ids_1 = [x for x in unique_ids if str(x) != 'nan']
                                filtered_unique_ids = list(filter(None, filtered_unique_ids_1))
                                final_new_data = pd.concat([interviewers_scid_diag, new_data], axis = 1)
                                st.markdown(f"The table below is a portion of the Discrepant ID db for subjects with problems with **{specific_disorder}**")
                                st.write(final_new_data)
                                csv = convert_df(final_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(filtered_unique_ids))
                            else:
                                scid_diag_problem = data.iloc[:, 0].dropna()
                                my_diag_problem = data.iloc[:, 1].dropna()
                                scid_diag_problem_ids = scid_diag_problem.values.tolist()
                                my_diag_problem_ids = my_diag_problem.values.tolist()
                                interviewers_scid_diag = filtered_full_db.loc[scid_diag_problem_ids, 'scid_interviewername']
                                interviewers_mine_diag = filtered_full_db.loc[my_diag_problem_ids, 'scid_interviewername']
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("### SCID Problems")
                                    st.write("---")
                                    scid_criteria_columns = [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis Validation" in x and "SCID" in x]
                                    final_scid_problem = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    final_scid_diag_problem = pd.concat([interviewers_scid_diag, final_scid_problem], axis = 1)                               
                                    st.markdown(f"The table below is a portion of the Discrepant ID db for subjects with problems with **{specific_disorder}**")
                                    st.write(final_scid_diag_problem) 
                                    csv = convert_df(final_scid_diag_problem)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(final_scid_diag_problem.values.tolist()))
                                with col2:
                                    st.write("### My Problems")
                                    st.write("---")
                                    my_criteria_columns = [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis Validation" in x and "MINE" in x]
                                    final_my_problem = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                    final_my_diag_problem = pd.concat([interviewers_mine_diag, final_my_problem], axis = 1)
                                    st.markdown(f"The table below is a portion of the Discrepant ID db for subjects with problems with **{specific_disorder}**")
                                    st.write(final_my_diag_problem)
                                    csv = convert_df(final_my_diag_problem)
                                    st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                                    st.write("The number of discrepant subjects is:", len(final_my_diag_problem.values.tolist()))
                        elif len(data.columns) == 1:
                            one_column_diag_problems = data.iloc[:, 0].dropna()
                            problem_diag_ids = one_column_diag_problems.values.tolist()
                            one_column_diag_type = one_column_diag_problems.name
                            interviewers_diag = filtered_full_db.loc[one_column_diag_problems, 'scid_interviewername']
                            if "[SCID]" in one_column_diag_type:
                                criteria_columns = [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis Validation" in x and "SCID" in x]
                                final_data = filtered_full_db.loc[problem_diag_ids, criteria_columns]
                                final_final_data = pd.concat([interviewers_diag, final_data], axis = 1)
                                st.dataframe(final_final_data)
                                st.write("The number of discrepant subjects is", len(final_final_data.index))
                                csv = convert_df(final_final_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                            elif "[MINE]" in one_column_diag_type:
                                criteria_columns = [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis Validation" in x and "MINE" in x]
                                final_data = filtered_full_db.loc[problem_diag_ids, criteria_columns]
                                final_final_data = pd.concat([interviewers_diag, final_data], axis = 1)
                                st.dataframe(final_final_data)
                                st.write("The number of discrepant subjects is", len(final_final_data.index))
                                csv = convert_df(final_final_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                        else:
                            st.write("### No problems in this syndrome!")
                            st.write(len(data.columns))
                else:
                    if specific_problem:
                        st.markdown(f"The tables below are the Discrepant ID dbs for subjects with problems with **{specific_disorder}**")
                        specific_scid_items_diag = st.checkbox("See the specific SCID Items?")
                        data = filtered_master_db_diag.filter(like = abreviated_name)
                        if len(data.columns) == 2:
                            scid_diag_problem = data.iloc[:, 0].dropna()
                            my_diag_problem = data.iloc[:, 1].dropna()
                            scid_diag_problem_ids = scid_diag_problem.values.tolist()
                            my_diag_problem_ids = my_diag_problem.values.tolist()
                            if specific_scid_items_diag:
                                st.write("Why did you do this to yourself?")
                            else:
                                # First getting the needed criteria items in a DB # Will have to break it down by criteria counts
                                if abreviated_name in diags_w_2_scid_cleaned:
                                    scid_criteria_columns = [x for x in two_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in two_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_3_scid_cleaned:
                                    scid_criteria_columns = [x for x in three_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in three_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_4_scid_cleaned:
                                    scid_criteria_columns = [x for x in four_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in four_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_5_scid_cleaned:
                                    scid_criteria_columns = [x for x in five_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in five_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_6_scid_cleaned:
                                    scid_criteria_columns = [x for x in six_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in six_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_7_scid_cleaned:
                                    scid_criteria_columns = [x for x in seven_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in seven_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_9_scid_cleaned:
                                    scid_criteria_columns = [x for x in nine_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in nine_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_10_scid_cleaned:
                                    scid_criteria_columns = [x for x in ten_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    my_criteria_columns = [x for x in ten_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("### SCID Problems")
                                st.write("---")
                                st.write(scid_new_data)
                                csv = convert_df(scid_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(scid_diag_problem_ids))
                            with col2:
                                st.write("### My Problems")
                                st.write("---")
                                st.write(my_new_data)
                                csv = convert_df(my_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of **unique** discrepant subjects is:", len(my_diag_problem_ids))
                        elif len(data.columns) == 1:
                            one_column =  data.columns.values.tolist()
                            if any("[SCID]" in x for x in one_column):
                                scid_diag_problem = data.iloc[:, 0].dropna()
                                scid_diag_problem_ids = scid_diag_problem.values.tolist()
                                if abreviated_name in diags_w_2_scid_cleaned:
                                    scid_criteria_columns = [x for x in two_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_3_scid_cleaned:
                                    scid_criteria_columns = [x for x in three_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_4_scid_cleaned:
                                    scid_criteria_columns = [x for x in four_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_5_scid_cleaned:
                                    scid_criteria_columns = [x for x in five_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_6_scid_cleaned:
                                    scid_criteria_columns = [x for x in six_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_7_scid_cleaned:
                                    scid_criteria_columns = [x for x in seven_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_9_scid_cleaned:
                                    scid_criteria_columns = [x for x in nine_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                elif abreviated_name in diags_w_10_scid_cleaned:
                                    scid_criteria_columns = [x for x in ten_criteria_diag_items_scid_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[MINE]" not in x]
                                    scid_new_data = filtered_full_db.loc[scid_diag_problem_ids, scid_criteria_columns]
                                final_scid_new_data = pd.concat([interviewers_scid_diag, scid_new_data], axis = 1)
                                st.write("### SCID Problems")
                                st.write("---")
                                st.write(scid_new_data)
                                csv = convert_df(scid_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_scid_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(interviewers_scid_diag))
                            elif any("[MINE]" in x for x in one_column):
                                my_diag_problem = data.iloc[:, 0].dropna()
                                my_diag_problem_ids = my_diag_problem.values.tolist()
                                if abreviated_name in diags_w_2_scid_cleaned:
                                    my_criteria_columns = [x for x in two_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_3_scid_cleaned:
                                    my_criteria_columns = [x for x in three_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_4_scid_cleaned:
                                    my_criteria_columns = [x for x in four_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_5_scid_cleaned:
                                    my_criteria_columns = [x for x in five_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_6_scid_cleaned:
                                    my_criteria_columns = [x for x in six_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_7_scid_cleaned:
                                    my_criteria_columns = [x for x in seven_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_9_scid_cleaned:
                                    my_criteria_columns = [x for x in nine_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif abreviated_name in diags_w_10_scid_cleaned:
                                    my_criteria_columns = [x for x in ten_criteria_diag_items_mine_cleaned if abreviated_name in x] + [x for x in filtered_full_db.columns if abreviated_name in x and "Diagnosis" in x and "[SCID]" not in x]
                                    my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                elif "CSUD" in abreviated_name or "PSUD" in abreviated_name:
                                    if "CSUD" in abreviated_name:
                                        pure_drug = specific_disorder.split(" ")[1]
                                        upper_drug = pure_drug.upper()
                                        my_criteria_columns = ([x for x in filtered_full_db.columns if abreviated_name in x and "Count [SCID]" in x] + 
                                                               [x for x in filtered_full_db.columns if abreviated_name in x and "[SCID]" not in x and "Comparison" not in x and not x.endswith(f"(CSUD [{upper_drug}])") and "Discrepancy" not in x] +
                                                               [x for x in filtered_full_db.columns if "Diagnosis" in x and "CSUD" in x and pure_drug in x])
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                    else:
                                        pure_drug = specific_disorder.split(" ")[1]
                                        upper_drug = pure_drug.upper()
                                        my_criteria_columns = ([x for x in filtered_full_db.columns if abreviated_name in x and "Count [SCID]" in x] + 
                                                               [x for x in filtered_full_db.columns if abreviated_name in x and "[SCID]" not in x and "Comparison" not in x and not x.endswith(f"(PSUD [{upper_drug}])") and "Discrepancy" not in x] +
                                                               [x for x in filtered_full_db.columns if "Diagnosis" in x and "PSUD" in x and pure_drug in x])
                                        my_new_data = filtered_full_db.loc[my_diag_problem_ids, my_criteria_columns]
                                st.write("### My Problems")
                                st.write("---")
                                st.write(my_new_data)
                                csv = convert_df(my_new_data)
                                st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_my_problem_ids_{today}.csv', mime= 'text/csv')
                                st.write("The number of discrepant subjects is:", len(my_diag_problem_ids))
                        else:
                            st.write("### No problems in this syndrome!")
                            st.write(len(data.columns))
                    else:
                        if len(data.columns) == 2:
                            col1 = data.iloc[:, 0]
                            col2 = data.iloc[:, 1]
                            if col1.count() == col2.count():
                                new_data = pd.DataFrame({
                                    col1.name: col1.dropna(),
                                    col2.name: col2.dropna()
                                })
                                col1_ids = col1.values.tolist()
                                col2_ids = col2.values.tolist()
                                full_ids = col1_ids + col2_ids
                                unique_ids = [*set(full_ids)]
                                filtered_unique_ids_1 = [x for x in unique_ids if str(x) != 'nan']
                                filtered_unique_ids = list(filter(None, filtered_unique_ids_1))
                            else:
                                max_len = max(col1.count(), col2.count())
                                new_col1 = col1.reindex(range(max_len)).fillna(np.nan)
                                new_col2 = col2.reindex(range(max_len)).fillna(np.nan)
                                new_data = pd.DataFrame({
                                    col1.name: new_col1.dropna(),
                                    col2.name: new_col2.dropna()
                                })
                                col1_ids = new_col1.values.tolist()
                                col2_ids = new_col2.values.tolist()
                                full_ids = col1_ids + col2_ids
                                unique_ids = [*set(full_ids)]
                                filtered_unique_ids = [x for x in unique_ids if str(x) != 'nan']
                            st.markdown(f"The table below is a portion of the Discrepant ID db for subjects with problems with **{specific_disorder}**")
                            st.write(new_data)
                            csv = convert_df(new_data)
                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                            st.write("The number of **unique** discrepant subjects is:", len(filtered_unique_ids))
                        elif len(data.columns) == 1:
                            final_data = data.dropna(axis = 0)
                            st.markdown(f"The table below is a portion of the Discrepant ID db for subjects with problems with {specific_disorder}")
                            st.dataframe(final_data)
                            st.write("The number of discrepant subjects is", len(final_data.index))
                            csv = convert_df(data)
                            st.download_button(label = 'Download Data as a CSV', data = csv, file_name = f'{abreviated_name}_problem_ids_{today}.csv', mime= 'text/csv')
                        else:
                            st.write("### No problems in this syndrome!")
                            st.write(len(data.columns))
        elif specific_disorder_scope == 'All':
            disorder_list = [''] + syndrome_names_list_cleaned
            specific_disorder = st.sidebar.selectbox("What disorder would you like to look at?", disorder_list)
        else:
            st.write("# Ante-room")
            st.write("---")
            st.write("Please select the scope of the problem you would like to look at using the selectbox found on the sidebar.")
            st.write("The options are as follows:")
            st.write("1. Criterion Counts - Subjects with problems with their symptom counts.")
            st.write("2. Criterion Validations - Subjects who either should have or incorrectly marked criteria items.")
            st.write("3. Diagnoses - Subjects with incorrect diagnoses.")
            st.write("4. All - All of the above problems at once. Don't say I didn't warn you....")

    