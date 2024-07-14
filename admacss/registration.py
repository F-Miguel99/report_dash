# home.py
import streamlit as st
import sys
# from time import sleep
from PIL import Image
from pathlib import Path

sys.path.append('/Users/macbook/Desktop/projectos_py/streamlit/Mobile_Money_PRJ')
from authentication import get_all_users, register_user, delete_user, user_exists



img = Image.open('/Users/macbook/Desktop/projectos_py/streamlit/Mobile_Money_PRJ/unitel-logo.png')

st.set_page_config(
    page_title="Registration",
    page_icon=img,
)
#  --- PATH SETTINGS ---
#current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
# css_file = current_dir / "main.css"
css_file = '/Users/macbook/Desktop/projectos_py/streamlit/Mobile_Money_PRJ/admacss/main.css'


#  --- LOAD CSS, PDF & PROFILE PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)    


model_training = st.container()

tab1, tab2, tab3 = st.tabs(["Registration", "List Users", "Delete Users"])


def registration():
    st.title('Registration')
    
    with st.form(key="test", clear_on_submit=True): 
    
        new_username = st.text_input("Usuário", key="user")
        new_password = st.text_input("Password", key="pswrd", type="password")
        confirm_password = st.text_input("Confirm Password", key="confirm_pswrd", type="password")
        
    
        submitted = st.form_submit_button("Submit")
        if submitted:
            if new_password == confirm_password:
                register_user(new_username, new_password)
                st.success(f'User {new_username} registered successfully!')
            else:
                st.error('Passwords do not match. Please try again.')
    

def view_all_users():
    st.title('All Users')
    users = get_all_users()
    if users:
        st.write("All users in the database:")
        for user in users:
            st.write(user[1])  # Displaying usernames
            
    else:
        st.write("No users found in the database.")


def delete_user_section():
    st.title('Delete User')
    user_to_delete = st.text_input('Enter the username to delete:')
    if st.button('Delete User'):
        if user_exists(user_to_delete):
            delete_user(user_to_delete)
            st.success(f'User {user_to_delete} deleted successfully!')
            
        else:
            st.error(f'User {user_to_delete} does not exist.')


def main():
    # login()
    with tab1:
        registration()
    with tab2:
        view_all_users()
    with tab3:
        delete_user_section()

if __name__ == "__main__":
    main()
