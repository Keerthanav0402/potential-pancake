import pandas as pd
import openpyxl
import io
import streamlit as st
from streamlit_option_menu import option_menu

output = io.BytesIO()

app_mode = option_menu(None, ["Project_1","Project_2"],
                    icons=['sliders','kanban'],
                    menu_icon="app-indicator", default_index=0,
                    styles={
        "container": {"padding": "5!important", "background-color": "#f0f2f6"},
        "icon": {"color": "orange", "font-size": "28px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2C3845"},
                    }
)

if app_mode == "Project_1":
    st.title("Welcome To Project_1")
    input_data = st.file_uploader("Upload a Input Data",type=['csv'])

    if input_data is not None:

        df=pd.read_csv(input_data)
        
        df2=df[['External Code','Processing Group Code','Best Received External Description']]
        df2['process']=""
        for i in range(len(df2)):
            txt=df2.loc[i,'Processing Group Code']
            if txt=='KVT':
                df2.loc[i,'process']='out of scope'
            else:
                df2.loc[i,'process']='inscope'


        df3=df2[df2['process']=='inscope']

        writer = pd.ExcelWriter("sample.xlsx", engine="xlsxwriter")
        writer.book.filename = output

        df3.to_excel(writer,sheet_name="Output",index=False)
        df.to_excel(writer,sheet_name="Input Data",index=False)

        writer.save()
        writer.close()

        st.success("Completed Successfully")
        st.info("Please Click Download Button")

        st.download_button(
            label="Download Output",
            data = output.getvalue(),
            file_name="output.xlsx",
            mime="application/vnd.ms-excel"
        )
