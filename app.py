import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Beam Stock Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM STYLE ----------------
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

# ---------------- HEADER ----------------
st.markdown('<p class="main-title">📊 Beam Stock Details Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Upload your production Excel file and analyze beam data interactively.</p>', unsafe_allow_html=True)

st.divider()

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:

    df1 = pd.read_excel(uploaded_file, sheet_name='Sizing')
    df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce').dt.date

    df2 = pd.read_excel(uploaded_file, sheet_name='Sectional')
    df2['Date'] = pd.to_datetime(df2['Date'], errors='coerce').dt.date

    # ---------------- SIDEBAR ----------------
    st.sidebar.header("🔎 Filter Options")
    option = st.sidebar.selectbox(
        "Select Beam Type",
        ["Tissue Beam", "Asha Beam"]
    )

    # ---------------- MAIN DISPLAY ----------------
    if option == "Tissue Beam":
        df_ts = df1[['Date','Beam no','Set no','WO','SAP Beam Mtr']]
        df_ts.dropna(how='all', inplace=True)
        df_ts.ffill(inplace=True)

        st.subheader("🧵 Tissue Beams Data")
        st.dataframe(df_ts, use_container_width=True)

        beam_list = df_ts['Beam no'].unique()

    else:
        df_asha = df2[['Date','Beam no','Set no','Work order','SAP Beam Mtr']]
        df_asha.dropna(how='all', inplace=True)
        df_asha.ffill(inplace=True)

        st.subheader("🧶 Asha Beams Data")
        st.dataframe(df_asha, use_container_width=True)

        beam_list = df_asha['Beam no'].unique()

    st.divider()

    # ---------------- BEAM SELECTION ----------------
    bn = st.selectbox("🎯 Select Beam No", beam_list)

    if option == "Tissue Beam":
        df_bn = df_ts[df_ts['Beam no'] == bn]
    else:
        df_bn = df_asha[df_asha['Beam no'] == bn]

    st.subheader("📌 Selected Beam Details")
    st.dataframe(df_bn, use_container_width=True)

   
