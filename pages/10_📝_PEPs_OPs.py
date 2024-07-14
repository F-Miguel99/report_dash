import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import datetime
import plotly.graph_objs as go
from authentication import is_authenticated

showSidebarNavigation = False
def page2():
     
    if not is_authenticated(st.session_state.username, st.session_state.password):
            st.error("Access denied. Please login.")
            st.stop()
        
    showSidebarNavigation = True
    img = Image.open('unitel-logo.png')


    st.set_page_config(
        page_title="PEP Ops",
        page_icon=img,
        layout="wide"
    )


    #  --- PATH SETTINGS ---
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    css_file = current_dir / "styles" / "main.css"

    #  --- LOAD CSS, PDF & PROFILE PIC ---
    with open(css_file) as f:
        st.markdown("<style>{}</style".format(f.read()), unsafe_allow_html=True)

    # st.set_page_config(layout="wide")

    # Function to generate a download link for a CSV file
    def get_table_download_link_csv(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="table_data.csv">Download CSV file</a>'
        return href

    # Function to convert DataFrame to PDF - simple version
    def convert_df_to_pdf(df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        for i in range(len(df)):
            pdf.cell(0, 10, f'{df.iloc[i, 0]} {df.iloc[i, 1]} {df.iloc[i, 2]}', ln=True)
        pdf.output("/mnt/data/table_data.pdf")


    # -------------------------- Loading data SECTION
    # df = pd.read_csv('datasets/total_daily_transact.csv')
    @st.cache_data
    def load_data_transctions():
        # Load your DataFrame here / CSV file
        data = pd.read_csv('datasets/total_daily_transact.csv')
        return data

    # data = load_data_transctions() 

    # Filter transactions function
    def get_completed_cash_in_transactions(data):
        # Filter for 'Completed' status and 'Cash in' transaction type
        filtered_data = data[(data['STATUS'] == 'Completed') & (data['TRANSACTION_TYPE'] == 'Cash in')]
        return filtered_data


    @st.cache_data
    def load_data_pep():
        # Load your DataFrame here
        bet_data = pd.read_csv('datasets/pep_ops.csv', encoding = "cp1252")
        return bet_data
    

    @st.cache_data
    def load_data_2():
        # Load your DataFrame here
        df = pd.read_csv('datasets/saldo_por_org.csv')
        return df
    
    df_2 = load_data_2()

    @st.cache_data
    def load_data_3():
        # Load your DataFrame here
        df = pd.read_csv('datasets/total_de_contas_criadas.csv')
        return df
    
    df_3 = load_data_3()

    @st.cache_data
    def load_data_4():
        # Load your DataFrame here
        df = pd.read_csv('datasets/contas_activas_por_niveis.csv')
        return df
    
    df_4 = load_data_4()


    # st.dataframe(df)
    # df


    # -------------------------LAYOUT USING COLUMNS col = st.columns(1,2,3)
    # Display the Recent Sales table
    st.header('PEP TRANSACTIONS')
    #st.write('Clientes com carregamentos acima de 50.000 Kzs.')

    df_pep = load_data_pep()

    filtered_column_bet = df_pep[['NAME','MSISDN','REASON_TYPE','TRANSACTION_TYPE', 'TOTAL_AMOUNT_AOA']]

    filtered_df = df_pep
    df_pep['MSISDN'] = df_pep['MSISDN'].astype("category")
    # df_pep['DATA_CARREGAMENTO'] = df_pep['DATA_CARREGAMENTO'].astype("category")
    # st.write(df_bet)
    columns =['NAME','TRANSACTION_TYPE',"TOTAL_AMOUNT_AOA"]
    total_amount_by_type = filtered_column_bet.groupby(['NAME','TRANSACTION_TYPE'])['TOTAL_AMOUNT_AOA'].sum().reset_index()
    # valor_acimade50 = df_pep[(df_pep["VALOR_CARREGADO"] > 50000)]

    st.dataframe(total_amount_by_type[columns],
                column_config ={
                    "TOTAL_AMOUNT_AOA": st.column_config.ProgressColumn("Valor", format="%d", min_value=0, max_value=300000),
                    # "MSIDN":st.column_config.NumberColumn(),
                    "NAME":st.column_config.TextColumn(),
                    "TRANSACTION_TYPE": st.column_config.TextColumn(),
                    # "Flag": st.column_config.ImageColumn("Country"),
                    }, height=200, width = 1300)

    total_per_pep_col = df_pep[['NAME','TRANSACTION_TYPE','TOTAL_AMOUNT_AOA']]

    total_per_pep = total_per_pep_col.groupby(['TRANSACTION_TYPE','NAME'])['TOTAL_AMOUNT_AOA'].sum().reset_index()
        
        # second dashboard
    fig_reason_type = go.Figure()

    for transaction_type, sub_df in total_per_pep.groupby('TRANSACTION_TYPE'):
            for name, sub_sub_df in sub_df.groupby('NAME'):
                fig_reason_type.add_trace(go.Bar(
                    x=[transaction_type],  # Set the x-axis value to TRANSACTION_TYPE
                    y=[sub_sub_df['TOTAL_AMOUNT_AOA'].sum()],  # Sum of TOTAL_AMOUNT_AOA for each NAME under TRANSACTION_TYPE
                    text=[sub_sub_df['TOTAL_AMOUNT_AOA'].sum()],  # Set text to the sum of TOTAL_AMOUNT_AOA
                    textposition='auto',
                    name=name,
                ))
        # Update layout if needed
    fig_reason_type.update_layout(
    title='PEP OPS',
    # xaxis_title='Reason Type',
    yaxis_title='Total Amount AOA')

    st.plotly_chart(fig_reason_type, use_container_width=False)

    # st.write(total_per_pep)


    col1, col2 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col_a, col_b = st.columns(2)

    col9, col10 = st.columns(2)

def main():
    page2()


if __name__ == "__main__":
    main()