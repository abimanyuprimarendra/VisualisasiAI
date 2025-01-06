
# Load dataset
@st.cache
def load_data_from_drive():
    csv_url = "https://drive.google.com/uc?id=1lto09pdlh825Gv0TfBUkgk1e2JVQW19c"
    data = pd.read_csv(csv_url)
    return data

data = load_data_from_drive()

# Sidebar untuk filter dan informasi
st.sidebar.title("Dashboard Visualisasi AI Global Index")
st.sidebar.metric("Jumlah Negara", data['Country'].nunique())
st.sidebar.metric("Jumlah Cluster", data['Cluster'].nunique())

# Pilihan Visualisasi
options = st.selectbox(
    "Pilih Visualisasi:",
    ["Distribusi Total Score", "Scatter Plot", "Peta Geografis", 
     "Box Plot", "Pie Chart", "Bubble Chart"]
)

# Filter data awal (gunakan seluruh data terlebih dahulu)
filtered_data = data.copy()

# Filter cluster hanya jika diperlukan
if options == "Distribusi Total Score":
    st.subheader("Total Score per Country Berdasarkan Region dan Cluster")
    
    # Filter region
    region_filter = st.multiselect("Pilih Region:", data['Region'].unique(), default=data['Region'].unique())
    filtered_data = data[data['Region'].isin(region_filter)]
    
    # Filter rentang total score
    score_range = st.slider("Pilih Rentang Total Score:",
                            min_value=int(data['Total score'].min()),
                            max_value=int(data['Total score'].max()),
                            value=(int(data['Total score'].min()), int(data['Total score'].max())))
    filtered_data = filtered_data[(filtered_data['Total score'] >= score_range[0]) & 
                                  (filtered_data['Total score'] <= score_range[1])]
    
    # Filter cluster
    cluster_filter = st.multiselect("Pilih Cluster:", data['Cluster'].unique(), default=data['Cluster'].unique())
    filtered_data = filtered_data[filtered_data['Cluster'].isin(cluster_filter)]
    
    # Loop untuk membuat diagram batang per region dan cluster
    for region in filtered_data['Region'].unique():
        region_data = filtered_data[filtered_data['Region'] == region]
        
        fig = px.bar(
            region_data, 
            x='Country', 
            y='Total score', 
            color='Cluster',  # Menambahkan warna berdasarkan cluster
            title=f'Total Score untuk Region: {region}',
            labels={'Total score': 'Total Score', 'Country': 'Country'},
            text='Total score',  # Menampilkan nilai pada batang
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        # Menambahkan teks dan memiringkan label Country untuk lebih rapi
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_tickangle=-45,  # Memiringkan nama negara untuk lebih rapi
            width=1000,           # Lebar diagram
            height=600            # Tinggi diagram
        )
        
        # Menampilkan diagram untuk region tertentu
        st.plotly_chart(fig)


elif options == "Scatter Plot":
    st.subheader("Hubungan Talent dan Infrastructure Berdasarkan Income Group")

    fig = px.scatter(
        filtered_data, x='Talent', y='Infrastructure',
        color='Income group', size='Total score', hover_data=['Country'],
        title="Scatter Plot Talent vs Infrastructure",
        labels={'Talent': 'Talent', 'Infrastructure': 'Infrastructure'}
    )
    st.plotly_chart(fig)

elif options == "Peta Geografis":
    st.subheader("Peta Geografis Total Score per Country")
    
    # Menambahkan filter untuk region
    region_filter = st.multiselect("Pilih Region:", data['Region'].unique(), default=data['Region'].unique())
    filtered_data = filtered_data[filtered_data['Region'].isin(region_filter)]

    # Membuat peta choropleth
    fig = px.choropleth(
        filtered_data,
        locations='Country',
        locationmode='country names',
        color='Total score',
        hover_name='Country',
        title='Total Score per Country',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig)


elif options == "Box Plot":
    st.subheader("Box Plot Berdasarkan Cluster")
    fig = px.box(
        filtered_data, x='Cluster', y='Talent', color='Cluster', title="Box Plot Talent per Cluster",
        labels={'Talent': 'Talent', 'Cluster': 'Cluster'}
    )
    st.plotly_chart(fig)

    fig = px.box(
        filtered_data, x='Cluster', y='Infrastructure', color='Cluster', title="Box Plot Infrastructure per Cluster",
        labels={'Infrastructure': 'Infrastructure', 'Cluster': 'Cluster'}
    )
    st.plotly_chart(fig)

elif options == "Pie Chart":
    st.subheader("Pie Chart untuk Political Regime")
    fig = px.pie(
        filtered_data, names='Political regime', title='Distribusi Political Regime',
        labels={'Political regime': 'Political Regime'}
    )
    st.plotly_chart(fig)

elif options == "Bubble Chart":
    st.subheader("Bubble Chart: Talent vs Infrastructure Berdasarkan Political Regime")

    fig = px.scatter(
        filtered_data, x='Talent', y='Infrastructure', size='Total score', color='Political regime',
        hover_data=['Country'], title="Bubble Chart Talent vs Infrastructure by Political Regime",
        labels={'Talent': 'Talent', 'Infrastructure': 'Infrastructure'}
    )
    st.plotly_chart(fig)
