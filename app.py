import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Police Reports Dashboard",
                   page_icon=":police_car:",
                   layout="wide")

@st.cache
def get_data_from_excel():
    df = pd.read_excel("Police_Department_Incident_Reports__2018_to_Present_1.xlsx")
    df["Hour"] = pd.to_datetime(df["Incident Time"], format= "%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()
#st.dataframe(df)

#---SIDEBAR----
st.sidebar.header("Please filter here:")
day = st.sidebar.multiselect(
    "Select the week day",
    options=df["Incident Day of Week"].unique(),
    default=df["Incident Day of Week"].unique()
)

category = st.sidebar.multiselect(
    "Select the Incident Category",
    options=df["Incident Category"].unique(),
    default=df["Incident Category"].unique()
)

neighborhood = st.sidebar.multiselect(
    "Select the Neighborhood",
    options=df["Analysis Neighborhood"].unique(),
    default=df["Analysis Neighborhood"].unique()
)

df_selection = df.query(
    "`Incident Day of Week` == @day & `Incident Category` == @category & `Analysis Neighborhood` == @neighborhood"
)

#st.dataframe(df_selection)

#----MAINPAGE----
st.title(":police_car: Police Reports Dashboard")
st.markdown("##")

# TOP KPI's
total_incidents = df_selection.shape[0]
recuento_resolucion = df_selection['Incident Category'].value_counts()
porcentaje_resolucion = recuento_resolucion / len(df_selection) * 100

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Incidents:")
    st.subheader(total_incidents)
with right_column:
    st.subheader("Percentage of Incidents per Category:")
    st.subheader(porcentaje_resolucion)


st.markdown("---")

#PERCENTAGE OF INCIDENTS PER DAY
porcentaje_dias = df_selection["Incident Day of Week"].value_counts(normalize=True) * 100
porcentaje_dias = porcentaje_dias.reset_index()
porcentaje_dias.columns = ["Incident Day of Week","Percentage"]
fig_day = px.pie(porcentaje_dias, values="Percentage", names="Incident Day of Week", title="Percentage of Incidents per Day")

st.plotly_chart(fig_day)

#INCIDENTS PER HOUR
incidents_hour = df_selection['Hour'].value_counts().reset_index()
incidents_hour.columns = ['Hour','Count']
fig_hour = px.bar(incidents_hour, x='Hour', y='Count', title = "Number of Incidents per Hour")

st.plotly_chart(fig_hour)

#PERCENTAGE OF INCIDENTS PER NEIGHBORHOOD
porcentaje_barrio = df_selection["Analysis Neighborhood"].value_counts(normalize=True) * 100
porcentaje_barrio = porcentaje_barrio.reset_index()
porcentaje_barrio.columns = ["Analysis Neighborhood","Percentage"]
fig_barrio = px.pie(porcentaje_barrio, values="Percentage", names="Analysis Neighborhood", title="Percentage of Incidents per Neighborhood")

st.plotly_chart(fig_barrio)