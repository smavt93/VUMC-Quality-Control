import pandas as pd
import numpy as np
import streamlit as st
from datetime import date

# Files used later (set up)
module_a_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20A%20Items.xlsx?raw=true'
module_e_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20E%20Items.xlsx?raw=true'
module_f_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20F%20Items.xlsx?raw=true'
module_k_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20K%20Items.xlsx?raw=true'
module_c_file = 'https://github.com/smavt93/VUMC-Quality-Control/blob/main/Module%20C%20Items.xlsx?raw=true'

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
                    problem_children_pdd_final = only_problem_children_pdd.loc[:, ['scid_interviewername', 'B1 Items', 'B2 Items', 'B3 Items', 'B4 Items','scid_a178', 'PDD Criterion B Discrepancy', 'scid_a178cnt', 
                    'New PDD Symptom Count (B)', 'Count Discrepancy Direction (B)', 'Count Discrepancy Value (B)', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items',
                    'C6 Items', 'C7 Items', 'scid_a186', 'PDD Criterion C Discrepancy', 'scid_a187', 'PDD Criterion B+C Discrepancy', 'scid_a187cnt', 'New PDD Symptom Count (B+C)', 'Count Discrepancy Direction (B+C)',
                    'Count Discrepancy Value (B+C)']]
                    st.write(problem_children_pdd_final)
                    csv = convert_df(problem_children_pdd_final)
                else:
                    problem_children_pdd_final = only_problem_children_pdd.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items','scid_a178', 'PDD Criterion B Discrepancy', 'scid_a178cnt', 
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
                drug_selection_csud = st.selectbox("Which Drug would you like to look at?", ["---", "All", "Sed/Hyp/Anx", "Cannabis", "Stimulants", "Opioids", "Inhalants", "PCP", "Hallucinogens", "Other/Unknown"])
                if drug_selection_csud == "---":
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
                if drug_selection_csud == "All":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")
                if drug_selection_csud == "Sed/Hyp/Anx":
                    st.markdown(f"#### {drug_selection_csud}")
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
                if drug_selection_csud == "Cannabis":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Cannabis # Just Checking Calculation errors
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
                if drug_selection_csud == "Stimulants":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Stimulants # Just Checking Calculation errors
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
                if drug_selection_csud == "Opioids":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Opioids # Just Checking Calculation errors
                    csud_opi_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e54a', 'scid_e54b', 'scid_e62a', 'scid_e62b', 'scid_e70', 'scid_e78', 'scid_e86a', 'scid_e86b', 'scid_e94', 'scid_e102',
                    'scid_e110', 'scid_e118a', 'scid_e118b', 'scid_e126a', 'scid_e126b', 'scid_e134', 'scid_e142', 'scid_e142cnt']]

                    # Setting index to subject_id
                    csud_opi_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_opi_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_opi_full_db['scid_e78'] = csud_opi_full_db['scid_e78'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_opi_full_db = csud_opi_full_db.astype({'scid_e54a':'int', 'scid_e54b':'int', 'scid_e62a':'int', 'scid_e62b':'int', 'scid_e70':'int', 'scid_e78':'int', 'scid_e86a':'int', 'scid_e86b':'int',
                    'scid_e94':'int', 'scid_e102':'int', 'scid_e110':'int', 'scid_e118a':'int', 'scid_e118b':'int', 'scid_e126a':'int', 'scid_e126b':'int', 'scid_e134':'int', 'scid_e142':'int', 
                    'scid_e142cnt':'int'})

                    # Counting CSUD OPI symptoms # Max is 11
                    csud_opi_full_db['A1 Items'] = np.where(((csud_opi_full_db['scid_e54a'] == 3) | (csud_opi_full_db['scid_e54b'] == 3)), 1, 0)
                    csud_opi_full_db['A2 Items'] = np.where(((csud_opi_full_db['scid_e62a'] == 3) | (csud_opi_full_db['scid_e62b'] == 3)), 1, 0)
                    csud_opi_full_db['A3 Items'] = np.where(((csud_opi_full_db['scid_e70'] == 3)), 1, 0)
                    csud_opi_full_db['A4 Items'] = np.where(((csud_opi_full_db['scid_e78'] == 3)), 1, 0)
                    csud_opi_full_db['A5 Items'] = np.where(((csud_opi_full_db['scid_e86a'] == 3) | (csud_opi_full_db['scid_e86b'] == 3)), 1, 0)
                    csud_opi_full_db['A6 Items'] = np.where(((csud_opi_full_db['scid_e94'] == 3)), 1, 0)
                    csud_opi_full_db['A7 Items'] = np.where(((csud_opi_full_db['scid_e102'] == 3)), 1, 0)
                    csud_opi_full_db['A8 Items'] = np.where(((csud_opi_full_db['scid_e110'] == 3)), 1, 0)
                    csud_opi_full_db['A9 Items'] = np.where(((csud_opi_full_db['scid_e118a'] == 3) | (csud_opi_full_db['scid_e118b'] == 3)), 1, 0)
                    csud_opi_full_db['A10 Items'] = np.where(((csud_opi_full_db['scid_e126a'] == 3) | (csud_opi_full_db['scid_e126b'] == 3)), 1, 0)
                    csud_opi_full_db['A11 Items'] = np.where(((csud_opi_full_db['scid_e134'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_opi_full_db['CSUD OPI Criterion A Discrepancy'] = np.where(((csud_opi_full_db['scid_e142cnt'] >= 2) & (csud_opi_full_db['scid_e142'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_opi_full_db['New CSUD OPI Symptom Count'] = csud_opi_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    csud_opi_full_db['CSUD OPI Symptom Count Discrepancy'] = np.where(((csud_opi_full_db['New CSUD OPI Symptom Count'] != csud_opi_full_db['scid_e142cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_opi_db = csud_opi_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e142', 'scid_e142cnt', 'CSUD OPI Criterion A Discrepancy', 'New CSUD OPI Symptom Count', 'CSUD OPI Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_opi_db['Count Discrepancy Direction'] = np.where(((csud_opi_full_db['scid_e142cnt'] - csud_opi_full_db['New CSUD OPI Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_opi_full_db['scid_e142cnt'] == csud_opi_full_db['New CSUD OPI Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_opi_db['Count Discrepancy Value'] = csud_opi_full_db['scid_e142cnt'] - csud_opi_full_db['New CSUD OPI Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_opi = refined_csud_opi_db.loc[((refined_csud_opi_db['CSUD OPI Symptom Count Discrepancy'] == "Problem") | (refined_csud_opi_db['CSUD OPI Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e142cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD OPI Criterion A Discrepancy** - The Criterion A item (scid_e142) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD OPI Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD OPI Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_opi = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_opi')
                    if interviewer_selection_csud_opi:
                        problem_children_csud_opi_final = only_problem_children_csud_opi[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e142', 'CSUD OPI Criterion A Discrepancy', 'scid_e142cnt', 'New CSUD OPI Symptom Count', 'CSUD OPI Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_opi_final)
                        csv = convert_df(problem_children_csud_opi_final)
                    else:
                        problem_children_csud_opi_final = only_problem_children_csud_opi[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e142', 'CSUD OPI Criterion A Discrepancy', 'scid_e142cnt', 'New CSUD OPI Symptom Count', 'CSUD OPI Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_opi_final)
                        csv = convert_df(problem_children_csud_opi_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_opi_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_opi_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_opi_final[problem_children_csud_opi_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_opi_final[problem_children_csud_opi_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_opi_problem_subject_list = problem_children_csud_opi_final.index.values.tolist()
                    see_more_csud_opi = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_opi_problem_subject_list)
                    interviewer_selection_csud_opi_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_opi')
                    if see_more_csud_opi is not None:
                        if interviewer_selection_csud_opi_2:
                            specific_csud_opi_subject_db = csud_opi_full_db.loc[see_more_csud_opi,:]
                            specific_csud_opi_subject_db_2 = specific_csud_opi_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e54a', 'scid_e54b', 'A2 Items', 'scid_e62a', 'scid_e62b',
                            'A3 Items', 'scid_e70', 'A4 Items', 'scid_e78', 'A5 Items', 'scid_e86a', 'scid_e86b', 'A6 Items', 'scid_e94', 'A7 Items', 'scid_e102', 'A8 Items', 'scid_e110', 
                            'A9 Items', 'scid_e118a', 'scid_e118b', 'A10 Items', 'scid_e126a', 'scid_e126b', 'A11 Items', 'scid_e134', 'scid_e142', 'scid_e142cnt', 'New CSUD OPI Symptom Count']]
                            specific_csud_opi_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_opi_subject_db_2)
                            csv = convert_df(specific_csud_opi_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_opi_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_opi_subject_db = csud_opi_full_db.loc[see_more_csud_opi,:]
                            specific_csud_opi_subject_db_2 = specific_csud_opi_subject_db.loc[:,['A1 Items', 'scid_e54a', 'scid_e54b', 'A2 Items', 'scid_e62a', 'scid_e62b',
                            'A3 Items', 'scid_e70', 'A4 Items', 'scid_e78', 'A5 Items', 'scid_e86a', 'scid_e86b', 'A6 Items', 'scid_e94', 'A7 Items', 'scid_e102', 'A8 Items', 'scid_e110', 
                            'A9 Items', 'scid_e118a', 'scid_e118b', 'A10 Items', 'scid_e126a', 'scid_e126b', 'A11 Items', 'scid_e134', 'scid_e142', 'scid_e142cnt', 'New CSUD OPI Symptom Count']]
                            specific_csud_opi_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_opi_subject_db_2)
                            csv = convert_df(specific_csud_opi_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_opi_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_csud == "Inhalants":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Inhalants # Just Checking Calculation errors
                    csud_inh_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e55a', 'scid_e55b', 'scid_e63a', 'scid_e63b', 'scid_e71', 'scid_e79', 'scid_e87a', 'scid_e87b', 'scid_e95', 'scid_e103',
                    'scid_e111', 'scid_e119a', 'scid_e119b', 'scid_e127a', 'scid_e127b', 'scid_e144', 'scid_e144cnt']]

                    # Setting index to subject_id
                    csud_inh_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_inh_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_inh_full_db['scid_e79'] = csud_inh_full_db['scid_e79'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_inh_full_db = csud_inh_full_db.astype({'scid_e55a':'int', 'scid_e55b':'int', 'scid_e63a':'int', 'scid_e63b':'int', 'scid_e71':'int', 'scid_e79':'int', 'scid_e87a':'int', 'scid_e87b':'int',
                    'scid_e95':'int', 'scid_e103':'int', 'scid_e111':'int', 'scid_e119a':'int', 'scid_e119b':'int', 'scid_e127a':'int', 'scid_e127b':'int', 'scid_e144':'int', 'scid_e144cnt':'int'})

                    # Counting CSUD INH symptoms # Max is 11
                    csud_inh_full_db['A1 Items'] = np.where(((csud_inh_full_db['scid_e55a'] == 3) | (csud_inh_full_db['scid_e55b'] == 3)), 1, 0)
                    csud_inh_full_db['A2 Items'] = np.where(((csud_inh_full_db['scid_e63a'] == 3) | (csud_inh_full_db['scid_e63b'] == 3)), 1, 0)
                    csud_inh_full_db['A3 Items'] = np.where(((csud_inh_full_db['scid_e71'] == 3)), 1, 0)
                    csud_inh_full_db['A4 Items'] = np.where(((csud_inh_full_db['scid_e79'] == 3)), 1, 0)
                    csud_inh_full_db['A5 Items'] = np.where(((csud_inh_full_db['scid_e87a'] == 3) | (csud_inh_full_db['scid_e87b'] == 3)), 1, 0)
                    csud_inh_full_db['A6 Items'] = np.where(((csud_inh_full_db['scid_e95'] == 3)), 1, 0)
                    csud_inh_full_db['A7 Items'] = np.where(((csud_inh_full_db['scid_e103'] == 3)), 1, 0)
                    csud_inh_full_db['A8 Items'] = np.where(((csud_inh_full_db['scid_e111'] == 3)), 1, 0)
                    csud_inh_full_db['A9 Items'] = np.where(((csud_inh_full_db['scid_e119a'] == 3) | (csud_inh_full_db['scid_e119b'] == 3)), 1, 0)
                    csud_inh_full_db['A10 Items'] = np.where(((csud_inh_full_db['scid_e127a'] == 3) | (csud_inh_full_db['scid_e127b'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_inh_full_db['CSUD INH Criterion A Discrepancy'] = np.where(((csud_inh_full_db['scid_e144cnt'] >= 2) & (csud_inh_full_db['scid_e144'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_inh_full_db['New CSUD INH Symptom Count'] = csud_inh_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items']].sum(axis = 1)
                    csud_inh_full_db['CSUD INH Symptom Count Discrepancy'] = np.where(((csud_inh_full_db['New CSUD INH Symptom Count'] != csud_inh_full_db['scid_e144cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_inh_db = csud_inh_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'scid_e144', 'scid_e144cnt', 'CSUD INH Criterion A Discrepancy', 'New CSUD INH Symptom Count', 'CSUD INH Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_inh_db['Count Discrepancy Direction'] = np.where(((csud_inh_full_db['scid_e144cnt'] - csud_inh_full_db['New CSUD INH Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_inh_full_db['scid_e144cnt'] == csud_inh_full_db['New CSUD INH Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_inh_db['Count Discrepancy Value'] = csud_inh_full_db['scid_e144cnt'] - csud_inh_full_db['New CSUD INH Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_inh = refined_csud_inh_db.loc[((refined_csud_inh_db['CSUD INH Symptom Count Discrepancy'] == "Problem") | (refined_csud_inh_db['CSUD INH Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e144cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD INH Criterion A Discrepancy** - The Criterion A item (scid_e144) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD INH Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD INH Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_inh = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_inh')
                    if interviewer_selection_csud_inh:
                        problem_children_csud_inh_final = only_problem_children_csud_inh[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e144', 'CSUD INH Criterion A Discrepancy', 'scid_e144cnt', 'New CSUD INH Symptom Count', 'CSUD INH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_inh_final)
                        csv = convert_df(problem_children_csud_inh_final)
                    else:
                        problem_children_csud_inh_final = only_problem_children_csud_inh[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e144', 'CSUD INH Criterion A Discrepancy', 'scid_e144cnt', 'New CSUD INH Symptom Count', 'CSUD INH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_inh_final)
                        csv = convert_df(problem_children_csud_inh_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_inh_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_inh_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_inh_final[problem_children_csud_inh_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_inh_final[problem_children_csud_inh_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_inh_problem_subject_list = problem_children_csud_inh_final.index.values.tolist()
                    see_more_csud_inh = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_inh_problem_subject_list)
                    interviewer_selection_csud_inh_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_inh')
                    if see_more_csud_inh is not None:
                        if interviewer_selection_csud_inh_2:
                            specific_csud_inh_subject_db = csud_inh_full_db.loc[see_more_csud_inh,:]
                            specific_csud_inh_subject_db_2 = specific_csud_inh_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e55a', 'scid_e55b', 'A2 Items', 'scid_e63a', 'scid_e63b',
                            'A3 Items', 'scid_e71', 'A4 Items', 'scid_e79', 'A5 Items', 'scid_e87a', 'scid_e87b', 'A6 Items', 'scid_e95', 'A7 Items', 'scid_e103', 'A8 Items', 'scid_e111', 
                            'A9 Items', 'scid_e119a', 'scid_e119b', 'A10 Items', 'scid_e127a', 'scid_e127b', 'scid_e144', 'scid_e144cnt', 'New CSUD INH Symptom Count']]
                            specific_csud_inh_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_inh_subject_db_2)
                            csv = convert_df(specific_csud_inh_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_inh_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_inh_subject_db = csud_inh_full_db.loc[see_more_csud_inh,:]
                            specific_csud_inh_subject_db_2 = specific_csud_inh_subject_db.loc[:,['A1 Items', 'scid_e55a', 'scid_e55b', 'A2 Items', 'scid_e63a', 'scid_e63b',
                            'A3 Items', 'scid_e71', 'A4 Items', 'scid_e79', 'A5 Items', 'scid_e87a', 'scid_e87b', 'A6 Items', 'scid_e95', 'A7 Items', 'scid_e103', 'A8 Items', 'scid_e111', 
                            'A9 Items', 'scid_e119a', 'scid_e119b', 'A10 Items', 'scid_e127a', 'scid_e127b', 'scid_e144', 'scid_e144cnt', 'New CSUD INH Symptom Count']]
                            specific_csud_inh_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_inh_subject_db_2)
                            csv = convert_df(specific_csud_inh_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_inh_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_csud == "PCP":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD PCP # Just Checking Calculation errors
                    csud_pcp_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e56a', 'scid_e56b', 'scid_e64a', 'scid_e64b', 'scid_e72', 'scid_e80', 'scid_e88a', 'scid_e88b', 'scid_e96', 'scid_e104',
                    'scid_e112', 'scid_e120a', 'scid_e120b', 'scid_e128a', 'scid_e128b', 'scid_e146', 'scid_e146cnt']]

                    # Setting index to subject_id
                    csud_pcp_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_pcp_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_pcp_full_db['scid_e80'] = csud_pcp_full_db['scid_e80'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_pcp_full_db = csud_pcp_full_db.astype({'scid_e56a':'int', 'scid_e56b':'int', 'scid_e64a':'int', 'scid_e64b':'int', 'scid_e72':'int', 'scid_e80':'int', 'scid_e88a':'int', 'scid_e88b':'int',
                    'scid_e96':'int', 'scid_e104':'int', 'scid_e112':'int', 'scid_e120a':'int', 'scid_e120b':'int', 'scid_e128a':'int', 'scid_e128b':'int', 'scid_e146':'int', 'scid_e146cnt':'int'})

                    # Counting CSUD PCP symptoms # Max is 11
                    csud_pcp_full_db['A1 Items'] = np.where(((csud_pcp_full_db['scid_e56a'] == 3) | (csud_pcp_full_db['scid_e56b'] == 3)), 1, 0)
                    csud_pcp_full_db['A2 Items'] = np.where(((csud_pcp_full_db['scid_e64a'] == 3) | (csud_pcp_full_db['scid_e64b'] == 3)), 1, 0)
                    csud_pcp_full_db['A3 Items'] = np.where(((csud_pcp_full_db['scid_e72'] == 3)), 1, 0)
                    csud_pcp_full_db['A4 Items'] = np.where(((csud_pcp_full_db['scid_e80'] == 3)), 1, 0)
                    csud_pcp_full_db['A5 Items'] = np.where(((csud_pcp_full_db['scid_e88a'] == 3) | (csud_pcp_full_db['scid_e88b'] == 3)), 1, 0)
                    csud_pcp_full_db['A6 Items'] = np.where(((csud_pcp_full_db['scid_e96'] == 3)), 1, 0)
                    csud_pcp_full_db['A7 Items'] = np.where(((csud_pcp_full_db['scid_e104'] == 3)), 1, 0)
                    csud_pcp_full_db['A8 Items'] = np.where(((csud_pcp_full_db['scid_e112'] == 3)), 1, 0)
                    csud_pcp_full_db['A9 Items'] = np.where(((csud_pcp_full_db['scid_e120a'] == 3) | (csud_pcp_full_db['scid_e120b'] == 3)), 1, 0)
                    csud_pcp_full_db['A10 Items'] = np.where(((csud_pcp_full_db['scid_e128a'] == 3) | (csud_pcp_full_db['scid_e128b'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_pcp_full_db['CSUD PCP Criterion A Discrepancy'] = np.where(((csud_pcp_full_db['scid_e146cnt'] >= 2) & (csud_pcp_full_db['scid_e146'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_pcp_full_db['New CSUD PCP Symptom Count'] = csud_pcp_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items']].sum(axis = 1)
                    csud_pcp_full_db['CSUD PCP Symptom Count Discrepancy'] = np.where(((csud_pcp_full_db['New CSUD PCP Symptom Count'] != csud_pcp_full_db['scid_e146cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_pcp_db = csud_pcp_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'scid_e146', 'scid_e146cnt', 'CSUD PCP Criterion A Discrepancy', 'New CSUD PCP Symptom Count', 'CSUD PCP Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_pcp_db['Count Discrepancy Direction'] = np.where(((csud_pcp_full_db['scid_e146cnt'] - csud_pcp_full_db['New CSUD PCP Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_pcp_full_db['scid_e146cnt'] == csud_pcp_full_db['New CSUD PCP Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_pcp_db['Count Discrepancy Value'] = csud_pcp_full_db['scid_e146cnt'] - csud_pcp_full_db['New CSUD PCP Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_pcp = refined_csud_pcp_db.loc[((refined_csud_pcp_db['CSUD PCP Symptom Count Discrepancy'] == "Problem") | (refined_csud_pcp_db['CSUD PCP Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e146cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD PCP Criterion A Discrepancy** - The Criterion A item (scid_e146) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD PCP Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD PCP Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_pcp = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_pcp')
                    if interviewer_selection_csud_pcp:
                        problem_children_csud_pcp_final = only_problem_children_csud_pcp[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e146', 'CSUD PCP Criterion A Discrepancy', 'scid_e146cnt', 'New CSUD PCP Symptom Count', 'CSUD PCP Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_pcp_final)
                        csv = convert_df(problem_children_csud_pcp_final)
                    else:
                        problem_children_csud_pcp_final = only_problem_children_csud_pcp[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e146', 'CSUD PCP Criterion A Discrepancy', 'scid_e146cnt', 'New CSUD PCP Symptom Count', 'CSUD PCP Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_pcp_final)
                        csv = convert_df(problem_children_csud_pcp_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_pcp_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_pcp_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_pcp_final[problem_children_csud_pcp_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_pcp_final[problem_children_csud_pcp_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_pcp_problem_subject_list = problem_children_csud_pcp_final.index.values.tolist()
                    see_more_csud_pcp = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_pcp_problem_subject_list)
                    interviewer_selection_csud_pcp_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_pcp')
                    if see_more_csud_pcp is not None:
                        if interviewer_selection_csud_pcp_2:
                            specific_csud_pcp_subject_db = csud_pcp_full_db.loc[see_more_csud_pcp,:]
                            specific_csud_pcp_subject_db_2 = specific_csud_pcp_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e56a', 'scid_e56b', 'A2 Items', 'scid_e64a', 'scid_e64b',
                            'A3 Items', 'scid_e72', 'A4 Items', 'scid_e80', 'A5 Items', 'scid_e88a', 'scid_e88b', 'A6 Items', 'scid_e96', 'A7 Items', 'scid_e104', 'A8 Items', 'scid_e112', 
                            'A9 Items', 'scid_e120a', 'scid_e120b', 'A10 Items', 'scid_e128a', 'scid_e128b', 'scid_e146', 'scid_e146cnt', 'New CSUD PCP Symptom Count']]
                            specific_csud_pcp_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_pcp_subject_db_2)
                            csv = convert_df(specific_csud_pcp_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_pcp_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_pcp_subject_db = csud_pcp_full_db.loc[see_more_csud_pcp,:]
                            specific_csud_pcp_subject_db_2 = specific_csud_pcp_subject_db.loc[:,['A1 Items', 'scid_e56a', 'scid_e56b', 'A2 Items', 'scid_e64a', 'scid_e64b',
                            'A3 Items', 'scid_e72', 'A4 Items', 'scid_e80', 'A5 Items', 'scid_e88a', 'scid_e88b', 'A6 Items', 'scid_e96', 'A7 Items', 'scid_e104', 'A8 Items', 'scid_e112', 
                            'A9 Items', 'scid_e120a', 'scid_e120b', 'A10 Items', 'scid_e128a', 'scid_e128b', 'scid_e146', 'scid_e146cnt', 'New CSUD PCP Symptom Count']]
                            specific_csud_pcp_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_pcp_subject_db_2)
                            csv = convert_df(specific_csud_pcp_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_pcp_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_csud == "Hallucinogens":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Hallucinogens # Just Checking Calculation errors
                    csud_hal_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e57a', 'scid_e57b', 'scid_e65a', 'scid_e65b', 'scid_e73', 'scid_e81', 'scid_e89a', 'scid_e89b', 'scid_e97', 'scid_e105',
                    'scid_e113', 'scid_e121a', 'scid_e121b', 'scid_e129a', 'scid_e129b', 'scid_e148', 'scid_e148cnt']]

                    # Setting index to subject_id
                    csud_hal_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_hal_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_hal_full_db['scid_e81'] = csud_hal_full_db['scid_e81'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_hal_full_db = csud_hal_full_db.astype({'scid_e57a':'int', 'scid_e57b':'int', 'scid_e65a':'int', 'scid_e65b':'int', 'scid_e73':'int', 'scid_e81':'int', 'scid_e89a':'int', 'scid_e89b':'int',
                    'scid_e97':'int', 'scid_e105':'int', 'scid_e113':'int', 'scid_e121a':'int', 'scid_e121b':'int', 'scid_e129a':'int', 'scid_e129b':'int', 'scid_e148':'int', 'scid_e148cnt':'int'})

                    # Counting CSUD HALL symptoms # Max is 11
                    csud_hal_full_db['A1 Items'] = np.where(((csud_hal_full_db['scid_e57a'] == 3) | (csud_hal_full_db['scid_e57b'] == 3)), 1, 0)
                    csud_hal_full_db['A2 Items'] = np.where(((csud_hal_full_db['scid_e65a'] == 3) | (csud_hal_full_db['scid_e65b'] == 3)), 1, 0)
                    csud_hal_full_db['A3 Items'] = np.where(((csud_hal_full_db['scid_e73'] == 3)), 1, 0)
                    csud_hal_full_db['A4 Items'] = np.where(((csud_hal_full_db['scid_e81'] == 3)), 1, 0)
                    csud_hal_full_db['A5 Items'] = np.where(((csud_hal_full_db['scid_e89a'] == 3) | (csud_hal_full_db['scid_e89b'] == 3)), 1, 0)
                    csud_hal_full_db['A6 Items'] = np.where(((csud_hal_full_db['scid_e97'] == 3)), 1, 0)
                    csud_hal_full_db['A7 Items'] = np.where(((csud_hal_full_db['scid_e105'] == 3)), 1, 0)
                    csud_hal_full_db['A8 Items'] = np.where(((csud_hal_full_db['scid_e113'] == 3)), 1, 0)
                    csud_hal_full_db['A9 Items'] = np.where(((csud_hal_full_db['scid_e121a'] == 3) | (csud_hal_full_db['scid_e121b'] == 3)), 1, 0)
                    csud_hal_full_db['A10 Items'] = np.where(((csud_hal_full_db['scid_e129a'] == 3) | (csud_hal_full_db['scid_e129b'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_hal_full_db['CSUD HALL Criterion A Discrepancy'] = np.where(((csud_hal_full_db['scid_e148cnt'] >= 2) & (csud_hal_full_db['scid_e148'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_hal_full_db['New CSUD HALL Symptom Count'] = csud_hal_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items']].sum(axis = 1)
                    csud_hal_full_db['CSUD HALL Symptom Count Discrepancy'] = np.where(((csud_hal_full_db['New CSUD HALL Symptom Count'] != csud_hal_full_db['scid_e148cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_hal_db = csud_hal_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'scid_e148', 'scid_e148cnt', 'CSUD HALL Criterion A Discrepancy', 'New CSUD HALL Symptom Count', 'CSUD HALL Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_hal_db['Count Discrepancy Direction'] = np.where(((csud_hal_full_db['scid_e148cnt'] - csud_hal_full_db['New CSUD HALL Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_hal_full_db['scid_e148cnt'] == csud_hal_full_db['New CSUD HALL Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_hal_db['Count Discrepancy Value'] = csud_hal_full_db['scid_e148cnt'] - csud_hal_full_db['New CSUD HALL Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_hal = refined_csud_hal_db.loc[((refined_csud_hal_db['CSUD HALL Symptom Count Discrepancy'] == "Problem") | (refined_csud_hal_db['CSUD HALL Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e148cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD HALL Criterion A Discrepancy** - The Criterion A item (scid_e148) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD HALL Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD HALL Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_hal = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_hal')
                    if interviewer_selection_csud_hal:
                        problem_children_csud_hal_final = only_problem_children_csud_hal[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e148', 'CSUD HALL Criterion A Discrepancy', 'scid_e148cnt', 'New CSUD HALL Symptom Count', 'CSUD HALL Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_hal_final)
                        csv = convert_df(problem_children_csud_hal_final)
                    else:
                        problem_children_csud_hal_final = only_problem_children_csud_hal[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e148', 'CSUD HALL Criterion A Discrepancy', 'scid_e148cnt', 'New CSUD HALL Symptom Count', 'CSUD HALL Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_hal_final)
                        csv = convert_df(problem_children_csud_hal_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_hal_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_hal_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_hal_final[problem_children_csud_hal_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_hal_final[problem_children_csud_hal_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_hal_problem_subject_list = problem_children_csud_hal_final.index.values.tolist()
                    see_more_csud_hal = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_hal_problem_subject_list)
                    interviewer_selection_csud_hal_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_hal')
                    if see_more_csud_hal is not None:
                        if interviewer_selection_csud_hal_2:
                            specific_csud_hal_subject_db = csud_hal_full_db.loc[see_more_csud_hal,:]
                            specific_csud_hal_subject_db_2 = specific_csud_hal_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e57a', 'scid_e57b', 'A2 Items', 'scid_e65a', 'scid_e65b',
                            'A3 Items', 'scid_e73', 'A4 Items', 'scid_e81', 'A5 Items', 'scid_e89a', 'scid_e89b', 'A6 Items', 'scid_e97', 'A7 Items', 'scid_e105', 'A8 Items', 'scid_e113', 
                            'A9 Items', 'scid_e121a', 'scid_e121b', 'A10 Items', 'scid_e129a', 'scid_e129b', 'scid_e148', 'scid_e148cnt', 'New CSUD HALL Symptom Count']]
                            specific_csud_hal_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_hal_subject_db_2)
                            csv = convert_df(specific_csud_hal_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_hal_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_hal_subject_db = csud_hal_full_db.loc[see_more_csud_hal,:]
                            specific_csud_hal_subject_db_2 = specific_csud_hal_subject_db.loc[:,['A1 Items', 'scid_e57a', 'scid_e57b', 'A2 Items', 'scid_e65a', 'scid_e65b',
                            'A3 Items', 'scid_e73', 'A4 Items', 'scid_e81', 'A5 Items', 'scid_e89a', 'scid_e89b', 'A6 Items', 'scid_e97', 'A7 Items', 'scid_e105', 'A8 Items', 'scid_e113', 
                            'A9 Items', 'scid_e121a', 'scid_e121b', 'A10 Items', 'scid_e129a', 'scid_e129b', 'scid_e148', 'scid_e148cnt', 'New CSUD HALL Symptom Count']]
                            specific_csud_hal_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_hal_subject_db_2)
                            csv = convert_df(specific_csud_hal_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_hal_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_csud == "Other/Unknown":
                    st.markdown(f"#### {drug_selection_csud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # CSUD Other/Unknown # Just Checking Calculation errors
                    csud_oth_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e58a', 'scid_e58b', 'scid_e66a', 'scid_e66b', 'scid_e74', 'scid_e82', 'scid_e90a', 'scid_e90b', 'scid_e98', 'scid_e106',
                    'scid_e114', 'scid_e122a', 'scid_e122b', 'scid_e130a', 'scid_e130b', 'scid_e135', 'scid_e150', 'scid_e150cnt']]

                    # Setting index to subject_id
                    csud_oth_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    csud_oth_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    csud_oth_full_db['scid_e82'] = csud_oth_full_db['scid_e82'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    csud_oth_full_db = csud_oth_full_db.astype({'scid_e58a':'int', 'scid_e58b':'int', 'scid_e66a':'int', 'scid_e66b':'int', 'scid_e74':'int', 'scid_e82':'int', 'scid_e90a':'int', 'scid_e90b':'int',
                    'scid_e98':'int', 'scid_e106':'int', 'scid_e114':'int', 'scid_e122a':'int', 'scid_e122b':'int', 'scid_e130a':'int', 'scid_e130b':'int', 'scid_e135':'int', 'scid_e150':'int', 
                    'scid_e150cnt':'int'})

                    # Counting CSUD OTH symptoms # Max is 11
                    csud_oth_full_db['A1 Items'] = np.where(((csud_oth_full_db['scid_e58a'] == 3) | (csud_oth_full_db['scid_e58b'] == 3)), 1, 0)
                    csud_oth_full_db['A2 Items'] = np.where(((csud_oth_full_db['scid_e66a'] == 3) | (csud_oth_full_db['scid_e66b'] == 3)), 1, 0)
                    csud_oth_full_db['A3 Items'] = np.where(((csud_oth_full_db['scid_e74'] == 3)), 1, 0)
                    csud_oth_full_db['A4 Items'] = np.where(((csud_oth_full_db['scid_e82'] == 3)), 1, 0)
                    csud_oth_full_db['A5 Items'] = np.where(((csud_oth_full_db['scid_e90a'] == 3) | (csud_oth_full_db['scid_e90b'] == 3)), 1, 0)
                    csud_oth_full_db['A6 Items'] = np.where(((csud_oth_full_db['scid_e98'] == 3)), 1, 0)
                    csud_oth_full_db['A7 Items'] = np.where(((csud_oth_full_db['scid_e106'] == 3)), 1, 0)
                    csud_oth_full_db['A8 Items'] = np.where(((csud_oth_full_db['scid_e114'] == 3)), 1, 0)
                    csud_oth_full_db['A9 Items'] = np.where(((csud_oth_full_db['scid_e122a'] == 3) | (csud_oth_full_db['scid_e122b'] == 3)), 1, 0)
                    csud_oth_full_db['A10 Items'] = np.where(((csud_oth_full_db['scid_e130a'] == 3) | (csud_oth_full_db['scid_e130b'] == 3)), 1, 0)
                    csud_oth_full_db['A11 Items'] = np.where(((csud_oth_full_db['scid_e135'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    csud_oth_full_db['CSUD OTH Criterion A Discrepancy'] = np.where(((csud_oth_full_db['scid_e150cnt'] >= 2) & (csud_oth_full_db['scid_e150'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    csud_oth_full_db['New CSUD OTH Symptom Count'] = csud_oth_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    csud_oth_full_db['CSUD OTH Symptom Count Discrepancy'] = np.where(((csud_oth_full_db['New CSUD OTH Symptom Count'] != csud_oth_full_db['scid_e150cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_csud_oth_db = csud_oth_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e150', 'scid_e150cnt', 'CSUD OTH Criterion A Discrepancy', 'New CSUD OTH Symptom Count', 'CSUD OTH Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_csud_oth_db['Count Discrepancy Direction'] = np.where(((csud_oth_full_db['scid_e150cnt'] - csud_oth_full_db['New CSUD OTH Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((csud_oth_full_db['scid_e150cnt'] == csud_oth_full_db['New CSUD OTH Symptom Count'])), "Same", "New Count Larger"))
                    refined_csud_oth_db['Count Discrepancy Value'] = csud_oth_full_db['scid_e150cnt'] - csud_oth_full_db['New CSUD OTH Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_csud_oth = refined_csud_oth_db.loc[((refined_csud_oth_db['CSUD OTH Symptom Count Discrepancy'] == "Problem") | (refined_csud_oth_db['CSUD OTH Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e150cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **CSUD OTH Criterion A Discrepancy** - The Criterion A item (scid_e150) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New CSUD OTH Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **CSUD OTH Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_csud_oth = st.checkbox("Would you like to see the associated interviewer?", key = 'csud_oth')
                    if interviewer_selection_csud_oth:
                        problem_children_csud_oth_final = only_problem_children_csud_oth[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e150', 'CSUD OTH Criterion A Discrepancy', 'scid_e150cnt', 'New CSUD OTH Symptom Count', 'CSUD OTH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_oth_final)
                        csv = convert_df(problem_children_csud_oth_final)
                    else:
                        problem_children_csud_oth_final = only_problem_children_csud_oth[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e150', 'CSUD OTH Criterion A Discrepancy', 'scid_e150cnt', 'New CSUD OTH Symptom Count', 'CSUD OTH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_csud_oth_final)
                        csv = convert_df(problem_children_csud_oth_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_csud_oth_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'csud_oth_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_csud_oth_final[problem_children_csud_oth_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_csud_oth_final[problem_children_csud_oth_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    csud_oth_problem_subject_list = problem_children_csud_oth_final.index.values.tolist()
                    see_more_csud_oth = st.multiselect("See Specific Subject Info? [Select as many as you would like]", csud_oth_problem_subject_list)
                    interviewer_selection_csud_oth_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_csud_oth')
                    if see_more_csud_oth is not None:
                        if interviewer_selection_csud_oth_2:
                            specific_csud_oth_subject_db = csud_oth_full_db.loc[see_more_csud_oth,:]
                            specific_csud_oth_subject_db_2 = specific_csud_oth_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e58a', 'scid_e58b', 'A2 Items', 'scid_e66a', 'scid_e66b',
                            'A3 Items', 'scid_e74', 'A4 Items', 'scid_e82', 'A5 Items', 'scid_e90a', 'scid_e90b', 'A6 Items', 'scid_e98', 'A7 Items', 'scid_e106', 'A8 Items', 'scid_e114', 
                            'A9 Items', 'scid_e122a', 'scid_e122b', 'A10 Items', 'scid_e130a', 'scid_e130b', 'A11 Items', 'scid_e135', 'scid_e150', 'scid_e150cnt', 'New CSUD OTH Symptom Count']]
                            specific_csud_oth_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_oth_subject_db_2)
                            csv = convert_df(specific_csud_oth_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_oth_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_csud_oth_subject_db = csud_oth_full_db.loc[see_more_csud_oth,:]
                            specific_csud_oth_subject_db_2 = specific_csud_oth_subject_db.loc[:,['A1 Items', 'scid_e58a', 'scid_e58b', 'A2 Items', 'scid_e66a', 'scid_e66b',
                            'A3 Items', 'scid_e74', 'A4 Items', 'scid_e82', 'A5 Items', 'scid_e90a', 'scid_e90b', 'A6 Items', 'scid_e98', 'A7 Items', 'scid_e106', 'A8 Items', 'scid_e114', 
                            'A9 Items', 'scid_e122a', 'scid_e122b', 'A10 Items', 'scid_e130a', 'scid_e130b', 'A11 Items', 'scid_e135', 'scid_e150', 'scid_e150cnt', 'New CSUD OTH Symptom Count']]
                            specific_csud_oth_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_csud_oth_subject_db_2)
                            csv = convert_df(specific_csud_oth_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'csud_oth_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_e_syndrome_selection == 'PSUD':
                st.markdown(f"### {module_e_syndrome_selection}")
                st.markdown("---")
                drug_selection_psud = st.selectbox("Which Drug would you like to look at?", ["---", "All", "Sed/Hyp/Anx", "Cannabis", "Stimulants", "Opioids", "Inhalants", "PCP", "Hallucinogens", "Other/Unknown"])
                if drug_selection_psud == "---":
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
                if drug_selection_psud == "All":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")
                if drug_selection_psud == "Sed/Hyp/Anx":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Sed/Hyp/Anx # Just Checking Calculation errors
                    psud_sed_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e214a', 'scid_e214b', 'scid_e222a', 'scid_e222b', 'scid_e230', 'scid_e238', 'scid_e246a', 'scid_e246b', 'scid_e254', 'scid_e262',
                    'scid_e270', 'scid_e278a', 'scid_e278b', 'scid_e286a', 'scid_e286b', 'scid_e294', 'scid_e299', 'scid_e299cnt']]

                    # Setting index to subject_id
                    psud_sed_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_sed_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_sed_full_db['scid_e238'] = psud_sed_full_db['scid_e238'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_sed_full_db = psud_sed_full_db.astype({'scid_e214a':'int', 'scid_e214b':'int', 'scid_e222a':'int', 'scid_e222b':'int', 'scid_e230':'int', 'scid_e238':'int', 'scid_e246a':'int', 'scid_e246b':'int',
                    'scid_e254':'int', 'scid_e262':'int', 'scid_e270':'int', 'scid_e278a':'int', 'scid_e278b':'int', 'scid_e286a':'int', 'scid_e286b':'int', 'scid_e294':'int', 'scid_e299':'int', 
                    'scid_e299cnt':'int'})

                    # Counting PSUD SED symptoms # Max is 11
                    psud_sed_full_db['A1 Items'] = np.where(((psud_sed_full_db['scid_e214a'] == 3) | (psud_sed_full_db['scid_e214b'] == 3)), 1, 0)
                    psud_sed_full_db['A2 Items'] = np.where(((psud_sed_full_db['scid_e222a'] == 3) | (psud_sed_full_db['scid_e222b'] == 3)), 1, 0)
                    psud_sed_full_db['A3 Items'] = np.where(((psud_sed_full_db['scid_e230'] == 3)), 1, 0)
                    psud_sed_full_db['A4 Items'] = np.where(((psud_sed_full_db['scid_e238'] == 3)), 1, 0)
                    psud_sed_full_db['A5 Items'] = np.where(((psud_sed_full_db['scid_e246a'] == 3) | (psud_sed_full_db['scid_e246b'] == 3)), 1, 0)
                    psud_sed_full_db['A6 Items'] = np.where(((psud_sed_full_db['scid_e254'] == 3)), 1, 0)
                    psud_sed_full_db['A7 Items'] = np.where(((psud_sed_full_db['scid_e262'] == 3)), 1, 0)
                    psud_sed_full_db['A8 Items'] = np.where(((psud_sed_full_db['scid_e270'] == 3)), 1, 0)
                    psud_sed_full_db['A9 Items'] = np.where(((psud_sed_full_db['scid_e278a'] == 3) | (psud_sed_full_db['scid_e278b'] == 3)), 1, 0)
                    psud_sed_full_db['A10 Items'] = np.where(((psud_sed_full_db['scid_e286a'] == 3) | (psud_sed_full_db['scid_e286b'] == 3)), 1, 0)
                    psud_sed_full_db['A11 Items'] = np.where(((psud_sed_full_db['scid_e294'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_sed_full_db['PSUD SED Criterion A Discrepancy'] = np.where(((psud_sed_full_db['scid_e299cnt'] >= 2) & (psud_sed_full_db['scid_e299'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_sed_full_db['New PSUD SED Symptom Count'] = psud_sed_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    psud_sed_full_db['PSUD SED Symptom Count Discrepancy'] = np.where(((psud_sed_full_db['New PSUD SED Symptom Count'] != psud_sed_full_db['scid_e299cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Discrepancy Items
                    refined_psud_sed_db = psud_sed_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e299', 'scid_e299cnt', 'PSUD SED Criterion A Discrepancy', 'New PSUD SED Symptom Count', 'PSUD SED Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_sed_db['Count Discrepancy Direction'] = np.where(((psud_sed_full_db['scid_e299cnt'] - psud_sed_full_db['New PSUD SED Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_sed_full_db['scid_e299cnt'] == psud_sed_full_db['New PSUD SED Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_sed_db['Count Discrepancy Value'] = psud_sed_full_db['scid_e299cnt'] - psud_sed_full_db['New PSUD SED Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_sed = refined_psud_sed_db.loc[((refined_psud_sed_db['PSUD SED Symptom Count Discrepancy'] == "Problem") | (refined_psud_sed_db['PSUD SED Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e299cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD SED Criterion A Discrepancy** - The Criterion A item (scid_e299) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD SED Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD SED Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_sed = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_sed')
                    if interviewer_selection_psud_sed:
                        problem_children_psud_sed_final = only_problem_children_psud_sed[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e299', 'PSUD SED Criterion A Discrepancy', 'scid_e299cnt', 'New PSUD SED Symptom Count', 'PSUD SED Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_sed_final)
                        csv = convert_df(problem_children_psud_sed_final)
                    else:
                        problem_children_psud_sed_final = only_problem_children_psud_sed[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e299', 'PSUD SED Criterion A Discrepancy', 'scid_e299cnt', 'New PSUD SED Symptom Count', 'PSUD SED Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_sed_final)
                        csv = convert_df(problem_children_psud_sed_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_sed_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_sed_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_sed_final[problem_children_psud_sed_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_sed_final[problem_children_psud_sed_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_sed_problem_subject_list = problem_children_psud_sed_final.index.values.tolist()
                    see_more_psud_sed = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_sed_problem_subject_list)
                    interviewer_selection_psud_sed_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_sed')
                    if see_more_psud_sed is not None:
                        if interviewer_selection_psud_sed_2:
                            specific_psud_sed_subject_db = psud_sed_full_db.loc[see_more_psud_sed,:]
                            specific_psud_sed_subject_db_2 = specific_psud_sed_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e214a', 'scid_e214b', 'A2 Items', 'scid_e222a', 'scid_e222b',
                            'A3 Items', 'scid_e230', 'A4 Items', 'scid_e238', 'A5 Items', 'scid_e246a', 'scid_e246b', 'A6 Items', 'scid_e254', 'A7 Items', 'scid_e262', 'A8 Items', 'scid_e270', 
                            'A9 Items', 'scid_e278a', 'scid_e278b', 'A10 Items', 'scid_e286a', 'scid_e286b', 'A11 Items', 'scid_e294', 'scid_e299', 'scid_e299cnt', 'New PSUD SED Symptom Count']]
                            specific_psud_sed_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_sed_subject_db_2)
                            csv = convert_df(specific_psud_sed_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_sed_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_sed_subject_db = psud_sed_full_db.loc[see_more_psud_sed,:]
                            specific_psud_sed_subject_db_2 = specific_psud_sed_subject_db.loc[:,['A1 Items', 'scid_e214a', 'scid_e214b', 'A2 Items', 'scid_e222a', 'scid_e222b',
                            'A3 Items', 'scid_e230', 'A4 Items', 'scid_e238', 'A5 Items', 'scid_e246a', 'scid_e246b', 'A6 Items', 'scid_e254', 'A7 Items', 'scid_e262', 'A8 Items', 'scid_e270', 
                            'A9 Items', 'scid_e278a', 'scid_e278b', 'A10 Items', 'scid_e286a', 'scid_e286b', 'A11 Items', 'scid_e294', 'scid_e299', 'scid_e299cnt', 'New PSUD SED Symptom Count']]
                            specific_psud_sed_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_sed_subject_db_2)
                            csv = convert_df(specific_psud_sed_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_sed_problem_subject_more_depth_{today}.csv', mime = 'text/csv')  
                if drug_selection_psud == "Cannabis":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Cannabis # Just Checking Calculation errors
                    psud_can_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e215a', 'scid_e215b', 'scid_e223a', 'scid_e223b', 'scid_e231', 'scid_e239', 'scid_e247a', 'scid_e247b', 'scid_e255', 'scid_e263',
                    'scid_e271', 'scid_e279a', 'scid_e279b', 'scid_e287a', 'scid_e287b', 'scid_e295', 'scid_e303', 'scid_e303cnt']]

                    # Setting index to subject_id
                    psud_can_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_can_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_can_full_db['scid_e239'] = psud_can_full_db['scid_e239'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_can_full_db = psud_can_full_db.astype({'scid_e215a':'int', 'scid_e215b':'int', 'scid_e223a':'int', 'scid_e223b':'int', 'scid_e231':'int', 'scid_e239':'int', 'scid_e247a':'int', 'scid_e247b':'int',
                    'scid_e255':'int', 'scid_e263':'int', 'scid_e271':'int', 'scid_e279a':'int', 'scid_e279b':'int', 'scid_e287a':'int', 'scid_e287b':'int', 'scid_e295':'int', 'scid_e303':'int', 
                    'scid_e303cnt':'int'})

                    # Counting PSUD CAN symptoms # Max is 11
                    psud_can_full_db['A1 Items'] = np.where(((psud_can_full_db['scid_e215a'] == 3) | (psud_can_full_db['scid_e215b'] == 3)), 1, 0)
                    psud_can_full_db['A2 Items'] = np.where(((psud_can_full_db['scid_e223a'] == 3) | (psud_can_full_db['scid_e223b'] == 3)), 1, 0)
                    psud_can_full_db['A3 Items'] = np.where(((psud_can_full_db['scid_e231'] == 3)), 1, 0)
                    psud_can_full_db['A4 Items'] = np.where(((psud_can_full_db['scid_e239'] == 3)), 1, 0)
                    psud_can_full_db['A5 Items'] = np.where(((psud_can_full_db['scid_e247a'] == 3) | (psud_can_full_db['scid_e247b'] == 3)), 1, 0)
                    psud_can_full_db['A6 Items'] = np.where(((psud_can_full_db['scid_e255'] == 3)), 1, 0)
                    psud_can_full_db['A7 Items'] = np.where(((psud_can_full_db['scid_e263'] == 3)), 1, 0)
                    psud_can_full_db['A8 Items'] = np.where(((psud_can_full_db['scid_e271'] == 3)), 1, 0)
                    psud_can_full_db['A9 Items'] = np.where(((psud_can_full_db['scid_e279a'] == 3) | (psud_can_full_db['scid_e279b'] == 3)), 1, 0)
                    psud_can_full_db['A10 Items'] = np.where(((psud_can_full_db['scid_e287a'] == 3) | (psud_can_full_db['scid_e287b'] == 3)), 1, 0)
                    psud_can_full_db['A11 Items'] = np.where(((psud_can_full_db['scid_e295'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_can_full_db['PSUD CAN Criterion A Discrepancy'] = np.where(((psud_can_full_db['scid_e303cnt'] >= 2) & (psud_can_full_db['scid_e303'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_can_full_db['New PSUD CAN Symptom Count'] = psud_can_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    psud_can_full_db['PSUD CAN Symptom Count Discrepancy'] = np.where(((psud_can_full_db['New PSUD CAN Symptom Count'] != psud_can_full_db['scid_e303cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_can_db = psud_can_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e303', 'scid_e303cnt', 'PSUD CAN Criterion A Discrepancy', 'New PSUD CAN Symptom Count', 'PSUD CAN Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_can_db['Count Discrepancy Direction'] = np.where(((psud_can_full_db['scid_e303cnt'] - psud_can_full_db['New PSUD CAN Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_can_full_db['scid_e303cnt'] == psud_can_full_db['New PSUD CAN Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_can_db['Count Discrepancy Value'] = psud_can_full_db['scid_e303cnt'] - psud_can_full_db['New PSUD CAN Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_can = refined_psud_can_db.loc[((refined_psud_can_db['PSUD CAN Symptom Count Discrepancy'] == "Problem") | (refined_psud_can_db['PSUD CAN Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e303cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD CAN Criterion A Discrepancy** - The Criterion A item (scid_e303) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD CAN Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD CAN Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_can = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_can')
                    if interviewer_selection_psud_can:
                        problem_children_psud_can_final = only_problem_children_psud_can[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e303', 'PSUD CAN Criterion A Discrepancy', 'scid_e303cnt', 'New PSUD CAN Symptom Count', 'PSUD CAN Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_can_final)
                        csv = convert_df(problem_children_psud_can_final)
                    else:
                        problem_children_psud_can_final = only_problem_children_psud_can[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e303', 'PSUD CAN Criterion A Discrepancy', 'scid_e303cnt', 'New PSUD CAN Symptom Count', 'PSUD CAN Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_can_final)
                        csv = convert_df(problem_children_psud_can_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_can_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_can_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_can_final[problem_children_psud_can_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_can_final[problem_children_psud_can_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_can_problem_subject_list = problem_children_psud_can_final.index.values.tolist()
                    see_more_psud_can = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_can_problem_subject_list)
                    interviewer_selection_psud_can_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_can')
                    if see_more_psud_can is not None:
                        if interviewer_selection_psud_can_2:
                            specific_psud_can_subject_db = psud_can_full_db.loc[see_more_psud_can,:]
                            specific_psud_can_subject_db_2 = specific_psud_can_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e215a', 'scid_e215b', 'A2 Items', 'scid_e223a', 'scid_e223b',
                            'A3 Items', 'scid_e231', 'A4 Items', 'scid_e239', 'A5 Items', 'scid_e247a', 'scid_e247b', 'A6 Items', 'scid_e255', 'A7 Items', 'scid_e263', 'A8 Items', 'scid_e271', 
                            'A9 Items', 'scid_e279a', 'scid_e279b', 'A10 Items', 'scid_e287a', 'scid_e287b', 'A11 Items', 'scid_e295', 'scid_e303', 'scid_e303cnt', 'New PSUD CAN Symptom Count']]
                            specific_psud_can_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_can_subject_db_2)
                            csv = convert_df(specific_psud_can_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_can_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_can_subject_db = psud_can_full_db.loc[see_more_psud_can,:]
                            specific_psud_can_subject_db_2 = specific_psud_can_subject_db.loc[:,['A1 Items', 'scid_e215a', 'scid_e215b', 'A2 Items', 'scid_e223a', 'scid_e223b',
                            'A3 Items', 'scid_e231', 'A4 Items', 'scid_e239', 'A5 Items', 'scid_e247a', 'scid_e247b', 'A6 Items', 'scid_e255', 'A7 Items', 'scid_e263', 'A8 Items', 'scid_e271', 
                            'A9 Items', 'scid_e279a', 'scid_e279b', 'A10 Items', 'scid_e287a', 'scid_e287b', 'A11 Items', 'scid_e295', 'scid_e303', 'scid_e303cnt', 'New PSUD CAN Symptom Count']]
                            specific_psud_can_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_can_subject_db_2)
                            csv = convert_df(specific_psud_can_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_can_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_psud == "Stimulants":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Stimulants # Just Checking Calculation errors
                    psud_stim_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e216a', 'scid_e216b', 'scid_e224a', 'scid_e224b', 'scid_e232', 'scid_e240', 'scid_e248a', 'scid_e248b', 'scid_e256', 'scid_e264',
                    'scid_e272', 'scid_e280a', 'scid_e280b', 'scid_e288a', 'scid_e288b', 'scid_e296', 'scid_e307', 'scid_e307cnt']]

                    # Setting index to subject_id
                    psud_stim_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_stim_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_stim_full_db['scid_e240'] = psud_stim_full_db['scid_e240'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_stim_full_db = psud_stim_full_db.astype({'scid_e216a':'int', 'scid_e216b':'int', 'scid_e224a':'int', 'scid_e224b':'int', 'scid_e232':'int', 'scid_e240':'int', 'scid_e248a':'int', 'scid_e248b':'int',
                    'scid_e256':'int', 'scid_e264':'int', 'scid_e272':'int', 'scid_e280a':'int', 'scid_e280b':'int', 'scid_e288a':'int', 'scid_e288b':'int', 'scid_e296':'int', 'scid_e307':'int', 
                    'scid_e307cnt':'int'})

                    # Counting PSUD STIM symptoms # Max is 11
                    psud_stim_full_db['A1 Items'] = np.where(((psud_stim_full_db['scid_e216a'] == 3) | (psud_stim_full_db['scid_e216b'] == 3)), 1, 0)
                    psud_stim_full_db['A2 Items'] = np.where(((psud_stim_full_db['scid_e224a'] == 3) | (psud_stim_full_db['scid_e224b'] == 3)), 1, 0)
                    psud_stim_full_db['A3 Items'] = np.where(((psud_stim_full_db['scid_e232'] == 3)), 1, 0)
                    psud_stim_full_db['A4 Items'] = np.where(((psud_stim_full_db['scid_e240'] == 3)), 1, 0)
                    psud_stim_full_db['A5 Items'] = np.where(((psud_stim_full_db['scid_e248a'] == 3) | (psud_stim_full_db['scid_e248b'] == 3)), 1, 0)
                    psud_stim_full_db['A6 Items'] = np.where(((psud_stim_full_db['scid_e256'] == 3)), 1, 0)
                    psud_stim_full_db['A7 Items'] = np.where(((psud_stim_full_db['scid_e264'] == 3)), 1, 0)
                    psud_stim_full_db['A8 Items'] = np.where(((psud_stim_full_db['scid_e272'] == 3)), 1, 0)
                    psud_stim_full_db['A9 Items'] = np.where(((psud_stim_full_db['scid_e280a'] == 3) | (psud_stim_full_db['scid_e280b'] == 3)), 1, 0)
                    psud_stim_full_db['A10 Items'] = np.where(((psud_stim_full_db['scid_e288a'] == 3) | (psud_stim_full_db['scid_e288b'] == 3)), 1, 0)
                    psud_stim_full_db['A11 Items'] = np.where(((psud_stim_full_db['scid_e296'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_stim_full_db['PSUD STIM Criterion A Discrepancy'] = np.where(((psud_stim_full_db['scid_e307cnt'] >= 2) & (psud_stim_full_db['scid_e307'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_stim_full_db['New PSUD STIM Symptom Count'] = psud_stim_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    psud_stim_full_db['PSUD STIM Symptom Count Discrepancy'] = np.where(((psud_stim_full_db['New PSUD STIM Symptom Count'] != psud_stim_full_db['scid_e307cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_stim_db = psud_stim_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e307', 'scid_e307cnt', 'PSUD STIM Criterion A Discrepancy', 'New PSUD STIM Symptom Count', 'PSUD STIM Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_stim_db['Count Discrepancy Direction'] = np.where(((psud_stim_full_db['scid_e307cnt'] - psud_stim_full_db['New PSUD STIM Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_stim_full_db['scid_e307cnt'] == psud_stim_full_db['New PSUD STIM Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_stim_db['Count Discrepancy Value'] = psud_stim_full_db['scid_e307cnt'] - psud_stim_full_db['New PSUD STIM Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_stim = refined_psud_stim_db.loc[((refined_psud_stim_db['PSUD STIM Symptom Count Discrepancy'] == "Problem") | (refined_psud_stim_db['PSUD STIM Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e307cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD STIM Criterion A Discrepancy** - The Criterion A item (scid_e307) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD STIM Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD STIM Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_stim = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_stim')
                    if interviewer_selection_psud_stim:
                        problem_children_psud_stim_final = only_problem_children_psud_stim[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e307', 'PSUD STIM Criterion A Discrepancy', 'scid_e307cnt', 'New PSUD STIM Symptom Count', 'PSUD STIM Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_stim_final)
                        csv = convert_df(problem_children_psud_stim_final)
                    else:
                        problem_children_psud_stim_final = only_problem_children_psud_stim[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e307', 'PSUD STIM Criterion A Discrepancy', 'scid_e307cnt', 'New PSUD STIM Symptom Count', 'PSUD STIM Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_stim_final)
                        csv = convert_df(problem_children_psud_stim_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_stim_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_stim_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_stim_final[problem_children_psud_stim_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_stim_final[problem_children_psud_stim_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_stim_problem_subject_list = problem_children_psud_stim_final.index.values.tolist()
                    see_more_psud_stim = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_stim_problem_subject_list)
                    interviewer_selection_psud_stim_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_stim')
                    if see_more_psud_stim is not None:
                        if interviewer_selection_psud_stim_2:
                            specific_psud_stim_subject_db = psud_stim_full_db.loc[see_more_psud_stim,:]
                            specific_psud_stim_subject_db_2 = specific_psud_stim_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e216a', 'scid_e216b', 'A2 Items', 'scid_e224a', 'scid_e224b',
                            'A3 Items', 'scid_e232', 'A4 Items', 'scid_e240', 'A5 Items', 'scid_e248a', 'scid_e248b', 'A6 Items', 'scid_e256', 'A7 Items', 'scid_e264', 'A8 Items', 'scid_e272', 
                            'A9 Items', 'scid_e280a', 'scid_e280b', 'A10 Items', 'scid_e288a', 'scid_e288b', 'A11 Items', 'scid_e296', 'scid_e307', 'scid_e307cnt', 'New PSUD STIM Symptom Count']]
                            specific_psud_stim_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_stim_subject_db_2)
                            csv = convert_df(specific_psud_stim_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_stim_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_stim_subject_db = psud_stim_full_db.loc[see_more_psud_stim,:]
                            specific_psud_stim_subject_db_2 = specific_psud_stim_subject_db.loc[:,['A1 Items', 'scid_e216a', 'scid_e216b', 'A2 Items', 'scid_e224a', 'scid_e224b',
                            'A3 Items', 'scid_e232', 'A4 Items', 'scid_e240', 'A5 Items', 'scid_e248a', 'scid_e248b', 'A6 Items', 'scid_e256', 'A7 Items', 'scid_e264', 'A8 Items', 'scid_e272', 
                            'A9 Items', 'scid_e280a', 'scid_e280b', 'A10 Items', 'scid_e288a', 'scid_e288b', 'A11 Items', 'scid_e296', 'scid_e307', 'scid_e307cnt', 'New PSUD STIM Symptom Count']]
                            specific_psud_stim_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_stim_subject_db_2)
                            csv = convert_df(specific_psud_stim_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_stim_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_psud == "Opioids":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Opioids # Just Checking Calculation errors
                    psud_opi_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e217a', 'scid_e217b', 'scid_e225a', 'scid_e225b', 'scid_e233', 'scid_e241', 'scid_e249a', 'scid_e249b', 'scid_e257', 'scid_e265',
                    'scid_e273', 'scid_e281a', 'scid_e281b', 'scid_e289a', 'scid_e289b', 'scid_e297', 'scid_e311', 'scid_e311cnt']]

                    # Setting index to subject_id
                    psud_opi_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_opi_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_opi_full_db['scid_e241'] = psud_opi_full_db['scid_e241'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_opi_full_db = psud_opi_full_db.astype({'scid_e217a':'int', 'scid_e217b':'int', 'scid_e225a':'int', 'scid_e225b':'int', 'scid_e233':'int', 'scid_e241':'int', 'scid_e249a':'int', 'scid_e249b':'int',
                    'scid_e257':'int', 'scid_e265':'int', 'scid_e273':'int', 'scid_e281a':'int', 'scid_e281b':'int', 'scid_e289a':'int', 'scid_e289b':'int', 'scid_e297':'int', 'scid_e311':'int', 
                    'scid_e311cnt':'int'})

                    # Counting PSUD OPI symptoms # Max is 11
                    psud_opi_full_db['A1 Items'] = np.where(((psud_opi_full_db['scid_e217a'] == 3) | (psud_opi_full_db['scid_e217b'] == 3)), 1, 0)
                    psud_opi_full_db['A2 Items'] = np.where(((psud_opi_full_db['scid_e225a'] == 3) | (psud_opi_full_db['scid_e225b'] == 3)), 1, 0)
                    psud_opi_full_db['A3 Items'] = np.where(((psud_opi_full_db['scid_e233'] == 3)), 1, 0)
                    psud_opi_full_db['A4 Items'] = np.where(((psud_opi_full_db['scid_e241'] == 3)), 1, 0)
                    psud_opi_full_db['A5 Items'] = np.where(((psud_opi_full_db['scid_e249a'] == 3) | (psud_opi_full_db['scid_e249b'] == 3)), 1, 0)
                    psud_opi_full_db['A6 Items'] = np.where(((psud_opi_full_db['scid_e257'] == 3)), 1, 0)
                    psud_opi_full_db['A7 Items'] = np.where(((psud_opi_full_db['scid_e265'] == 3)), 1, 0)
                    psud_opi_full_db['A8 Items'] = np.where(((psud_opi_full_db['scid_e273'] == 3)), 1, 0)
                    psud_opi_full_db['A9 Items'] = np.where(((psud_opi_full_db['scid_e281a'] == 3) | (psud_opi_full_db['scid_e281b'] == 3)), 1, 0)
                    psud_opi_full_db['A10 Items'] = np.where(((psud_opi_full_db['scid_e289a'] == 3) | (psud_opi_full_db['scid_e289b'] == 3)), 1, 0)
                    psud_opi_full_db['A11 Items'] = np.where(((psud_opi_full_db['scid_e297'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_opi_full_db['PSUD OPI Criterion A Discrepancy'] = np.where(((psud_opi_full_db['scid_e311cnt'] >= 2) & (psud_opi_full_db['scid_e311'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_opi_full_db['New PSUD OPI Symptom Count'] = psud_opi_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    psud_opi_full_db['PSUD OPI Symptom Count Discrepancy'] = np.where(((psud_opi_full_db['New PSUD OPI Symptom Count'] != psud_opi_full_db['scid_e311cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_opi_db = psud_opi_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e311', 'scid_e311cnt', 'PSUD OPI Criterion A Discrepancy', 'New PSUD OPI Symptom Count', 'PSUD OPI Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_opi_db['Count Discrepancy Direction'] = np.where(((psud_opi_full_db['scid_e311cnt'] - psud_opi_full_db['New PSUD OPI Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_opi_full_db['scid_e311cnt'] == psud_opi_full_db['New PSUD OPI Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_opi_db['Count Discrepancy Value'] = psud_opi_full_db['scid_e311cnt'] - psud_opi_full_db['New PSUD OPI Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_opi = refined_psud_opi_db.loc[((refined_psud_opi_db['PSUD OPI Symptom Count Discrepancy'] == "Problem") | (refined_psud_opi_db['PSUD OPI Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e311cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD OPI Criterion A Discrepancy** - The Criterion A item (scid_e311) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD OPI Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD OPI Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_opi = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_opi')
                    if interviewer_selection_psud_opi:
                        problem_children_psud_opi_final = only_problem_children_psud_opi[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e311', 'PSUD OPI Criterion A Discrepancy', 'scid_e311cnt', 'New PSUD OPI Symptom Count', 'PSUD OPI Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_opi_final)
                        csv = convert_df(problem_children_psud_opi_final)
                    else:
                        problem_children_psud_opi_final = only_problem_children_psud_opi[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e311', 'PSUD OPI Criterion A Discrepancy', 'scid_e311cnt', 'New PSUD OPI Symptom Count', 'PSUD OPI Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_opi_final)
                        csv = convert_df(problem_children_psud_opi_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_opi_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_opi_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_opi_final[problem_children_psud_opi_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_opi_final[problem_children_psud_opi_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_opi_problem_subject_list = problem_children_psud_opi_final.index.values.tolist()
                    see_more_psud_opi = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_opi_problem_subject_list)
                    interviewer_selection_psud_opi_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_opi')
                    if see_more_psud_opi is not None:
                        if interviewer_selection_psud_opi_2:
                            specific_psud_opi_subject_db = psud_opi_full_db.loc[see_more_psud_opi,:]
                            specific_psud_opi_subject_db_2 = specific_psud_opi_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e217a', 'scid_e217b', 'A2 Items', 'scid_e225a', 'scid_e225b',
                            'A3 Items', 'scid_e233', 'A4 Items', 'scid_e241', 'A5 Items', 'scid_e249a', 'scid_e249b', 'A6 Items', 'scid_e257', 'A7 Items', 'scid_e265', 'A8 Items', 'scid_e273', 
                            'A9 Items', 'scid_e281a', 'scid_e281b', 'A10 Items', 'scid_e289a', 'scid_e289b', 'A11 Items', 'scid_e297', 'scid_e311', 'scid_e311cnt', 'New PSUD OPI Symptom Count']]
                            specific_psud_opi_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_opi_subject_db_2)
                            csv = convert_df(specific_psud_opi_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_opi_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_opi_subject_db = psud_opi_full_db.loc[see_more_psud_opi,:]
                            specific_psud_opi_subject_db_2 = specific_psud_opi_subject_db.loc[:,['A1 Items', 'scid_e217a', 'scid_e217b', 'A2 Items', 'scid_e225a', 'scid_e225b',
                            'A3 Items', 'scid_e233', 'A4 Items', 'scid_e241', 'A5 Items', 'scid_e249a', 'scid_e249b', 'A6 Items', 'scid_e257', 'A7 Items', 'scid_e265', 'A8 Items', 'scid_e273', 
                            'A9 Items', 'scid_e281a', 'scid_e281b', 'A10 Items', 'scid_e289a', 'scid_e289b', 'A11 Items', 'scid_e297', 'scid_e311', 'scid_e311cnt', 'New PSUD OPI Symptom Count']]
                            specific_psud_opi_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_opi_subject_db_2)
                            csv = convert_df(specific_psud_opi_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_opi_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_psud == "Inhalants":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Inhalants # Just Checking Calculation errors
                    psud_inh_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e218a', 'scid_e218b', 'scid_e226a', 'scid_e226b', 'scid_e234', 'scid_e242', 'scid_e250a', 'scid_e250b', 'scid_e258', 'scid_e266',
                    'scid_e274', 'scid_e282a', 'scid_e282b', 'scid_e290a', 'scid_e290b', 'scid_e315', 'scid_e315cnt']]

                    # Setting index to subject_id
                    psud_inh_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_inh_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_inh_full_db['scid_e242'] = psud_inh_full_db['scid_e242'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_inh_full_db = psud_inh_full_db.astype({'scid_e218a':'int', 'scid_e218b':'int', 'scid_e226a':'int', 'scid_e226b':'int', 'scid_e234':'int', 'scid_e242':'int', 'scid_e250a':'int', 'scid_e250b':'int',
                    'scid_e258':'int', 'scid_e266':'int', 'scid_e274':'int', 'scid_e282a':'int', 'scid_e282b':'int', 'scid_e290a':'int', 'scid_e290b':'int', 'scid_e315':'int', 'scid_e315cnt':'int'})

                    # Counting PSUD INH symptoms # Max is 10
                    psud_inh_full_db['A1 Items'] = np.where(((psud_inh_full_db['scid_e218a'] == 3) | (psud_inh_full_db['scid_e218b'] == 3)), 1, 0)
                    psud_inh_full_db['A2 Items'] = np.where(((psud_inh_full_db['scid_e226a'] == 3) | (psud_inh_full_db['scid_e226b'] == 3)), 1, 0)
                    psud_inh_full_db['A3 Items'] = np.where(((psud_inh_full_db['scid_e234'] == 3)), 1, 0)
                    psud_inh_full_db['A4 Items'] = np.where(((psud_inh_full_db['scid_e242'] == 3)), 1, 0)
                    psud_inh_full_db['A5 Items'] = np.where(((psud_inh_full_db['scid_e250a'] == 3) | (psud_inh_full_db['scid_e250b'] == 3)), 1, 0)
                    psud_inh_full_db['A6 Items'] = np.where(((psud_inh_full_db['scid_e258'] == 3)), 1, 0)
                    psud_inh_full_db['A7 Items'] = np.where(((psud_inh_full_db['scid_e266'] == 3)), 1, 0)
                    psud_inh_full_db['A8 Items'] = np.where(((psud_inh_full_db['scid_e274'] == 3)), 1, 0)
                    psud_inh_full_db['A9 Items'] = np.where(((psud_inh_full_db['scid_e282a'] == 3) | (psud_inh_full_db['scid_e282b'] == 3)), 1, 0)
                    psud_inh_full_db['A10 Items'] = np.where(((psud_inh_full_db['scid_e290a'] == 3) | (psud_inh_full_db['scid_e290b'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_inh_full_db['PSUD INH Criterion A Discrepancy'] = np.where(((psud_inh_full_db['scid_e315cnt'] >= 2) & (psud_inh_full_db['scid_e315'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_inh_full_db['New PSUD INH Symptom Count'] = psud_inh_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items']].sum(axis = 1)
                    psud_inh_full_db['PSUD INH Symptom Count Discrepancy'] = np.where(((psud_inh_full_db['New PSUD INH Symptom Count'] != psud_inh_full_db['scid_e315cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_inh_db = psud_inh_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'scid_e315', 'scid_e315cnt', 'PSUD INH Criterion A Discrepancy', 'New PSUD INH Symptom Count', 'PSUD INH Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_inh_db['Count Discrepancy Direction'] = np.where(((psud_inh_full_db['scid_e315cnt'] - psud_inh_full_db['New PSUD INH Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_inh_full_db['scid_e315cnt'] == psud_inh_full_db['New PSUD INH Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_inh_db['Count Discrepancy Value'] = psud_inh_full_db['scid_e315cnt'] - psud_inh_full_db['New PSUD INH Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_inh = refined_psud_inh_db.loc[((refined_psud_inh_db['PSUD INH Symptom Count Discrepancy'] == "Problem") | (refined_psud_inh_db['PSUD INH Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e315cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD INH Criterion A Discrepancy** - The Criterion A item (scid_e315) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD INH Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD INH Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_inh = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_inh')
                    if interviewer_selection_psud_inh:
                        problem_children_psud_inh_final = only_problem_children_psud_inh[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e315', 'PSUD INH Criterion A Discrepancy', 'scid_e315cnt', 'New PSUD INH Symptom Count', 'PSUD INH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_inh_final)
                        csv = convert_df(problem_children_psud_inh_final)
                    else:
                        problem_children_psud_inh_final = only_problem_children_psud_inh[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e315', 'PSUD INH Criterion A Discrepancy', 'scid_e315cnt', 'New PSUD INH Symptom Count', 'PSUD INH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_inh_final)
                        csv = convert_df(problem_children_psud_inh_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_inh_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_inh_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_inh_final[problem_children_psud_inh_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_inh_final[problem_children_psud_inh_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_inh_problem_subject_list = problem_children_psud_inh_final.index.values.tolist()
                    see_more_psud_inh = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_inh_problem_subject_list)
                    interviewer_selection_psud_inh_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_inh')
                    if see_more_psud_inh is not None:
                        if interviewer_selection_psud_inh_2:
                            specific_psud_inh_subject_db = psud_inh_full_db.loc[see_more_psud_inh,:]
                            specific_psud_inh_subject_db_2 = specific_psud_inh_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e218a', 'scid_e218b', 'A2 Items', 'scid_e226a', 'scid_e226b',
                            'A3 Items', 'scid_e234', 'A4 Items', 'scid_e242', 'A5 Items', 'scid_e250a', 'scid_e250b', 'A6 Items', 'scid_e258', 'A7 Items', 'scid_e266', 'A8 Items', 'scid_e274', 
                            'A9 Items', 'scid_e282a', 'scid_e282b', 'A10 Items', 'scid_e290a', 'scid_e290b', 'scid_e315', 'scid_e315cnt', 'New PSUD INH Symptom Count']]
                            specific_psud_inh_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_inh_subject_db_2)
                            csv = convert_df(specific_psud_inh_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_inh_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_inh_subject_db = psud_inh_full_db.loc[see_more_psud_inh,:]
                            specific_psud_inh_subject_db_2 = specific_psud_inh_subject_db.loc[:,['A1 Items', 'scid_e218a', 'scid_e218b', 'A2 Items', 'scid_e226a', 'scid_e226b',
                            'A3 Items', 'scid_e234', 'A4 Items', 'scid_e242', 'A5 Items', 'scid_e250a', 'scid_e250b', 'A6 Items', 'scid_e258', 'A7 Items', 'scid_e266', 'A8 Items', 'scid_e274', 
                            'A9 Items', 'scid_e282a', 'scid_e282b', 'A10 Items', 'scid_e290a', 'scid_e290b', 'scid_e315', 'scid_e315cnt', 'New PSUD INH Symptom Count']]
                            specific_psud_inh_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_inh_subject_db_2)
                            csv = convert_df(specific_psud_inh_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_inh_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_psud == "PCP":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD PCP # Just Checking Calculation errors
                    psud_pcp_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e219a', 'scid_e219b', 'scid_e227a', 'scid_e227b', 'scid_e235', 'scid_e243', 'scid_e251a', 'scid_e251b', 'scid_e259', 'scid_e267',
                    'scid_e275', 'scid_e283a', 'scid_e283b', 'scid_e291a', 'scid_e291b', 'scid_e319', 'scid_e319cnt']]

                    # Setting index to subject_id
                    psud_pcp_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_pcp_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_pcp_full_db['scid_e243'] = psud_pcp_full_db['scid_e243'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_pcp_full_db = psud_pcp_full_db.astype({'scid_e219a':'int', 'scid_e219b':'int', 'scid_e227a':'int', 'scid_e227b':'int', 'scid_e235':'int', 'scid_e243':'int', 'scid_e251a':'int', 'scid_e251b':'int',
                    'scid_e259':'int', 'scid_e267':'int', 'scid_e275':'int', 'scid_e283a':'int', 'scid_e283b':'int', 'scid_e291a':'int', 'scid_e291b':'int', 'scid_e319':'int', 'scid_e319cnt':'int'})

                    # Counting PSUD PCP symptoms # Max is 10
                    psud_pcp_full_db['A1 Items'] = np.where(((psud_pcp_full_db['scid_e219a'] == 3) | (psud_pcp_full_db['scid_e219b'] == 3)), 1, 0)
                    psud_pcp_full_db['A2 Items'] = np.where(((psud_pcp_full_db['scid_e227a'] == 3) | (psud_pcp_full_db['scid_e227b'] == 3)), 1, 0)
                    psud_pcp_full_db['A3 Items'] = np.where(((psud_pcp_full_db['scid_e235'] == 3)), 1, 0)
                    psud_pcp_full_db['A4 Items'] = np.where(((psud_pcp_full_db['scid_e243'] == 3)), 1, 0)
                    psud_pcp_full_db['A5 Items'] = np.where(((psud_pcp_full_db['scid_e251a'] == 3) | (psud_pcp_full_db['scid_e251b'] == 3)), 1, 0)
                    psud_pcp_full_db['A6 Items'] = np.where(((psud_pcp_full_db['scid_e259'] == 3)), 1, 0)
                    psud_pcp_full_db['A7 Items'] = np.where(((psud_pcp_full_db['scid_e267'] == 3)), 1, 0)
                    psud_pcp_full_db['A8 Items'] = np.where(((psud_pcp_full_db['scid_e275'] == 3)), 1, 0)
                    psud_pcp_full_db['A9 Items'] = np.where(((psud_pcp_full_db['scid_e283a'] == 3) | (psud_pcp_full_db['scid_e283b'] == 3)), 1, 0)
                    psud_pcp_full_db['A10 Items'] = np.where(((psud_pcp_full_db['scid_e291a'] == 3) | (psud_pcp_full_db['scid_e291b'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_pcp_full_db['PSUD PCP Criterion A Discrepancy'] = np.where(((psud_pcp_full_db['scid_e319cnt'] >= 2) & (psud_pcp_full_db['scid_e319'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_pcp_full_db['New PSUD PCP Symptom Count'] = psud_pcp_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items']].sum(axis = 1)
                    psud_pcp_full_db['PSUD PCP Symptom Count Discrepancy'] = np.where(((psud_pcp_full_db['New PSUD PCP Symptom Count'] != psud_pcp_full_db['scid_e319cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_pcp_db = psud_pcp_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'scid_e319', 'scid_e319cnt', 'PSUD PCP Criterion A Discrepancy', 'New PSUD PCP Symptom Count', 'PSUD PCP Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_pcp_db['Count Discrepancy Direction'] = np.where(((psud_pcp_full_db['scid_e319cnt'] - psud_pcp_full_db['New PSUD PCP Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_pcp_full_db['scid_e319cnt'] == psud_pcp_full_db['New PSUD PCP Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_pcp_db['Count Discrepancy Value'] = psud_pcp_full_db['scid_e319cnt'] - psud_pcp_full_db['New PSUD PCP Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_pcp = refined_psud_pcp_db.loc[((refined_psud_pcp_db['PSUD PCP Symptom Count Discrepancy'] == "Problem") | (refined_psud_pcp_db['PSUD PCP Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e319cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD PCP Criterion A Discrepancy** - The Criterion A item (scid_e319) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD PCP Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD PCP Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_pcp = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_pcp')
                    if interviewer_selection_psud_pcp:
                        problem_children_psud_pcp_final = only_problem_children_psud_pcp[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e319', 'PSUD PCP Criterion A Discrepancy', 'scid_e319cnt', 'New PSUD PCP Symptom Count', 'PSUD PCP Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_pcp_final)
                        csv = convert_df(problem_children_psud_pcp_final)
                    else:
                        problem_children_psud_pcp_final = only_problem_children_psud_pcp[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e319', 'PSUD PCP Criterion A Discrepancy', 'scid_e319cnt', 'New PSUD PCP Symptom Count', 'PSUD PCP Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_pcp_final)
                        csv = convert_df(problem_children_psud_pcp_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_pcp_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_pcp_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_pcp_final[problem_children_psud_pcp_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_pcp_final[problem_children_psud_pcp_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_pcp_problem_subject_list = problem_children_psud_pcp_final.index.values.tolist()
                    see_more_psud_pcp = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_pcp_problem_subject_list)
                    interviewer_selection_psud_pcp_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_pcp')
                    if see_more_psud_pcp is not None:
                        if interviewer_selection_psud_pcp_2:
                            specific_psud_pcp_subject_db = psud_pcp_full_db.loc[see_more_psud_pcp,:]
                            specific_psud_pcp_subject_db_2 = specific_psud_pcp_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e219a', 'scid_e219b', 'A2 Items', 'scid_e227a', 'scid_e227b',
                            'A3 Items', 'scid_e235', 'A4 Items', 'scid_e243', 'A5 Items', 'scid_e251a', 'scid_e251b', 'A6 Items', 'scid_e259', 'A7 Items', 'scid_e267', 'A8 Items', 'scid_e275', 
                            'A9 Items', 'scid_e283a', 'scid_e283b', 'A10 Items', 'scid_e291a', 'scid_e291b', 'scid_e319', 'scid_e319cnt', 'New PSUD PCP Symptom Count']]
                            specific_psud_pcp_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_pcp_subject_db_2)
                            csv = convert_df(specific_psud_pcp_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_pcp_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_pcp_subject_db = psud_pcp_full_db.loc[see_more_psud_pcp,:]
                            specific_psud_pcp_subject_db_2 = specific_psud_pcp_subject_db.loc[:,['A1 Items', 'scid_e219a', 'scid_e219b', 'A2 Items', 'scid_e227a', 'scid_e227b',
                            'A3 Items', 'scid_e235', 'A4 Items', 'scid_e243', 'A5 Items', 'scid_e251a', 'scid_e251b', 'A6 Items', 'scid_e259', 'A7 Items', 'scid_e267', 'A8 Items', 'scid_e275', 
                            'A9 Items', 'scid_e283a', 'scid_e283b', 'A10 Items', 'scid_e291a', 'scid_e291b', 'scid_e319', 'scid_e319cnt', 'New PSUD PCP Symptom Count']]
                            specific_psud_pcp_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_pcp_subject_db_2)
                            csv = convert_df(specific_psud_pcp_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_pcp_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_psud == "Hallucinogens":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Hallucinogens # Just Checking Calculation errors
                    psud_hal_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e220a', 'scid_e220b', 'scid_e228a', 'scid_e228b', 'scid_e236', 'scid_e244', 'scid_e252a', 'scid_e252b', 'scid_e260', 'scid_e268',
                    'scid_e276', 'scid_e284a', 'scid_e284b', 'scid_e292a', 'scid_e292b', 'scid_e323', 'scid_e323cnt']]

                    # Setting index to subject_id
                    psud_hal_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_hal_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_hal_full_db['scid_e244'] = psud_hal_full_db['scid_e244'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_hal_full_db = psud_hal_full_db.astype({'scid_e220a':'int', 'scid_e220b':'int', 'scid_e228a':'int', 'scid_e228b':'int', 'scid_e236':'int', 'scid_e244':'int', 'scid_e252a':'int', 'scid_e252b':'int',
                    'scid_e260':'int', 'scid_e268':'int', 'scid_e276':'int', 'scid_e284a':'int', 'scid_e284b':'int', 'scid_e292a':'int', 'scid_e292b':'int', 'scid_e323':'int', 'scid_e323cnt':'int'})

                    # Counting PSUD HAL symptoms # Max is 10
                    psud_hal_full_db['A1 Items'] = np.where(((psud_hal_full_db['scid_e220a'] == 3) | (psud_hal_full_db['scid_e220b'] == 3)), 1, 0)
                    psud_hal_full_db['A2 Items'] = np.where(((psud_hal_full_db['scid_e228a'] == 3) | (psud_hal_full_db['scid_e228b'] == 3)), 1, 0)
                    psud_hal_full_db['A3 Items'] = np.where(((psud_hal_full_db['scid_e236'] == 3)), 1, 0)
                    psud_hal_full_db['A4 Items'] = np.where(((psud_hal_full_db['scid_e244'] == 3)), 1, 0)
                    psud_hal_full_db['A5 Items'] = np.where(((psud_hal_full_db['scid_e252a'] == 3) | (psud_hal_full_db['scid_e252b'] == 3)), 1, 0)
                    psud_hal_full_db['A6 Items'] = np.where(((psud_hal_full_db['scid_e260'] == 3)), 1, 0)
                    psud_hal_full_db['A7 Items'] = np.where(((psud_hal_full_db['scid_e268'] == 3)), 1, 0)
                    psud_hal_full_db['A8 Items'] = np.where(((psud_hal_full_db['scid_e276'] == 3)), 1, 0)
                    psud_hal_full_db['A9 Items'] = np.where(((psud_hal_full_db['scid_e284a'] == 3) | (psud_hal_full_db['scid_e284b'] == 3)), 1, 0)
                    psud_hal_full_db['A10 Items'] = np.where(((psud_hal_full_db['scid_e292a'] == 3) | (psud_hal_full_db['scid_e292b'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_hal_full_db['PSUD HAL Criterion A Discrepancy'] = np.where(((psud_hal_full_db['scid_e323cnt'] >= 2) & (psud_hal_full_db['scid_e323'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_hal_full_db['New PSUD HAL Symptom Count'] = psud_hal_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items']].sum(axis = 1)
                    psud_hal_full_db['PSUD HAL Symptom Count Discrepancy'] = np.where(((psud_hal_full_db['New PSUD HAL Symptom Count'] != psud_hal_full_db['scid_e323cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_hal_db = psud_hal_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'scid_e323', 'scid_e323cnt', 'PSUD HAL Criterion A Discrepancy', 'New PSUD HAL Symptom Count', 'PSUD HAL Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_hal_db['Count Discrepancy Direction'] = np.where(((psud_hal_full_db['scid_e323cnt'] - psud_hal_full_db['New PSUD HAL Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_hal_full_db['scid_e323cnt'] == psud_hal_full_db['New PSUD HAL Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_hal_db['Count Discrepancy Value'] = psud_hal_full_db['scid_e323cnt'] - psud_hal_full_db['New PSUD HAL Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_hal = refined_psud_hal_db.loc[((refined_psud_hal_db['PSUD HAL Symptom Count Discrepancy'] == "Problem") | (refined_psud_hal_db['PSUD HAL Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e323cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD HAL Criterion A Discrepancy** - The Criterion A item (scid_e323) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD HAL Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD HAL Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_hal = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_hal')
                    if interviewer_selection_psud_hal:
                        problem_children_psud_hal_final = only_problem_children_psud_hal[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e323', 'PSUD HAL Criterion A Discrepancy', 'scid_e323cnt', 'New PSUD HAL Symptom Count', 'PSUD HAL Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_hal_final)
                        csv = convert_df(problem_children_psud_hal_final)
                    else:
                        problem_children_psud_hal_final = only_problem_children_psud_hal[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'scid_e323', 'PSUD HAL Criterion A Discrepancy', 'scid_e323cnt', 'New PSUD HAL Symptom Count', 'PSUD HAL Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_hal_final)
                        csv = convert_df(problem_children_psud_hal_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_hal_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_hal_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_hal_final[problem_children_psud_hal_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_hal_final[problem_children_psud_hal_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_hal_problem_subject_list = problem_children_psud_hal_final.index.values.tolist()
                    see_more_psud_hal = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_hal_problem_subject_list)
                    interviewer_selection_psud_hal_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_hal')
                    if see_more_psud_hal is not None:
                        if interviewer_selection_psud_hal_2:
                            specific_psud_hal_subject_db = psud_hal_full_db.loc[see_more_psud_hal,:]
                            specific_psud_hal_subject_db_2 = specific_psud_hal_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e220a', 'scid_e220b', 'A2 Items', 'scid_e228a', 'scid_e228b',
                            'A3 Items', 'scid_e236', 'A4 Items', 'scid_e244', 'A5 Items', 'scid_e252a', 'scid_e252b', 'A6 Items', 'scid_e260', 'A7 Items', 'scid_e268', 'A8 Items', 'scid_e276', 
                            'A9 Items', 'scid_e284a', 'scid_e284b', 'A10 Items', 'scid_e292a', 'scid_e292b', 'scid_e323', 'scid_e323cnt', 'New PSUD HAL Symptom Count']]
                            specific_psud_hal_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_hal_subject_db_2)
                            csv = convert_df(specific_psud_hal_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_hal_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_hal_subject_db = psud_hal_full_db.loc[see_more_psud_hal,:]
                            specific_psud_hal_subject_db_2 = specific_psud_hal_subject_db.loc[:,['A1 Items', 'scid_e220a', 'scid_e220b', 'A2 Items', 'scid_e228a', 'scid_e228b',
                            'A3 Items', 'scid_e236', 'A4 Items', 'scid_e244', 'A5 Items', 'scid_e252a', 'scid_e252b', 'A6 Items', 'scid_e260', 'A7 Items', 'scid_e268', 'A8 Items', 'scid_e276', 
                            'A9 Items', 'scid_e284a', 'scid_e284b', 'A10 Items', 'scid_e292a', 'scid_e292b', 'scid_e323', 'scid_e323cnt', 'New PSUD HAL Symptom Count']]
                            specific_psud_hal_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_hal_subject_db_2)
                            csv = convert_df(specific_psud_hal_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_hal_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                if drug_selection_psud == "Other/Unknown":
                    st.markdown(f"#### {drug_selection_psud}")
                    st.markdown("---")

                    # Opening datafile
                    full_db = pd.read_csv(full_data)
                    module_e_items_db = pd.read_excel(module_e_file)
                    
                    # Selecting only module E items (including subject_id of course) [THIS IS ALL OF MODULE E]
                    module_e_item_list = module_e_items_db['module_e_items'].values.tolist()
                    final_list = ['subject_id', 'scid_interviewername'] + module_e_item_list

                    module_e_db = full_db.loc[:, final_list]

                    # PSUD Other/Unknown # Just Checking Calculation errors
                    psud_oth_full_db = module_e_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_e221a', 'scid_e221b', 'scid_e229a', 'scid_e229b', 'scid_e237', 'scid_e245', 'scid_e253a', 'scid_e253b', 'scid_e261', 'scid_e269',
                    'scid_e277', 'scid_e285a', 'scid_e285b', 'scid_e293a', 'scid_e293b', 'scid_e298', 'scid_e327', 'scid_e327cnt']]

                    # Setting index to subject_id
                    psud_oth_full_db.set_index('subject_id', inplace = True)

                    # Filling all na values with 0 in order to run comparisons
                    psud_oth_full_db.fillna(0, inplace = True)

                    # Have to convert 3u option in scid_e25 to just 3
                    psud_oth_full_db['scid_e245'] = psud_oth_full_db['scid_e245'].replace("3u", "3")

                    # Setting the scid variable to integers instead of floats as it's more legible
                    psud_oth_full_db = psud_oth_full_db.astype({'scid_e221a':'int', 'scid_e221b':'int', 'scid_e229a':'int', 'scid_e229b':'int', 'scid_e237':'int', 'scid_e245':'int', 'scid_e253a':'int', 'scid_e253b':'int',
                    'scid_e261':'int', 'scid_e269':'int', 'scid_e277':'int', 'scid_e285a':'int', 'scid_e285b':'int', 'scid_e293a':'int', 'scid_e293b':'int', 'scid_e327':'int', 'scid_e327cnt':'int'})

                    # Counting PSUD OTH symptoms # Max is 11
                    psud_oth_full_db['A1 Items'] = np.where(((psud_oth_full_db['scid_e221a'] == 3) | (psud_oth_full_db['scid_e221b'] == 3)), 1, 0)
                    psud_oth_full_db['A2 Items'] = np.where(((psud_oth_full_db['scid_e229a'] == 3) | (psud_oth_full_db['scid_e229b'] == 3)), 1, 0)
                    psud_oth_full_db['A3 Items'] = np.where(((psud_oth_full_db['scid_e237'] == 3)), 1, 0)
                    psud_oth_full_db['A4 Items'] = np.where(((psud_oth_full_db['scid_e245'] == 3)), 1, 0)
                    psud_oth_full_db['A5 Items'] = np.where(((psud_oth_full_db['scid_e253a'] == 3) | (psud_oth_full_db['scid_e253b'] == 3)), 1, 0)
                    psud_oth_full_db['A6 Items'] = np.where(((psud_oth_full_db['scid_e261'] == 3)), 1, 0)
                    psud_oth_full_db['A7 Items'] = np.where(((psud_oth_full_db['scid_e269'] == 3)), 1, 0)
                    psud_oth_full_db['A8 Items'] = np.where(((psud_oth_full_db['scid_e277'] == 3)), 1, 0)
                    psud_oth_full_db['A9 Items'] = np.where(((psud_oth_full_db['scid_e285a'] == 3) | (psud_oth_full_db['scid_e285b'] == 3)), 1, 0)
                    psud_oth_full_db['A10 Items'] = np.where(((psud_oth_full_db['scid_e293a'] == 3) | (psud_oth_full_db['scid_e293b'] == 3)), 1, 0)
                    psud_oth_full_db['A11 Items'] = np.where(((psud_oth_full_db['scid_e298'] == 3)), 1, 0)

                    # Checking Criterion A Discrepancy # Needs to have at least 2 # checking against original eInterview count
                    psud_oth_full_db['PSUD OTH Criterion A Discrepancy'] = np.where(((psud_oth_full_db['scid_e327cnt'] >= 2) & (psud_oth_full_db['scid_e327'] != 3)), "Problem", "Fine")

                    # Checking Count Discrepancy
                    psud_oth_full_db['New PSUD OTH Symptom Count'] = psud_oth_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'A10 Items', 'A11 Items']].sum(axis = 1)
                    psud_oth_full_db['PSUD OTH Symptom Count Discrepancy'] = np.where(((psud_oth_full_db['New PSUD OTH Symptom Count'] != psud_oth_full_db['scid_e327cnt'])), "Problem", "Fine")

                    # Getting the Count Items and the Dsicrepancy Items
                    refined_psud_oth_db = psud_oth_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items',
                    'A10 Items', 'A11 Items', 'scid_e327', 'scid_e327cnt', 'PSUD OTH Criterion A Discrepancy', 'New PSUD OTH Symptom Count', 'PSUD OTH Symptom Count Discrepancy']]

                    # Getting Count Discrepancy direction and Value
                    refined_psud_oth_db['Count Discrepancy Direction'] = np.where(((psud_oth_full_db['scid_e327cnt'] - psud_oth_full_db['New PSUD OTH Symptom Count']) > 0), "Original Count Larger", 
                    np.where(((psud_oth_full_db['scid_e327cnt'] == psud_oth_full_db['New PSUD OTH Symptom Count'])), "Same", "New Count Larger"))
                    refined_psud_oth_db['Count Discrepancy Value'] = psud_oth_full_db['scid_e327cnt'] - psud_oth_full_db['New PSUD OTH Symptom Count']

                    # Getting Only "Problem Subjects"
                    only_problem_children_psud_oth = refined_psud_oth_db.loc[((refined_psud_oth_db['PSUD OTH Symptom Count Discrepancy'] == "Problem") | (refined_psud_oth_db['PSUD OTH Criterion A Discrepancy'] == 'Problem'))]

                    col1, col2 = st.columns(2)
                    with col2:
                            st.write("**Export Breakdown**")
                            st.write("- In the SCID there is a Criterion A count item (scid_e327cnt) and the table below outlines where the count item does not match the actual symptom count.")
                    with col1:
                        st.write("**Column Definitions:**")
                        st.markdown("- **PSUD OTH Criterion A Discrepancy** - The Criterion A item (scid_e327) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                        st.markdown("- **New PSUD OTH Symptom Count** - My new symptom count using the Ax Item columns.")
                        st.markdown("- **PSUD OTH Symptom Count Discrepancy** - Checks whether the the scid criterion A count matches my manual count.")

                    # Creating the framework to be able to see the corresponding interviewers
                    interviewer_selection_psud_oth = st.checkbox("Would you like to see the associated interviewer?", key = 'psud_oth')
                    if interviewer_selection_psud_oth:
                        problem_children_psud_oth_final = only_problem_children_psud_oth[['scid_interviewername','A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items' 'scid_e327', 'PSUD OTH Criterion A Discrepancy', 'scid_e327cnt', 'New PSUD OTH Symptom Count', 'PSUD OTH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_oth_final)
                        csv = convert_df(problem_children_psud_oth_final)
                    else:
                        problem_children_psud_oth_final = only_problem_children_psud_oth[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 
                        'A10 Items', 'A11 Items', 'scid_e327', 'PSUD OTH Criterion A Discrepancy', 'scid_e327cnt', 'New PSUD OTH Symptom Count', 'PSUD OTH Symptom Count Discrepancy', 'Count Discrepancy Direction', 
                        'Count Discrepancy Value']]
                        st.write(problem_children_psud_oth_final)
                        csv = convert_df(problem_children_psud_oth_final)
                    
                    column1, column2 = st.columns(2)
                    with column1:
                        st.write("Number of Problem Subjects:", len(problem_children_psud_oth_final.index))
                        st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'psud_oth_problem_subjects_export_{today}.csv', mime = 'text/csv')
                    with column2:
                        st.write("Number of Subjects with **New Count Larger**:", len(problem_children_psud_oth_final[problem_children_psud_oth_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                        st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_psud_oth_final[problem_children_psud_oth_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                    psud_oth_problem_subject_list = problem_children_psud_oth_final.index.values.tolist()
                    see_more_psud_oth = st.multiselect("See Specific Subject Info? [Select as many as you would like]", psud_oth_problem_subject_list)
                    interviewer_selection_psud_oth_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_psud_oth')
                    if see_more_psud_oth is not None:
                        if interviewer_selection_psud_oth_2:
                            specific_psud_oth_subject_db = psud_oth_full_db.loc[see_more_psud_oth,:]
                            specific_psud_oth_subject_db_2 = specific_psud_oth_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_e221a', 'scid_e221b', 'A2 Items', 'scid_e229a', 'scid_e229b',
                            'A3 Items', 'scid_e237', 'A4 Items', 'scid_e245', 'A5 Items', 'scid_e253a', 'scid_e253b', 'A6 Items', 'scid_e261', 'A7 Items', 'scid_e269', 'A8 Items', 'scid_e277', 
                            'A9 Items', 'scid_e285a', 'scid_e285b', 'A10 Items', 'scid_e293a', 'scid_e293b', 'A11 Items', 'scid_e298', 'scid_e327', 'scid_e327cnt', 'New PSUD OTH Symptom Count']]
                            specific_psud_oth_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_oth_subject_db_2)
                            csv = convert_df(specific_psud_oth_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_oth_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                        else:
                            specific_psud_oth_subject_db = psud_oth_full_db.loc[see_more_psud_oth,:]
                            specific_psud_oth_subject_db_2 = specific_psud_oth_subject_db.loc[:,['A1 Items', 'scid_e221a', 'scid_e221b', 'A2 Items', 'scid_e229a', 'scid_e229b',
                            'A3 Items', 'scid_e237', 'A4 Items', 'scid_e245', 'A5 Items', 'scid_e253a', 'scid_e253b', 'A6 Items', 'scid_e261', 'A7 Items', 'scid_e269', 'A8 Items', 'scid_e277', 
                            'A9 Items', 'scid_e285a', 'scid_e285b', 'A10 Items', 'scid_e293a', 'scid_e293b', 'A11 Items', 'scid_e298', 'scid_e327', 'scid_e327cnt', 'New PSUD OTH Symptom Count']]
                            specific_psud_oth_subject_db_2.sort_values('subject_id', inplace=True)
                            st.write(specific_psud_oth_subject_db_2)
                            csv = convert_df(specific_psud_oth_subject_db_2)
                            st.download_button("Download Data as a CSV", data = csv, file_name=f'psud_oth_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
        if module_selection == "Module F":
            module_f_syndrome_selection = st.sidebar.selectbox("Which disorder would you like to look at?", ["---", "Panic Attack", "Agoraphobia", "CGAD", "PGAD"])
            st.markdown(f"## {module_selection}")
            st.markdown("---")
            if module_f_syndrome_selection == "---":
                st.markdown("### Options:")
                st.markdown("- **'Panic Attack'**")
                st.markdown("- **'Agoraphobia'**")
                st.markdown("- **'CGAD'** - Current Generalized Anxiety Disorder")
                st.markdown("- **'PGAD'** - Past Generalized Anxiety Disorder")
            if module_f_syndrome_selection == "Panic Attack":
                st.markdown(f"#### {module_f_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_f_items_db = pd.read_excel(module_f_file)
                
                # Selecting only module F items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE F]
                module_f_item_list = module_f_items_db['module_f_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_f_item_list

                module_f_db = full_db.loc[:, final_list]

                # Panic Attack # Just Checking Calculation errors
                pa_full_db = module_f_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_f2', 'scid_f3', 'scid_f4', 'scid_f5', 'scid_f6', 'scid_f7', 'scid_f8', 'scid_f9', 'scid_f10',
                'scid_f11', 'scid_f12', 'scid_f13a', 'scid_f13b', 'scid_f14', 'scid_f15', 'scid_f16', 'scid_f16cnt']]

                # Setting index to subject_id
                pa_full_db.set_index("subject_id", inplace = True)

                # Filling all na values with 0 in order to run comparisons
                pa_full_db.fillna(0, inplace = True)

                # Setting the SCID variable to integers instead of floats as it's more readable
                pa_full_db = pa_full_db.astype({'scid_f2':'int', 'scid_f3':'int', 'scid_f4':'int', 'scid_f5':'int', 'scid_f6':'int', 'scid_f7':'int', 'scid_f8':'int', 'scid_f9':'int', 'scid_f10':'int',
                'scid_f11':'int', 'scid_f12':'int', 'scid_f13a':'int', 'scid_f13b':'int', 'scid_f14':'int', 'scid_f15':'int', 'scid_f16':'int', 'scid_f16cnt':'int'})

                # Counting Panic Attack Symptoms # Max is 13 (Not counting sudden symptoms)
                pa_full_db['Sudden Symptoms'] = np.where(((pa_full_db['scid_f2'] == 3)), 1, 0)
                pa_full_db['Palpitations'] = np.where(((pa_full_db['scid_f3'] == 3)), 1, 0)
                pa_full_db['Sweating'] = np.where(((pa_full_db['scid_f4'] == 3)), 1 ,0)
                pa_full_db['Trembling'] = np.where(((pa_full_db['scid_f5'] == 3)), 1, 0)
                pa_full_db['Shortness of Breath'] = np.where(((pa_full_db['scid_f6'] == 3)), 1 ,0)
                pa_full_db['Choking'] = np.where(((pa_full_db['scid_f7'] == 3)), 1, 0)
                pa_full_db['Chest Pain'] = np.where(((pa_full_db['scid_f8'] == 3)), 1, 0)
                pa_full_db['Nausea'] = np.where(((pa_full_db['scid_f9'] == 3)), 1, 0)
                pa_full_db['Dizzy'] = np.where(((pa_full_db['scid_f10'] == 3)), 1, 0)
                pa_full_db['Flushes or Chills'] = np.where(((pa_full_db['scid_f11'] == 3)), 1, 0)
                pa_full_db['Paresthesias'] = np.where(((pa_full_db['scid_f12'] == 3)), 1 , 0)
                pa_full_db['Depersonalization/Derealization'] = np.where(((pa_full_db['scid_f13a'] == 3) | (pa_full_db['scid_f13b'] == 3)), 1, 0)
                pa_full_db['Fear of Losing Control'] = np.where(((pa_full_db['scid_f14'] == 3)), 1, 0)
                pa_full_db['Fear of Dying'] = np.where(((pa_full_db['scid_f15'] == 3)), 1, 0)

                # Checking the Panic Attack Criteria Discrepancy # Need to have 4 or more symptoms with one of them being sudden symptoms (scid_f2) # Checking against original eInterview Count
                pa_full_db['PA Criteria Discrepancy'] = np.where((((pa_full_db['scid_f16cnt'] >= 4) & (pa_full_db['scid_f2'] == 3) & (pa_full_db['scid_f16'] != 3)) |
                ((pa_full_db['scid_f16cnt'] < 4) & (pa_full_db['scid_f2'] == 3) & (pa_full_db['scid_f16'] == 3)) | ((pa_full_db['scid_f16cnt'] < 4) & (pa_full_db['scid_f2'] != 3) & (pa_full_db['scid_f16'] == 3)) |
                ((pa_full_db['scid_f16cnt'] >= 4) & (pa_full_db['scid_f2'] != 3) & (pa_full_db['scid_f16'] == 3))), "Problem", "Fine")

                # Checking Count Discrepancy
                pa_full_db['New PA Symptom Count'] = pa_full_db.loc[:, ['Palpitations', 'Sweating', 'Trembling', 'Shortness of Breath', 'Choking', 'Chest Pain', 'Nausea', 'Dizzy', 'Flushes or Chills',
                'Paresthesias', 'Depersonalization/Derealization', 'Fear of Losing Control', 'Fear of Dying']].sum(axis = 1)
                pa_full_db['PA Symptom Count Discrepancy'] = np.where(((pa_full_db['scid_f16cnt'] != pa_full_db['New PA Symptom Count'])), "Problem", "Fine")

                # Getting the Count Items and the Discrepancy Values
                refined_pa_db = pa_full_db.loc[:, ['scid_interviewername', 'Sudden Symptoms', 'Palpitations', 'Sweating', 'Trembling', 'Shortness of Breath', 'Choking', 'Chest Pain', 'Nausea', 
                'Dizzy', 'Flushes or Chills', 'Paresthesias', 'Depersonalization/Derealization', 'Fear of Losing Control', 'Fear of Dying', 'scid_f16', 'scid_f16cnt', 'PA Criteria Discrepancy',
                'New PA Symptom Count', 'PA Symptom Count Discrepancy']]

                # Getting Count Discrepancy and Value
                refined_pa_db['Count Discrepancy Direction'] = np.where(((refined_pa_db['scid_f16cnt'] - refined_pa_db['New PA Symptom Count']) > 0), "Original Count Larger", 
                np.where(((refined_pa_db['scid_f16cnt'] == refined_pa_db['New PA Symptom Count'])), "Same", "New Count Larger"))
                refined_pa_db['Count Discrepancy Value'] = refined_pa_db['scid_f16cnt'] - refined_pa_db['New PA Symptom Count']

                # Getting only "Problem Subjects"
                only_problem_children_pa = refined_pa_db.loc[((refined_pa_db['PA Criteria Discrepancy'] == "Problem") | (refined_pa_db['PA Symptom Count Discrepancy'] == "Problem"))]

                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Panic Attack item (scid_f16cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PA Criteria Discrepancy** - The Panic Attack item (scid_f16) should only be marked 3 (threshold) if 4 or more symptoms are accounted for and the sudden symptoms item (scid_f2) is threshold (3). This column checks to see if that is the case.")
                    st.markdown("- **New PA Symptom Count** - My new symptom count using the Panic attack Item columns.")
                    st.markdown("- **PA Symptom Count Discrepancy** - Checks whether the the scid Panic Attack Symptom count matches my manual count.")

                # Creating the framework to be able to see the corresponding interviewers
                interviewer_selection_pa = st.checkbox("Would you like to see the associated interviewer?", key = 'pa')
                if interviewer_selection_pa:
                    problem_children_pa_final = only_problem_children_pa[['scid_interviewername', 'Sudden Symptoms', 'Palpitations', 'Sweating', 'Trembling', 'Shortness of Breath', 'Choking', 
                    'Chest Pain', 'Nausea', 'Dizzy', 'Flushes or Chills', 'Paresthesias', 'Depersonalization/Derealization', 'Fear of Losing Control', 'Fear of Dying', 'scid_f16', 
                    'PA Criteria Discrepancy', 'scid_f16cnt', 'New PA Symptom Count', 'PA Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_pa_final)
                    csv = convert_df(problem_children_pa_final)
                else:
                    problem_children_pa_final = only_problem_children_pa[['Sudden Symptoms', 'Palpitations', 'Sweating', 'Trembling', 'Shortness of Breath', 'Choking', 
                    'Chest Pain', 'Nausea', 'Dizzy', 'Flushes or Chills', 'Paresthesias', 'Depersonalization/Derealization', 'Fear of Losing Control', 'Fear of Dying', 'scid_f16', 
                    'PA Criteria Discrepancy', 'scid_f16cnt', 'New PA Symptom Count', 'PA Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    st.write(problem_children_pa_final)
                    csv = convert_df(problem_children_pa_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_pa_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'pa_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_pa_final[problem_children_pa_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_pa_final[problem_children_pa_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pa_problem_subject_list = problem_children_pa_final.index.values.tolist()
                see_more_pa = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pa_problem_subject_list)
                interviewer_selection_pa_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_pa')
                if see_more_pa is not None:
                    if interviewer_selection_pa_2:
                        specific_pa_subject_db = pa_full_db.loc[see_more_pa,:]
                        specific_pa_subject_db_2 = specific_pa_subject_db.loc[:,['scid_interviewername','Sudden Symptoms', 'scid_f2', 'Palpitations', 'scid_f3',
                        'Sweating', 'scid_f4', 'Trembling', 'scid_f5', 'Shortness of Breath', 'scid_f6', 'Choking', 'scid_f7', 'Chest Pain', 'scid_f8', 'Nausea', 'scid_f9', 
                        'Dizzy', 'scid_f10', 'Flushes or Chills', 'scid_f11', 'Paresthesias', 'scid_f12', 'Depersonalization/Derealization', 'scid_f13a', 'scid_f13b',
                        'Fear of Losing Control', 'scid_f14', 'Fear of Dying', 'scid_f15', 'scid_f16', 'scid_f16cnt', 'New PA Symptom Count']]
                        specific_pa_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pa_subject_db_2)
                        csv = convert_df(specific_pa_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pa_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_pa_subject_db = pa_full_db.loc[see_more_pa,:]
                        specific_pa_subject_db_2 = specific_pa_subject_db.loc[:,['Sudden Symptoms', 'scid_f2', 'Palpitations', 'scid_f3',
                        'Sweating', 'scid_f4', 'Trembling', 'scid_f5', 'Shortness of Breath', 'scid_f6', 'Choking', 'scid_f7', 'Chest Pain', 'scid_f8', 'Nausea', 'scid_f9', 
                        'Dizzy', 'scid_f10', 'Flushes or Chills', 'scid_f11', 'Paresthesias', 'scid_f12', 'Depersonalization/Derealization', 'scid_f13a', 'scid_f13b',
                        'Fear of Losing Control', 'scid_f14', 'Fear of Dying', 'scid_f15', 'scid_f16', 'scid_f16cnt', 'New PA Symptom Count']]
                        specific_pa_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pa_subject_db_2)
                        csv = convert_df(specific_pa_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pa_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_f_syndrome_selection == "Agoraphobia":
                st.markdown(f"#### {module_f_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_f_items_db = pd.read_excel(module_f_file)
                
                # Selecting only module F items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE F]
                module_f_item_list = module_f_items_db['module_f_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_f_item_list

                module_f_db = full_db.loc[:, final_list]

                # Agoraphobia # Just Checking Calculation errors
                agora_full_db = module_f_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_f44', 'scid_f45', 'scid_f46', 'scid_f47', 'scid_f48', 'scid_f49', 'scid_f49cnt']]

                # Setting index to subject_id
                agora_full_db.set_index("subject_id", inplace = True)

                # Filling all na values with 0 in order to run comparisons
                agora_full_db.fillna(0, inplace = True)

                # Setting the SCID variable to integers instead of floats as it's more readable
                agora_full_db = agora_full_db.astype({'scid_f44':'int', 'scid_f45':'int', 'scid_f46':'int', 'scid_f47':'int', 'scid_f48':'int', 'scid_f49':'int', 'scid_f49cnt':'int'})

                # Counting Agoraphobia Criterion A # Max is 5
                agora_full_db['A1 Items'] = np.where(((agora_full_db['scid_f44'] == 3)), 1, 0)
                agora_full_db['A2 Items'] = np.where(((agora_full_db['scid_f45'] == 3)), 1, 0)
                agora_full_db['A3 Items'] = np.where(((agora_full_db['scid_f46'] == 3)), 1 ,0)
                agora_full_db['A4 Items'] = np.where(((agora_full_db['scid_f47'] == 3)), 1, 0)
                agora_full_db['A5 Items'] = np.where(((agora_full_db['scid_f48'] == 3)), 1 ,0)

                # Checking the Agoraphobia Criterion A Discrepancy # Need to have 2 or more symptoms) # Checking against original eInterview Count
                agora_full_db['AGORA Criterion A Discrepancy'] = np.where((((agora_full_db['scid_f49cnt'] >= 2) & (agora_full_db['scid_f49'] != 3)) |
                ((agora_full_db['scid_f49cnt'] < 2) & (agora_full_db['scid_f49'] == 3))), "Problem", "Fine")

                # Checking Count Discrepancy
                agora_full_db['New AGORA Symptom Count'] = agora_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items']].sum(axis = 1)
                agora_full_db['AGORA Symptom Count Discrepancy'] = np.where(((agora_full_db['scid_f49cnt'] != agora_full_db['New AGORA Symptom Count'])), "Problem", "Fine")

                # Getting the Count Items and the Discrepancy Values
                refined_agora_db = agora_full_db.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'scid_f49', 'scid_f49cnt', 'AGORA Criterion A Discrepancy',
                'New AGORA Symptom Count', 'AGORA Symptom Count Discrepancy']]

                # Getting Count Discrepancy and Value
                refined_agora_db['Count Discrepancy Direction'] = np.where(((refined_agora_db['scid_f49cnt'] - refined_agora_db['New AGORA Symptom Count']) > 0), "Original Count Larger", 
                np.where(((refined_agora_db['scid_f49cnt'] == refined_agora_db['New AGORA Symptom Count'])), "Same", "New Count Larger"))
                refined_agora_db['Count Discrepancy Value'] = refined_agora_db['scid_f49cnt'] - refined_agora_db['New AGORA Symptom Count']

                # Getting only "Problem Subjects"
                only_problem_children_agora = refined_agora_db.loc[((refined_agora_db['AGORA Criterion A Discrepancy'] == "Problem") | (refined_agora_db['AGORA Symptom Count Discrepancy'] == "Problem"))]
                
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criteria A item (scid_f49cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **AGORA Criterion A Discrepancy** - The Criterion A item (sciaxd_f49) should only be marked 3 (threshold) if 2 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New AGORA Symptom Count** - My new symptom count using the Panic attack Item columns.")
                    st.markdown("- **AGORA Symptom Count Discrepancy** - Checks whether the the scid Criterion A count matches my manual count.")

                # Creating the framework to be able to see the corresponding interviewers
                interviewer_selection_agora = st.checkbox("Would you like to see the associated interviewer?", key = 'agora')
                if interviewer_selection_agora:
                    problem_children_agora_final = only_problem_children_agora.loc[:, ['scid_interviewername', 'A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'scid_f49', 
                    'AGORA Criterion A Discrepancy', 'scid_f49cnt', 'New AGORA Symptom Count', 'AGORA Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_agora_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_agora_final)
                    csv = convert_df(problem_children_agora_final)
                else:
                    problem_children_agora_final = only_problem_children_agora.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'scid_f49', 'AGORA Criterion A Discrepancy',
                    'scid_f49cnt', 'New AGORA Symptom Count', 'AGORA Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_agora_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_agora_final)
                    csv = convert_df(problem_children_agora_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_agora_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'agora_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_agora_final[problem_children_agora_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_agora_final[problem_children_agora_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pa_problem_subject_list = problem_children_agora_final.index.values.tolist()
                see_more_agora = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pa_problem_subject_list)
                interviewer_selection_agora_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_agora')
                if see_more_agora is not None:
                    if interviewer_selection_agora_2:
                        specific_agora_subject_db = agora_full_db.loc[see_more_agora,:]
                        specific_agora_subject_db_2 = specific_agora_subject_db.loc[:,['scid_interviewername','A1 Items', 'scid_f44', 'A2 Items', 'scid_f45',
                        'A3 Items', 'scid_f46', 'A4 Items', 'scid_f47', 'A5 Items', 'scid_f48', 'scid_f49', 'scid_f49cnt', 'New AGORA Symptom Count']]
                        specific_agora_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_agora_subject_db_2)
                        csv = convert_df(specific_agora_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'agora_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_agora_subject_db = agora_full_db.loc[see_more_agora,:]
                        specific_agora_subject_db_2 = specific_agora_subject_db.loc[:,['A1 Items', 'scid_f44', 'A2 Items', 'scid_f45',
                        'A3 Items', 'scid_f46', 'A4 Items', 'scid_f47', 'A5 Items', 'scid_f48', 'scid_f49', 'scid_f49cnt', 'New AGORA Symptom Count']]
                        specific_agora_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_agora_subject_db_2)
                        csv = convert_df(specific_agora_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'agora_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_f_syndrome_selection == "CGAD":
                st.markdown(f"#### {module_f_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_f_items_db = pd.read_excel(module_f_file)
                
                # Selecting only module F items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE F]
                module_f_item_list = module_f_items_db['module_f_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_f_item_list

                module_f_db = full_db.loc[:, final_list]

                # CGAD # Just Checking Calculation errors
                cgad_full_db = module_f_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_f114', 'scid_f115', 'scid_f116', 'scid_f117', 'scid_f118', 'scid_f119', 'scid_f120', 'scid_f120cnt', 'scid_f120s']]

                # Setting index to subject_id
                cgad_full_db.set_index("subject_id", inplace = True)

                # Filling all na values with 0 in order to run comparisons
                cgad_full_db.fillna(0, inplace = True)

                # Setting the SCID variable to integers instead of floats as it's more readable
                cgad_full_db = cgad_full_db.astype({'scid_f114':'int', 'scid_f115':'int', 'scid_f116':'int', 'scid_f117':'int', 'scid_f118':'int', 'scid_f119':'int', 'scid_f120':'int',
                'scid_f120cnt':'int', 'scid_f120s':'int'})

                # Counting CGAD Criterion C # Max is 6
                cgad_full_db['C1 Items'] = np.where(((cgad_full_db['scid_f114'] == 3)), 1, 0)
                cgad_full_db['C2 Items'] = np.where(((cgad_full_db['scid_f115'] == 3)), 1, 0)
                cgad_full_db['C3 Items'] = np.where(((cgad_full_db['scid_f116'] == 3)), 1 ,0)
                cgad_full_db['C4 Items'] = np.where(((cgad_full_db['scid_f117'] == 3)), 1, 0)
                cgad_full_db['C5 Items'] = np.where(((cgad_full_db['scid_f118'] == 3)), 1 ,0)
                cgad_full_db['C6 Items'] = np.where(((cgad_full_db['scid_f119'] == 3)), 1 ,0)

                # Checking the CGAD Criterion C Discrepancy # Need to have 3 or more symptoms # Checking against original eInterview Count
                cgad_full_db['CGAD Criterion C Discrepancy'] = np.where(((cgad_full_db['scid_f120cnt'] >= 3) & (cgad_full_db['scid_f120'] != 3) & (cgad_full_db['scid_f120s'] == 4)), "Problem",
                np.where(((cgad_full_db['scid_f120'] == 3) & (cgad_full_db['scid_f120cnt'] < 3)), "Problem", "Fine"))

                # Checking Count Discrepancy
                cgad_full_db['New CGAD Symptom Count'] = cgad_full_db.loc[:, ['C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items']].sum(axis = 1)
                cgad_full_db['CGAD Symptom Count Discrepancy'] = np.where(((cgad_full_db['scid_f120cnt'] != cgad_full_db['New CGAD Symptom Count'])), "Problem", "Fine")

                # Getting the Count Items and the Discrepancy Values
                refined_cgad_db = cgad_full_db.loc[:, ['scid_interviewername', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'scid_f120', 'scid_f120cnt', 'scid_f120s',
                'CGAD Criterion C Discrepancy', 'New CGAD Symptom Count', 'CGAD Symptom Count Discrepancy']]

                # Getting Count Discrepancy and Value
                refined_cgad_db['Count Discrepancy Direction'] = np.where(((refined_cgad_db['scid_f120cnt'] - refined_cgad_db['New CGAD Symptom Count']) > 0), "Original Count Larger", 
                np.where(((refined_cgad_db['scid_f120cnt'] == refined_cgad_db['New CGAD Symptom Count'])), "Same", "New Count Larger"))
                refined_cgad_db['Count Discrepancy Value'] = refined_cgad_db['scid_f120cnt'] - refined_cgad_db['New CGAD Symptom Count']

                # Getting only "Problem Subjects"
                only_problem_children_cgad = refined_cgad_db.loc[((refined_cgad_db['CGAD Criterion C Discrepancy'] == "Problem") | (refined_cgad_db['CGAD Symptom Count Discrepancy'] == "Problem"))]

                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criteria C item (scid_f120cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CGAD Criterion C Discrepancy** - The Criterion C item (scid_f120) should only be marked 3 (threshold) if 3 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New CGAD Symptom Count** - My new symptom count using the Cx Item columns.")
                    st.markdown("- **CGAD Symptom Count Discrepancy** - Checks whether the the scid Criterion C count matches my manual count.")

                # Creating the framework to be able to see the corresponding interviewers
                interviewer_selection_cgad = st.checkbox("Would you like to see the associated interviewer?", key = 'cgad')
                if interviewer_selection_cgad:
                    problem_children_cgad_final = only_problem_children_cgad[['scid_interviewername', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'scid_f120', 'scid_f120s',
                    'CGAD Criterion C Discrepancy', 'scid_f120cnt', 'New CGAD Symptom Count', 'CGAD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_cgad_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_cgad_final)
                    csv = convert_df(problem_children_cgad_final)
                else:
                    problem_children_cgad_final = only_problem_children_cgad[['C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'scid_f120', 'scid_f120s',
                    'CGAD Criterion C Discrepancy', 'scid_f120cnt', 'New CGAD Symptom Count', 'CGAD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_cgad_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_cgad_final)
                    csv = convert_df(problem_children_cgad_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_cgad_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'cgad_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_cgad_final[problem_children_cgad_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_cgad_final[problem_children_cgad_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pa_problem_subject_list = problem_children_cgad_final.index.values.tolist()
                see_more_cgad = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pa_problem_subject_list)
                interviewer_selection_cgad_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_cgad')
                if see_more_cgad is not None:
                    if interviewer_selection_cgad_2:
                        specific_cgad_subject_db = cgad_full_db.loc[see_more_cgad,:]
                        specific_cgad_subject_db_2 = specific_cgad_subject_db.loc[:,['scid_interviewername','C1 Items', 'scid_f114', 'C2 Items', 'scid_f115', 'C3 Items', 'scid_f116', 'C4 Items', 
                        'scid_f117', 'C5 Items', 'scid_f118', 'C6 Items', 'scid_f119', 'scid_f120', 'scid_f120s', 'scid_f120cnt', 'New CGAD Symptom Count']]
                        specific_cgad_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cgad_subject_db_2)
                        csv = convert_df(specific_cgad_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cgad_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_cgad_subject_db = cgad_full_db.loc[see_more_cgad,:]
                        specific_cgad_subject_db_2 = specific_cgad_subject_db.loc[:,['C1 Items', 'scid_f114', 'C2 Items', 'scid_f115', 'C3 Items', 'scid_f116', 'C4 Items', 'scid_f117', 
                        'C5 Items', 'scid_f118', 'C6 Items', 'scid_f119', 'scid_f120', 'scid_f120s', 'scid_f120cnt', 'New CGAD Symptom Count']]
                        specific_cgad_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_cgad_subject_db_2)
                        csv = convert_df(specific_cgad_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'cgad_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_f_syndrome_selection == "PGAD":
                st.markdown(f"#### {module_f_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_f_items_db = pd.read_excel(module_f_file)
                
                # Selecting only module F items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE F]
                module_f_item_list = module_f_items_db['module_f_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_f_item_list

                module_f_db = full_db.loc[:, final_list]

                # PGAD # Just Checking Calculation errors
                pgad_full_db = module_f_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_f130', 'scid_f131', 'scid_f132', 'scid_f133', 'scid_f134', 'scid_f135', 'scid_f136', 'scid_f136cnt', 'scid_f136s']]

                # Setting index to subject_id
                pgad_full_db.set_index("subject_id", inplace = True)

                # Filling all na values with 0 in order to run comparisons
                pgad_full_db.fillna(0, inplace = True)

                # Setting the SCID variable to integers instead of floats as it's more readable
                pgad_full_db = pgad_full_db.astype({'scid_f130':'int', 'scid_f131':'int', 'scid_f132':'int', 'scid_f133':'int', 'scid_f134':'int', 'scid_f135':'int', 'scid_f136':'int',
                'scid_f136cnt':'int', 'scid_f136s':'int'})

                # Counting PGAD Criterion C # Max is 6
                pgad_full_db['C1 Items'] = np.where(((pgad_full_db['scid_f130'] == 3)), 1, 0)
                pgad_full_db['C2 Items'] = np.where(((pgad_full_db['scid_f131'] == 3)), 1, 0)
                pgad_full_db['C3 Items'] = np.where(((pgad_full_db['scid_f132'] == 3)), 1 ,0)
                pgad_full_db['C4 Items'] = np.where(((pgad_full_db['scid_f133'] == 3)), 1, 0)
                pgad_full_db['C5 Items'] = np.where(((pgad_full_db['scid_f134'] == 3)), 1 ,0)
                pgad_full_db['C6 Items'] = np.where(((pgad_full_db['scid_f135'] == 3)), 1 ,0)

                # Checking the PGAD Criterion C Discrepancy # Need to have 3 or more symptoms # Checking against original eInterview Count
                pgad_full_db['PGAD Criterion C Discrepancy'] = np.where(((pgad_full_db['scid_f136cnt'] >= 3) & (pgad_full_db['scid_f136'] != 3) & (pgad_full_db['scid_f136s'] == 4)), "Problem",
                np.where(((pgad_full_db['scid_f136'] == 3) & (pgad_full_db['scid_f136cnt'] < 3)), "Problem", "Fine"))

                # Checking Count Discrepancy
                pgad_full_db['New PGAD Symptom Count'] = pgad_full_db.loc[:, ['C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items']].sum(axis = 1)
                pgad_full_db['PGAD Symptom Count Discrepancy'] = np.where(((pgad_full_db['scid_f136cnt'] != pgad_full_db['New PGAD Symptom Count'])), "Problem", "Fine")

                # Getting the Count Items and the Discrepancy Values
                refined_pgad_db = pgad_full_db.loc[:, ['scid_interviewername', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'scid_f136', 'scid_f136cnt', 'scid_f136s',
                'PGAD Criterion C Discrepancy', 'New PGAD Symptom Count', 'PGAD Symptom Count Discrepancy']]

                # Getting Count Discrepancy and Value
                refined_pgad_db['Count Discrepancy Direction'] = np.where(((refined_pgad_db['scid_f136cnt'] - refined_pgad_db['New PGAD Symptom Count']) > 0), "Original Count Larger", 
                np.where(((refined_pgad_db['scid_f136cnt'] == refined_pgad_db['New PGAD Symptom Count'])), "Same", "New Count Larger"))
                refined_pgad_db['Count Discrepancy Value'] = refined_pgad_db['scid_f136cnt'] - refined_pgad_db['New PGAD Symptom Count']

                # Getting only "Problem Subjects"
                only_problem_children_pgad = refined_pgad_db.loc[((refined_pgad_db['PGAD Criterion C Discrepancy'] == "Problem") | (refined_pgad_db['PGAD Symptom Count Discrepancy'] == "Problem"))]

                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criteria C item (scid_f136cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PGAD Criterion C Discrepancy** - The Criterion C item (scid_f136) should only be marked 3 (threshold) if 3 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New PGAD Symptom Count** - My new symptom count using the Cx Item columns.")
                    st.markdown("- **PGAD Symptom Count Discrepancy** - Checks whether the the scid Criterion C count matches my manual count.")

                # Creating the framework to be able to see the corresponding interviewers
                interviewer_selection_pgad = st.checkbox("Would you like to see the associated interviewer?", key = 'pgad')
                if interviewer_selection_pgad:
                    problem_children_pgad_final = only_problem_children_pgad.loc[:, ['scid_interviewername', 'C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'scid_f136', 'scid_f136s',
                    'PGAD Criterion C Discrepancy', 'scid_f136cnt', 'New PGAD Symptom Count', 'PGAD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_pgad_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_pgad_final)
                    csv = convert_df(problem_children_pgad_final)
                else:
                    problem_children_pgad_final = only_problem_children_pgad.loc[:, ['C1 Items', 'C2 Items', 'C3 Items', 'C4 Items', 'C5 Items', 'C6 Items', 'scid_f136', 'scid_f136s',
                    'PGAD Criterion C Discrepancy', 'scid_f136cnt', 'New PGAD Symptom Count', 'PGAD Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_pgad_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_pgad_final)
                    csv = convert_df(problem_children_pgad_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_pgad_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'pgad_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_pgad_final[problem_children_pgad_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_pgad_final[problem_children_pgad_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pa_problem_subject_list = problem_children_pgad_final.index.values.tolist()
                see_more_pgad = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pa_problem_subject_list)
                interviewer_selection_pgad_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_pgad')
                if see_more_pgad is not None:
                    if interviewer_selection_pgad_2:
                        specific_pgad_subject_db = pgad_full_db.loc[see_more_pgad,:]
                        specific_pgad_subject_db_2 = specific_pgad_subject_db.loc[:,['scid_interviewername','C1 Items', 'scid_f130', 'C2 Items', 'scid_f131', 'C3 Items', 'scid_f132', 'C4 Items', 
                        'scid_f133', 'C5 Items', 'scid_f134', 'C6 Items', 'scid_f135', 'scid_f136', 'scid_f136s', 'scid_f136cnt', 'New PGAD Symptom Count']]
                        specific_pgad_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pgad_subject_db_2)
                        csv = convert_df(specific_pgad_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pgad_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_pgad_subject_db = pgad_full_db.loc[see_more_pgad,:]
                        specific_pgad_subject_db_2 = specific_pgad_subject_db.loc[:,['C1 Items', 'scid_f130', 'C2 Items', 'scid_f131', 'C3 Items', 'scid_f132', 'C4 Items', 'scid_f133', 
                        'C5 Items', 'scid_f134', 'C6 Items', 'scid_f135', 'scid_f136', 'scid_f136s', 'scid_f136cnt', 'New PGAD Symptom Count']]
                        specific_pgad_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_pgad_subject_db_2)
                        csv = convert_df(specific_pgad_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'pgad_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
        if module_selection == 'Module K':
            module_k_syndrome_selection = st.sidebar.selectbox("Which disorder would you like to look at?", ["---", "ADHD Inattention", "ADHD Hyperactivity"])
            st.markdown(f"## {module_selection}")
            st.markdown("---")
            if module_k_syndrome_selection == "---":
                st.markdown("### Options:")
                st.markdown("- **'ADHD Inattention'**")
                st.markdown("- **'ADHD Hyperactivity'**")
            if module_k_syndrome_selection == "ADHD Inattention":
                st.markdown(f"#### {module_k_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_k_items_db = pd.read_excel(module_k_file)
                
                # Selecting only module K items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE K]
                module_k_item_list = module_k_items_db['module_k_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_k_item_list

                module_k_db = full_db.loc[:, final_list]

                # ADHD Inattention # Just Checking Calculation errors
                adhd_ina_full_db = module_k_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_k4', 'scid_k5', 'scid_k6', 'scid_k7', 'scid_k8a', 'scid_k8b', 'scid_k8c', 'scid_k9', 'scid_k10',
                'scid_k11a', 'scid_k11b', 'scid_k12', 'scid_k13', 'scid_k13cnt']]

                # Setting index to subject_id
                adhd_ina_full_db.set_index("subject_id", inplace = True)

                # Filling all na values with 0 in order to run comparisons
                adhd_ina_full_db.fillna(0, inplace = True)

                # Setting the SCID variable to integers instead of floats as it's more readable
                adhd_ina_full_db = adhd_ina_full_db.astype({'scid_k4':'int', 'scid_k5':'int', 'scid_k6':'int', 'scid_k7':'int', 'scid_k8a':'int', 'scid_k8b':'int', 'scid_k8c':'int',
                'scid_k9':'int', 'scid_k10':'int', 'scid_k11a':'int', 'scid_k11b':'int', 'scid_k12':'int', 'scid_k13':'int', 'scid_k13cnt':'int'})

                # Counting Inattention Symptoms # Max is 9
                adhd_ina_full_db['Inattention A'] = np.where(((adhd_ina_full_db['scid_k4'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention B'] = np.where(((adhd_ina_full_db['scid_k5'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention C'] = np.where(((adhd_ina_full_db['scid_k6'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention D'] = np.where(((adhd_ina_full_db['scid_k7'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention E'] = np.where(((adhd_ina_full_db['scid_k8a'] == 3) | (adhd_ina_full_db['scid_k8b'] == 3) | (adhd_ina_full_db['scid_k8c'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention F'] = np.where(((adhd_ina_full_db['scid_k9'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention G'] = np.where(((adhd_ina_full_db['scid_k10'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention H'] = np.where(((adhd_ina_full_db['scid_k11a'] == 3) | (adhd_ina_full_db['scid_k11b'] == 3)), 1, 0)
                adhd_ina_full_db['Inattention I'] = np.where(((adhd_ina_full_db['scid_k12'] == 3)), 1, 0)

                # Checking the ADHD Inattention Discrepancy # Need to have at least 5 Inattention symptoms # Checking against eInterview Count
                adhd_ina_full_db['ADHD Inattention Criteria Discrepancy'] = np.where((((adhd_ina_full_db['scid_k13'] != 3) & (adhd_ina_full_db['scid_k13cnt'] >= 5)) | ((adhd_ina_full_db['scid_k13'] == 3) & (adhd_ina_full_db['scid_k13cnt'] < 5))), "Problem", "Fine")
                
                # Checking Count Discrepancy
                adhd_ina_full_db['New ADHD INA Symptom Count'] = adhd_ina_full_db.loc[:, ['Inattention A', 'Inattention B', 'Inattention C', 'Inattention D', 'Inattention E', 'Inattention F', 'Inattention G', 
                'Inattention H', 'Inattention I']].sum(axis = 1)
                adhd_ina_full_db['ADHD INA Symptom Count Discrepancy'] = np.where(((adhd_ina_full_db['scid_k13cnt'] != adhd_ina_full_db['New ADHD INA Symptom Count'])), "Problem", "Fine")

                # Getting the Count Items and the Discrepancy Values
                refined_adhd_ina_db = adhd_ina_full_db.loc[:, ['scid_interviewername', 'Inattention A', 'Inattention B', 'Inattention C', 'Inattention D', 'Inattention E', 'Inattention F', 'Inattention G', 
                'Inattention H', 'Inattention I', 'scid_k13', 'scid_k13cnt', 'ADHD Inattention Criteria Discrepancy', 'New ADHD INA Symptom Count', 'ADHD INA Symptom Count Discrepancy']]
                
                # Getting Count Discrepancy Direction and Value
                refined_adhd_ina_db['Count Discrepancy Direction'] = np.where(((refined_adhd_ina_db['scid_k13cnt'] - refined_adhd_ina_db['New ADHD INA Symptom Count']) > 0), "Original Count Larger",
                np.where(((refined_adhd_ina_db['scid_k13cnt'] - refined_adhd_ina_db['New ADHD INA Symptom Count']) == 0), "Same", "New Count Larger"))
                refined_adhd_ina_db['Count Discrepancy Value'] = refined_adhd_ina_db['scid_k13cnt'] - refined_adhd_ina_db['New ADHD INA Symptom Count']

                # Getting only "Problem Subjects"
                only_problem_children_adhd_ina = refined_adhd_ina_db.loc[((refined_adhd_ina_db['ADHD Inattention Criteria Discrepancy'] == "Problem") | (refined_adhd_ina_db['ADHD INA Symptom Count Discrepancy'] == "Problem"))]

                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a ADHD Inattention item (scid_k13cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **ADHD Inattention Criteria Discrepancy** - The ADHD INA item (scid_k13) should only be marked 3 (threshold) if 5 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New ADHD INA Symptom Count** - My new symptom count using the Inattention X columns.")
                    st.markdown("- **ADHD INA Symptom Count Discrepancy** - Checks whether the the scid Inattention count matches my manual count.")

                # Creating the framework to be able to see the corresponding interviewers
                interviewer_selection_adhd_ina = st.checkbox("Would you like to see the associated interviewer?", key = 'adhd_ina')
                if interviewer_selection_adhd_ina:
                    problem_children_adhd_ina_final = only_problem_children_adhd_ina.loc[:, ['scid_interviewername', 'Inattention A', 'Inattention B', 'Inattention C', 'Inattention D', 'Inattention E', 'Inattention F', 'Inattention G', 
                    'Inattention H', 'Inattention I' 'scid_k13', 'ADHD Inattention Criteria Discrepancy', 'scid_k13cnt', 'New ADHD INA Symptom Count', 'ADHD INA Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_adhd_ina_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_adhd_ina_final)
                    csv = convert_df(problem_children_adhd_ina_final)
                else:
                    problem_children_adhd_ina_final = only_problem_children_adhd_ina.loc[:, ['Inattention A', 'Inattention B', 'Inattention C', 'Inattention D', 'Inattention E', 'Inattention F', 'Inattention G', 
                    'Inattention H', 'Inattention I', 'scid_k13', 'ADHD Inattention Criteria Discrepancy', 'scid_k13cnt', 'New ADHD INA Symptom Count', 'ADHD INA Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_adhd_ina_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_adhd_ina_final)
                    csv = convert_df(problem_children_adhd_ina_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_adhd_ina_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'adhd_ina_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_adhd_ina_final[problem_children_adhd_ina_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_adhd_ina_final[problem_children_adhd_ina_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pa_problem_subject_list = problem_children_adhd_ina_final.index.values.tolist()
                see_more_adhd_ina = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pa_problem_subject_list)
                interviewer_selection_adhd_ina_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_adhd_ina')
                if see_more_adhd_ina is not None:
                    if interviewer_selection_adhd_ina_2:
                        specific_adhd_ina_subject_db = adhd_ina_full_db.loc[see_more_adhd_ina,:]
                        specific_adhd_ina_subject_db_2 = specific_adhd_ina_subject_db.loc[:,['scid_interviewername','Inattention A', 'scid_k4', 'Inattention B', 'scid_k5', 'Inattention C', 'scid_k6', 'Inattention D', 
                        'scid_k7', 'Inattention E', 'scid_k8a', 'scid_k8b', 'scid_k8c', 'Inattention F', 'scid_k9', 'Inattention G', 'scid_k10', 'Inattention H', 'scid_k11a', 'scid_k11b', 'Inattention I', 'scid_k12',
                        'scid_k13', 'scid_k13cnt', 'New ADHD INA Symptom Count']]
                        specific_adhd_ina_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_adhd_ina_subject_db_2)
                        csv = convert_df(specific_adhd_ina_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'adhd_ina_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_adhd_ina_subject_db = adhd_ina_full_db.loc[see_more_adhd_ina,:]
                        specific_adhd_ina_subject_db_2 = specific_adhd_ina_subject_db.loc[:,['Inattention A', 'scid_k4', 'Inattention B', 'scid_k5', 'Inattention C', 'scid_k6', 'Inattention D', 
                        'scid_k7', 'Inattention E', 'scid_k8a', 'scid_k8b', 'scid_k8c', 'Inattention F', 'scid_k9', 'Inattention G', 'scid_k10', 'Inattention H', 'scid_k11a', 'scid_k11b', 'Inattention I', 'scid_k12',
                        'scid_k13', 'scid_k13cnt', 'New ADHD INA Symptom Count']]
                        specific_adhd_ina_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_adhd_ina_subject_db_2)
                        csv = convert_df(specific_adhd_ina_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'adhd_ina_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_k_syndrome_selection == "ADHD Hyperactivity":
                st.markdown(f"#### {module_k_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_k_items_db = pd.read_excel(module_k_file)
                
                # Selecting only module K items (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE K]
                module_k_item_list = module_k_items_db['module_k_items'].values.tolist()
                final_list = ['subject_id', 'scid_interviewername'] + module_k_item_list

                module_k_db = full_db.loc[:, final_list]

                # ADHD Hyperactivity # Just Checking Calculation errors
                adhd_hyp_full_db = module_k_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_k14', 'scid_k15', 'scid_k16', 'scid_k17', 'scid_k18a', 'scid_k18b', 'scid_k19', 'scid_k20a', 'scid_k20b',
                'scid_k21', 'scid_k22a', 'scid_k22b', 'scid_k23', 'scid_k23cnt']]

                # Setting index to subject_id
                adhd_hyp_full_db.set_index("subject_id", inplace = True)

                # Filling all na values with 0 in order to run comparisons
                adhd_hyp_full_db.fillna(0, inplace = True)

                # Setting the SCID variable to integers instead of floats as it's more readable
                adhd_hyp_full_db = adhd_hyp_full_db.astype({'scid_k14':'int', 'scid_k15':'int', 'scid_k16':'int', 'scid_k17':'int', 'scid_k18a':'int', 'scid_k18b':'int',
                'scid_k19':'int', 'scid_k20a':'int', 'scid_k20b':'int', 'scid_k21':'int', 'scid_k22a':'int', 'scid_k22b':'int', 'scid_k23':'int', 'scid_k23cnt':'int'})

                # Counting Hyperactivity Symptoms # Max is 9
                adhd_hyp_full_db['Hyperactivity A'] = np.where(((adhd_hyp_full_db['scid_k14'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity B'] = np.where(((adhd_hyp_full_db['scid_k15'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity C'] = np.where(((adhd_hyp_full_db['scid_k16'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity D'] = np.where(((adhd_hyp_full_db['scid_k17'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity E'] = np.where(((adhd_hyp_full_db['scid_k18a'] == 3) | (adhd_hyp_full_db['scid_k18b'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity F'] = np.where(((adhd_hyp_full_db['scid_k19'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity G'] = np.where(((adhd_hyp_full_db['scid_k20a'] == 3) | (adhd_hyp_full_db['scid_k20b'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity H'] = np.where(((adhd_hyp_full_db['scid_k21'] == 3)), 1, 0)
                adhd_hyp_full_db['Hyperactivity I'] = np.where(((adhd_hyp_full_db['scid_k22a'] == 3) | (adhd_hyp_full_db['scid_k22b'] == 3)), 1, 0)

                # Checking the ADHD Hyperactivity Discrepancy # Need to have at least 5 Hyperactivity symptoms # Checking against eInterview Count
                adhd_hyp_full_db['ADHD Hyperactivity Criteria Discrepancy'] = np.where((((adhd_hyp_full_db['scid_k23'] != 3) & (adhd_hyp_full_db['scid_k23cnt'] >= 5)) | ((adhd_hyp_full_db['scid_k23'] == 3) & (adhd_hyp_full_db['scid_k23cnt'] < 5))), "Problem", "Fine")
                
                # Checking Count Discrepancy
                adhd_hyp_full_db['New ADHD HYP Symptom Count'] = adhd_hyp_full_db.loc[:, ['Hyperactivity A', 'Hyperactivity B', 'Hyperactivity C', 'Hyperactivity D', 'Hyperactivity E', 'Hyperactivity F', 'Hyperactivity G', 
                'Hyperactivity H', 'Hyperactivity I']].sum(axis = 1)
                adhd_hyp_full_db['ADHD HYP Symptom Count Discrepancy'] = np.where(((adhd_hyp_full_db['scid_k23cnt'] != adhd_hyp_full_db['New ADHD HYP Symptom Count'])), "Problem", "Fine")

                # Getting the Count Items and the Discrepancy Values
                refined_adhd_hyp_db = adhd_hyp_full_db.loc[:, ['scid_interviewername', 'Hyperactivity A', 'Hyperactivity B', 'Hyperactivity C', 'Hyperactivity D', 'Hyperactivity E', 'Hyperactivity F', 'Hyperactivity G', 
                'Hyperactivity H', 'Hyperactivity I', 'scid_k23', 'scid_k23cnt', 'ADHD Hyperactivity Criteria Discrepancy', 'New ADHD HYP Symptom Count', 'ADHD HYP Symptom Count Discrepancy']]
                
                # Getting Count Discrepancy Direction and Value
                refined_adhd_hyp_db['Count Discrepancy Direction'] = np.where(((refined_adhd_hyp_db['scid_k23cnt'] - refined_adhd_hyp_db['New ADHD HYP Symptom Count']) > 0), "Original Count Larger",
                np.where(((refined_adhd_hyp_db['scid_k23cnt'] - refined_adhd_hyp_db['New ADHD HYP Symptom Count']) == 0), "Same", "New Count Larger"))
                refined_adhd_hyp_db['Count Discrepancy Value'] = refined_adhd_hyp_db['scid_k23cnt'] - refined_adhd_hyp_db['New ADHD HYP Symptom Count']

                # Getting only "Problem Subjects"
                only_problem_children_adhd_hyp = refined_adhd_hyp_db.loc[((refined_adhd_hyp_db['ADHD Hyperactivity Criteria Discrepancy'] == "Problem") | (refined_adhd_hyp_db['ADHD HYP Symptom Count Discrepancy'] == "Problem"))]

                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a ADHD Hyperactivity item (scid_k23cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **ADHD Hyperactivity Criteria Discrepancy** - The ADHD HYP item (scid_k23) should only be marked 3 (threshold) if 5 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New ADHD HYP Symptom Count** - My new symptom count using the Hyperactivity X columns.")
                    st.markdown("- **ADHD HYP Symptom Count Discrepancy** - Checks whether the the scid Hyperactivity count matches my manual count.")

                # Creating the framework to be able to see the corresponding interviewers
                interviewer_selection_adhd_hyp = st.checkbox("Would you like to see the associated interviewer?", key = 'adhd_hyp')
                if interviewer_selection_adhd_hyp:
                    problem_children_adhd_hyp_final = only_problem_children_adhd_hyp[['scid_interviewername', 'Hyperactivity A', 'Hyperactivity B', 'Hyperactivity C', 'Hyperactivity D', 'Hyperactivity E', 'Hyperactivity F', 'Hyperactivity G', 
                    'Hyperactivity H', 'Hyperactivity I' 'scid_k23', 'ADHD Hyperactivity Criteria Discrepancy', 'scid_k23cnt', 'New ADHD HYP Symptom Count', 'ADHD HYP Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_adhd_hyp_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_adhd_hyp_final)
                    csv = convert_df(problem_children_adhd_hyp_final)
                else:
                    problem_children_adhd_hyp_final = only_problem_children_adhd_hyp[['Hyperactivity A', 'Hyperactivity B', 'Hyperactivity C', 'Hyperactivity D', 'Hyperactivity E', 'Hyperactivity F', 'Hyperactivity G', 
                    'Hyperactivity H', 'Hyperactivity I', 'scid_k23', 'ADHD Hyperactivity Criteria Discrepancy', 'scid_k23cnt', 'New ADHD HYP Symptom Count', 'ADHD HYP Symptom Count Discrepancy', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                    problem_children_adhd_hyp_final.sort_values('subject_id', inplace = True)
                    st.write(problem_children_adhd_hyp_final)
                    csv = convert_df(problem_children_adhd_hyp_final)
                
                column1, column2 = st.columns(2)
                with column1:
                    st.write("Number of Problem Subjects:", len(problem_children_adhd_hyp_final.index))
                    st.download_button(label = "Download Data as a CSV", data = csv, file_name = f'adhd_hyp_problem_subjects_export_{today}.csv', mime = 'text/csv')
                with column2:
                    st.write("Number of Subjects with **New Count Larger**:", len(problem_children_adhd_hyp_final[problem_children_adhd_hyp_final['Count Discrepancy Direction'] == 'New Count Larger'].index))
                    st.write("Number of Subjects with **Original Count Larger:**", len(problem_children_adhd_hyp_final[problem_children_adhd_hyp_final['Count Discrepancy Direction'] == 'Original Count Larger'].index))
                pa_problem_subject_list = problem_children_adhd_hyp_final.index.values.tolist()
                see_more_adhd_hyp = st.multiselect("See Specific Subject Info? [Select as many as you would like]", pa_problem_subject_list)
                interviewer_selection_adhd_hyp_2 = st.checkbox("Would you like to see the associated interviewer?", key =  'extra_adhd_hyp')
                if see_more_adhd_hyp is not None:
                    if interviewer_selection_adhd_hyp_2:
                        specific_adhd_hyp_subject_db = adhd_hyp_full_db.loc[see_more_adhd_hyp,:]
                        specific_adhd_hyp_subject_db_2 = specific_adhd_hyp_subject_db.loc[:,['scid_interviewername','Hyperactivity A', 'scid_k14', 'Hyperactivity B', 'scid_k15', 'Hyperactivity C', 'scid_k16', 'Hyperactivity D', 
                        'scid_k17', 'Hyperactivity E', 'scid_k18a', 'scid_k18b', 'Hyperactivity F', 'scid_k19', 'Hyperactivity G', 'scid_k20a', 'scid_k20b' 'Hyperactivity H', 'scid_k21', 'Hyperactivity I', 'scid_k22a', 'scid_k22b',
                        'scid_k23', 'scid_k23cnt', 'New ADHD HYP Symptom Count']]
                        specific_adhd_hyp_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_adhd_hyp_subject_db_2)
                        csv = convert_df(specific_adhd_hyp_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'adhd_hyp_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
                    else:
                        specific_adhd_hyp_subject_db = adhd_hyp_full_db.loc[see_more_adhd_hyp,:]
                        specific_adhd_hyp_subject_db_2 = specific_adhd_hyp_subject_db.loc[:,['Hyperactivity A', 'scid_k14', 'Hyperactivity B', 'scid_k15', 'Hyperactivity C', 'scid_k16', 'Hyperactivity D', 
                        'scid_k17', 'Hyperactivity E', 'scid_k18a', 'scid_k18b', 'Hyperactivity F', 'scid_k19', 'Hyperactivity G', 'scid_k20a', 'scid_k20b', 'Hyperactivity H', 'scid_k21', 'Hyperactivity I', 'scid_k22a', 'scid_k22b',
                        'scid_k23', 'scid_k23cnt', 'New ADHD HYP Symptom Count']]
                        specific_adhd_hyp_subject_db_2.sort_values('subject_id', inplace=True)
                        st.write(specific_adhd_hyp_subject_db_2)
                        csv = convert_df(specific_adhd_hyp_subject_db_2)
                        st.download_button("Download Data as a CSV", data = csv, file_name=f'adhd_hyp_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
        if module_selection == "Module C":
            module_c_syndrome_selection = st.sidebar.selectbox("Which disorder would you like to look at?", ["---", "Schizophrenia", "Schizphreniform Disorder", "Brief Psychotic Disorder"])
            st.markdown(f"## {module_selection}")
            st.markdown("---")
            if module_c_syndrome_selection == "---":
                st.markdown("### Options:")
                st.markdown("- **'Schizphrenia'** - Checking catatonia count!")
                st.markdown("- **'Schizophreniform Disorder'** -- Checking catatonia count!")
                st.markdown("- **'Brief Psychotic Disorder'** - Checking catatonia count!")
            if module_c_syndrome_selection == "Schizophrenia":
                st.markdown(f"#### {module_c_syndrome_selection}")
                st.markdown("---")

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_c_items_db = pd.read_excel(module_c_file)
                
                # Selecting only module C items and Catatonia Items from Module B (including subject_id and scid_interviewername of course) [THIS IS ALL OF MODULE C]
                module_c_item_list = module_k_items_db['module_k_items'].values.tolist()
                catatonia_list = ['scid_b27', 'scid_b28', 'scid_b29', 'scid_b30', 'scid_b31', 'scid_b32', 'scid_b33', 'scid_b34', 'scid_b35', 'scid_b36', 'scid_b37', 'scid_b38']
                final_list = ['subject_id', 'scid_interviewername'] + catatonia_list + module_k_item_list

                module_c_db = full_db.loc[:, final_list]

                # Schizophrenia # Just Checking Calculation errors
                schizo_full_db = module_c_db.loc[:, ['subject_id', 'scid_interviewername', 'scid_b27', 'scid_b28', 'scid_b29', 'scid_b30', 'scid_b31', 'scid_b32', 'scid_b33', 'scid_b34', 
                'scid_b35', 'scid_b36', 'scid_b37', 'scid_b38', 'scid_c10', 'scid_c11', 'scid_c11cnt']]

                # Setting index to subject_id
                schizo_full_db.set_index('subject_id', inplace = True)

                # Filling all the na values with 0 in order to run comparisons
                schizo_full_db.fillna(0, inplace = True)

                # Setting the SCID variables to integers instead of floats as it is more readable
                schizo_full_db = schizo_full_db.astype({'scid_b27':'int', 'scid_b28':'int', 'scid_b29':'int', 'scid_b30':'int', 'scid_b31':'int', 'scid_b32':'int', 'scid_b33':'int', 'scid_b34':'int', 
                'scid_b35':'int', 'scid_b36':'int', 'scid_b37':'int', 'scid_b38':'int', 'scid_c10':'int', 'scid_c11':'int', 'scid_c11cnt':'int'})

                # Counting Catatonia Items # Max is 12
                schizo_full_db['Stupor'] = np.where((schizo_full_db['scid_b27'] == 3), 1, 0)
                schizo_full_db['Grimacing'] = np.where((schizo_full_db['scid_b28'] == 3), 1, 0)
                schizo_full_db['Mannerism'] = np.where((schizo_full_db['scid_b29'] == 3), 1, 0)
                schizo_full_db['Posturing'] = np.where((schizo_full_db['scid_b30'] == 3), 1, 0)
                schizo_full_db['Agitation'] = np.where((schizo_full_db['scid_b31'] == 3), 1, 0)
                schizo_full_db['Stereotype'] = np.where((schizo_full_db['scid_b32'] == 3), 1, 0)
                schizo_full_db['Mutism'] = np.where((schizo_full_db['scid_b33'] == 3), 1, 0)
                schizo_full_db['Echolalia'] = np.where((schizo_full_db['scid_b34'] == 3), 1, 0)
                schizo_full_db['Negativism'] = np.where((schizo_full_db['scid_b35'] == 3), 1, 0)
                schizo_full_db['Echopraxia'] = np.where((schizo_full_db['scid_b36'] == 3), 1, 0)
                schizo_full_db['Catalepsy'] = np.where((schizo_full_db['scid_b37'] == 3), 1, 0)
                schizo_full_db['Waxy Flexibility'] = np.where((schizo_full_db['scid_b38'] == 3), 1, 0)

                # Checking the With Catatonia item of Schizophreniam # Needs to have 3 or more catatonic items to be present
                schizo_full_db['W/ CATA SCHIZOPHRENIA Discrepancy'] = np.where((((schizo_full_db['scid_c11'] == 1) & (schizo_full_db['scid_c11cnt'] < 3)) | ((schizo_full_db['scid_c10'] == 3) & (schizo_full_db['scid_c11cnt'] >= 3) & (schizo_full_db['scid_c11'] != 1))), "Problem", "Fine")