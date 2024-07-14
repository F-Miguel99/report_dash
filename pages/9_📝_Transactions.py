import streamlit as st
import cx_Oracle
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
# from authentication import authenticate_user
from authentication import is_authenticated


showSidebarNavigation = False
def page1():


    #Check if the user is authenticated before rendering the content
    if not is_authenticated(st.session_state.username, st.session_state.password):
        st.error("Access denied. Please login.")
        st.stop()

    showSidebarNavigation = True
    img = Image.open('unitel-logo.png')


    st.set_page_config(
        page_title="Transactions",
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


    # Create a function to plot the bar chart
    def plot_worldwide_sales():
        years = np.array([2016, 2017, 2018, 2019, 2020, 2021, 2022])
        sales_usa = np.random.randint(10, 100, size=len(years))
        sales_uk = np.random.randint(10, 100, size=len(years))
        sales_au = np.random.randint(10, 100, size=len(years))

        plt.figure(figsize=(10, 5))
        plt.bar(years - 0.2, sales_usa, width=0.2, color='r', align='center', label='USA')
        plt.bar(years, sales_uk, width=0.2, color='g', align='center', label='UK')
        plt.bar(years + 0.2, sales_au, width=0.2, color='b', align='center', label='AU')
        plt.xlabel('Year')
        plt.ylabel('Sales')
        plt.title('Worldwide Sales')
        plt.legend()
        st.pyplot(plt)


    def plot_sales_and_revenue():
        years = np.array([2016, 2017, 2018, 2019, 2020, 2021, 2022])
        sales = np.random.randint(50, 300, size=len(years))
        revenue = np.random.randint(50, 300, size=len(years))

        plt.figure(figsize=(10, 5))
        plt.fill_between(years, sales, color='r', alpha=0.3, label='Sales')
        plt.fill_between(years, revenue, color='b', alpha=0.3, label='Revenue')
        plt.plot(years, sales, color='r')
        plt.plot(years, revenue, color='b')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.title('Sales & Revenue')
        plt.legend()
        st.pyplot(plt)

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
    def load_data_1():
        # Load your DataFrame here
        df = pd.read_csv('datasets/saldo_por_niveis.csv')
        return df
    
    df_1 = load_data_1()

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


    # Custom styles to match the card design
    st.markdown("""
    <style>
    .card {
        background-color: #222; /* Adjust the card background color as needed */
        color: #fff; /* Adjust the text color as needed */
        padding: 20px;
        margin: 10px;
        border-radius: 5px; /* Adjust the border radius as needed */
    }
    .value {
        font-size: 24px; /* Adjust the font size as needed */
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    def display_card(icon, label, value):
        # You might want to replace 'icon' with actual Streamlit components or custom HTML
        st.markdown(f"""
        <div class="card">
            <div>{icon}</div>
            <div>{label}</div>
            <div class="value">{value}</div>
        </div>
        """, unsafe_allow_html=True)






    # -------------------------LAYOUT USING COLUMNS col = st.columns(1,2,3)
    col1, col2, col3, col4 = st.columns(4)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)

    data = load_data_transctions()
    completed_stats = data[(data["STATUS"] == "Completed")] #  & (data['TRANSACTION_TYPE'] == 'Pay Bill')]  
    selected = completed_stats[['STATUS','TRANSACTION_TYPE','TOTAL_AMOUNT_AOA']]

    columns =['STATUS','TRANSACTION_TYPE','TOTAL_AMOUNT_AOA']
    data.rename(columns={'TRANSACTION_TYPE' :'TRANSACTION TYPE'}, inplace=True)
    # total_amount_by_type = completed_stats.groupby('TRANSACTION_TYPE')['TOTAL_AMOUNT_AOA'].sum().reset_index()
    total_amount_by_type = selected.groupby(['TRANSACTION_TYPE', 'STATUS'])['TOTAL_AMOUNT_AOA'].sum().reset_index()

    # st.write(total_amount_by_type)

    st.dataframe(total_amount_by_type[columns], hide_index=True,
                column_config ={
                    "TOTAL_AMOUNT_AOA": st.column_config.ProgressColumn("Valor", format="%d", min_value=0, max_value=400000000),
                    # "MSIDN":st.column_config.NumberColumn(),
                    "STATUS":st.column_config.TextColumn(),
                    "TRANSACTION TYPE": st.column_config.TextColumn(),
                    # "Flag": st.column_config.ImageColumn("Country"),
                    }, height=200, width = 1300)


    col_a, col_b = st.columns(2)

    col_c, col_d = st.columns(2)

    col9, col10 = st.columns(2)



    with col1:
        data = load_data_transctions()
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Cash In')]
        total_amount_by_type = completed_stats.groupby('TRANSACTION_TYPE')['TOTAL_AMOUNT_AOA'].sum().reset_index()
        # only_value = total_amount_by_type.iloc[0][['TOTAL_AMOUNT_AOA']]
        only_value = total_amount_by_type['TOTAL_AMOUNT_AOA'].iloc[0].item() 
        # st.metric(label="Cash In", value=f"{only_value:,}")
        # st.metric(label="Cash In", value=f"${only_value:,.2f}")
        display_card("📈", "Cash In", f"AOA {only_value:,}")
        # display_card("Cash In", only_value)
        # st.markdown(f"## ${only_value}")

    with col2:
        data = load_data_transctions()
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Cash Out')]
        total_amount_by_type = completed_stats.groupby('TRANSACTION_TYPE')['TOTAL_AMOUNT_AOA'].sum().reset_index()
        only_value = total_amount_by_type['TOTAL_AMOUNT_AOA'].iloc[0].item() 
        display_card("📊", "Cash Out", f"AOA {only_value:,}")

    with col3:
        data = load_data_transctions()
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Airtime Purchase')]
        total_amount_by_type = completed_stats.groupby('TRANSACTION_TYPE')['TOTAL_AMOUNT_AOA'].sum().reset_index()
        only_value = total_amount_by_type['TOTAL_AMOUNT_AOA'].iloc[0].item() 
        display_card("💰", "Airtime Purchase", f"AOA {only_value:,}")

    with col4:
        data = load_data_transctions()
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Send Money')]
        total_amount_by_type = completed_stats.groupby('TRANSACTION_TYPE')['TOTAL_AMOUNT_AOA'].sum().reset_index()
        only_value = total_amount_by_type['TOTAL_AMOUNT_AOA'].iloc[0].item() 
        display_card("🏦", "Send Money", f"AOA {only_value:,}")

    with col5:
        data = load_data_transctions()
        filtered_data = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Cash Out')]
        dta = filtered_data[['TOTAL_AMOUNT_AOA', 'STATUS', 'REASON_TYPE']]
        dta.rename(columns={'REASON_TYPE' :'REASON TYPE', 'TOTAL_AMOUNT_AOA': 'TOTAL AMOUNT AOA'}, inplace=True)

        # st.header('Total Amount by Status')
        fig_status = px.bar(
        dta.groupby(['REASON TYPE'])['TOTAL AMOUNT AOA'].sum().reset_index(),
        x='REASON TYPE',
        y='TOTAL AMOUNT AOA',
        title='Cash Out by Description'
        )
        # st.plotly_chart(fig_status)
        # st.write(dta)

        # second dashboard
        fig_reason_type = go.Figure()
        for reason_type, sub_df in dta.groupby('REASON TYPE'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['REASON TYPE'],
                y=sub_df['TOTAL AMOUNT AOA'],
                text=sub_df['TOTAL AMOUNT AOA'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
        fig_reason_type.update_layout(
        title='Cash Out by Description',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type)

    with col6:
        data = load_data_transctions()
        filtered_data = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Send Money')]
        dta = filtered_data[['TOTAL_AMOUNT_AOA', 'STATUS', 'REASON_TYPE']]
        dta.rename(columns={'REASON_TYPE' :'REASON TYPE', 'TOTAL_AMOUNT_AOA': 'TOTAL AMOUNT AOA'}, inplace=True)
        

        # st.header('Total Amount by Status')
        fig_status = px.bar(
        dta.groupby(['REASON TYPE'])['TOTAL AMOUNT AOA'].sum().reset_index(),
        x='REASON TYPE',
        y='TOTAL AMOUNT AOA',
        title='Send Money by Description'
        )
        # st.plotly_chart(fig_status)

        # second dashboard
        # Plotly with text
        fig_reason_type = go.Figure()
        # Add the bar traces with text labels 1 CHOICE
        for reason_type, sub_df in dta.groupby('REASON TYPE'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['REASON TYPE'],
                y=sub_df['TOTAL AMOUNT AOA'],
                text=sub_df['TOTAL AMOUNT AOA'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
        fig_reason_type.update_layout(
        title='Send Money by Description',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type)



    with col7:

        fig_status = px.bar(
        dta.groupby('REASON TYPE')['TOTAL AMOUNT AOA'].sum().reset_index(),
        x='REASON TYPE',
        y='TOTAL AMOUNT AOA',
        title='Cash In by Description'
        )
        # st.plotly_chart(fig_status)
        # st.write(dta)

        # Second Dashboard
        fig_reason_type = go.Figure()
        # Add the bar traces with text labels 1 CHOICE
        for reason_type, sub_df in dta.groupby('REASON TYPE'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['REASON TYPE'],
                y=sub_df['TOTAL AMOUNT AOA'],
                text=sub_df['TOTAL AMOUNT AOA'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
        fig_reason_type.update_layout(
        title='Cash In by Description',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type)

    with col8:

        data = load_data_transctions()
        filtered_data = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Airtime Purchase')]
        dta = filtered_data[['TOTAL_AMOUNT_AOA', 'STATUS', 'REASON_TYPE']]
        dta.rename(columns={'REASON_TYPE' :'REASON TYPE', 'TOTAL_AMOUNT_AOA': 'TOTAL AMOUNT AOA'}, inplace=True)
        


        fig_status = px.bar(
        dta.groupby(['REASON TYPE'])['TOTAL AMOUNT AOA'].sum().reset_index(),
        x='REASON TYPE',
        y='TOTAL AMOUNT AOA',
        title='Airtime Purchase by Description'
        )

        # Second Dashboard
        fig_reason_type = go.Figure()
        # Add the bar traces with text labels 1 CHOICE
        for reason_type, sub_df in dta.groupby('REASON TYPE'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['REASON TYPE'],
                y=sub_df['TOTAL AMOUNT AOA'],
                text=sub_df['TOTAL AMOUNT AOA'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
        fig_reason_type.update_layout(
        title='Airtime Purchase by Description',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type)



    with col_a:
        
        # Load data
        data = load_data_transctions()
        
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Pay Bill')]
        
        selected = completed_stats[['TOTAL_AMOUNT_AOA', 'REASON_TYPE', 'STATUS']]
        
        total_amount_by_type = selected.groupby(['REASON_TYPE', 'STATUS'])['TOTAL_AMOUNT_AOA'].sum().reset_index()


        # Second Dashboard
        fig_reason_type = go.Figure()
        # Add the bar traces with text labels 1 CHOICE
        for reason_type, sub_df in total_amount_by_type.groupby('REASON_TYPE'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['REASON_TYPE'],
                y=sub_df['TOTAL_AMOUNT_AOA'],
                text=sub_df['TOTAL_AMOUNT_AOA'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
        fig_reason_type.update_layout(
        title='Pay Bill by Description',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type)
        


    with col_b:
        
        # Load data
        data = load_data_transctions()
        
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Pay Merchant')]
        
        selected = completed_stats[['TOTAL_AMOUNT_AOA', 'REASON_TYPE', 'STATUS']]
        
        total_amount_by_type = selected.groupby(['REASON_TYPE', 'STATUS'])['TOTAL_AMOUNT_AOA'].sum().reset_index()
    

        # Second Dashboard
        fig_reason_type = go.Figure()
        # Add the bar traces with text labels 1 CHOICE
        for reason_type, sub_df in total_amount_by_type.groupby('REASON_TYPE'):
            fig_reason_type.add_trace(go.Bar(
                x=sub_df['REASON_TYPE'],
                y=sub_df['TOTAL_AMOUNT_AOA'],
                text=sub_df['TOTAL_AMOUNT_AOA'],
                textposition='auto',
                name=reason_type,
                # marker_color='rgba(55, 128, 191, 0.7)',  # Custom color
                # marker_color=[f'rgba({r}, {g}, {b}, 0.7)' for r, g, b in zip(sub_df['r_column'], sub_df['g_column'], sub_df['b_column'])]
            ))
        # Update layout if needed
        fig_reason_type.update_layout(
        title='Pay Merchant by Description',
        # xaxis_title='Reason Type',
        yaxis_title='Total Amount AOA')

        st.plotly_chart(fig_reason_type)

    with col_c:
        # st.text('Completed "Pay Bill" Transactions')
        
        # Load data
        data = load_data_transctions()
        
        completed_stats = data[(data["STATUS"] == "Completed") & (data['TRANSACTION_TYPE'] == 'Pay Bill')]
        
        selected = completed_stats[['TOTAL_AMOUNT_AOA', 'REASON_TYPE', 'STATUS']]
        total_amount_by_type = selected.groupby(['REASON_TYPE', 'STATUS'])['TOTAL_AMOUNT_AOA'].sum().reset_index()
    
        # st.write(total_amount_by_type)


def main():
    page1()


if __name__ == "__main__":
    main()
  