import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import base64
from fpdf import FPDF
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
        page_title="BET Enterprises",
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
    def load_data_bet():
        # Load your DataFrame here
        bet_data = pd.read_csv('datasets/bet_credito_all_in.csv', encoding = "cp1252")
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
    st.header('Empresas de Apostas')
    st.write('Clientes com carregamentos acima de 50.000 Kzs.')

    df_bet = load_data_bet()

    filtered_column_bet = df_bet[['NAME','BET','VALOR_CARREGADO']]

    filtered_df = df_bet
    df_bet['MSISDN'] = df_bet['MSISDN'].astype("category")
    df_bet['DATA_CARREGAMENTO'] = df_bet['DATA_CARREGAMENTO'].astype("category")
    # st.write(df_bet)
    columns =['NAME','BET',"VALOR_CARREGADO"]
    valor_acimade50 = df_bet[(df_bet["VALOR_CARREGADO"] > 50000)]

    st.dataframe(valor_acimade50[columns],
                column_config ={
                    "VALOR_CARREGADO": st.column_config.ProgressColumn("Valor", format="%d", min_value=0, max_value=300000),
                    # "MSIDN":st.column_config.NumberColumn(),
                    "NAME":st.column_config.TextColumn(),
                    "BET": st.column_config.TextColumn(),
                    # "Flag": st.column_config.ImageColumn("Country"),
                    }, height=200, width = 1300)

    total_per_bet_col = df_bet[['BET','VALOR_CARREGADO']]

    st.write('---')

    total_per_bet = total_per_bet_col.groupby(['BET'])['VALOR_CARREGADO'].sum().reset_index()
        
        # second dashboard
    fig_reason_type = go.Figure()

    for reason_type, sub_df in total_per_bet.groupby('BET'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['BET'],
                y=sub_df['VALOR_CARREGADO'],
                text=sub_df['VALOR_CARREGADO'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
    fig_reason_type.update_layout(
    title='BET CREDIT',
    # xaxis_title='Reason Type',
    yaxis_title='Total Amount AOA')

    st.plotly_chart(fig_reason_type, use_container_width=False)

    # st.write(total_per_bet)


    col1, col2 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col_a, col_b = st.columns(2)

    col9, col10 = st.columns(2)

def main():
    page2()


if __name__ == "__main__":
    main()