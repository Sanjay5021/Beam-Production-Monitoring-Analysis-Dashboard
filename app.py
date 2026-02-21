import streamlit as st
import pandas as pd



st.set_page_config(
    page_title="Sanjay's Beam stock report ",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
    <style>
        .main-title {
            font-size:40px !important;
            font-weight:700;
            color:#1f77b4;
        }
        .sub-text {
            font-size:18px;
            color:gray;
        }
        .stDataFrame {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)




st.markdown('<p class="main-title">📊 Sanjay Beam Stock Details Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Upload your production Excel file and analyze beam data interactively.</p>', unsafe_allow_html=True)

st.divider()

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    df1=pd.read_excel(uploaded_file,sheet_name='Sizing')
    #latest_row = df1.iloc[-1]
    #latest_beam_no = latest_row["Beam no"]
    df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce').dt.date
    #latest_date = df1['Date'].max()
    #formatted_date = latest_date.strftime("%d-%m-%Y") 
    df2=pd.read_excel(uploaded_file,sheet_name='Sectional')
    #latest_row = df2.iloc[-1]
    #latest_beam_no = latest_row["Beam no"]
    df2['Date'] = pd.to_datetime(df2['Date'], errors='coerce').dt.date
    #latest_date = df2['Date'].max()
    #formatted_date = latest_date.strftime("%d-%m-%Y")

    st.sidebar.header("🔎 Filter Options")
    option = st.sidebar.selectbox(
        "Select Beam Type",
        ["Tissue Beam", "Asha Beam"]
    )

    
    
    if option == "Tissue Beam":
        df_ts=df1[['Date','Beam no','Set no','WO','SAP Beam Mtr']]
        df_ts.dropna(how='all',inplace=True)
        df_ts = df_ts[df_ts['Beam no'].notna()]
        df_ts.ffill(inplace=True)
        st.subheader(f"Tissue Beams")
        st.dataframe(df_ts)
        beam_list = df_ts['Beam no'].unique()
    else:
        df_asha=df2[['Date','Beam no','Set no','Work order','SAP Beam Mtr']]
        df_asha.dropna(how='all',inplace=True)
        df_asha.ffill(inplace=True)
        st.subheader(f"Asha Beams")
        st.dataframe(df_asha)
        beam_list = df_asha['Beam no'].unique()

    st.divider()
   
    bn = st.selectbox("Select Beam no", beam_list)

    if option == "Tissue Beam":
        df_bn = df_ts[df_ts['Beam no'] == bn]
        st.dataframe(df_bn)
    else:
        df_bn = df_asha[df_asha['Beam no'] == bn]
        st.dataframe(df_bn)







