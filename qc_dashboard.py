import pandas as pd
import numpy as np
import streamlit as st
from datetime import date

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
                # Datafile
                module_a_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Visual Studio Code/VUMC Quality Control/Module A Items.xlsx'

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Current Major Depression # Just checking for calculation erros
                cmde_full_db = module_a_db.loc[:, ['subject_id', 'scid_a1a', 'scid_a1b', 'scid_a2a', 'scid_a2ar', 'scid_a2b', 'scid_a2br', 'scid_a3a', 'scid_a3b1', 'scid_a3b2', 'scid_a6',
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

                # Checking diagnosis discrepancy
                cmde_full_db['CMDE Criterion A Discrepancy'] = np.where((((cmde_full_db['scid_a22cnt'] >= 5) & ((cmde_full_db['A1 Items'] == 1) | (cmde_full_db['A2 Items'] == 1))) & (cmde_full_db['scid_a22'] != 3)), "Problem", "Fine")

                # Checking count discrepancy
                cmde_full_db['New CMDE Symptom Count'] = cmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items']].sum(axis = 1)
                cmde_full_db['CMDE Symptom Count Discrepancy'] = np.where((cmde_full_db['scid_a22cnt'] != cmde_full_db['New CMDE Symptom Count']), "Problem", "Fine")

                # Only getting Count Items and Discrepancy Items
                refined_cmde_db = cmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a22', 'scid_a22cnt',
                'CMDE Criterion A Discrepancy', 'New CMDE Symptom Count', 'CMDE Symptom Count Discrepancy']]

                refined_cmde_db['Count Discrepancy Direction'] = np.where(((cmde_full_db['scid_a22cnt'] - cmde_full_db['New CMDE Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_cmde_db['Count Discrepancy Value'] = cmde_full_db['scid_a22cnt'] - cmde_full_db['New CMDE Symptom Count']
                
                only_problem_children_cmde = refined_cmde_db.loc[((refined_cmde_db['CMDE Criterion A Discrepancy'] == 'Problem') | (refined_cmde_db['CMDE Symptom Count Discrepancy'] == 'Problem'))]
                problem_children_cmde_final = only_problem_children_cmde[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a22', 'CMDE Criterion A Discrepancy',
                'scid_a22cnt', 'New CMDE Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion A count item (scid_a22cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CMDE Criterion A Discrepancy** - The Criterion A item (scid_a22) should only be marked 3 (threshold) if 5 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New CMDE Symptom Count** - My new symptom count using the Ax Item columns.")
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
                if see_more_cmde is not None:
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
                # Datafile
                module_a_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Visual Studio Code/VUMC Quality Control/Module A Items.xlsx'

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Major Depression # Just checking for calculation errors
                pmde_full_db = module_a_db.loc[:, ['subject_id','scid_a27a', 'scid_a27b', 'scid_a28a', 'scid_a28b', 'scid_a28ar', 'scid_a28br', 'scid_a29a', 'scid_a29b1', 'scid_a29b2',
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
                refined_pmde_db = pmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a48', 'scid_a48cnt',
                'PMDE Criterion A Discrepancy', 'New PMDE Symptom Count', 'PMDE Symptom Count Discrepancy']]

                refined_pmde_db['Count Discrepancy Direction'] = np.where(((pmde_full_db['scid_a48cnt'] - pmde_full_db['New PMDE Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_pmde_db['Count Discrepancy Value'] = pmde_full_db['scid_a48cnt'] - pmde_full_db['New PMDE Symptom Count']
                
                only_problem_children_pmde = refined_pmde_db.loc[((refined_pmde_db['PMDE Criterion A Discrepancy'] == 'Problem') | (refined_pmde_db['PMDE Symptom Count Discrepancy'] == 'Problem'))]
                problem_children_pmde_final = only_problem_children_pmde[['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a48', 'PMDE Criterion A Discrepancy',
                'scid_a48cnt', 'New PMDE Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion A count item (scid_a48cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PMDE Criterion A Discrepancy** - The Criterion A item (scid_a48) should only be marked 3 (threshold) if 5 or more symptoms are accounted for. This column checks to see if that is the case.")
                    st.markdown("- **New PMDE Symptom Count** - My new symptom count using the Ax Item columns.")
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
                if see_more_pmde is not None:
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
                # Datafile
                module_a_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Visual Studio Code/VUMC Quality Control/Module A Items.xlsx'

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Major Depression # Just checking for calculation errors
                cme_full_db = module_a_db.loc[:, ['subject_id', 'scid_a54a', 'scid_a54c1', 'scid_a54b', 'scid_a54c2', 'scid_a58', 'scid_a59', 'scid_a60', 
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
                refined_cme_db = cme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a67', 'scid_a67cnt',
                'CME Criterion B Discrepancy', 'New CME Symptom Count', 'CME Symptom Count Discrepancy']]
                
                refined_cme_db['Count Discrepancy Direction'] = np.where(((cme_full_db['scid_a67cnt'] - cme_full_db['New CME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_cme_db['Count Discrepancy Value'] = cme_full_db['scid_a67cnt'] - cme_full_db['New CME Symptom Count']
                
                only_problem_children_cme = refined_cme_db.loc[((refined_cme_db['CME Criterion B Discrepancy'] == 'Problem') | (refined_cme_db['CME Symptom Count Discrepancy'] == 'Problem'))]
                problem_children_cme_final = only_problem_children_cme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a67', 'CME Criterion B Discrepancy',
                'scid_a67cnt', 'New CME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a67cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CME Criterion A Discrepancy** - The Criterion A item (scid_a67) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New CME Symptom Count** - My new symptom count using the Bx Item columns.")
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
                if see_more_cme is not None:
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
                # Datafile
                module_a_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Visual Studio Code/VUMC Quality Control/Module A Items.xlsx'

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Major Depression # Just checking for calculation errors
                pme_full_db = module_a_db.loc[:, ['subject_id', 'scid_a92a', 'scid_a92c1', 'scid_a92b', 'scid_a92c2', 'scid_a96', 'scid_a97', 'scid_a98', 
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
                refined_pme_db = pme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a105', 'scid_a105cnt',
                'PME Criterion B Discrepancy', 'New PME Symptom Count', 'PME Symptom Count Discrepancy']]
                
                refined_pme_db['Count Discrepancy Direction'] = np.where(((pme_full_db['scid_a105cnt'] - pme_full_db['New PME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_pme_db['Count Discrepancy Value'] = pme_full_db['scid_a105cnt'] - pme_full_db['New PME Symptom Count']
                
                only_problem_children_pme = refined_pme_db.loc[((refined_pme_db['PME Criterion B Discrepancy'] == 'Problem') | (refined_pme_db['PME Symptom Count Discrepancy'] == 'Problem'))]
                problem_children_pme_final = only_problem_children_pme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a105', 'PME Criterion B Discrepancy',
                'scid_a105cnt', 'New PME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a105cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **PME Criterion A Discrepancy** - The Criterion A item (scid_a105) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New PME Symptom Count** - My new symptom count using the Bx Item columns.")
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
                if see_more_pme is not None:
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
                # Datafile
                module_a_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Visual Studio Code/VUMC Quality Control/Module A Items.xlsx'

                # Opening datafile
                full_db = pd.read_csv(full_data)
                module_a_items_db = pd.read_excel(module_a_file)

                # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
                module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
                final_list = ['subject_id'] + module_a_item_list

                module_a_db = full_db.loc[:, final_list]

                # Past Major Depression # Just checking for calculation errors
                chme_full_db = module_a_db.loc[:, ['subject_id', 'scid_a54a', 'scid_a54c1', 'scid_a54b', 'scid_a54c2', 'scid_a75', 'scid_a76', 'scid_a77', 
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
                refined_chme_db = chme_full_db.loc[:, ['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a84', 'scid_a84cnt',
                'CHME Criterion B Discrepancy', 'New CHME Symptom Count', 'CHME Symptom Count Discrepancy']]
                
                refined_chme_db['Count Discrepancy Direction'] = np.where(((chme_full_db['scid_a84cnt'] - chme_full_db['New CHME Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
                refined_chme_db['Count Discrepancy Value'] = chme_full_db['scid_a84cnt'] - chme_full_db['New CHME Symptom Count']
                
                only_problem_children_chme = refined_chme_db.loc[((refined_chme_db['CHME Criterion B Discrepancy'] == 'Problem') | (refined_chme_db['CHME Symptom Count Discrepancy'] == 'Problem'))]
                problem_children_chme_final = only_problem_children_chme[['B1 Items', 'B2 Items', 'B3 Items', 'B4 Items', 'B5 Items', 'B6 Items', 'B7 Items', 'scid_a84', 'CHME Criterion B Discrepancy',
                'scid_a84cnt', 'New CHME Symptom Count', 'Count Discrepancy Direction', 'Count Discrepancy Value']]
                col1, col2 = st.columns(2)
                with col2:
                    st.write("**Export Breakdown**")
                    st.write("- In the SCID there is a Criterion B count item (scid_a84cnt) and the table below outlines where the count item does not match the actual symptom count.")
                with col1:
                    st.write("**Column Definitions:**")
                    st.markdown("- **CHME Criterion A Discrepancy** - The Criterion A item (scid_a84) should only be marked 3 (threshold) if 3 or more symptoms are accounted for (4 or more if only irritable mood). This column checks to see if that is the case.")
                    st.markdown("- **New CHME Symptom Count** - My new symptom count using the Bx Item columns.")
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
                if see_more_chme is not None:
                    specific_chme_subject_db = chme_full_db.loc[see_more_chme,:]
                    specific_chme_subject_db_2 = specific_chme_subject_db.loc[:,['B1 Items', 'scid_a75', 'B2 Items', 'scid_a76', 'B3 Items', 'scid_a77', 
                    'B4 Items', 'scid_a78', 'B5 Items', 'scid_a79', 'B6 Items', 'scid_a80a', 'scid_a80b', 'B7 Items','scid_a83', 'scid_a84', 'scid_a84cnt', 'New CHME Symptom Count']]
                    specific_chme_subject_db_2.sort_values('subject_id', inplace=True)
                    st.write(specific_chme_subject_db_2)
                    csv = convert_df(specific_chme_subject_db_2)
                    st.download_button("Download Data as a CSV", data = csv, file_name=f'chme_problem_subject_more_depth_{today}.csv', mime = 'text/csv')
            if module_a_syndrome_selection == 'PHME':
                st.write("Hello")
            if module_a_syndrome_selection == 'CPDD':
                st.write("Hello")
            if module_a_syndrome_selection == 'PPDD':
                st.write("Hello")
            if module_a_syndrome_selection == 'PDD':
                st.write("Hello")
