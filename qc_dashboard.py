import pandas as pd
import numpy as np
import streamlit as st
from datetime import date

# Files used later (set up)
module_a_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20A%20Items.xlsx?raw=true'
module_e_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20E%20Items.xlsx?raw=true'

# Markdown Info
first_selection = st.sidebar.selectbox("What would you like to do?", ["---", "Symptom Counts", "Second Level Diagnosis Check"])
st.markdown("# VUMC QC Dashboard")
st.markdown("---")
if first_selection == '---':
    st.markdown("This dashboard was created to address two problems that still face the VUMC data.")
    st.markdown("1. Check if symptom count items are accurate.")
    st.markdown("2. Check to see if diagnosis values match the reported symptom presentations.")
    st.markdown("To get started, choose what you would like to do on the sidebar.")
    st.markdown("- Option 1: 'Symptom Counts' - Check to see if the in interview item symptom count is accurate.")
    st.markdown("- Option 2: 'Second Level Diagnosis Check' - Do a higher level QC check for VUMC diagnoses.")

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8') 

today = date.today()

if first_selection == 'Symptom Counts':
    full_data = st.file_uploader("Upload full RC database export", type='csv')
    module_selection = st.sidebar.selectbox("Which module would you like to look at?", ["---","Module A", "Module E", "Module F", "Module K", "Module C"])
    if module_selection == "---":
        st.markdown("To get started, upload the full RC data output and select which module you would like to look at.")
        st.markdown("### **Options:**")
        st.markdown("1. Module A")
        st.markdown("2. Module E")
        st.markdown("3. Module F")
        st.markdown("4. Module K")
        st.markdown("5. Module C")
    if full_data is not None:
        if module_selection == "Module A":
            module_a_syndrome_selection = st.sidebar.selectbox("Which disorder would you like to look at?", ["---", "CMDE", "PMDE", "CME", "PME", "CHME", "PHME", "CPDD", "PPDD", "PDD"])
            st.markdown(f"## {module_selection}")
            st.markdown("---")
            if module_a_syndrome_selection == '---':
                st.markdown("### Options:")
                st.markdown("- **'CMDE'** - Current Major Depressive Episode")
                st.markdown("- **'PMDE'** - Past Major Depressive Episode")
                st.markdown("- **'CME'** - Current Manic Episode")
                st.markdown("- **'PME'** - Past Manic Episode")
                st.markdown("- **'CHME'** - Current Hypomanic Episode")
                st.markdown("- **'PHME'** - Past Hypomanic Episode")
                st.markdown("- **'CPDD'** - Current Persistent Depressive Disoder")
                st.markdown("- **'PPDD'** - Past Persistent Depressive Disorder")
                st.markdown("- **'PDD'** - Premenstrual Dysphoric Disorder")
            if module_a_syndrome_selection == 'CMDE':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Current Major Depression # Just checking for calculation erros
                cmde_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_a1a', 'scid_a1b', 'scid_a2a', 'scid_a2ar', 'scid_a2b', 'scid_a2br', 'scid_a3a', 'scid_a3b1', 'scid_a3b2', 'scid_a6',
                'scid_a8', 'scid_a9a', 'scid_a9b', 'scid_a12', 'scid_a13a', 'scid_a13b','scid_a16a', 'scid_a16b', 'scid_a17', 'scid_a22', 'scid_a22cnt']]
                
                # Setting index to subject_id
                cmde_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                cmde_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                cmde_full_db = cmde_full_db.astype({'scid_a1a':'int', 'scid_a1b':'int', 'scid_a2a':'int', 'scid_a2ar':'int', 'scid_a2b':'int', 'scid_a2br':'int', 'scid_a3a':'int', 'scid_a3b1':'int', 
                'scid_a3b2':'int', 'scid_a6':'int','scid_a8':'int', 'scid_a9a':'int', 'scid_a9b':'int', 'scid_a12':'int', 'scid_a13a':'int', 'scid_a13b':'int','scid_a16a':'int', 'scid_a16b':'int', 
                'scid_a17':'int', 'scid_a22':'int', 'scid_a22cnt':'int'})

                # Counting cmde symptoms # Max number is 9
                cmde_full_db['A1 Items'] = np.where(((cmde_full_db['scid_a1a'] == 3) | (cmde_full_db['scid_a1b'] == 3)), 1, 0)
                cmde_full_db['A2 Items'] = np.where(((cmde_full_db['scid_a2a'] == 3) | (cmde_full_db['scid_a2ar'] == 3) | (cmde_full_db['scid_a2b'] == 3) | (cmde_full_db['scid_a2br'] == 3)), 1, 0)
                cmde_full_db['A3 Items'] = np.where(((cmde_full_db['scid_a3a'] == 3) | (cmde_full_db['scid_a3b1'] == 3) | (cmde_full_db['scid_a3b2'] == 3)), 1, 0)
                cmde_full_db['A4 Items'] = np.where(((cmde_full_db['scid_a6'] == 3) | (cmde_full_db['scid_a8'] == 3)), 1, 0)
                cmde_full_db['A5 Items'] = np.where(((cmde_full_db['scid_a9a'] == 3) | (cmde_full_db['scid_a9b'] == 3)), 1, 0)
                cmde_full_db['A6 Items'] = np.where(((cmde_full_db['scid_a12'] == 3)), 1, 0)
                cmde_full_db['A7 Items'] = np.where(((cmde_full_db['scid_a13a'] == 3) | (cmde_full_db['scid_a13b'] == 3)), 1, 0)
                cmde_full_db['A8 Items'] = np.where(((cmde_full_db['scid_a16a'] == 3) | (cmde_full_db['scid_a16b'] == 3)), 1, 0)
                cmde_full_db['A9 Items'] = np.where(((cmde_full_db['scid_a17'] == 3)), 1, 0)
                
                # Checking Criterion A Discrepancy
                cmde_full_db['CMDE Criterion A Discrepancy'] = np.where((((cmde_full_db['scid_a22cnt'] >= 5) & ((cmde_full_db['A1 Items'] == 1) | (cmde_full_db['A2 Items'] == 1))) & (cmde_full_db['scid_a22'] != 3)), "Problem", "Fine")

                # Checking count discrepancy
                cmde_full_db['New CMDE Symptom Count'] = cmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items']].sum(axis = 1)
                cmde_full_db['CMDE Symptom Count Discrepancy'] = np.where((cmde_full_db['scid_a22cnt'] != cmde_full_db['New CMDE Symptom Count']), "Problem", "Fine")

                # Only getting Count Items and Discrepancy Items
                refined_cmde_db = cmde_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a22', 'scid_a22cnt',
                'CMDE Criterion A Discrepancy', 'New CMDE Symptom Count', 'CMDE Symptom Count Discrepancy']]

                refined_cmde_db['Count Discrepancy Direction'] = np.where(((cmde_full_db['scid_a22cnt'] - cmde_full_db['New CMDE Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_cmde_db['Count Discrepancy Value'] = cmde_full_db['scid_a22cnt'] - cmde_full_db['New CMDE Symptom Count']
                
                only_problem_children_cmde = refined_cmde_db.loc[((refined_cmde_db['CMDE Criterion A Discrepancy'] == 'Problem') | (refined_cmde_db['CMDE Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                        st.write("**Export Breakdown**")
                        st.write("- In the SCID there is a Criterion A count item (scid_a22cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CMDE Criterion A Discrepancy** - The Criterion A item (scid_a22) should only be marked 3 (threshold) if 5 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New CMDE Symptom Count** - My new symptom count using the Ax Item columns.")

                interviewer_selection_cmde = st.checkbox("Would you like to see the associated interviewer?", key = 'cmde')
                if interviewer_selection_cmde:
                    problem_children_cmde_final = only_problem_children_cmde[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a22', 'CMDE Criterion A Discrepancy',
                    'scid_a22cnt', 'New CMDE Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    
                    st.write(problem_children_cmde_final)
                    csv = convert_df(problem_children_cmde_final)
                else:
                    problem_children_cmde_final = only_problem_children_cmde[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a22', 'CMDE Criterion A Discrepancy',
                    'scid_a22cnt', 'New CMDE Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_cmde_final)
                    csv = convert_df(problem_children_cmde_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_cmde_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'cmde_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_cmde_final[problem_children_cmde_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_cmde_final[problem_children_cmde_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                cmde_problem_subject_list = problem_children_cmde_final.index.values.tolist()
                see_more_cmde = st.multiselect("See Specific Subject Info? [Select as many as you would like]", cmde_problem_subject_list)
                interviewer_selection_cmde_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_cmde')
                if see_more_cmde is not None:
                    if interviewer_selection_cmde_2:
                        specific_cmde_subject_db = cmde_full_db.loc[see_more_cmde,:]
                        specific_cmde_subject_db_2 = specific_cmde_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_a1a', 'scid_a1b', 'A2 Items', 'scid_a2a', 'scid_a2ar', 'scid_a2b', 'scid_a2br',
                        'A3 Items', 'scid_a3a', 'scid_a3b1', 'scid_a3b2', 'A4 Items', 'scid_a6', 'scid_a8', 'A5 Items', 'scid_a9a', 'scid_a9b', 'A6 Items', 'scid_a12',
                        'A7 Items', 'scid_a13a', 'scid_a13b', 'A8 Items', 'scid_a16a', 'scid_a16b', 'A9 Items', 'scid_a17', 'scid_a22', 'scid_a22cnt', 'New CMDE Symptom Count']]
                        specific_cmde_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cmde_subject_db_2)
                        csv = convert_df(specific_cmde_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cmde_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_cmde_subject_db = cmde_full_db.loc[see_more_cmde,:]
                        specific_cmde_subject_db_2 = specific_cmde_subject_db.loc[:,['A1 Items', 'scid_a1a', 'scid_a1b', 'A2 Items', 'scid_a2a', 'scid_a2ar', 'scid_a2b', 'scid_a2br',
                        'A3 Items', 'scid_a3a', 'scid_a3b1', 'scid_a3b2', 'A4 Items', 'scid_a6', 'scid_a8', 'A5 Items', 'scid_a9a', 'scid_a9b', 'A6 Items', 'scid_a12',
                        'A7 Items', 'scid_a13a', 'scid_a13b', 'A8 Items', 'scid_a16a', 'scid_a16b', 'A9 Items', 'scid_a17', 'scid_a22', 'scid_a22cnt', 'New CMDE Symptom Count']]
                        specific_cmde_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cmde_subject_db_2)
                        csv = convert_df(specific_cmde_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cmde_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'PMDE':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Major Depression # Just checking for calculation errors
                pmde_full_db = module_a_db.loc[:, ['subject_id','scid_interviewername','scid_a27a', 'scid_a27b', 'scid_a28a', 'scid_a28b', 'scid_a28ar', 'scid_a28br', 'scid_a29a', 'scid_a29b1', 'scid_a29b2',
                'scid_a32', 'scid_a34', 'scid_a35a', 'scid_a35b', 'scid_a38', 'scid_a39a', 'scid_a39b', 'scid_a42a', 'scid_a42b', 'scid_a43', 'scid_a48', 'scid_a48cnt']]

                # Setting index to subject_id
                pmde_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                pmde_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                pmde_full_db = pmde_full_db.astype({'scid_a27a':'int', 'scid_a27b':'int', 'scid_a28a':'int', 'scid_a28ar':'int', 'scid_a28b':'int', 'scid_a28br':'int', 'scid_a29a':'int', 'scid_a29b1':'int', 
                'scid_a29b2':'int', 'scid_a32':'int','scid_a34':'int', 'scid_a35a':'int', 'scid_a35b':'int', 'scid_a38':'int', 'scid_a39a':'int', 'scid_a39b':'int','scid_a42a':'int', 'scid_a42b':'int', 
                'scid_a43':'int', 'scid_a48':'int', 'scid_a48cnt':'int'})

                # Counting pmde symptoms # Max number is 9
                pmde_full_db['A1 Items'] = np.where(((pmde_full_db['scid_a27a'] == 3) | (pmde_full_db['scid_a27b'] == 3)), 1, 0)
                pmde_full_db['A2 Items'] = np.where(((pmde_full_db['scid_a28a'] == 3) | (pmde_full_db['scid_a28ar'] == 3) | (pmde_full_db['scid_a28b'] == 3) | (pmde_full_db['scid_a28br'] == 3)), 1, 0)
                pmde_full_db['A3 Items'] = np.where(((pmde_full_db['scid_a29a'] == 3) | (pmde_full_db['scid_a29b1'] == 3) | (pmde_full_db['scid_a29b2'] == 3)), 1, 0)
                pmde_full_db['A4 Items'] = np.where(((pmde_full_db['scid_a32'] == 3) | (pmde_full_db['scid_a34'] == 3)), 1, 0)
                pmde_full_db['A5 Items'] = np.where(((pmde_full_db['scid_a35a'] == 3) | (pmde_full_db['scid_a35b'] == 3)), 1, 0)
                pmde_full_db['A6 Items'] = np.where(((pmde_full_db['scid_a38'] == 3)), 1, 0)
                pmde_full_db['A7 Items'] = np.where(((pmde_full_db['scid_a39a'] == 3) | (pmde_full_db['scid_a39b'] == 3)), 1, 0)
                pmde_full_db['A8 Items'] = np.where(((pmde_full_db['scid_a42a'] == 3) | (pmde_full_db['scid_a42b'] == 3)), 1, 0)
                pmde_full_db['A9 Items'] = np.where(((pmde_full_db['scid_a43'] == 3)), 1, 0)

                # Checking diagnosis discrepancy
                pmde_full_db['PMDE Criterion A Discrepancy'] = np.where((((pmde_full_db['scid_a48cnt'] >= 5) & ((pmde_full_db['A1 Items'] == 1) | (pmde_full_db['A2 Items'] == 1))) & (pmde_full_db['scid_a48'] != 3)), "Problem", "Fine")

                # Checking count discrepancy
                pmde_full_db['New PMDE Symptom Count'] = pmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items']].sum(axis = 1)
                pmde_full_db['PMDE Symptom Count Discrepancy'] = np.where((pmde_full_db['scid_a48cnt'] != pmde_full_db['New PMDE Symptom Count']), "Problem", "Fine")

                # Only getting Count Items and Discrepancy Items
                refined_pmde_db = pmde_full_db.loc[:, ['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a48', 'scid_a48cnt',
                'PMDE Criterion A Discrepancy', 'New PMDE Symptom Count', 'PMDE Symptom Count Discrepancy']]

                refined_pmde_db['Count Discrepancy Direction'] = np.where(((pmde_full_db['scid_a48cnt'] - pmde_full_db['New PMDE Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_pmde_db['Count Discrepancy Value'] = pmde_full_db['scid_a48cnt'] - pmde_full_db['New PMDE Symptom Count']
                
                only_problem_children_pmde = refined_pmde_db.loc[((refined_pmde_db['PMDE Criterion A Discrepancy'] == 'Problem') | (refined_pmde_db['PMDE Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion A count item (scid_a48cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PMDE Criterion A Discrepancy** - The Criterion A item (scid_a48) should only be marked 3 (threshold) if 5 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New PMDE Symptom Count** - My new symptom count using the Ax Item columns.")
                interviewer_selection_pmde = st.checkbox("Would you like to see the associated interviewer?", key = 'pmde')
                if interviewer_selection_pmde:
                    problem_children_pmde_final = only_problem_children_pmde[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a48', 'PMDE Criterion A Discrepancy',
                    'scid_a48cnt', 'New PMDE Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_pmde_final)
                    csv = convert_df(problem_children_pmde_final)
                else:
                    problem_children_pmde_final = only_problem_children_pmde[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a48', 'PMDE Criterion A Discrepancy',
                    'scid_a48cnt', 'New PMDE Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_pmde_final)
                    csv = convert_df(problem_children_pmde_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_pmde_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'pmde_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_pmde_final[problem_children_pmde_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_pmde_final[problem_children_pmde_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pmde_problem_subject_list = problem_children_pmde_final.index.values.tolist()
                see_more_pmde = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pmde_problem_subject_list)
                interviewer_selection_pmde_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_pmde')
                if see_more_pmde is not None:
                    if interviewer_selection_pmde_2:
                        specific_pmde_subject_db = pmde_full_db.loc[see_more_pmde,:]
                        specific_pmde_subject_db_2 = specific_pmde_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_a27a', 'scid_a27b', 'A2 Items', 'scid_a28a', 'scid_a28ar', 'scid_a28b', 'scid_a28br',
                        'A3 Items', 'scid_a29a', 'scid_a29b1', 'scid_a29b2', 'A4 Items', 'scid_a32', 'scid_a34', 'A5 Items', 'scid_a35a', 'scid_a35b', 'A6 Items', 'scid_a38',
                        'A7 Items', 'scid_a39a', 'scid_a39b', 'A8 Items', 'scid_a42a', 'scid_a42b', 'A9 Items', 'scid_a43', 'scid_a48', 'scid_a48cnt', 'New PMDE Symptom Count']]
                        specific_pmde_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pmde_subject_db_2)
                        csv = convert_df(specific_pmde_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pmde_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_pmde_subject_db = pmde_full_db.loc[see_more_pmde,:]
                        specific_pmde_subject_db_2 = specific_pmde_subject_db.loc[:,['A1 Items', 'scid_a27a', 'scid_a27b', 'A2 Items', 'scid_a28a', 'scid_a28ar', 'scid_a28b', 'scid_a28br',
                        'A3 Items', 'scid_a29a', 'scid_a29b1', 'scid_a29b2', 'A4 Items', 'scid_a32', 'scid_a34', 'A5 Items', 'scid_a35a', 'scid_a35b', 'A6 Items', 'scid_a38',
                        'A7 Items', 'scid_a39a', 'scid_a39b', 'A8 Items', 'scid_a42a', 'scid_a42b', 'A9 Items', 'scid_a43', 'scid_a48', 'scid_a48cnt', 'New PMDE Symptom Count']]
                        specific_pmde_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pmde_subject_db_2)
                        csv = convert_df(specific_pmde_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pmde_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'CME':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Current Manic Episode # Just checking for calculation errors
                cme_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername','scid_a54a', 'scid_a54c1', 'scid_a54b', 'scid_a54c2', 'scid_a58', 'scid_a59', 'scid_a60', 
                'scid_a61', 'scid_a62', 'scid_a63a', 'scid_a63b', 'scid_a66', 'scid_a67', 'scid_a67cnt']]

                # Setting index to subject_id
                cme_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                cme_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                cme_full_db = cme_full_db.astype({'scid_a54a':'int', 'scid_a54c1':'int', 'scid_a54b':'int', 'scid_a54c2':'int', 'scid_a58':'int', 'scid_a59':'int', 'scid_a60':'int', 
                'scid_a61':'int', 'scid_a62':'int', 'scid_a63a':'int', 'scid_a63b':'int', 'scid_a66':'int', 'scid_a67':'int', 'scid_a67cnt':'int'})

                # Counting cme symptoms # Max number is 7
                cme_full_db['B1 Items'] = np.where(((cme_full_db['scid_a58'] == 3)), 1, 0)
                cme_full_db['B2 Items'] = np.where(((cme_full_db['scid_a59'] == 3)), 1, 0)
                cme_full_db['B3 Items'] = np.where(((cme_full_db['scid_a60'] == 3)), 1, 0)
                cme_full_db['B4 Items'] = np.where(((cme_full_db['scid_a61'] == 3)), 1, 0)
                cme_full_db['B5 Items'] = np.where(((cme_full_db['scid_a62'] == 3)), 1, 0)
                cme_full_db['B6 Items'] = np.where(((cme_full_db['scid_a63a'] == 3) | (cme_full_db['scid_a63b'] == 3)), 1, 0)
                cme_full_db['B7 Items'] = np.where(((cme_full_db['scid_a66'] == 3)), 1, 0)
                cme_full_db['Hyp/Irr Mood'] = np.where((((cme_full_db['scid_a54a'] != 3) & (cme_full_db['scid_a54c1'] != 3)) & ((cme_full_db['scid_a54b'] == 3) | (cme_full_db['scid_a54c2'] == 3))), 
                "Only Irritable Mood", np.where((((cme_full_db['scid_a54a'] == 3) | (cme_full_db['scid_a54c1'] == 3)) & ((cme_full_db['scid_a54b'] != 3) & (cme_full_db['scid_a54c2'] != 3))), "Only Hyperactive", "Mix of both"))
                
                # Checking Criterion B item Discrepancy
                cme_full_db['CME Criterion B Discrepancy'] = np.where((((cme_full_db['scid_a67cnt'] >= 3) & (cme_full_db['scid_a67'] != 3) & (cme_full_db['Hyp/Irr Mood'] != 'Only Irritable Mood'))
                | ((cme_full_db['scid_a67'] != 3) & (cme_full_db['scid_a67cnt'] >= 4) & (cme_full_db['Hyp/Irr Mood'] == 'Only Irritable Mood'))), "Problem", "Fine")
                
                # Checking count discrepancy
                cme_full_db['New CME Symptom Count'] = cme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items']].sum(axis = 1)
                cme_full_db['CME Symptom Count Discrepancy'] = np.where((cme_full_db['scid_a67cnt'] != cme_full_db['New CME Symptom Count']), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_cme_db = cme_full_db.loc[:, ['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a67', 'scid_a67cnt',
                'CME Criterion B Discrepancy', 'New CME Symptom Count', 'CME Symptom Count Discrepancy']]
                
                refined_cme_db['Count Discrepancy Direction'] = np.where(((cme_full_db['scid_a67cnt'] - cme_full_db['New CME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_cme_db['Count Discrepancy Value'] = cme_full_db['scid_a67cnt'] - cme_full_db['New CME Symptom Count']
                
                only_problem_children_cme = refined_cme_db.loc[((refined_cme_db['CME Criterion B Discrepancy'] == 'Problem') | (refined_cme_db['CME Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a67cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CME Criterion A Discrepancy** - The Criterion A item (scid_a67) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New CME Symptom Count** - My new symptom count using the Bx Item columns.")
                
                interviewer_selection_cme = st.checkbox("Would you like to see the associated interviewer?", key = 'cme')
                if interviewer_selection_cme:
                    problem_children_cme_final = only_problem_children_cme[['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a67', 'CME Criterion B Discrepancy',
                    'scid_a67cnt', 'New CME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_cme_final)
                    csv = convert_df(problem_children_cme_final)
                else:
                    problem_children_cme_final = only_problem_children_cme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a67', 'CME Criterion B Discrepancy',
                    'scid_a67cnt', 'New CME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_cme_final)
                    csv = convert_df(problem_children_cme_final)

                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_cme_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'cme_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_cme_final[problem_children_cme_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_cme_final[problem_children_cme_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                cme_problem_subject_list = problem_children_cme_final.index.values.tolist()
                see_more_cme = st.multiselect("See Specific Subject Info? [Select as many as you would like]", cme_problem_subject_list)
                interviewer_selection_cme_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_cme')
                if see_more_cme is not None:
                    if interviewer_selection_cme_2:
                        specific_cme_subject_db = cme_full_db.loc[see_more_cme,:]
                        specific_cme_subject_db_2 = specific_cme_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a58', 'B2 Items', 'scid_a59', 'B3 Items', 'scid_a60', 
                        'B4 Items', 'scid_a61', 'B5 Items', 'scid_a62', 'B6 Items', 'scid_a63a', 'scid_a63b', 'B7 Items','scid_a66', 'scid_a67', 'scid_a67cnt', 'New CME Symptom Count']]
                        specific_cme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cme_subject_db_2)
                        csv = convert_df(specific_cme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_cme_subject_db = cme_full_db.loc[see_more_cme,:]
                        specific_cme_subject_db_2 = specific_cme_subject_db.loc[:,['B1 Items', 'scid_a58', 'B2 Items', 'scid_a59', 'B3 Items', 'scid_a60', 
                        'B4 Items', 'scid_a61', 'B5 Items', 'scid_a62', 'B6 Items', 'scid_a63a', 'scid_a63b', 'B7 Items','scid_a66', 'scid_a67', 'scid_a67cnt', 'New CME Symptom Count']]
                        specific_cme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cme_subject_db_2)
                        csv = convert_df(specific_cme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'PME':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Manic episode # Just checking for calculation errors
                pme_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername','scid_a92a', 'scid_a92c1', 'scid_a92b', 'scid_a92c2', 'scid_a96', 'scid_a97', 'scid_a98', 
                'scid_a99', 'scid_a100', 'scid_a101a', 'scid_a101b', 'scid_a104', 'scid_a105', 'scid_a105cnt']]

                # Setting index to subject_id
                pme_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                pme_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                pme_full_db = pme_full_db.astype({'scid_a92a':'int', 'scid_a92c1':'int', 'scid_a92b':'int', 'scid_a92c2':'int', 'scid_a96':'int', 'scid_a97':'int', 'scid_a98':'int', 
                'scid_a99':'int', 'scid_a100':'int', 'scid_a101a':'int', 'scid_a101b':'int', 'scid_a104':'int', 'scid_a105':'int', 'scid_a105cnt':'int'})

                # Counting pme symptoms # Max number is 7
                pme_full_db['B1 Items'] = np.where(((pme_full_db['scid_a96'] == 3)), 1, 0)
                pme_full_db['B2 Items'] = np.where(((pme_full_db['scid_a97'] == 3)), 1, 0)
                pme_full_db['B3 Items'] = np.where(((pme_full_db['scid_a98'] == 3)), 1, 0)
                pme_full_db['B4 Items'] = np.where(((pme_full_db['scid_a99'] == 3)), 1, 0)
                pme_full_db['B5 Items'] = np.where(((pme_full_db['scid_a100'] == 3)), 1, 0)
                pme_full_db['B6 Items'] = np.where(((pme_full_db['scid_a101a'] == 3) | (pme_full_db['scid_a101b'] == 3)), 1, 0)
                pme_full_db['B7 Items'] = np.where(((pme_full_db['scid_a104'] == 3)), 1, 0)
                pme_full_db['Hyp/Irr Mood'] = np.where((((pme_full_db['scid_a92a'] != 3) & (pme_full_db['scid_a92c1'] != 3)) & ((pme_full_db['scid_a92b'] == 3) | (pme_full_db['scid_a92c2'] == 3))), 
                "Only Irritable Mood", np.where((((pme_full_db['scid_a92a'] == 3) | (pme_full_db['scid_a92c1'] == 3)) & ((pme_full_db['scid_a92b'] != 3) & (pme_full_db['scid_a92c2'] != 3))), "Only Hyperactive", "Mix of both"))
                
                # Checking Criterion B item Discrepancy
                pme_full_db['PME Criterion B Discrepancy'] = np.where((((pme_full_db['scid_a105cnt'] >= 3) & (pme_full_db['scid_a105'] != 3) & (pme_full_db['Hyp/Irr Mood'] != 'Only Irritable Mood'))
                | ((pme_full_db['scid_a105'] != 3) & (pme_full_db['scid_a105cnt'] >= 4) & (pme_full_db['Hyp/Irr Mood'] == 'Only Irritable Mood'))), "Problem", "Fine")
                
                # Checking count discrepancy
                pme_full_db['New PME Symptom Count'] = pme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items']].sum(axis = 1)
                pme_full_db['PME Symptom Count Discrepancy'] = np.where((pme_full_db['scid_a105cnt'] != pme_full_db['New PME Symptom Count']), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_pme_db = pme_full_db.loc[:, ['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a105', 'scid_a105cnt',
                'PME Criterion B Discrepancy', 'New PME Symptom Count', 'PME Symptom Count Discrepancy']]
                
                refined_pme_db['Count Discrepancy Direction'] = np.where(((pme_full_db['scid_a105cnt'] - pme_full_db['New PME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_pme_db['Count Discrepancy Value'] = pme_full_db['scid_a105cnt'] - pme_full_db['New PME Symptom Count']
                
                only_problem_children_pme = refined_pme_db.loc[((refined_pme_db['PME Criterion B Discrepancy'] == 'Problem') | (refined_pme_db['PME Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a105cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PME Criterion A Discrepancy** - The Criterion A item (scid_a105) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New PME Symptom Count** - My new symptom count using the Bx Item columns.")
                
                interviewer_selection_pme = st.checkbox("Would you like to see the associated interviewer?", key = 'pme')
                if interviewer_selection_pme:
                    problem_children_pme_final = only_problem_children_pme[['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a105', 'PME Criterion B Discrepancy',
                    'scid_a105cnt', 'New PME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_pme_final)
                    csv = convert_df(problem_children_pme_final)
                else:
                    problem_children_pme_final = only_problem_children_pme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a105', 'PME Criterion B Discrepancy',
                    'scid_a105cnt', 'New PME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_pme_final)
                    csv = convert_df(problem_children_pme_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_pme_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'pme_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_pme_final[problem_children_pme_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_pme_final[problem_children_pme_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pme_problem_subject_list = problem_children_pme_final.index.values.tolist()
                see_more_pme = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pme_problem_subject_list)
                interviewer_selection_pme_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_pme')
                if see_more_pme is not None:
                    if interviewer_selection_pme_2:
                        specific_pme_subject_db = pme_full_db.loc[see_more_pme,:]
                        specific_pme_subject_db_2 = specific_pme_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a96', 'B2 Items', 'scid_a97', 'B3 Items', 'scid_a98', 
                        'B4 Items', 'scid_a99', 'B5 Items', 'scid_a100', 'B6 Items', 'scid_a101a', 'scid_a101b', 'B7 Items','scid_a104', 'scid_a105', 'scid_a105cnt', 'New PME Symptom Count']]
                        specific_pme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pme_subject_db_2)
                        csv = convert_df(specific_pme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_pme_subject_db = pme_full_db.loc[see_more_pme,:]
                        specific_pme_subject_db_2 = specific_pme_subject_db.loc[:,['B1 Items', 'scid_a96', 'B2 Items', 'scid_a97', 'B3 Items', 'scid_a98', 
                        'B4 Items', 'scid_a99', 'B5 Items', 'scid_a100', 'B6 Items', 'scid_a101a', 'scid_a101b', 'B7 Items','scid_a104', 'scid_a105', 'scid_a105cnt', 'New PME Symptom Count']]
                        specific_pme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pme_subject_db_2)
                        csv = convert_df(specific_pme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'CHME':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Current Hypomanic Episode # Just checking for calculation errors
                chme_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_a54a', 'scid_a54c1', 'scid_a54b', 'scid_a54c2', 'scid_a75', 'scid_a76', 'scid_a77', 
                'scid_a78', 'scid_a79', 'scid_a80a', 'scid_a80b', 'scid_a83', 'scid_a84', 'scid_a84cnt']]

                # Setting index to subject_id
                chme_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                chme_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                chme_full_db = chme_full_db.astype({'scid_a54a':'int', 'scid_a54c1':'int', 'scid_a54b':'int', 'scid_a54c2':'int', 'scid_a75':'int', 'scid_a76':'int', 'scid_a77':'int', 
                'scid_a78':'int', 'scid_a79':'int', 'scid_a80a':'int', 'scid_a80b':'int', 'scid_a83':'int', 'scid_a84':'int', 'scid_a84cnt':'int'})

                # Counting chme symptoms # Max number is 7
                chme_full_db['B1 Items'] = np.where(((chme_full_db['scid_a75'] == 3)), 1, 0)
                chme_full_db['B2 Items'] = np.where(((chme_full_db['scid_a76'] == 3)), 1, 0)
                chme_full_db['B3 Items'] = np.where(((chme_full_db['scid_a77'] == 3)), 1, 0)
                chme_full_db['B4 Items'] = np.where(((chme_full_db['scid_a78'] == 3)), 1, 0)
                chme_full_db['B5 Items'] = np.where(((chme_full_db['scid_a79'] == 3)), 1, 0)
                chme_full_db['B6 Items'] = np.where(((chme_full_db['scid_a80a'] == 3) | (chme_full_db['scid_a80b'] == 3)), 1, 0)
                chme_full_db['B7 Items'] = np.where(((chme_full_db['scid_a83'] == 3)), 1, 0)
                chme_full_db['Hyp/Irr Mood'] = np.where((((chme_full_db['scid_a54a'] != 3) & (chme_full_db['scid_a54c1'] != 3)) & ((chme_full_db['scid_a54b'] == 3) | (chme_full_db['scid_a54c2'] == 3))), 
                "Only Irritable Mood", np.where((((chme_full_db['scid_a54a'] == 3) | (chme_full_db['scid_a54c1'] == 3)) & ((chme_full_db['scid_a54b'] != 3) & (chme_full_db['scid_a54c2'] != 3))), "Only Hyperactive", "Mix of both"))
                
                # Checking Criterion B item Discrepancy
                chme_full_db['CHME Criterion B Discrepancy'] = np.where((((chme_full_db['scid_a84cnt'] >= 3) & (chme_full_db['scid_a84'] != 3) & (chme_full_db['Hyp/Irr Mood'] != 'Only Irritable Mood'))
                | ((chme_full_db['scid_a84'] != 3) & (chme_full_db['scid_a84cnt'] >= 4) & (chme_full_db['Hyp/Irr Mood'] == 'Only Irritable Mood'))), "Problem", "Fine")
                
                # Checking count discrepancy
                chme_full_db['New CHME Symptom Count'] = chme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items']].sum(axis = 1)
                chme_full_db['CHME Symptom Count Discrepancy'] = np.where((chme_full_db['scid_a84cnt'] != chme_full_db['New CHME Symptom Count']), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_chme_db = chme_full_db.loc[:, ['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a84', 'scid_a84cnt',
                'CHME Criterion B Discrepancy', 'New CHME Symptom Count', 'CHME Symptom Count Discrepancy']]
                
                refined_chme_db['Count Discrepancy Direction'] = np.where(((chme_full_db['scid_a84cnt'] - chme_full_db['New CHME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_chme_db['Count Discrepancy Value'] = chme_full_db['scid_a84cnt'] - chme_full_db['New CHME Symptom Count']
                
                only_problem_children_chme = refined_chme_db.loc[((refined_chme_db['CHME Criterion B Discrepancy'] == 'Problem') | (refined_chme_db['CHME Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a84cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CHME Criterion A Discrepancy** - The Criterion A item (scid_a84) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New CHME Symptom Count** - My new symptom count using the Bx Item columns.")
                interviewer_selection_chme = st.checkbox("Would you like to see the associated interviewer?", key = 'chme')
                if interviewer_selection_chme:
                    problem_children_chme_final = only_problem_children_chme[['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a84', 'CHME Criterion B Discrepancy',
                    'scid_a84cnt', 'New CHME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_chme_final)
                    csv = convert_df(problem_children_chme_final)
                else:
                    problem_children_chme_final = only_problem_children_chme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a84', 'CHME Criterion B Discrepancy',
                    'scid_a84cnt', 'New CHME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_chme_final)
                    csv = convert_df(problem_children_chme_final)
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_chme_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'chme_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_chme_final[problem_children_chme_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_chme_final[problem_children_chme_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                
                chme_problem_subject_list = problem_children_chme_final.index.values.tolist()
                see_more_chme = st.multiselect("See Specific Subject Info? [Select as many as you would like]", chme_problem_subject_list)
                interviewer_selection_chme_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_chme')
                if see_more_chme is not None:
                    if interviewer_selection_chme_2:
                        specific_chme_subject_db = chme_full_db.loc[see_more_chme,:]
                        specific_chme_subject_db_2 = specific_chme_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a75', 'B2 Items', 'scid_a76', 'B3 Items', 'scid_a77', 
                        'B4 Items', 'scid_a78', 'B5 Items', 'scid_a79', 'B6 Items', 'scid_a80a', 'scid_a80b', 'B7 Items','scid_a83', 'scid_a84', 'scid_a84cnt', 'New CHME Symptom Count']]
                        specific_chme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_chme_subject_db_2)
                        csv = convert_df(specific_chme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'chme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_chme_subject_db = chme_full_db.loc[see_more_chme,:]
                        specific_chme_subject_db_2 = specific_chme_subject_db.loc[:,['B1 Items', 'scid_a75', 'B2 Items', 'scid_a76', 'B3 Items', 'scid_a77', 
                        'B4 Items', 'scid_a78', 'B5 Items', 'scid_a79', 'B6 Items', 'scid_a80a', 'scid_a80b', 'B7 Items','scid_a83', 'scid_a84', 'scid_a84cnt', 'New CHME Symptom Count']]
                        specific_chme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_chme_subject_db_2)
                        csv = convert_df(specific_chme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'chme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'PHME':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
            
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Hypomanic Episode # Just checking for calculation errors
                phme_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_a92a', 'scid_a92c1', 'scid_a92b', 'scid_a92c2', 'scid_a113', 'scid_a114', 'scid_a115', 
                'scid_a116', 'scid_a117', 'scid_a118a', 'scid_a118b', 'scid_a121', 'scid_a122', 'scid_a122cnt']]

                # Setting index to subject_id
                phme_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                phme_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                phme_full_db = phme_full_db.astype({'scid_a92a':'int', 'scid_a92c1':'int', 'scid_a92b':'int', 'scid_a92c2':'int', 'scid_a113':'int', 'scid_a114':'int', 'scid_a115':'int', 
                'scid_a116':'int', 'scid_a117':'int', 'scid_a118a':'int', 'scid_a118b':'int', 'scid_a121':'int', 'scid_a122':'int', 'scid_a122cnt':'int'})

                # Counting phme symptoms # Max number is 7
                phme_full_db['B1 Items'] = np.where(((phme_full_db['scid_a113'] == 3)), 1, 0)
                phme_full_db['B2 Items'] = np.where(((phme_full_db['scid_a114'] == 3)), 1, 0)
                phme_full_db['B3 Items'] = np.where(((phme_full_db['scid_a115'] == 3)), 1, 0)
                phme_full_db['B4 Items'] = np.where(((phme_full_db['scid_a116'] == 3)), 1, 0)
                phme_full_db['B5 Items'] = np.where(((phme_full_db['scid_a117'] == 3)), 1, 0)
                phme_full_db['B6 Items'] = np.where(((phme_full_db['scid_a118a'] == 3) | (phme_full_db['scid_a118b'] == 3)), 1, 0)
                phme_full_db['B7 Items'] = np.where(((phme_full_db['scid_a121'] == 3)), 1, 0)
                phme_full_db['Hyp/Irr Mood'] = np.where((((phme_full_db['scid_a92a'] != 3) & (phme_full_db['scid_a92c1'] != 3)) & ((phme_full_db['scid_a92b'] == 3) | (phme_full_db['scid_a92c2'] == 3))), 
                "Only Irritable Mood", np.where((((phme_full_db['scid_a92a'] == 3) | (phme_full_db['scid_a92c1'] == 3)) & ((phme_full_db['scid_a92b'] != 3) & (phme_full_db['scid_a92c2'] != 3))), "Only Hyperactive", "Mix of both"))
                
                # Checking Criterion B item Discrepancy
                phme_full_db['PHME Criterion B Discrepancy'] = np.where((((phme_full_db['scid_a122cnt'] >= 3) & (phme_full_db['scid_a122'] != 3) & (phme_full_db['Hyp/Irr Mood'] != 'Only Irritable Mood'))
                | ((phme_full_db['scid_a122'] != 3) & (phme_full_db['scid_a122cnt'] >= 4) & (phme_full_db['Hyp/Irr Mood'] == 'Only Irritable Mood'))), "Problem", "Fine")
                
                # Checking count discrepancy
                phme_full_db['New PHME Symptom Count'] = phme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items']].sum(axis = 1)
                phme_full_db['PHME Symptom Count Discrepancy'] = np.where((phme_full_db['scid_a122cnt'] != phme_full_db['New PHME Symptom Count']), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_phme_db = phme_full_db.loc[:, ['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a122', 'scid_a122cnt',
                'PHME Criterion B Discrepancy', 'New PHME Symptom Count', 'PHME Symptom Count Discrepancy']]
                
                refined_phme_db['Count Discrepancy Direction'] = np.where(((phme_full_db['scid_a122cnt'] - phme_full_db['New PHME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_phme_db['Count Discrepancy Value'] = phme_full_db['scid_a122cnt'] - phme_full_db['New PHME Symptom Count']
                
                only_problem_children_phme = refined_phme_db.loc[((refined_phme_db['PHME Criterion B Discrepancy'] == 'Problem') | (refined_phme_db['PHME Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a122cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PHME Criterion A Discrepancy** - The Criterion A item (scid_a122) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New PHME Symptom Count** - My new symptom count using the Bx Item columns.")
                interviewer_selection_phme = st.checkbox("Would you like to see the associated interviewer?", key = 'phme')
                if interviewer_selection_phme:
                    problem_children_phme_final = only_problem_children_phme[['scid_interviewername','B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a122', 'PHME Criterion B Discrepancy',
                    'scid_a122cnt', 'New PHME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_phme_final)
                    csv = convert_df(problem_children_phme_final)
                else:
                    problem_children_phme_final = only_problem_children_phme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a122', 'PHME Criterion B Discrepancy',
                    'scid_a122cnt', 'New PHME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_phme_final)
                    csv = convert_df(problem_children_phme_final)
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_phme_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'phme_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_phme_final[problem_children_phme_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_phme_final[problem_children_phme_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                phme_problem_subject_list = problem_children_phme_final.index.values.tolist()
                see_more_phme = st.multiselect("See Specific Subject Info? [Select as many as you would like]", phme_problem_subject_list)
                interviewer_selection_phme_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_phme')
                if see_more_phme is not None:
                    if interviewer_selection_phme_2:
                        specific_phme_subject_db = phme_full_db.loc[see_more_phme,:]
                        specific_phme_subject_db_2 = specific_phme_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a113', 'B2 Items', 'scid_a114', 'B3 Items', 'scid_a115', 
                        'B4 Items', 'scid_a116', 'B5 Items', 'scid_a117', 'B6 Items', 'scid_a118a', 'scid_a118b', 'B7 Items','scid_a121', 'scid_a122', 'scid_a122cnt', 'New PHME Symptom Count']]
                        specific_phme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_phme_subject_db_2)
                        csv = convert_df(specific_phme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'phme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_phme_subject_db = phme_full_db.loc[see_more_phme,:]
                        specific_phme_subject_db_2 = specific_phme_subject_db.loc[:,['B1 Items', 'scid_a113', 'B2 Items', 'scid_a114', 'B3 Items', 'scid_a115', 
                        'B4 Items', 'scid_a116', 'B5 Items', 'scid_a117', 'B6 Items', 'scid_a118a', 'scid_a118b', 'B7 Items','scid_a121', 'scid_a122', 'scid_a122cnt', 'New PHME Symptom Count']]
                        specific_phme_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_phme_subject_db_2)
                        csv = convert_df(specific_phme_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'phme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'CPDD':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Current Persistent Depressive Disorder # Just checking for calculation errors
                cpdd_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_a141', 'scid_a142', 'scid_a143', 'scid_a144', 'scid_a145', 'scid_a146', 'scid_a147', 
                'scid_a147cnt']]

                # Setting index to subject_id
                cpdd_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                cpdd_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                cpdd_full_db = cpdd_full_db.astype({'scid_a141':'int', 'scid_a142':'int', 'scid_a143':'int', 'scid_a144':'int', 'scid_a145':'int', 'scid_a146':'int', 'scid_a147':'int', 
                'scid_a147cnt':'int'})

                # Counting cpdd symptoms # Max number is 7
                cpdd_full_db['B1 Items'] = np.where(((cpdd_full_db['scid_a141'] == 3)), 1, 0)
                cpdd_full_db['B2 Items'] = np.where(((cpdd_full_db['scid_a142'] == 3)), 1, 0)
                cpdd_full_db['B3 Items'] = np.where(((cpdd_full_db['scid_a143'] == 3)), 1, 0)
                cpdd_full_db['B4 Items'] = np.where(((cpdd_full_db['scid_a144'] == 3)), 1, 0)
                cpdd_full_db['B5 Items'] = np.where(((cpdd_full_db['scid_a145'] == 3)), 1, 0)
                cpdd_full_db['B6 Items'] = np.where(((cpdd_full_db['scid_a146'] == 3)), 1, 0)
                
                # Checking Criterion B item Discrepancy
                cpdd_full_db['CPDD Criterion B Discrepancy'] = np.where(((cpdd_full_db['scid_a147cnt'] >= 2) & (cpdd_full_db['scid_a147'] !=3)), "Problem", "Fine")
                
                # Checking count discrepancy
                cpdd_full_db['New CPDD Symptom Count'] = cpdd_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items']].sum(axis = 1)
                cpdd_full_db['CPDD Symptom Count Discrepancy'] = np.where((cpdd_full_db['scid_a147cnt'] != cpdd_full_db['New CPDD Symptom Count']), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_cpdd_db = cpdd_full_db.loc[:, ['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'scid_a147', 'scid_a147cnt',
                'CPDD Criterion B Discrepancy', 'New CPDD Symptom Count', 'CPDD Symptom Count Discrepancy']]
                
                refined_cpdd_db['Count Discrepancy Direction'] = np.where(((cpdd_full_db['scid_a147cnt'] - cpdd_full_db['New CPDD Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_cpdd_db['Count Discrepancy Value'] = cpdd_full_db['scid_a147cnt'] - cpdd_full_db['New CPDD Symptom Count']
                
                only_problem_children_cpdd = refined_cpdd_db.loc[((refined_cpdd_db['CPDD Criterion B Discrepancy'] == 'Problem') | (refined_cpdd_db['CPDD Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a147cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CPDD Criterion A Discrepancy** - The Criterion A item (scid_a147) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New CPDD Symptom Count** - My new symptom count using the Bx Item columns.")
                
                interviewer_selection_cpdd = st.checkbox("Would you like to see the associated interviewer?", key = 'cpdd')
                if interviewer_selection_cpdd:
                    problem_children_cpdd_final = only_problem_children_cpdd[['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'scid_a147', 'CPDD Criterion B Discrepancy',
                    'scid_a147cnt', 'New CPDD Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_cpdd_final)
                    csv = convert_df(problem_children_cpdd_final)
                else:
                    problem_children_cpdd_final = only_problem_children_cpdd[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'scid_a147', 'CPDD Criterion B Discrepancy',
                    'scid_a147cnt', 'New CPDD Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_cpdd_final)
                    csv = convert_df(problem_children_cpdd_final)  
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_cpdd_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'cpdd_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_cpdd_final[problem_children_cpdd_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_cpdd_final[problem_children_cpdd_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                cpdd_problem_subject_list = problem_children_cpdd_final.index.values.tolist()
                see_more_cpdd = st.multiselect("See Specific Subject Info? [Select as many as you would like]", cpdd_problem_subject_list)
                interviewer_selection_cpdd_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_cpdd')
                if see_more_cpdd is not None:
                    if interviewer_selection_cpdd_2:
                        specific_cpdd_subject_db = cpdd_full_db.loc[see_more_cpdd,:]
                        specific_cpdd_subject_db_2 = specific_cpdd_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a141', 'B2 Items', 'scid_a142', 'B3 Items', 'scid_a143', 
                        'B4 Items', 'scid_a144', 'B5 Items', 'scid_a145', 'B6 Items', 'scid_a146', 'scid_a147', 'scid_a147cnt', 'New CPDD Symptom Count']]
                        specific_cpdd_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cpdd_subject_db_2)
                        csv = convert_df(specific_cpdd_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cpdd_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_cpdd_subject_db = cpdd_full_db.loc[see_more_cpdd,:]
                        specific_cpdd_subject_db_2 = specific_cpdd_subject_db.loc[:,['B1 Items', 'scid_a141', 'B2 Items', 'scid_a142', 'B3 Items', 'scid_a143', 
                        'B4 Items', 'scid_a144', 'B5 Items', 'scid_a145', 'B6 Items', 'scid_a146', 'scid_a147', 'scid_a147cnt', 'New CPDD Symptom Count']]
                        specific_cpdd_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cpdd_subject_db_2)
                        csv = convert_df(specific_cpdd_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cpdd_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'PPDD':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Persistent Depressive Disorder # Just checking for calculation errors
                ppdd_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_a158', 'scid_a159', 'scid_a160', 'scid_a161', 'scid_a162', 'scid_a163', 'scid_a164', 
                'scid_a164cnt']]

                # Setting index to subject_id
                ppdd_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                ppdd_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                ppdd_full_db = ppdd_full_db.astype({'scid_a158':'int', 'scid_a159':'int', 'scid_a160':'int', 'scid_a161':'int', 'scid_a162':'int', 'scid_a163':'int', 'scid_a164':'int', 
                'scid_a164cnt':'int'})

                # Counting ppdd symptoms # Max number is 7
                ppdd_full_db['B1 Items'] = np.where(((ppdd_full_db['scid_a158'] == 3)), 1, 0)
                ppdd_full_db['B2 Items'] = np.where(((ppdd_full_db['scid_a159'] == 3)), 1, 0)
                ppdd_full_db['B3 Items'] = np.where(((ppdd_full_db['scid_a160'] == 3)), 1, 0)
                ppdd_full_db['B4 Items'] = np.where(((ppdd_full_db['scid_a161'] == 3)), 1, 0)
                ppdd_full_db['B5 Items'] = np.where(((ppdd_full_db['scid_a162'] == 3)), 1, 0)
                ppdd_full_db['B6 Items'] = np.where(((ppdd_full_db['scid_a163'] == 3)), 1, 0)
                
                # Checking Criterion B item Discrepancy
                ppdd_full_db['PPDD Criterion B Discrepancy'] = np.where(((ppdd_full_db['scid_a164cnt'] >= 2) & (ppdd_full_db['scid_a164'] !=3)), "Problem", "Fine")
                
                # Checking count discrepancy
                ppdd_full_db['New PPDD Symptom Count'] = ppdd_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items']].sum(axis = 1)
                ppdd_full_db['PPDD Symptom Count Discrepancy'] = np.where((ppdd_full_db['scid_a164cnt'] != ppdd_full_db['New PPDD Symptom Count']), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_ppdd_db = ppdd_full_db.loc[:, ['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'scid_a164', 'scid_a164cnt',
                'PPDD Criterion B Discrepancy', 'New PPDD Symptom Count', 'PPDD Symptom Count Discrepancy']]
                
                refined_ppdd_db['Count Discrepancy Direction'] = np.where(((ppdd_full_db['scid_a164cnt'] - ppdd_full_db['New PPDD Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_ppdd_db['Count Discrepancy Value'] = ppdd_full_db['scid_a164cnt'] - ppdd_full_db['New PPDD Symptom Count']
                
                only_problem_children_ppdd = refined_ppdd_db.loc[((refined_ppdd_db['PPDD Criterion B Discrepancy'] == 'Problem') | (refined_ppdd_db['PPDD Symptom Count Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a164cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PPDD Criterion A Discrepancy** - The Criterion A item (scid_a164) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New PPDD Symptom Count** - My new symptom count using the Bx Item columns.")
                
                interviewer_selection_ppdd = st.checkbox("Would you like to see the associated interviewer?", key = 'ppdd')
                if interviewer_selection_ppdd:
                    problem_children_ppdd_final = only_problem_children_ppdd[['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'scid_a164', 'PPDD Criterion B Discrepancy',
                    'scid_a164cnt', 'New PPDD Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_ppdd_final)
                    csv = convert_df(problem_children_ppdd_final)
                else:
                    problem_children_ppdd_final = only_problem_children_ppdd[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'scid_a164', 'PPDD Criterion B Discrepancy',
                    'scid_a164cnt', 'New PPDD Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_ppdd_final)
                    csv = convert_df(problem_children_ppdd_final)  
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_ppdd_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'ppdd_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_ppdd_final[problem_children_ppdd_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_ppdd_final[problem_children_ppdd_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                ppdd_problem_subject_list = problem_children_ppdd_final.index.values.tolist()
                see_more_ppdd = st.multiselect("See Specific Subject Info? [Select as many as you would like]", ppdd_problem_subject_list)
                interviewer_selection_ppdd_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_ppdd')
                if see_more_ppdd is not None:
                    if interviewer_selection_ppdd_2:
                        specific_ppdd_subject_db = ppdd_full_db.loc[see_more_ppdd,:]
                        specific_ppdd_subject_db_2 = specific_ppdd_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a158', 'B2 Items', 'scid_a159', 'B3 Items', 'scid_a160', 
                        'B4 Items', 'scid_a161', 'B5 Items', 'scid_a162', 'B6 Items', 'scid_a163', 'scid_a164', 'scid_a164cnt', 'New PPDD Symptom Count']]
                        specific_ppdd_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_ppdd_subject_db_2)
                        csv = convert_df(specific_ppdd_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'ppdd_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_ppdd_subject_db = ppdd_full_db.loc[see_more_ppdd,:]
                        specific_ppdd_subject_db_2 = specific_ppdd_subject_db.loc[:,['B1 Items', 'scid_a158', 'B2 Items', 'scid_a159', 'B3 Items', 'scid_a160', 
                        'B4 Items', 'scid_a161', 'B5 Items', 'scid_a162', 'B6 Items', 'scid_a163', 'scid_a164', 'scid_a164cnt', 'New PPDD Symptom Count']]
                        specific_ppdd_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_ppdd_subject_db_2)
                        csv = convert_df(specific_ppdd_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'ppdd_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'PDD':
                st.markdown(f"### {module_a_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Premenstrual Dysphoric Disorder # Just checking for calculation errors
                pdd_full_db = module_a_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_a174', 'scid_a175a', 'scid_a175b', 'scid_a176a', 'scid_a176b', 'scid_a177', 'scid_a178', 
                'scid_a178cnt', 'scid_a179', 'scid_a180', 'scid_a181', 'scid_a182', 'scid_a183', 'scid_a184', 'scid_a185', 'scid_a186', 'scid_a187', 'scid_a187cnt']]

                # Setting index to subject_id
                pdd_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                pdd_full_db.fillna(0, inplace = True)

                # Setting the scid variable to integers instead of floats as it's more legible
                pdd_full_db = pdd_full_db.astype({'scid_a174':'int', 'scid_a175a':'int', 'scid_a175b':'int', 'scid_a176a':'int', 'scid_a176b':'int', 'scid_a177':'int', 'scid_a178':'int', 
                'scid_a178cnt':'int', 'scid_a179':'int', 'scid_a180':'int', 'scid_a181':'int', 'scid_a182':'int', 'scid_a183':'int', 'scid_a184':'int', 'scid_a185':'int', 'scid_a186':'int',
                'scid_a187':'int', 'scid_a187cnt':'int'})

                # Counting pdd symptoms # Max number is 6
                pdd_full_db['B1 Items'] = np.where(((pdd_full_db['scid_a174'] == 3)), 1, 0)
                pdd_full_db['B2 Items'] = np.where(((pdd_full_db['scid_a175a'] == 3) | (pdd_full_db['scid_a175b'])), 1, 0)
                pdd_full_db['B3 Items'] = np.where(((pdd_full_db['scid_a176a'] == 3)  | (pdd_full_db['scid_a176b'])), 1, 0)
                pdd_full_db['B4 Items'] = np.where(((pdd_full_db['scid_a177'] == 3)), 1, 0)
                pdd_full_db['C1 Items'] = np.where(((pdd_full_db['scid_a179'] == 3)), 1, 0)
                pdd_full_db['C2 Items'] = np.where(((pdd_full_db['scid_a180'] == 3)), 1, 0)
                pdd_full_db['C3 Items'] = np.where(((pdd_full_db['scid_a181'] == 3)), 1, 0)
                pdd_full_db['C4 Items'] = np.where(((pdd_full_db['scid_a182'] == 3)), 1, 0)
                pdd_full_db['C5 Items'] = np.where(((pdd_full_db['scid_a183'] == 3)), 1, 0)
                pdd_full_db['C6 Items'] = np.where(((pdd_full_db['scid_a184'] == 3)), 1, 0)
                pdd_full_db['C7 Items'] = np.where(((pdd_full_db['scid_a185'] == 3)), 1, 0)
                
                # Checking Criterion B item Discrepancy (For B >= 2 and for B + C >= 5) # Based on the eInterview count
                pdd_full_db['PDD Criterion B Discrepancy'] = np.where(((pdd_full_db['scid_a178cnt'] >= 2) & (pdd_full_db['scid_a178'] !=3)), "Problem", "Fine")
                pdd_full_db['PDD Criterion B+C Discrepancy'] = np.where(((pdd_full_db['scid_a187cnt'] >= 5) & (pdd_full_db['scid_a187'] != 3)), "Problem", "Fine")
                
                # Checking count discrepancy
                # Getting Manual Count
                pdd_full_db['New PDD Symptom Count (B)'] = pdd_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items']].sum(axis = 1)
                pdd_full_db['New PDD Symptom Count (C)'] = pdd_full_db.loc[:, ['C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'C7 Items']].sum(axis = 1)
                pdd_full_db['New PDD Symptom Count (B+C)'] = pdd_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items','C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'C7 Items']].sum(axis = 1)
                # Checking real count vs. eInterview count
                pdd_full_db['PDD Symptom Count Discrepancy (B)'] = np.where((pdd_full_db['scid_a178cnt'] != pdd_full_db['New PDD Symptom Count (B)']), "Problem", "Fine")
                pdd_full_db['PDD Symptom Count Discrepancy (B+C)'] = np.where((pdd_full_db['scid_a187cnt'] != pdd_full_db['New PDD Symptom Count (B+C)']), "Problem", "Fine")
                # Checking Criterion C Discrepancy using new Manual Count
                pdd_full_db['PDD Criterion C Discrepancy'] = np.where(((pdd_full_db['New PDD Symptom Count (C)'] >= 1) & (pdd_full_db['scid_a186'] != 3)), "Problem", "Fine")
                
                # Only getting Count Items and Discrepancy Items
                refined_pdd_db = pdd_full_db.loc[:, ['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'scid_a178', 'scid_a178cnt', 'C1 Items', 'C2 Items', 'C3 Items', 
                'C4 Items', 'C5 Items', 'C6 Items', 'C7 Items', 'scid_a186', 'scid_a187', 'scid_a187cnt', 'PDD Criterion B Discrepancy', 'PDD Criterion C Discrepancy', 'PDD Criterion B+C Discrepancy',
                'New PDD Symptom Count (B)', 'New PDD Symptom Count (C)', 'New PDD Symptom Count (B+C)', 'PDD Symptom Count Discrepancy (B)', 'PDD Symptom Count Discrepancy (B+C)']]
                
                # Checking the Discrepancy between eInterview count and the new manual count
                refined_pdd_db['Count Discrepancy Direction (B)'] = np.where(((pdd_full_db['scid_a178cnt'] - pdd_full_db['New PDD Symptom Count (B)']) > 0), 'Original Count Larger', np.where(((pdd_full_db['scid_a178cnt'] - pdd_full_db['New PDD Symptom Count (B)']) == 0), "Same", "New Count Larger"))
                refined_pdd_db['Count Discrepancy Value (B)'] = pdd_full_db['scid_a178cnt'] - pdd_full_db['New PDD Symptom Count (B)']
                refined_pdd_db['Count Discrepancy Direction (B+C)'] = np.where(((pdd_full_db['scid_a187cnt'] - pdd_full_db['New PDD Symptom Count (B+C)']) > 0), 'Original Count Larger', np.where(((pdd_full_db['scid_a187cnt'] - pdd_full_db['New PDD Symptom Count (B+C)']) == 0), "Same", "New Count Larger"))
                refined_pdd_db['Count Discrepancy Value (B+C)'] = pdd_full_db['scid_a187cnt'] - pdd_full_db['New PDD Symptom Count (B+C)']
                
                # Filtering for subjects that have problems
                only_problem_children_pdd = refined_pdd_db.loc[((refined_pdd_db['PDD Criterion B Discrepancy'] == 'Problem') | (refined_pdd_db['PDD Symptom Count Discrepancy (B)'] == 'Problem') |
                (refined_pdd_db['PDD Symptom Count Discrepancy (B+C)'] == 'Problem') | (refined_pdd_db['PDD Criterion C Discrepancy'] == 'Problem') | (refined_pdd_db['PDD Criterion B+C Discrepancy'] == 'Problem'))]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a178cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PDD Criterion B Discrepancy** - The Criterion B item (scid_a178) should only be marked 3 (threshold) if 1 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **PDD Criterion C Discrepancy** - The Criterion C item (scid_a186) should only be marked as 3 if 1 or more symptoms are accounted for. This column checks to see if that is the case. ")
                    st.markdown("- **PDD Criterion B+C Discrepancy** - The Criterion B+C item (scid_a187) should only be marked 3 if 5 or more symptoms are accounted for. this column checks to see if that is the case.")
                    st.markdown("- **New PDD Symptom Count (B)** - My new symptom count using the Bx Item columns.")
                    st.markdown("- **New PDD Symptom Count (C)** - My new symptom count using the Cx items columns.")
                    st.markdown("- **New PDD Symptom Count (B+C)** - My new symptom count using the Bx Item columns and the Cx Item columns.")
                
                interviewer_selection_pdd = st.checkbox("Would you like to see the associated interviewer?", key = 'pdd')
                if interviewer_selection_pdd:
                    problem_children_pdd_final = only_problem_children_pdd[['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items','scid_a178', 'PDD Criterion B Discrepancy', 'scid_a178cnt', 
                    'New PDD Symptom Count (B)', 'Count Discrepancy Direction (B)', 'Count Discrepancy Value (B)', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items',
                    'C6 Items', 'C7 Items', 'scid_a186', 'PDD Criterion C Discrepancy', 'scid_a187', 'PDD Criterion B+C Discrepancy', 'scid_a187cnt', 'New PDD Symptom Count (B+C)', 'Count Discrepancy Direction (B+C)',
                    'Count Discrepancy Value (B+C)']]
                    st.write(problem_children_pdd_final)
                    csv = convert_df(problem_children_pdd_final)
                else:
                    problem_children_pdd_final = only_problem_children_pdd[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items','scid_a178', 'PDD Criterion B Discrepancy', 'scid_a178cnt', 
                    'New PDD Symptom Count (B)', 'Count Discrepancy Direction (B)', 'Count Discrepancy Value (B)', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items',
                    'C6 Items', 'C7 Items', 'scid_a186', 'PDD Criterion C Discrepancy', 'scid_a187', 'PDD Criterion B+C Discrepancy', 'scid_a187cnt', 'New PDD Symptom Count (B+C)', 'Count Discrepancy Direction (B+C)',
                    'Count Discrepancy Value (B+C)']]
                    st.write(problem_children_pdd_final)
                    csv = convert_df(problem_children_pdd_final)  
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_pdd_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'pdd_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with Criterion B **New Count Larger**:", len(problem_children_pdd_final[problem_children_pdd_final['Count Discrepancy Direction (B)'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with Criterion B **Original Count Larger:**", len(problem_children_pdd_final[problem_children_pdd_final['Count Discrepancy Direction (B)'] == 'Original Count Larger'].index))
                    st.write("Number of Subjects with Criterion B **Counts the Same:**", len(problem_children_pdd_final[problem_children_pdd_final['Count Discrepancy Direction (B)'] == 'Same'].index))
                    st.write("Number of Subjects with Criterion B+C **New Count Larger**:", len(problem_children_pdd_final[problem_children_pdd_final['Count Discrepancy Direction (B+C)'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with Criterion B+C **Original Count Larger:**", len(problem_children_pdd_final[problem_children_pdd_final['Count Discrepancy Direction (B+C)'] == 'Original Count Larger'].index))
                    st.write("Number of Subjects with Criterion B+C **Counts the Same:**", len(problem_children_pdd_final[problem_children_pdd_final['Count Discrepancy Direction (B+C)'] == 'Same'].index))
                pdd_problem_subject_list = problem_children_pdd_final.index.values.tolist()
                see_more_pdd = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pdd_problem_subject_list)
                interviewer_selection_pdd_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_pdd')
                if see_more_pdd is not None:
                    if interviewer_selection_pdd_2:
                        specific_pdd_subject_db = pdd_full_db.loc[see_more_pdd,:]
                        specific_pdd_subject_db_2 = specific_pdd_subject_db.loc[:,['scid_interviewername','B1 Items', 'scid_a174', 'B2 Items', 'scid_a175a', 'scid_a175b', 'B3 Items', 'scid_a176a', 'scid_a176b',
                        'B4 Items', 'scid_a177', 'scid_a178', 'scid_a178cnt', 'New PDD Symptom Count (B)', 'C1 Items', 'scid_a179', 'C2 Items', 'scid_a180', 'C3 Items','scid_a181', 'C4 Items', 'scid_a182',
                        'C5 Items', 'scid_a183', 'C6 Items', 'scid_a184', 'C7 Items', 'scid_a185', 'scid_a186', 'scid_a187', 'scid_a187cnt', 'New PDD Symptom Count (B+C)']]
                        specific_pdd_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pdd_subject_db_2)
                        csv = convert_df(specific_pdd_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pdd_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_pdd_subject_db = pdd_full_db.loc[see_more_pdd,:]
                        specific_pdd_subject_db_2 = specific_pdd_subject_db.loc[:,['B1 Items', 'scid_a174', 'B2 Items', 'scid_a175a', 'scid_a175b', 'B3 Items', 'scid_a176a', 'scid_a176b',
                        'B4 Items', 'scid_a177', 'scid_a178', 'scid_a178cnt', 'New PDD Symptom Count (B)', 'C1 Items', 'scid_a179', 'C2 Items', 'scid_a180', 'C3 Items','scid_a181', 'C4 Items', 'scid_a182',
                        'C5 Items', 'scid_a183', 'C6 Items', 'scid_a184', 'C7 Items', 'scid_a185', 'scid_a186', 'scid_a187', 'scid_a187cnt', 'New PDD Symptom Count (B+C)']]
                        specific_pdd_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pdd_subject_db_2)
                        csv = convert_df(specific_pdd_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pdd_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
        if module_selection == 'Module E':
            module_e_syndrome_selection = st.sidebar.selectbox("Which disorder would you like to look at?", ["---", "CAUD", "PAUD", "CSUD", "PSUD"])
            st.markdown(f"## {module_selection}")
            st.markdown("---")
            if module_e_syndrome_selection == '---':
                st.markdown("### Options:")
                st.markdown("- **'CAUD'** - Current Alcohol Use Disorder")
                st.markdown("- **'PAUD'** - Past Alcohol Use Disorder")
                st.markdown("- **'CSUD'** - Current Substance Use Disorder [Will have the option to look at individual substances]")
                st.markdown("- **'PSUD'** - Past Substance Use Disorder [Will have the option to look at individual substances]")
            if module_e_syndrome_selection == 'CAUD':
                st.markdown(f"### {module_e_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_e_items_db = pd.read_excel(module_e_file)
                
                # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                module_e_db = full_db.loc[:, final_list]

                # Current Alcohol Use Disorder # Just Checking Calculation errors
                caud_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e2a', 'scid_e2b', 'scid_e3a', 'scid_e3b', 'scid_e4', 'scid_e5', 'scid_e6a', 'scid_e6b', 'scid_e7', 'scid_e8',
                'scid_e9', 'scid_e10a', 'scid_e10b', 'scid_e11a', 'scid_e11b', 'scid_e12a', 'scid_e12b', 'scid_e13', 'scid_e13cnt', 'scid_e14s', 'scid_e14cnt']]

                # Setting index to subject_id
                caud_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                caud_full_db.fillna(0, inplace = True)

                # Have to convert 3u option in scid_e5 to just 3
                caud_full_db['scid_e5'] = caud_full_db['scid_e5'].replace("3u", "3")

                # Setting the scid variable to integers instead of floats as it's more legible
                caud_full_db = caud_full_db.astype({'scid_e2a':'int', 'scid_e2b':'int', 'scid_e3a':'int', 'scid_e3b':'int', 'scid_e4':'int', 'scid_e5':'int', 'scid_e6a':'int', 'scid_e6b':'int',
                'scid_e7':'int', 'scid_e8':'int', 'scid_e9':'int', 'scid_e10a':'int', 'scid_e10b':'int', 'scid_e11a':'int', 'scid_e11b':'int', 'scid_e12a':'int', 'scid_e12b':'int',
                'scid_e13':'int', 'scid_e13cnt':'int', 'scid_e14s':'int', 'scid_e14cnt':'int'})

                # Counting CAUD symptoms # Max is 11
                caud_full_db['A1 Items'] = np.where(((caud_full_db['scid_e2a'] == 3) | (caud_full_db['scid_e2b'] == 3)), 1, 0)
                caud_full_db['A2 Items'] = np.where(((caud_full_db['scid_e3a'] == 3) | (caud_full_db['scid_e3b'] == 3)), 1, 0)
                caud_full_db['A3 Items'] = np.where(((caud_full_db['scid_e4'] == 3)), 1, 0)
                caud_full_db['A4 Items'] = np.where(((caud_full_db['scid_e5'] == 3)), 1, 0)
                caud_full_db['A5 Items'] = np.where(((caud_full_db['scid_e6a'] == 3) | (caud_full_db['scid_e6b'] == 3)), 1, 0)
                caud_full_db['A6 Items'] = np.where(((caud_full_db['scid_e7'] == 3)), 1, 0)
                caud_full_db['A7 Items'] = np.where(((caud_full_db['scid_e8'] == 3)), 1, 0)
                caud_full_db['A8 Items'] = np.where(((caud_full_db['scid_e9'] == 3)), 1, 0)
                caud_full_db['A9 Items'] = np.where(((caud_full_db['scid_e10a'] == 3) | (caud_full_db['scid_e10b'] == 3)), 1, 0)
                caud_full_db['A10 Items'] = np.where(((caud_full_db['scid_e11a'] == 3) | (caud_full_db['scid_e11b'] == 3)), 1, 0)
                caud_full_db['A11 Items'] = np.where(((caud_full_db['scid_e12a'] == 3) | (caud_full_db['scid_e12b'] == 3)), 1, 0)

                # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                caud_full_db['CAUD Criterion A Discrepancy'] = np.where(((caud_full_db['scid_e13cnt'] >= 2) & (caud_full_db['scid_e13'] != 3)), "Problem", "Fine")

                # Checking Count Discrepancy
                caud_full_db['New CAUD Symptom Count'] = caud_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                caud_full_db['CAUD Symptom Count Discrepancy'] = np.where(((caud_full_db['New CAUD Symptom Count'] != caud_full_db['scid_e13cnt'])), "Problem", "Fine")
                # Checking the Severity symptom count item # Should only be entered if scid_e13 == 3 (will want to catch those who answered when they shouldn't have and catch those that should have and didn't)
                caud_full_db['CAUD Severity Count Discrepancy'] = np.where(((caud_full_db['scid_e13'] == 1) & (caud_full_db['scid_e14s'] != 0)), "Shouldn't have answered e14s", 
                np.where(((caud_full_db['scid_e13'] == 3) & (caud_full_db['scid_e14s'] == 0)), "Should have answered e14s", 
                np.where(((caud_full_db['scid_e13'] == 3) & (caud_full_db['scid_e13cnt'] != caud_full_db['scid_e14cnt'])), "Problem", "Fine")))

                # Getting the Count Items and the Dsicrepancy Items
                refined_caud_db = caud_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                'A10 Items', 'A11 Items', 'scid_e13', 'scid_e13cnt', 'scid_e14s', 'scid_e14cnt', 'CAUD Criterion A Discrepancy', 'New CAUD Symptom Count', 
                'CAUD Symptom Count Discrepancy', 'CAUD Severity Count Discrepancy']]

                # Getting Count Discrepancy direction and Value
                refined_caud_db['Count Discrepancy Direction'] = np.where(((caud_full_db['scid_e13cnt'] - caud_full_db['New CAUD Symptom Count']) > 0), "Original Count Larger", 
                np.where(((caud_full_db['scid_e13cnt'] == caud_full_db['New CAUD Symptom Count'])), "Same", "New Count Larger"))
                refined_caud_db['Count Discrepancy Value'] = caud_full_db['scid_e13cnt'] - caud_full_db['New CAUD Symptom Count']
                
                # Selecting to see All problems or just normal Criteria A problems
                error_selection_caud = st.selectbox("What errors would you like to see?", ["---", "All", "Only Criterion A"])
                if error_selection_caud == "---":
                    st.write("Selecting All will display all errors including discrepancies found with the severity item count.")
                    st.write("Selection Only Criterion A will only check the new manual count versus the old eInterview count.")
                if error_selection_caud == "All":
                    # Getting Only "Problem Subjects"
                    only_problem_children_caud = refined_caud_db.loc[((refined_caud_db['CAUD Symptom Count Discrepancy'] == "Problem") | (refined_caud_db['CAUD Criterion A Discrepancy'] == 'Problem')
                    | (refined_caud_db['CAUD Severity Count Discrepancy'] != "Fine"))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e13cnt) and the table below outlines where the count item does not match the actual symptom count.")
                            st.write("- There is also a severity item symptom count scid_e14cnt, which should in theory be identical to scid_e13cnt.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CAUD Criterion A Discrepancy** - The Criterion A item (scid_e13) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CAUD Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CAUD Severity Count Discrepancy** - Checks first whether the severity item was or was not answered appropriately. Then, for the appropriate subjects, it checks to see if the symptom counts match between scid_e13cnt and scid_e14cnt.")
                        st.markdown("- **CAUD Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_caud = st.checkbox("Would you like to see the associated interviewer?", key = 'caud')
                    if interviewer_selection_caud:
                        problem_children_caud_final = only_problem_children_caud[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e13', 'scid_e14s', 'CAUD Criterion A Discrepancy', 'scid_e13cnt', 'New CAUD Symptom Count', 'scid_e14cnt', 'CAUD Severity Count Discrepancy',
                        'CAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        
                        st.write(problem_children_caud_final)
                        csv = convert_df(problem_children_caud_final)
                    else:
                        problem_children_caud_final = only_problem_children_caud[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e13', 'scid_e14s', 'CAUD Criterion A Discrepancy', 'scid_e13cnt', 'New CAUD Symptom Count', 'scid_e14cnt', 'CAUD Severity Count Discrepancy',
                        'CAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        st.write(problem_children_caud_final)
                        csv = convert_df(problem_children_caud_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_caud_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'caud_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_caud_final[problem_children_caud_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_caud_final[problem_children_caud_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                        st.write("Number of Subjects with **Counts being equal:**", len(problem_children_caud_final[problem_children_caud_final['Count Discrepancy Direction'] == 'Same'].index))
                    caud_problem_subject_list = problem_children_caud_final.index.values.tolist()
                    see_more_caud = st.multiselect("See Specific Subject Info? [Select as many as you would like]", caud_problem_subject_list)
                    interviewer_selection_caud_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_caud')
                    if see_more_caud is not None:
                        if interviewer_selection_caud_2:
                            specific_caud_subject_db = caud_full_db.loc[see_more_caud,:]
                            specific_caud_subject_db_2 = specific_caud_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e2a', 'scid_e2b', 'A2 Items', 'scid_e3a', 'scid_e3b',
                            'A3 Items', 'scid_e4', 'A4 Items', 'scid_e5', 'A5 Items', 'scid_e6a', 'scid_e6b', 'A6 Items', 'scid_e7', 'A7 Items', 'scid_e8', 'A8 Items', 'scid_e9', 
                            'A9 Items', 'scid_e10a', 'scid_e10b', 'A10 Items', 'scid_e11a', 'scid_e11b', 'A11 Items', 'scid_e12a', 'scid_e12b', 'scid_e13', 'scid_e13cnt', 'New CAUD Symptom Count',
                            'scid_e14s', 'scid_e14cnt']]
                            specific_caud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_caud_subject_db_2)
                            csv = convert_df(specific_caud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'caud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_caud_subject_db = caud_full_db.loc[see_more_caud,:]
                            specific_caud_subject_db_2 = specific_caud_subject_db.loc[:,['A1 Items', 'scid_e2a', 'scid_e2b', 'A2 Items', 'scid_e3a', 'scid_e3b',
                            'A3 Items', 'scid_e4', 'A4 Items', 'scid_e5', 'A5 Items', 'scid_e6a', 'scid_e6b', 'A6 Items', 'scid_e7', 'A7 Items', 'scid_e8', 'A8 Items', 'scid_e9', 
                            'A9 Items', 'scid_e10a', 'scid_e10b', 'A10 Items', 'scid_e11a', 'scid_e11b', 'A11 Items', 'scid_e12a', 'scid_e12b', 'scid_e13', 'scid_e13cnt', 'New CAUD Symptom Count',
                            'scid_e14s', 'scid_e14cnt']]
                            specific_caud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_caud_subject_db_2)
                            csv = convert_df(specific_caud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'caud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if error_selection_caud == "Only Criterion A":
                     # Getting Only "Problem Subjects"
                    only_problem_children_caud = refined_caud_db.loc[((refined_caud_db['CAUD Symptom Count Discrepancy'] == "Problem") | (refined_caud_db['CAUD Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e13cnt) and the table below outlines where the count item does not match the actual symptom count.")
                            st.write("- There is also a severity item symptom count scid_e14cnt, which should in theory be identical to scid_e13cnt.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CAUD Criterion A Discrepancy** - The Criterion A item (scid_e13) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CAUD Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CAUD Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_caud = st.checkbox("Would you like to see the associated interviewer?", key = 'caud')
                    if interviewer_selection_caud:
                        problem_children_caud_final = only_problem_children_caud[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e13', 'scid_e14s', 'CAUD Criterion A Discrepancy', 'scid_e13cnt', 'New CAUD Symptom Count', 'scid_e14cnt',
                        'CAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        
                        st.write(problem_children_caud_final)
                        csv = convert_df(problem_children_caud_final)
                    else:
                        problem_children_caud_final = only_problem_children_caud[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e13', 'scid_e14s', 'CAUD Criterion A Discrepancy', 'scid_e13cnt', 'New CAUD Symptom Count', 'scid_e14cnt',
                        'CAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        st.write(problem_children_caud_final)
                        csv = convert_df(problem_children_caud_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_caud_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'caud_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_caud_final[problem_children_caud_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_caud_final[problem_children_caud_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    caud_problem_subject_list = problem_children_caud_final.index.values.tolist()
                    see_more_caud = st.multiselect("See Specific Subject Info? [Select as many as you would like]", caud_problem_subject_list)
                    interviewer_selection_caud_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_caud')
                    if see_more_caud is not None:
                        if interviewer_selection_caud_2:
                            specific_caud_subject_db = caud_full_db.loc[see_more_caud,:]
                            specific_caud_subject_db_2 = specific_caud_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e2a', 'scid_e2b', 'A2 Items', 'scid_e3a', 'scid_e3b',
                            'A3 Items', 'scid_e4', 'A4 Items', 'scid_e5', 'A5 Items', 'scid_e6a', 'scid_e6b', 'A6 Items', 'scid_e7', 'A7 Items', 'scid_e8', 'A8 Items', 'scid_e9', 
                            'A9 Items', 'scid_e10a', 'scid_e10b', 'A10 Items', 'scid_e11a', 'scid_e11b', 'A11 Items', 'scid_e12a', 'scid_e12b', 'scid_e13', 'scid_e13cnt', 'New CAUD Symptom Count']]
                            specific_caud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_caud_subject_db_2)
                            csv = convert_df(specific_caud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'caud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_caud_subject_db = caud_full_db.loc[see_more_caud,:]
                            specific_caud_subject_db_2 = specific_caud_subject_db.loc[:,['A1 Items', 'scid_e2a', 'scid_e2b', 'A2 Items', 'scid_e3a', 'scid_e3b',
                            'A3 Items', 'scid_e4', 'A4 Items', 'scid_e5', 'A5 Items', 'scid_e6a', 'scid_e6b', 'A6 Items', 'scid_e7', 'A7 Items', 'scid_e8', 'A8 Items', 'scid_e9', 
                            'A9 Items', 'scid_e10a', 'scid_e10b', 'A10 Items', 'scid_e11a', 'scid_e11b', 'A11 Items', 'scid_e12a', 'scid_e12b', 'scid_e13', 'scid_e13cnt', 'New CAUD Symptom Count']]
                            specific_caud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_caud_subject_db_2)
                            csv = convert_df(specific_caud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'caud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_e_syndrome_selection == 'PAUD':
                st.markdown(f"### {module_e_syndrome_selection}")
                st.markdown("---")
                
                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_e_items_db = pd.read_excel(module_e_file)
                
                # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                module_e_db = full_db.loc[:, final_list]

                # Past Alcohol Use Disorder # Just Checking Calculation errors
                paud_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e22a', 'scid_e22b', 'scid_e23a', 'scid_e23b', 'scid_e24', 'scid_e25', 'scid_e26a', 'scid_e26b', 'scid_e27', 'scid_e28',
                'scid_e29', 'scid_e30a', 'scid_e30b', 'scid_e31a', 'scid_e31b', 'scid_e32a', 'scid_e32b', 'scid_e33', 'scid_e33cnt', 'scid_e34', 'scid_e34cnt']]

                # Setting index to subject_id
                paud_full_db.set_index('subject_id', inplace = True)

                # Filling all na values with 0 in order to run comparisons
                paud_full_db.fillna(0, inplace = True)

                # Have to convert 3u option in scid_e25 to just 3
                paud_full_db['scid_e25'] = paud_full_db['scid_e25'].replace("3u", "3")

                # Setting the scid variable to integers instead of floats as it's more legible
                paud_full_db = paud_full_db.astype({'scid_e22a':'int', 'scid_e22b':'int', 'scid_e23a':'int', 'scid_e23b':'int', 'scid_e24':'int', 'scid_e25':'int', 'scid_e26a':'int', 'scid_e26b':'int',
                'scid_e27':'int', 'scid_e28':'int', 'scid_e29':'int', 'scid_e30a':'int', 'scid_e30b':'int', 'scid_e31a':'int', 'scid_e31b':'int', 'scid_e32a':'int', 'scid_e32b':'int',
                'scid_e33':'int', 'scid_e33cnt':'int', 'scid_e34':'int', 'scid_e34cnt':'int'})

                # Counting PAUD symptoms # Max is 11
                paud_full_db['A1 Items'] = np.where(((paud_full_db['scid_e22a'] == 3) | (paud_full_db['scid_e22b'] == 3)), 1, 0)
                paud_full_db['A2 Items'] = np.where(((paud_full_db['scid_e23a'] == 3) | (paud_full_db['scid_e23b'] == 3)), 1, 0)
                paud_full_db['A3 Items'] = np.where(((paud_full_db['scid_e24'] == 3)), 1, 0)
                paud_full_db['A4 Items'] = np.where(((paud_full_db['scid_e25'] == 3)), 1, 0)
                paud_full_db['A5 Items'] = np.where(((paud_full_db['scid_e26a'] == 3) | (paud_full_db['scid_e26b'] == 3)), 1, 0)
                paud_full_db['A6 Items'] = np.where(((paud_full_db['scid_e27'] == 3)), 1, 0)
                paud_full_db['A7 Items'] = np.where(((paud_full_db['scid_e28'] == 3)), 1, 0)
                paud_full_db['A8 Items'] = np.where(((paud_full_db['scid_e29'] == 3)), 1, 0)
                paud_full_db['A9 Items'] = np.where(((paud_full_db['scid_e30a'] == 3) | (paud_full_db['scid_e30b'] == 3)), 1, 0)
                paud_full_db['A10 Items'] = np.where(((paud_full_db['scid_e31a'] == 3) | (paud_full_db['scid_e31b'] == 3)), 1, 0)
                paud_full_db['A11 Items'] = np.where(((paud_full_db['scid_e32a'] == 3) | (paud_full_db['scid_e32b'] == 3)), 1, 0)

                # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                paud_full_db['PAUD Criterion A Discrepancy'] = np.where(((paud_full_db['scid_e33cnt'] >= 2) & (paud_full_db['scid_e33'] != 3)), "Problem", "Fine")

                # Checking Count Discrepancy
                paud_full_db['New PAUD Symptom Count'] = paud_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                paud_full_db['PAUD Symptom Count Discrepancy'] = np.where(((paud_full_db['New PAUD Symptom Count'] != paud_full_db['scid_e33cnt'])), "Problem", "Fine")
                # Checking the Severity symptom count item # Should only be entered if scid_e33 == 3 (will want to catch those who answered when they shouldn't have and catch those that should have and didn't)
                paud_full_db['PAUD Severity Count Discrepancy'] = np.where(((paud_full_db['scid_e33'] == 1) & (paud_full_db['scid_e34'] != 0)), "Shouldn't have answered e14s", 
                np.where(((paud_full_db['scid_e33'] == 3) & (paud_full_db['scid_e34'] == 0)), "Should have answered e14s", 
                np.where(((paud_full_db['scid_e33'] == 3) & (paud_full_db['scid_e33cnt'] != paud_full_db['scid_e34cnt'])), "Problem", "Fine")))

                # Getting the Count Items and the Dsicrepancy Items
                refined_paud_db = paud_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                'A10 Items', 'A11 Items', 'scid_e33', 'scid_e33cnt', 'scid_e34', 'scid_e34cnt', 'PAUD Criterion A Discrepancy', 'New PAUD Symptom Count', 
                'PAUD Symptom Count Discrepancy', 'PAUD Severity Count Discrepancy']]

                # Getting Count Discrepancy direction and Value
                refined_paud_db['Count Discrepancy Direction'] = np.where(((paud_full_db['scid_e33cnt'] - paud_full_db['New PAUD Symptom Count']) > 0), "Original Count Larger", 
                np.where(((paud_full_db['scid_e33cnt'] == paud_full_db['New PAUD Symptom Count'])), "Same", "New Count Larger"))
                refined_paud_db['Count Discrepancy Value'] = paud_full_db['scid_e33cnt'] - paud_full_db['New PAUD Symptom Count']
                
                # Selecting to see All problems or just normal Criteria A problems
                error_selection_paud = st.selectbox("What errors would you like to see?", ["---", "All", "Only Criterion A"])
                if error_selection_paud == "---":
                    st.write("Selecting All will display all errors including discrepancies found with the severity item count.")
                    st.write("Selection Only Criterion A will only check the new manual count versus the old eInterview count.")
                if error_selection_paud == "All":
                    # Getting Only "Problem Subjects"
                    only_problem_children_paud = refined_paud_db.loc[((refined_paud_db['PAUD Symptom Count Discrepancy'] == "Problem") | (refined_paud_db['PAUD Criterion A Discrepancy'] == 'Problem')
                    | (refined_paud_db['PAUD Severity Count Discrepancy'] != "Fine"))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e33cnt) and the table below outlines where the count item does not match the actual symptom count.")
                            st.write("- There is also a severity item symptom count scid_e34cnt, which should in theory be identical to scid_e33cnt.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PAUD Criterion A Discrepancy** - The Criterion A item (scid_e33) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PAUD Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PAUD Severity Count Discrepancy** - Checks first whether the severity item was or was not answered appropriately. Then, for the appropriate subjects, it checks to see if the symptom counts match between scid_e33cnt and scid_e34cnt.")
                        st.markdown("- **PAUD Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_paud = st.checkbox("Would you like to see the associated interviewer?", key = 'paud')
                    if interviewer_selection_paud:
                        problem_children_paud_final = only_problem_children_paud[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e33', 'scid_e34', 'PAUD Criterion A Discrepancy', 'scid_e33cnt', 'New PAUD Symptom Count', 'scid_e34cnt', 'PAUD Severity Count Discrepancy',
                        'PAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        
                        st.write(problem_children_paud_final)
                        csv = convert_df(problem_children_paud_final)
                    else:
                        problem_children_paud_final = only_problem_children_paud[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e33', 'scid_e34', 'PAUD Criterion A Discrepancy', 'scid_e33cnt', 'New PAUD Symptom Count', 'scid_e34cnt', 'PAUD Severity Count Discrepancy',
                        'PAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        st.write(problem_children_paud_final)
                        csv = convert_df(problem_children_paud_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_paud_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'paud_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_paud_final[problem_children_paud_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_paud_final[problem_children_paud_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                        st.write("Number of Subjects with **Counts being equal:**", len(problem_children_paud_final[problem_children_paud_final['Count Discrepancy Direction'] == 'Same'].index))
                    paud_problem_subject_list = problem_children_paud_final.index.values.tolist()
                    see_more_paud = st.multiselect("See Specific Subject Info? [Select as many as you would like]", paud_problem_subject_list)
                    interviewer_selection_paud_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_paud')
                    if see_more_paud is not None:
                        if interviewer_selection_paud_2:
                            specific_paud_subject_db = paud_full_db.loc[see_more_paud,:]
                            specific_paud_subject_db_2 = specific_paud_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e22a', 'scid_e22b', 'A2 Items', 'scid_e23a', 'scid_e23b',
                            'A3 Items', 'scid_e24', 'A4 Items', 'scid_e25', 'A5 Items', 'scid_e26a', 'scid_e26b', 'A6 Items', 'scid_e27', 'A7 Items', 'scid_e28', 'A8 Items', 'scid_e29', 
                            'A9 Items', 'scid_e30a', 'scid_e30b', 'A10 Items', 'scid_e31a', 'scid_e31b', 'A11 Items', 'scid_e32a', 'scid_e32b', 'scid_e33', 'scid_e33cnt', 'New PAUD Symptom Count',
                            'scid_e34', 'scid_e34cnt']]
                            specific_paud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_paud_subject_db_2)
                            csv = convert_df(specific_paud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'paud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_paud_subject_db = paud_full_db.loc[see_more_paud,:]
                            specific_paud_subject_db_2 = specific_paud_subject_db.loc[:,['A1 Items', 'scid_e22a', 'scid_e22b', 'A2 Items', 'scid_e23a', 'scid_e23b',
                            'A3 Items', 'scid_e24', 'A4 Items', 'scid_e25', 'A5 Items', 'scid_e26a', 'scid_e26b', 'A6 Items', 'scid_e27', 'A7 Items', 'scid_e28', 'A8 Items', 'scid_e29', 
                            'A9 Items', 'scid_e30a', 'scid_e30b', 'A10 Items', 'scid_e31a', 'scid_e31b', 'A11 Items', 'scid_e32a', 'scid_e32b', 'scid_e33', 'scid_e33cnt', 'New PAUD Symptom Count',
                            'scid_e34', 'scid_e34cnt']]
                            specific_paud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_paud_subject_db_2)
                            csv = convert_df(specific_paud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'paud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if error_selection_paud == "Only Criterion A":
                    # Getting Only "Problem Subjects"
                    only_problem_children_paud = refined_paud_db.loc[((refined_paud_db['PAUD Symptom Count Discrepancy'] == "Problem") | (refined_paud_db['PAUD Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e33cnt) and the table below outlines where the count item does not match the actual symptom count.")
                            st.write("- There is also a severity item symptom count scid_e34cnt, which should in theory be identical to scid_e33cnt.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PAUD Criterion A Discrepancy** - The Criterion A item (scid_e33) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PAUD Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PAUD Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_paud = st.checkbox("Would you like to see the associated interviewer?", key = 'paud')
                    if interviewer_selection_paud:
                        problem_children_paud_final = only_problem_children_paud[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e33', 'scid_e34', 'PAUD Criterion A Discrepancy', 'scid_e33cnt', 'New PAUD Symptom Count', 'scid_e34cnt',
                        'PAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        
                        st.write(problem_children_paud_final)
                        csv = convert_df(problem_children_paud_final)
                    else:
                        problem_children_paud_final = only_problem_children_paud[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e33', 'scid_e34', 'PAUD Criterion A Discrepancy', 'scid_e33cnt', 'New PAUD Symptom Count', 'scid_e34cnt',
                        'PAUD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                        st.write(problem_children_paud_final)
                        csv = convert_df(problem_children_paud_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_paud_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'paud_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_paud_final[problem_children_paud_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_paud_final[problem_children_paud_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    paud_problem_subject_list = problem_children_paud_final.index.values.tolist()
                    see_more_paud = st.multiselect("See Specific Subject Info? [Select as many as you would like]", paud_problem_subject_list)
                    interviewer_selection_paud_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_paud')
                    if see_more_paud is not None:
                        if interviewer_selection_paud_2:
                            specific_paud_subject_db = paud_full_db.loc[see_more_paud,:]
                            specific_paud_subject_db_2 = specific_paud_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e22a', 'scid_e22b', 'A2 Items', 'scid_e23a', 'scid_e23b',
                            'A3 Items', 'scid_e24', 'A4 Items', 'scid_e25', 'A5 Items', 'scid_e26a', 'scid_e26b', 'A6 Items', 'scid_e27', 'A7 Items', 'scid_e28', 'A8 Items', 'scid_e29', 
                            'A9 Items', 'scid_e30a', 'scid_e30b', 'A10 Items', 'scid_e31a', 'scid_e31b', 'A11 Items', 'scid_e32a', 'scid_e32b', 'scid_e33', 'scid_e33cnt', 'New PAUD Symptom Count']]
                            specific_paud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_paud_subject_db_2)
                            csv = convert_df(specific_paud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'paud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_paud_subject_db = paud_full_db.loc[see_more_paud,:]
                            specific_paud_subject_db_2 = specific_paud_subject_db.loc[:,['A1 Items', 'scid_e22a', 'scid_e22b', 'A2 Items', 'scid_e23a', 'scid_e23b',
                            'A3 Items', 'scid_e24', 'A4 Items', 'scid_e25', 'A5 Items', 'scid_e26a', 'scid_e26b', 'A6 Items', 'scid_e27', 'A7 Items', 'scid_e28', 'A8 Items', 'scid_e29', 
                            'A9 Items', 'scid_e30a', 'scid_e30b', 'A10 Items', 'scid_e31a', 'scid_e31b', 'A11 Items', 'scid_e32a', 'scid_e32b', 'scid_e33', 'scid_e33cnt', 'New PAUD Symptom Count']]
                            specific_paud_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_paud_subject_db_2)
                            csv = convert_df(specific_paud_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'paud_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_e_syndrome_selection == 'CSUD':
                st.markdown(f"### {module_e_syndrome_selection}")
                st.markdown("---")
                drug_selection_caud = st.selectbox("Which Drug would you like to look at?", ["---", "All", "Sed/Hyp/Anx", "Cannabis", "Stimulants", "Opioids", "Inhalants", "PCP", "Hallucinogens", "Other/Unknown"])
                if drug_selection_caud == "---":
                    st.write("Your options are as follows:")
                    st.markdown("- **All** - See all of the CSUD problems.")
                    st.markdown("- **Sed/Hyp/Anx**")
                    st.markdown("- **Cannabis**")
                    st.markdown("- **Stimulants**")
                    st.markdown("- **Opioids**")
                    st.markdown("- **Inhalants**")
                    st.markdown("- **PCP**")
                    st.markdown("- **Hallucinogens**")
                    st.markdown("- **Other/Unknown**")
                if drug_selection_caud == "All":
                    st.markdown(f"#### {drug_selection_caud}")
                    st.markdown("---")
                if drug_selection_caud == "Sed/Hyp/Anx":
                    st.markdown(f"#### {drug_selection_caud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Sed/Hyp/Anx # Just Checking Calculation errors
                    csud_sed_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e51a', 'scid_e51b', 'scid_e59a', 'scid_e59b', 'scid_e67', 'scid_e75', 'scid_e83a', 'scid_e83b', 'scid_e91', 'scid_e99',
                    'scid_e107', 'scid_e115a', 'scid_e115b', 'scid_e123a', 'scid_e123b', 'scid_e131', 'scid_e136', 'scid_e136cnt']]

                    # Setting index to subject_id
                    csud_sed_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_sed_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_sed_full_db['scid_e75'] = csud_sed_full_db['scid_e75'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_sed_full_db = csud_sed_full_db.astype({'scid_e51a':'int', 'scid_e51b':'int', 'scid_e59a':'int', 'scid_e59b':'int', 'scid_e67':'int', 'scid_e75':'int', 'scid_e83a':'int', 'scid_e83b':'int',
                    'scid_e91':'int', 'scid_e99':'int', 'scid_e107':'int', 'scid_e115a':'int', 'scid_e115b':'int', 'scid_e123a':'int', 'scid_e123b':'int', 'scid_e131':'int', 'scid_e136':'int', 
                    'scid_e136cnt':'int'})

                    # Counting CSUD SED symptoms # Max is 11
                    csud_sed_full_db['A1 Items'] = np.where(((csud_sed_full_db['scid_e51a'] == 3) | (csud_sed_full_db['scid_e51b'] == 3)), 1, 0)
                    csud_sed_full_db['A2 Items'] = np.where(((csud_sed_full_db['scid_e59a'] == 3) | (csud_sed_full_db['scid_e59b'] == 3)), 1, 0)
                    csud_sed_full_db['A3 Items'] = np.where(((csud_sed_full_db['scid_e67'] == 3)), 1, 0)
                    csud_sed_full_db['A4 Items'] = np.where(((csud_sed_full_db['scid_e75'] == 3)), 1, 0)
                    csud_sed_full_db['A5 Items'] = np.where(((csud_sed_full_db['scid_e83a'] == 3) | (csud_sed_full_db['scid_e83b'] == 3)), 1, 0)
                    csud_sed_full_db['A6 Items'] = np.where(((csud_sed_full_db['scid_e91'] == 3)), 1, 0)
                    csud_sed_full_db['A7 Items'] = np.where(((csud_sed_full_db['scid_e99'] == 3)), 1, 0)
                    csud_sed_full_db['A8 Items'] = np.where(((csud_sed_full_db['scid_e107'] == 3)), 1, 0)
                    csud_sed_full_db['A9 Items'] = np.where(((csud_sed_full_db['scid_e115a'] == 3) | (csud_sed_full_db['scid_e115b'] == 3)), 1, 0)
                    csud_sed_full_db['A10 Items'] = np.where(((csud_sed_full_db['scid_e123a'] == 3) | (csud_sed_full_db['scid_e123b'] == 3)), 1, 0)
                    csud_sed_full_db['A11 Items'] = np.where(((csud_sed_full_db['scid_e131'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_sed_full_db['CSUD SED Criterion A Discrepancy'] = np.where(((csud_sed_full_db['scid_e136cnt'] >= 2) & (csud_sed_full_db['scid_e136'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_sed_full_db['New CSUD SED Symptom Count'] = csud_sed_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    csud_sed_full_db['CSUD SED Symptom Count Discrepancy'] = np.where(((csud_sed_full_db['New CSUD SED Symptom Count'] != csud_sed_full_db['scid_e136cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_sed_db = csud_sed_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e136', 'scid_e136cnt', 'CSUD SED Criterion A Discrepancy', 'New CSUD SED Symptom Count', 'CSUD SED Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_sed_db['Count Discrepancy Direction'] = np.where(((csud_sed_full_db['scid_e136cnt'] - csud_sed_full_db['New CSUD SED Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_sed_full_db['scid_e136cnt'] == csud_sed_full_db['New CSUD SED Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_sed_db['Count Discrepancy Value'] = csud_sed_full_db['scid_e136cnt'] - csud_sed_full_db['New CSUD SED Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_sed = refined_csud_sed_db.loc[((refined_csud_sed_db['CSUD SED Symptom Count Discrepancy'] == "Problem") | (refined_csud_sed_db['CSUD SED Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e136cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD SED Criterion A Discrepancy** - The Criterion A item (scid_e136) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD SED Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD SED Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_sed = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_sed')
                    if interviewer_selection_csud_sed:
                        problem_children_csud_sed_final = only_problem_children_csud_sed[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e136', 'CSUD SED Criterion A Discrepancy', 'scid_e136cnt', 'New CSUD SED Symptom Count', 'CSUD SED Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_sed_final)
                        csv = convert_df(problem_children_csud_sed_final)
                    else:
                        problem_children_csud_sed_final = only_problem_children_csud_sed[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e136', 'CSUD SED Criterion A Discrepancy', 'scid_e136cnt', 'New CSUD SED Symptom Count', 'CSUD SED Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_sed_final)
                        csv = convert_df(problem_children_csud_sed_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_sed_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_sed_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_sed_final[problem_children_csud_sed_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_sed_final[problem_children_csud_sed_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_sed_problem_subject_list = problem_children_csud_sed_final.index.values.tolist()
                    see_more_csud_sed = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_sed_problem_subject_list)
                    interviewer_selection_csud_sed_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_sed')
                    if see_more_csud_sed is not None:
                        if interviewer_selection_csud_sed_2:
                            specific_csud_sed_subject_db = csud_sed_full_db.loc[see_more_csud_sed,:]
                            specific_csud_sed_subject_db_2 = specific_csud_sed_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e51a', 'scid_e51b', 'A2 Items', 'scid_e59a', 'scid_e59b',
                            'A3 Items', 'scid_e67', 'A4 Items', 'scid_e75', 'A5 Items', 'scid_e83a', 'scid_e83b', 'A6 Items', 'scid_e91', 'A7 Items', 'scid_e99', 'A8 Items', 'scid_e107', 
                            'A9 Items', 'scid_e115a', 'scid_e115b', 'A10 Items', 'scid_e123a', 'scid_e123b', 'A11 Items', 'scid_e131', 'scid_e136', 'scid_e136cnt', 'New CSUD SED Symptom Count']]
                            specific_csud_sed_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_sed_subject_db_2)
                            csv = convert_df(specific_csud_sed_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_sed_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_sed_subject_db = csud_sed_full_db.loc[see_more_csud_sed,:]
                            specific_csud_sed_subject_db_2 = specific_csud_sed_subject_db.loc[:,['A1 Items', 'scid_e51a', 'scid_e51b', 'A2 Items', 'scid_e59a', 'scid_e59b',
                            'A3 Items', 'scid_e67', 'A4 Items', 'scid_e75', 'A5 Items', 'scid_e83a', 'scid_e83b', 'A6 Items', 'scid_e91', 'A7 Items', 'scid_e99', 'A8 Items', 'scid_e107', 
                            'A9 Items', 'scid_e115a', 'scid_e115b', 'A10 Items', 'scid_e123a', 'scid_e123b', 'A11 Items', 'scid_e131', 'scid_e136', 'scid_e136cnt', 'New CSUD SED Symptom Count']]
                            specific_csud_sed_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_sed_subject_db_2)
                            csv = convert_df(specific_csud_sed_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_sed_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_caud == "Cannabis":
                    st.markdown(f"#### {drug_selection_caud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Sed/Hyp/Anx # Just Checking Calculation errors
                    csud_can_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e52a', 'scid_e52b', 'scid_e60a', 'scid_e60b', 'scid_e68', 'scid_e76', 'scid_e84a', 'scid_e84b', 'scid_e92', 'scid_e100',
                    'scid_e108', 'scid_e116a', 'scid_e116b', 'scid_e124a', 'scid_e124b', 'scid_e132', 'scid_e138', 'scid_e138cnt']]

                    # Setting index to subject_id
                    csud_can_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_can_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_can_full_db['scid_e76'] = csud_can_full_db['scid_e76'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_can_full_db = csud_can_full_db.astype({'scid_e52a':'int', 'scid_e52b':'int', 'scid_e60a':'int', 'scid_e60b':'int', 'scid_e68':'int', 'scid_e76':'int', 'scid_e84a':'int', 'scid_e84b':'int',
                    'scid_e92':'int', 'scid_e100':'int', 'scid_e108':'int', 'scid_e116a':'int', 'scid_e116b':'int', 'scid_e124a':'int', 'scid_e124b':'int', 'scid_e132':'int', 'scid_e138':'int', 
                    'scid_e138cnt':'int'})

                    # Counting CSUD CAN symptoms # Max is 11
                    csud_can_full_db['A1 Items'] = np.where(((csud_can_full_db['scid_e52a'] == 3) | (csud_can_full_db['scid_e52b'] == 3)), 1, 0)
                    csud_can_full_db['A2 Items'] = np.where(((csud_can_full_db['scid_e60a'] == 3) | (csud_can_full_db['scid_e60b'] == 3)), 1, 0)
                    csud_can_full_db['A3 Items'] = np.where(((csud_can_full_db['scid_e68'] == 3)), 1, 0)
                    csud_can_full_db['A4 Items'] = np.where(((csud_can_full_db['scid_e76'] == 3)), 1, 0)
                    csud_can_full_db['A5 Items'] = np.where(((csud_can_full_db['scid_e84a'] == 3) | (csud_can_full_db['scid_e84b'] == 3)), 1, 0)
                    csud_can_full_db['A6 Items'] = np.where(((csud_can_full_db['scid_e92'] == 3)), 1, 0)
                    csud_can_full_db['A7 Items'] = np.where(((csud_can_full_db['scid_e100'] == 3)), 1, 0)
                    csud_can_full_db['A8 Items'] = np.where(((csud_can_full_db['scid_e108'] == 3)), 1, 0)
                    csud_can_full_db['A9 Items'] = np.where(((csud_can_full_db['scid_e116a'] == 3) | (csud_can_full_db['scid_e116b'] == 3)), 1, 0)
                    csud_can_full_db['A10 Items'] = np.where(((csud_can_full_db['scid_e124a'] == 3) | (csud_can_full_db['scid_e124b'] == 3)), 1, 0)
                    csud_can_full_db['A11 Items'] = np.where(((csud_can_full_db['scid_e132'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_can_full_db['CSUD CAN Criterion A Discrepancy'] = np.where(((csud_can_full_db['scid_e138cnt'] >= 2) & (csud_can_full_db['scid_e138'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_can_full_db['New CSUD CAN Symptom Count'] = csud_can_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    csud_can_full_db['CSUD CAN Symptom Count Discrepancy'] = np.where(((csud_can_full_db['New CSUD CAN Symptom Count'] != csud_can_full_db['scid_e138cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_can_db = csud_can_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e138', 'scid_e138cnt', 'CSUD CAN Criterion A Discrepancy', 'New CSUD CAN Symptom Count', 'CSUD CAN Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_can_db['Count Discrepancy Direction'] = np.where(((csud_can_full_db['scid_e138cnt'] - csud_can_full_db['New CSUD CAN Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_can_full_db['scid_e138cnt'] == csud_can_full_db['New CSUD CAN Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_can_db['Count Discrepancy Value'] = csud_can_full_db['scid_e138cnt'] - csud_can_full_db['New CSUD CAN Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_can = refined_csud_can_db.loc[((refined_csud_can_db['CSUD CAN Symptom Count Discrepancy'] == "Problem") | (refined_csud_can_db['CSUD CAN Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e138cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD CAN Criterion A Discrepancy** - The Criterion A item (scid_e138) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD CAN Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD CAN Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_can = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_can')
                    if interviewer_selection_csud_can:
                        problem_children_csud_can_final = only_problem_children_csud_can[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e138', 'CSUD CAN Criterion A Discrepancy', 'scid_e138cnt', 'New CSUD CAN Symptom Count', 'CSUD CAN Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_can_final)
                        csv = convert_df(problem_children_csud_can_final)
                    else:
                        problem_children_csud_can_final = only_problem_children_csud_can[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e138', 'CSUD CAN Criterion A Discrepancy', 'scid_e138cnt', 'New CSUD CAN Symptom Count', 'CSUD CAN Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_can_final)
                        csv = convert_df(problem_children_csud_can_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_can_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_can_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_can_final[problem_children_csud_can_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_can_final[problem_children_csud_can_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_can_problem_subject_list = problem_children_csud_can_final.index.values.tolist()
                    see_more_csud_can = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_can_problem_subject_list)
                    interviewer_selection_csud_can_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_can')
                    if see_more_csud_can is not None:
                        if interviewer_selection_csud_can_2:
                            specific_csud_can_subject_db = csud_can_full_db.loc[see_more_csud_can,:]
                            specific_csud_can_subject_db_2 = specific_csud_can_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e52a', 'scid_e52b', 'A2 Items', 'scid_e60a', 'scid_e60b',
                            'A3 Items', 'scid_e68', 'A4 Items', 'scid_e76', 'A5 Items', 'scid_e84a', 'scid_e84b', 'A6 Items', 'scid_e92', 'A7 Items', 'scid_e100', 'A8 Items', 'scid_e108', 
                            'A9 Items', 'scid_e116a', 'scid_e116b', 'A10 Items', 'scid_e124a', 'scid_e124b', 'A11 Items', 'scid_e132', 'scid_e138', 'scid_e138cnt', 'New CSUD CAN Symptom Count']]
                            specific_csud_can_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_can_subject_db_2)
                            csv = convert_df(specific_csud_can_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_can_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_can_subject_db = csud_can_full_db.loc[see_more_csud_can,:]
                            specific_csud_can_subject_db_2 = specific_csud_can_subject_db.loc[:,['A1 Items', 'scid_e52a', 'scid_e52b', 'A2 Items', 'scid_e60a', 'scid_e60b',
                            'A3 Items', 'scid_e68', 'A4 Items', 'scid_e76', 'A5 Items', 'scid_e84a', 'scid_e84b', 'A6 Items', 'scid_e92', 'A7 Items', 'scid_e100', 'A8 Items', 'scid_e108', 
                            'A9 Items', 'scid_e116a', 'scid_e116b', 'A10 Items', 'scid_e124a', 'scid_e124b', 'A11 Items', 'scid_e132', 'scid_e138', 'scid_e138cnt', 'New CSUD CAN Symptom Count']]
                            specific_csud_can_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_can_subject_db_2)
                            csv = convert_df(specific_csud_can_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_can_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_caud == "Stimulants":
                    st.markdown(f"#### {drug_selection_caud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Sed/Hyp/Anx # Just Checking Calculation errors
                    csud_stim_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e53a', 'scid_e53b', 'scid_e61a', 'scid_e61b', 'scid_e69', 'scid_e77', 'scid_e85a', 'scid_e85b', 'scid_e93', 'scid_e101',
                    'scid_e109', 'scid_e117a', 'scid_e117b', 'scid_e125a', 'scid_e125b', 'scid_e133', 'scid_e140', 'scid_e140cnt']]

                    # Setting index to subject_id
                    csud_stim_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_stim_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_stim_full_db['scid_e77'] = csud_stim_full_db['scid_e77'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_stim_full_db = csud_stim_full_db.astype({'scid_e53a':'int', 'scid_e53b':'int', 'scid_e61a':'int', 'scid_e61b':'int', 'scid_e69':'int', 'scid_e77':'int', 'scid_e85a':'int', 'scid_e85b':'int',
                    'scid_e93':'int', 'scid_e101':'int', 'scid_e109':'int', 'scid_e117a':'int', 'scid_e117b':'int', 'scid_e125a':'int', 'scid_e125b':'int', 'scid_e133':'int', 'scid_e140':'int', 
                    'scid_e140cnt':'int'})

                    # Counting CSUD STIM symptoms # Max is 11
                    csud_stim_full_db['A1 Items'] = np.where(((csud_stim_full_db['scid_e53a'] == 3) | (csud_stim_full_db['scid_e53b'] == 3)), 1, 0)
                    csud_stim_full_db['A2 Items'] = np.where(((csud_stim_full_db['scid_e61a'] == 3) | (csud_stim_full_db['scid_e61b'] == 3)), 1, 0)
                    csud_stim_full_db['A3 Items'] = np.where(((csud_stim_full_db['scid_e69'] == 3)), 1, 0)
                    csud_stim_full_db['A4 Items'] = np.where(((csud_stim_full_db['scid_e77'] == 3)), 1, 0)
                    csud_stim_full_db['A5 Items'] = np.where(((csud_stim_full_db['scid_e85a'] == 3) | (csud_stim_full_db['scid_e85b'] == 3)), 1, 0)
                    csud_stim_full_db['A6 Items'] = np.where(((csud_stim_full_db['scid_e93'] == 3)), 1, 0)
                    csud_stim_full_db['A7 Items'] = np.where(((csud_stim_full_db['scid_e101'] == 3)), 1, 0)
                    csud_stim_full_db['A8 Items'] = np.where(((csud_stim_full_db['scid_e109'] == 3)), 1, 0)
                    csud_stim_full_db['A9 Items'] = np.where(((csud_stim_full_db['scid_e117a'] == 3) | (csud_stim_full_db['scid_e117b'] == 3)), 1, 0)
                    csud_stim_full_db['A10 Items'] = np.where(((csud_stim_full_db['scid_e125a'] == 3) | (csud_stim_full_db['scid_e125b'] == 3)), 1, 0)
                    csud_stim_full_db['A11 Items'] = np.where(((csud_stim_full_db['scid_e133'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_stim_full_db['CSUD STIM Criterion A Discrepancy'] = np.where(((csud_stim_full_db['scid_e140cnt'] >= 2) & (csud_stim_full_db['scid_e140'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_stim_full_db['New CSUD STIM Symptom Count'] = csud_stim_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    csud_stim_full_db['CSUD STIM Symptom Count Discrepancy'] = np.where(((csud_stim_full_db['New CSUD STIM Symptom Count'] != csud_stim_full_db['scid_e140cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_stim_db = csud_stim_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e140', 'scid_e140cnt', 'CSUD STIM Criterion A Discrepancy', 'New CSUD STIM Symptom Count', 'CSUD STIM Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_stim_db['Count Discrepancy Direction'] = np.where(((csud_stim_full_db['scid_e140cnt'] - csud_stim_full_db['New CSUD STIM Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_stim_full_db['scid_e140cnt'] == csud_stim_full_db['New CSUD STIM Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_stim_db['Count Discrepancy Value'] = csud_stim_full_db['scid_e140cnt'] - csud_stim_full_db['New CSUD STIM Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_stim = refined_csud_stim_db.loc[((refined_csud_stim_db['CSUD STIM Symptom Count Discrepancy'] == "Problem") | (refined_csud_stim_db['CSUD STIM Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e140cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD STIM Criterion A Discrepancy** - The Criterion A item (scid_e140) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD STIM Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD STIM Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_stim = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_stim')
                    if interviewer_selection_csud_stim:
                        problem_children_csud_stim_final = only_problem_children_csud_stim[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e140', 'CSUD STIM Criterion A Discrepancy', 'scid_e140cnt', 'New CSUD STIM Symptom Count', 'CSUD STIM Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_stim_final)
                        csv = convert_df(problem_children_csud_stim_final)
                    else:
                        problem_children_csud_stim_final = only_problem_children_csud_stim[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e140', 'CSUD STIM Criterion A Discrepancy', 'scid_e140cnt', 'New CSUD STIM Symptom Count', 'CSUD STIM Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_stim_final)
                        csv = convert_df(problem_children_csud_stim_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_stim_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_stim_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_stim_final[problem_children_csud_stim_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_stim_final[problem_children_csud_stim_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_stim_problem_subject_list = problem_children_csud_stim_final.index.values.tolist()
                    see_more_csud_stim = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_stim_problem_subject_list)
                    interviewer_selection_csud_stim_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_stim')
                    if see_more_csud_stim is not None:
                        if interviewer_selection_csud_stim_2:
                            specific_csud_stim_subject_db = csud_stim_full_db.loc[see_more_csud_stim,:]
                            specific_csud_stim_subject_db_2 = specific_csud_stim_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e53a', 'scid_e53b', 'A2 Items', 'scid_e61a', 'scid_e61b',
                            'A3 Items', 'scid_e69', 'A4 Items', 'scid_e77', 'A5 Items', 'scid_e85a', 'scid_e85b', 'A6 Items', 'scid_e93', 'A7 Items', 'scid_e101', 'A8 Items', 'scid_e109', 
                            'A9 Items', 'scid_e117a', 'scid_e117b', 'A10 Items', 'scid_e125a', 'scid_e125b', 'A11 Items', 'scid_e133', 'scid_e140', 'scid_e140cnt', 'New CSUD STIM Symptom Count']]
                            specific_csud_stim_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_stim_subject_db_2)
                            csv = convert_df(specific_csud_stim_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_stim_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_stim_subject_db = csud_stim_full_db.loc[see_more_csud_stim,:]
                            specific_csud_stim_subject_db_2 = specific_csud_stim_subject_db.loc[:,['A1 Items', 'scid_e53a', 'scid_e53b', 'A2 Items', 'scid_e61a', 'scid_e61b',
                            'A3 Items', 'scid_e69', 'A4 Items', 'scid_e77', 'A5 Items', 'scid_e85a', 'scid_e85b', 'A6 Items', 'scid_e93', 'A7 Items', 'scid_e101', 'A8 Items', 'scid_e109', 
                            'A9 Items', 'scid_e117a', 'scid_e117b', 'A10 Items', 'scid_e125a', 'scid_e125b', 'A11 Items', 'scid_e133', 'scid_e140', 'scid_e140cnt', 'New CSUD STIM Symptom Count']]
                            specific_csud_stim_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_stim_subject_db_2)
                            csv = convert_df(specific_csud_stim_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_stim_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
        if module_selection == "Module F":
            st.write("hello")
        if module_selection == 'Module K':
            st.write("Hello")
        if module_selection == "Module C":
            st.write("Hello")