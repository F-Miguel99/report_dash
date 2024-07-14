import streamlit as st
#  import cx_Oracle
from PIL import Image
from pathlib import Path
from authentication import authenticate_user
# from authentication import is_authenticated


img = Image.open('unitel-logo.png')


st.set_page_config(
    page_title="CCAF - REALTIME",
    page_icon=img,
)

showSidebarNavigation = False
def login():
    st.title('Login')
    st.session_state.username = st.text_input('Username')
    st.session_state.password = st.text_input('Password', type='password')

    if st.button('Login'):
        user = authenticate_user(st.session_state.username, st.session_state.password)
        if user:
            st.success(f'Welcome, {st.session_state.username}!')
            showSidebarNavigation = True
            # Set session variables or cookies for authentication
            st.stop()
        else:
            st.error('Authentication failed')


    

#  --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

#  --- LOAD CSS, PDF & PROFILE PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style".format(f.read()), unsafe_allow_html=True)

img = Image.open('unitel-logo.png')
img2 = Image.open('ccaf-realtime.png')



#  my_variable = "From Main /MoMo_Report/1_🏠_Home.py Page"

model_training = st.container()



def main():
    st.markdown("<h1 style='text-align: center; color: white;'>CCAF REAL-TIME</h1>", unsafe_allow_html=True)
    #  st.markdown("<h2 style='text-align: center; color: #d33682;'>MOMO MODULE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d33682; font-size:500%;'>MOMO MODULE</p>", unsafe_allow_html=True)
    login()
    #  st.markdown("< img src = 'w3html.gif' alt = 'W3Schools.com' width = '100'height = '132' >",  unsafe_allow_html=True)

    #  st.image(img2)

    #  st.image(img2, caption='Enter any caption here')

    #  st.title("CCAF REAL-TIME")
    #  st.subheader("Main Page")
    #  st.write(my_variable)

    #with st.expander("Concurso Mini Estrelas ao Palco"):
    #    stmt2 = """ """




if __name__ == '__main__':
    main()
