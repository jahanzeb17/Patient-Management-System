import streamlit as st
import requests
import json
import pandas as pd
import time



ALL_RECORD_URL = "http://127.0.0.1:8000/view"
SINGLE_PATIENT_URL = "http://127.0.0.1:8000/view"
CREATE_URL = "http://127.0.0.1:8000/create"
UPDATE_URL = "http://127.0.0.1:8000/update"
DELETE_URL = "http://127.0.0.1:8000/delete"


options = st.sidebar.selectbox("Select the Options", ['Show Records', 'Show Patient', "Add Patient", "Update", "Delete"])

def show_all_records():

    button = st.button('Fetch', key="btn_all_records")
    if button:
        response = requests.get(url=ALL_RECORD_URL)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            st.subheader("All Patient Record", divider='blue')
            # st.dataframe(df.T)
            st.table(df)
        else:
            st.error("Failed tp fetch data")
    

def show_single_patient():

    patient_id = st.text_input("Enter Patient ID: ")
    button = st.button("Click", key="btn_single_records")
    
    if patient_id and button:
            full_url = f"{SINGLE_PATIENT_URL}/{patient_id}"
            response = requests.get(url=full_url)
            # response = requests.get(url=SINGLE_PATIENT_URL, params={"id": user_id})

            if response.status_code == 200:
                data = response.json()

                df = pd.DataFrame([data])
                st.table(df)
            else:
                st.error("Patient not found")


def create_patient():
    st.subheader("Add New Patient")

    with st.form("Patient Form", clear_on_submit=True):

        id = st.text_input("Enter ID: (Format: P001)")
        name = st.text_input("Patient Name")
        city = st.text_input("City")
        age = st.number_input('Age', min_value=1, max_value=100)
        gender = st.selectbox("Select Gender", ['Male', 'Female', 'Others'])
        height = st.number_input("Height", min_value=1.0)
        weight = st.number_input("Weight", min_value=1.0)

        submit_button = st.form_submit_button("Submit Patient")

    if submit_button:

        if not id:
            st.error("ID is required! Data cannot be saved.")
        elif not name:
            st.error("Patient Name is required!")
        elif not city:
            st.error("City is required!")
        else:
            patient_data = {
                "id": id,
                "name": name,
                "city": city,
                "age": age,
                "gender": gender.lower(),
                "height": height,
                "weight": weight
            }

            try:
                response = requests.post(url=CREATE_URL, json=patient_data)

                if response.status_code in [200, 201]:
                    st.success(f"Patient {name} added successfully")
                    # st.rerun()
                else:
                    error_msg = response.json().get("detail", "Unknown Error")
                    st.error(f"Failed: {error_msg}")
            
            except Exception as e:
                st.error(f"Could not connect to Server: {e}")




def update_patient_record():
    st.subheader("Update Patient Record")

    search_id = st.text_input("Enter Patient ID (e.g., P017)")
    
    if st.button("Fetch Data", key="fetch_btn"):
        if search_id:
            response = requests.get(url=f"{SINGLE_PATIENT_URL}/{search_id.strip()}")
            if response.status_code == 200:
                # Store both the data AND the ID used to find it
                st.session_state['update_data'] = response.json()
                st.session_state['target_id'] = search_id.strip()
                st.success(f"Record for {search_id} loaded.")
            else:
                st.error("Patient not found.")
                st.session_state['update_data'] = None

    # Only show the form if data exists in session state
    if st.session_state.get('update_data'):
        p = st.session_state['update_data']
        tid = st.session_state['target_id']

        with st.form("update_form", clear_on_submit=True):
            st.info(f"Editing: {tid}")
            
            # Form Inputs
            new_name = st.text_input("Name", value=p.get('name'))
            new_city = st.text_input("City", value=p.get('city'))
            new_age = st.number_input("Age", value=int(p.get('age', 1)), min_value=1)
            
            g_opts = ['male', 'female', 'others']
            cur_g = p.get('gender', 'male').lower()
            new_gender = st.selectbox("Gender", g_opts, index=0 if cur_g == 'male' else 1)
            
            new_h = st.number_input("Height", value=float(p.get('height', 1.0)), min_value=1.0)
            new_w = st.number_input("Weight", value=float(p.get('weight', 1.0)), min_value=1.0)

            save_btn = st.form_submit_button("Save Changes")

        if save_btn:
            payload = {
                "name": new_name,
                "city": new_city,
                "age": new_age,
                "gender": new_gender,
                "height": new_h,
                "weight": new_w
            }
            
            # Use the ID we stored during the Fetch step
            res = requests.put(url=f"{UPDATE_URL}/{tid}", json=payload)
            
            if res.status_code == 200:
                st.success(f"Patient {tid} updated successfully!")
                st.session_state['update_data'] = None
                st.session_state['target_id'] = None

                time.sleep(3)

                st.rerun()
            else:
                try:
                    error_msg = res.json().get('detail', 'Unknown error')
                except:
                    error_msg = res.text
                st.error(f"Update Failed (Status {res.status_code}): {error_msg}")
            



def delete_patient():

    st.subheader("Delete Patient Record")

    p_id = st.text_input("Enter the ID")
    button = st.button("Delete", key="delete_btn")

    if button and p_id:

        full_url = f"{DELETE_URL}/{p_id}"
        response = requests.delete(url=full_url)

        if response.status_code == 200:
            st.success(f"Patient ID: {p_id} deleted successfully")
            time.sleep(2)
            st.rerun()
        else:
            st.error("Failed to delete")




def main():

    st.title("Patient Management System")

    st.divider()


    if options == "Show Records":
        show_all_records()
    
    elif options == "Show Patient":
        show_single_patient()

    elif options == "Add Patient":
        create_patient()
    
    elif options == "Update":
        update_patient_record()
    
    else:
        delete_patient()

    
if __name__=="__main__":
    main()