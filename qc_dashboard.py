import pandas as pd
import numpy as np
import streamlit as st

# Markdown Info
first_selection = st.sidebar.selectbox("What would you like to do?", ["---", "Symptom Counts", "Second Level Diagnosis Check"])
st.markdown("## VUMC QC Dashboard")
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

if first_selection == 'Symptom Counts':
    module_selection = st.sidebar.selectbox("Which module would you like to look at?", ["---","Module A", "Module E", "Module F", "Module K", "Module C"])
    if module_selection == "---":
        st.markdown("Select which module you would like to look at?")
        st.markdown("Options:")
        st.markdown("1. Module A")
        st.markdown("2. Module E")
        st.markdown("3. Module F")
        st.markdown("4. Module K")
        st.markdown("5. Module C")
    if module_selection == "Module A":
        module_a_syndrome_selection = st.sidebar.selectbox("Which disorder would you like to look at?", ["---", "CMDE", "PMDE", "CME", "PME", "CHME", "PHME", "CPDD", "PPDD", "PDD"])
        st.markdown(f"### {module_selection}")
        if module_a_syndrome_selection == '---':
            st.markdown("Options:")
            st.markdown("- 'CMDE' - Current Major Depressive Episode")
            st.markdown("- 'PMDE' - Past Major Depressive Episode")
            st.markdown("- 'CME' - Current Manic Episode")
            st.markdown("- 'PME' - Past Manic Episode")
            st.markdown("- 'CHME' - Current Hypomanic Episode")
            st.markdown("- 'PHME' - Past Hypomanic Episode")
            st.markdown("- 'CPDD' - Current Persistent Depressive Disoder")
            st.markdown("- 'PPDD' - Past Persistent Depressive Disorder")
            st.markdown("- 'PDD' - Premenstrual Dysphoric Disorder")
        if module_a_syndrome_selection == 'CMDE':

            # Datafile
            data_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Vandy Pull Data/Pull 20 (1:24:23)/full_db_(1:24:23).csv'
            module_a_file = '/Users/canluser/Library/CloudStorage/Box-Box/CANL Docs/SVT Files/Coding/Visual Studio Code/VUMC Quality Control/Module A Items.xlsx'

            # Opening datafile
            full_db = pd.read_csv(data_file)
            module_a_items_db = pd.read_excel(module_a_file)

            # Selecting only module A items (including subject_id of course) [THIS IS ALL OF MODULE A EXCLUDING GMC OR SUBSTANCE DISORDERS]
            module_a_item_list = module_a_items_db['module_a_items'].values.tolist()
            final_list = ['subject_id'] + module_a_item_list

            module_a_db = full_db.loc[:, final_list]

            # Current Major Depression # Just checking for calculation erros
            cmde_full_db = module_a_db.loc[:, ['subject_id', 'scid_a1a', 'scid_a1b', 'scid_a2a', 'scid_a2ar', 'scid_a2b', 'scid_a2br', 'scid_a3a', 'scid_a3b1', 'scid_a3b2', 'scid_a6',
            'scid_a8', 'scid_a9a', 'scid_a9b', 'scid_a12', 'scid_a13a', 'scid_a13b','scid_a16a', 'scid_a16b', 'scid_a17', 'scid_a22', 'scid_a22cnt', 'scid_a23i', 'scid_a23d', 'scid_a24', 'scid_a25',
            'scid_a25s', 'scid_a25scnt']]

            # Setting index to subject_id
            cmde_full_db.set_index('subject_id', inplace = True)

            # Filling all na values with 0 in order to run comparisons
            cmde_full_db.fillna(0, inplace = True)

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
            cmde_full_db['CMDE Diag Discrepancy'] = np.where((((cmde_full_db['scid_a22cnt'] >= 5) & ((cmde_full_db['A1 Items'] == 1) | (cmde_full_db['A2 Items'] == 1))) & (cmde_full_db['scid_a22'] != 3)), "Problem", "Fine")

            # Checking count discrepancy
            cmde_full_db['New CMDE Symptom Count'] = cmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items']].sum(axis = 1)
            cmde_full_db['CMDE Symptom Count Discrepancy'] = np.where((cmde_full_db['scid_a22cnt'] != cmde_full_db['New CMDE Symptom Count']), "Problem", "Fine")

            # Only getting Count Items and Discrepancy Items
            refined_cmde_db = cmde_full_db.loc[:, ['A1 Items', 'A2 Items', 'A3 Items', 'A4 Items', 'A5 Items', 'A6 Items', 'A7 Items', 'A8 Items', 'A9 Items', 'scid_a22', 'scid_a22cnt',
            'CMDE Diag Discrepancy', 'New CMDE Symptom Count', 'CMDE Symptom Count Discrepancy']]

            refined_cmde_db['Count Discrepancy Direction'] = np.where(((cmde_full_db['scid_a22cnt'] - cmde_full_db['New CMDE Symptom Count']) > 0), 'Original Count Larger', 'New Count Larger')
            refined_cmde_db['Count Discrepancy Value'] = cmde_full_db['scid_a22cnt'] - cmde_full_db['New CMDE Symptom Count']

            only_problem_children = refined_cmde_db.loc[((refined_cmde_db['CMDE Diag Discrepancy'] == 'Problem') | (refined_cmde_db['CMDE Symptom Count Discrepancy'] == 'Problem'))]

            st.write(only_problem_children)
            st.write("Number of Problem Subjects:", len(only_problem_children.index))
