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
        #  page_title="CCAF - REALTIME",
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
    def load_client_data():
        # Load your DataFrame here / CSV file
        data = pd.read_csv('datasets/single_clients_balance.csv', encoding = "cp1252")
        return data

    # data = load_data_transctions() 

    # Filter transactions function
    def get_completed_cash_in_transactions(data):
        # Filter for 'Completed' status and 'Cash in' transaction type
        filtered_data = data[(data['STATUS'] == 'Completed') & (data['TRANSACTION_TYPE'] == 'Cash in')]
        return filtered_data


    @st.cache_data
    def load_enterprise_client_data():
        # Load your DataFrame here
        enterprise_data = pd.read_csv('datasets/enterprise_clients_balance.csv', encoding = "cp1252")
        return enterprise_data
    

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
    st.header('Top Clients Balance')
    #st.write('Clientes com carregamentos acima de 50.000 Kzs.')

    df_sngle_clnt = load_client_data()

    filtered_column_clnt = df_sngle_clnt[['NAME','MSISDN','TOTAL_BALANCE','ACCOUNT_STATUS', 'TRUST_LEVEL']]

    filtered_df = df_sngle_clnt
    df_sngle_clnt['MSISDN'] = df_sngle_clnt['MSISDN'].astype("category")
    # df_pep['DATA_CARREGAMENTO'] = df_pep['DATA_CARREGAMENTO'].astype("category")
    # st.write(df_bet)
    columns =['NAME','TRUST_LEVEL',"TOTAL_BALANCE"]
    total_amount_by_type = df_sngle_clnt.groupby(['NAME','TRUST_LEVEL'])['TOTAL_BALANCE'].sum().reset_index()
    # valor_acimade50 = df_pep[(df_pep["VALOR_CARREGADO"] > 50000)]

    st.dataframe(filtered_column_clnt[columns], hide_index=True,
                column_config ={
                    "TOTAL_BALANCE": st.column_config.ProgressColumn("Valor", format="%d", min_value=0, max_value=20000000),
                    # "MSIDN":st.column_config.NumberColumn(),
                    "NAME":st.column_config.TextColumn(),
                    "TRUST_LEVEL": st.column_config.TextColumn(),
                    # "Flag": st.column_config.ImageColumn("Country"),
                    }, height=300, width = 1300)

    # Downloadd Button
    coded_data = base64.b64encode(filtered_column_clnt.to_csv(index=False).encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{coded_data}" download="Top Client Balance.csv" style="float: left;">Download Data </a>',
                unsafe_allow_html=True)

    total_per_clnt_col = df_sngle_clnt[['NAME','TRUST_LEVEL','TOTAL_BALANCE']]

    total_per_clt = total_per_clnt_col.groupby(['TRUST_LEVEL'])['TOTAL_BALANCE'].sum().reset_index()
        
    #--------------------------------------------------------------------------------------


    df_sngle_entprse = load_enterprise_client_data()

    filtered_column_entrpse = df_sngle_entprse[['ORGANIZATION_NAME','ORG_TOTAL_BALANCE','IDENTITY_STATUS', 'TRUST_LEVEL']].head(50)

    filtered_df = df_sngle_entprse

    columns =['ORGANIZATION_NAME','TRUST_LEVEL',"ORG_TOTAL_BALANCE"]
    total_amount_by_type = df_sngle_entprse.groupby(['ORGANIZATION_NAME','TRUST_LEVEL'])['ORG_TOTAL_BALANCE'].sum().reset_index()



    total_per_trust_col = df_sngle_entprse[['ORGANIZATION_NAME','TRUST_LEVEL','ORG_TOTAL_BALANCE']]

    total_per_entprse = total_per_trust_col.groupby(['TRUST_LEVEL'])['ORG_TOTAL_BALANCE'].sum().reset_index()



    col1, col2 = st.columns(2)
    with col1:
        # second dashboard
        fig_reason_type1 = go.Figure()

        for diff_trust_level, sub_df in total_per_clt.groupby('TRUST_LEVEL'):
            fig_reason_type1.add_trace(go.Bar(
                x=sub_df['TRUST_LEVEL'],
                y=sub_df['TOTAL_BALANCE'],
                text=sub_df['TOTAL_BALANCE'],
                textposition='auto',
                name=diff_trust_level,
            ))
            # Update layout if needed
        fig_reason_type1.update_layout(
        title='Total Per Trust Level',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type1, use_container_width=False)

    #st.write(filtered_df)

    with col2:
        # second dashboard
        fig_reason_type = go.Figure()

        for diff_trust_level, sub_df in total_per_entprse.groupby('TRUST_LEVEL'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['ORG_TOTAL_BALANCE'],
                y=sub_df['TRUST_LEVEL'],
                text=sub_df['ORG_TOTAL_BALANCE'],
                textposition='auto',
                name=diff_trust_level,
                orientation='h'
            ))
            # Update layout if needed
        fig_reason_type.update_layout(
        title='Total Per Organization Level',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type, use_container_width=False)

    st.header('Top Organization Balance')
    st.dataframe(filtered_column_entrpse[columns], hide_index=True,
                column_config ={
                    "ORG_TOTAL_BALANCE": st.column_config.ProgressColumn("Valor", format="%d", min_value=0, max_value=200000000),
                    # "MSIDN":st.column_config.NumberColumn(),
                    "NAME":st.column_config.TextColumn(),
                    "TRUST_LEVEL": st.column_config.TextColumn(),
                    # "Flag": st.column_config.ImageColumn("Country"),
                    }, height=300, width = 1300)

    # Downloadd Button
    coded_data = base64.b64encode(filtered_column_entrpse.to_csv(index=False).encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{coded_data}" download="Top Enterprise Balance.csv" style="float: left;">Download Data </a>',
                unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col_a, col_b = st.columns(2)

    col9, col10 = st.columns(2)

def main():
    page2()


if __name__ == "__main__":
    main()