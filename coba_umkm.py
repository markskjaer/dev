# -- coding: utf-8 --
"""
Created on Wed Oct  4 11:54:31 2023

@author: Asus
"""

import streamlit as st
import pandas as pd
import openpyxl as opy

st.title("UMKM Sekarwangi")

st.sidebar.markdown("### Data")

### Import Data Lengkap

uploaded_file = st.file_uploader("Choose a file", type = 'xlsx', accept_multiple_files=False)
dataumkm = pd.read_excel(uploaded_file)

#dataumkm = pd.read_excel("C:/Users/wella/Documents/Asha/SMT7/magang/DESA SEKARWANGI/Data UMKM Sekarwangi_ready.xlsx")
df = dataumkm
type(dataumkm)
dataumkm["NIK"] = dataumkm["NIK"].astype("string")
dataumkm["No HP"] = dataumkm["No HP"].astype("string")
#st.write(dataumkm)

### Filter Data

from pandas.api.types import(
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
    )

st.subheader("Data Lengkap UMKM Desa Sekarwangi")
st.write("Pilih kolom yang ingin ditampilkan")

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan UI di atas dataframe untuk memungkinkan pengguna melakukan filter kolom

    Args:
        df(pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe

    Sumber: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
    """
    modify = st.checkbox("Tambahkan filter")
    if not modify:
        return df
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter data berdasarkan", dataumkm.columns)
        for column in to_filter_columns:
            left, right = st.columns((1,20))
            left.write("↳")
            #Treat columns with < 10 unique values a s categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                    )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                 f"Values for {column}",
                 min_value=_min,
                 max_value=_max,
                 value=(_min, _max),
                 step=step,
            )
            df = df[df[column].between(*user_num_input)]
        return df
filtered_df = filter_dataframe(df)
### Opsi Download Data


@st.cache_data
def convert_df(filtered_df):
    return filtered_df.to_csv().encode('utf-8')
csv = convert_df(filtered_df)
st.download_button(
    label = "Unduh Data",
    data = csv,
    file_name='download_sekarwangi.csv',
    mime='text/csv',
    )

st.dataframe(filtered_df)   #menampilkan hasil filter



### Import Masing-Masing Data + coding untuk kolom yang belum ada
## Import/upload file
## Coding kolom baru
# RT/RW
# Kategori Usaha
# Status DTKS dan P3KE
# Usia


### Pivot Table

st.subheader("Pivot Table")

df = pd.DataFrame(dataumkm)
kolom_1 = st.selectbox("Pilih Karakteristik Pertama", dataumkm.columns)
kolom_2 = st.selectbox("Pilih Karakteristik Kedua", dataumkm.columns)

#tabel_kontingensi = pd.crosstab(dataumkm[kolom_1], dataumkm[kolom_2])
#st.write(tabel_kontingensi)

#pivot2 = df.pivot_table(index = kolom_1,
#                             values = kolom_2,
#                             aggfunc = "count"
#                             )
#st.write(pivot2)

st.subheader("Pivot Lagi")

pivot3 = df.pivot_table(index = [kolom_1,kolom_2],
                             values = ['NAMA PEMILIK'],
                             aggfunc = "count"
                             )
st.write(pivot3)

st.write("ini contoh pivot fixed")

pivot = df.pivot_table(index = ['KATEGORI','STATUS P3KE DAN DTKS'],
                             values = ['PENDAPATAN PER BULAN'],
                             aggfunc = "sum"
                             )
st.write(pivot)

#Bar Chart
st.subheader("Barchart Jumlah Usaha Menurut Kategori dan Status P3KE dan DTKS")
tes = pd.crosstab(dataumkm['STATUS P3KE DAN DTKS'],dataumkm['KATEGORI'])
#st.write(tes)
st.bar_chart(data = tes, height = 700)

#Scatter Plot
#st.scatter_chart(data = dataumkm,
#                 x = 'BESARNYA MODAL USAHA',
#                 y = 'PENDAPATAN PER BULAN')

import plotly.express as px
fig = px.scatter(
    data_frame=dataumkm, x="BESARNYA MODAL USAHA", y="PENDAPATAN PER BULAN",color=kolom_1,symbol=kolom_2 , title="Scatter Test",
)
st.plotly_chart(fig)
