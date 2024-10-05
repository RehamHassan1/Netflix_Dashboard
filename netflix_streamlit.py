import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>Netflix Data Analysis</h1>", unsafe_allow_html=True)
st.divider()

@st.cache_data
def load_data():
    return pd.read_csv('netflix1.csv')
df = load_data()
df2 = df[['show_id', 'title', 'country', 'type']]
df2.dropna(subset=['country'], inplace=True)

continent_map = {
    # Africa
    'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa', 'Burkina Faso': 'Africa',
    'Burundi': 'Africa', 'Cabo Verde': 'Africa', 'Cameroon': 'Africa', 'Central African Republic': 'Africa',
    'Chad': 'Africa', 'Comoros': 'Africa', 'Congo': 'Africa', 'Congo (Democratic Republic)': 'Africa',
    'Djibouti': 'Africa', 'Egypt': 'Africa', 'Equatorial Guinea': 'Africa', 'Eritrea': 'Africa', 'Eswatini': 'Africa',
    'Ethiopia': 'Africa', 'Gabon': 'Africa', 'Gambia': 'Africa', 'Ghana': 'Africa', 'Guinea': 'Africa',
    'Guinea-Bissau': 'Africa', 'Ivory Coast': 'Africa', 'Kenya': 'Africa', 'Lesotho': 'Africa', 'Liberia': 'Africa',
    'Libya': 'Africa', 'Madagascar': 'Africa', 'Malawi': 'Africa', 'Mali': 'Africa', 'Mauritania': 'Africa',
    'Mauritius': 'Africa', 'Morocco': 'Africa', 'Mozambique': 'Africa', 'Namibia': 'Africa', 'Niger': 'Africa',
    'Nigeria': 'Africa', 'Rwanda': 'Africa', 'Sao Tome and Principe': 'Africa', 'Senegal': 'Africa', 'Seychelles': 'Africa',
    'Sierra Leone': 'Africa', 'Somalia': 'Africa', 'South Africa': 'Africa', 'South Sudan': 'Africa', 'Sudan': 'Africa',
    'Tanzania': 'Africa', 'Togo': 'Africa', 'Tunisia': 'Africa', 'Uganda': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
    # Asia
    'Afghanistan': 'Asia', 'Armenia': 'Asia', 'Azerbaijan': 'Asia', 'Bahrain': 'Asia', 'Bangladesh': 'Asia',
    'Bhutan': 'Asia', 'Brunei': 'Asia', 'Cambodia': 'Asia', 'China': 'Asia', 'Cyprus': 'Asia', 'Georgia': 'Asia',
    'India': 'Asia', 'Indonesia': 'Asia', 'Iran': 'Asia', 'Iraq': 'Asia', 'Israel': 'Asia', 'Japan': 'Asia',
    'Jordan': 'Asia', 'Kazakhstan': 'Asia', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia', 'Laos': 'Asia', 'Lebanon': 'Asia',
    'Malaysia': 'Asia', 'Maldives': 'Asia', 'Mongolia': 'Asia', 'Myanmar': 'Asia', 'Nepal': 'Asia', 'North Korea': 'Asia',
    'Oman': 'Asia', 'Pakistan': 'Asia', 'Palestine': 'Asia', 'Philippines': 'Asia', 'Qatar': 'Asia', 'Saudi Arabia': 'Asia',
    'Singapore': 'Asia', 'South Korea': 'Asia', 'Sri Lanka': 'Asia', 'Syria': 'Asia', 'Taiwan': 'Asia', 'Tajikistan': 'Asia',
    'Thailand': 'Asia', 'Timor-Leste': 'Asia', 'Turkey': 'Asia', 'Turkmenistan': 'Asia', 'United Arab Emirates': 'Asia',
    'Uzbekistan': 'Asia', 'Vietnam': 'Asia', 'Yemen': 'Asia',
    # Europe
    'Albania': 'Europe', 'Andorra': 'Europe', 'Armenia': 'Europe', 'Austria': 'Europe', 'Azerbaijan': 'Europe',
    'Belarus': 'Europe', 'Belgium': 'Europe', 'Bosnia and Herzegovina': 'Europe', 'Bulgaria': 'Europe', 'Croatia': 'Europe',
    'Cyprus': 'Europe', 'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe',
    'France': 'Europe', 'Georgia': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe',
    'Iceland': 'Europe', 'Ireland': 'Europe', 'Italy': 'Europe', 'Kazakhstan': 'Europe', 'Kosovo': 'Europe',
    'Latvia': 'Europe', 'Liechtenstein': 'Europe', 'Lithuania': 'Europe', 'Luxembourg': 'Europe', 'Malta': 'Europe',
    'Moldova': 'Europe', 'Monaco': 'Europe', 'Montenegro': 'Europe', 'Netherlands': 'Europe', 'North Macedonia': 'Europe',
    'Norway': 'Europe', 'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe', 'Russia': 'Europe', 'San Marino': 'Europe',
    'Serbia': 'Europe', 'Slovakia': 'Europe', 'Slovenia': 'Europe', 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe',
    'Ukraine': 'Europe', 'United Kingdom': 'Europe', 'Vatican City': 'Europe',
    # North America
    'Antigua and Barbuda': 'North America', 'Bahamas': 'North America', 'Barbados': 'North America', 'Belize': 'North America',
    'Canada': 'North America', 'Costa Rica': 'North America', 'Cuba': 'North America', 'Dominica': 'North America',
    'Dominican Republic': 'North America', 'El Salvador': 'North America', 'Grenada': 'North America', 'Guatemala': 'North America',
    'Haiti': 'North America', 'Honduras': 'North America', 'Jamaica': 'North America', 'Mexico': 'North America',
    'Nicaragua': 'North America', 'Panama': 'North America', 'Saint Kitts and Nevis': 'North America', 'Saint Lucia': 'North America',
    'Saint Vincent and the Grenadines': 'North America', 'Trinidad and Tobago': 'North America', 'United States': 'North America',
    # South America
    'Argentina': 'South America', 'Bolivia': 'South America', 'Brazil': 'South America', 'Chile': 'South America',
    'Colombia': 'South America', 'Ecuador': 'South America', 'Guyana': 'South America', 'Paraguay': 'South America',
    'Peru': 'South America', 'Suriname': 'South America', 'Uruguay': 'South America', 'Venezuela': 'South America',
    # Australia/Oceania
    'Australia': 'Oceania', 'Fiji': 'Oceania', 'Kiribati': 'Oceania', 'Marshall Islands': 'Oceania', 'Micronesia': 'Oceania',
    'Nauru': 'Oceania', 'New Zealand': 'Oceania', 'Palau': 'Oceania', 'Papua New Guinea': 'Oceania', 'Samoa': 'Oceania',
    'Solomon Islands': 'Oceania', 'Tonga': 'Oceania', 'Tuvalu': 'Oceania', 'Vanuatu': 'Oceania',
    # Antarctica
    'Antarctica': 'Antarctica'
}


df2['continent'] = df2['country'].map(continent_map)
col4=st.columns(2)
with col4[0]:
    selected_continents = st.multiselect('Select Continents', options=df2['continent'].unique(), default=df2['continent'].unique())
    filtered_df2 = df2[df2['continent'].isin(selected_continents)]
    types = filtered_df2['type'].value_counts().reset_index()
    types.columns = ['type', 'count']
col1, trendline_chart, category_chart = st.columns([1.5, 3.5, 3])
with col1:
    st.subheader('Distribution of Movies and TV Shows')
    fig = px.pie(types, 
                 names='type', 
                 values='count', 
                 color_discrete_sequence=['lightblue', 'lightcoral'])
    fig.update_traces(textinfo='percent+label', 
                      pull=[0, 0.1], 
                      textfont_size=15, 
                      marker=dict(line=dict(color='white', width=.5)))
    fig.update_layout(showlegend=False, 
                      paper_bgcolor='rgba(0,0,0,0)', 
                      plot_bgcolor='rgba(0,0,0,0)', 
                      font=dict(color='white', family='Arial'),
                      margin=dict(t=0, b=0, l=0, r=0))
    
    st.plotly_chart(fig)

with trendline_chart:
    st.subheader("Movies & TV Shows Trendline")
    df["date"] = pd.to_datetime(df["date_added"])
    df['year'] = df['date'].dt.year
    filtered_df = df[df['country'].map(continent_map).isin(selected_continents)]
    cnt_years = filtered_df.groupby(['type', 'year']).size().reset_index().rename(columns={0: 'count'})
    st.plotly_chart(
        px.line(cnt_years,
                x='year',
                y='count',
                color='type',
                markers=True,
                color_discrete_sequence=['#B7E0FF', '#E78F81'])
    )

with category_chart:
    st.subheader('Most Common Categories in Movies and TV Shows by Type')
    df_split = df.assign(category=df['listed_in'].str.split(', ')).explode('category')
    category_count = df_split.groupby(['type','category']).size().reset_index().rename(columns={0: 'count'})
    category = st.multiselect('Select Category', category_count['category'])
    category_df = pd.DataFrame()
    category_count = category_count.sort_values(['type','count'], ascending=False)
    if not category:
        category_df = category_count.groupby('type').head(10).reset_index(drop=True)
    else:
        category_df = category_count[category_count['category'].isin(category)]
    st.plotly_chart(
        px.bar(category_df,
               x='category',
               y='count',
               color='type', 
               labels={'count': 'Count', 'category': 'Category','type':'Type'}, 
               barmode='group',
               color_discrete_sequence=['#B7E0FF', '#E78F81'])
    )
col2,bar2=st.columns(2)
with col2:
    st.subheader('Movies & Shows by Countries')
    country_count = df2['country'].value_counts().reset_index()
    country_count.columns = ['country', 'count']
    fig = px.scatter_geo(country_count, 
                         locations="country", 
                         locationmode="country names",
                         color="count",
                         hover_name="country",
                         size="count",
                         projection="natural earth",
                         color_continuous_scale='orrd')
    fig.update_geos(
        showcoastlines=True, coastlinecolor="#656565",  
        showland=True, landcolor="rgba(0, 0, 0, 0)",  
        showocean=True, oceancolor="rgba(0, 0, 0, 0)", 
        showlakes=True, lakecolor="rgba(0, 0, 0, 0)",  
        showrivers=True, rivercolor="rgba(0, 0, 0, 0)",  
        showcountries=True, countrycolor="#656565"  
    )
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        font_color="white",  
        geo=dict(
            bgcolor="rgba(0, 0, 0, 0)")
    )
    st.plotly_chart(fig, use_container_width=True)

with bar2:
    st.subheader('Top 10 Directors')
    value = st.radio('Select top 10 directors in', ['Both', 'Movie', 'TV Show'], horizontal=True)
    if value == 'Both':
        value = ['Movie', 'TV Show']
    else:
        value = [value]
    
    director = df.groupby(['type', 'director']).size().reset_index().rename(columns={0: 'count'})
    top_10_director = director[(director['director'] != 'Not Given')].sort_values(['count', 'type'], ascending=False)
    top_10_director = top_10_director.groupby('type').head(10)

    st.plotly_chart(
        px.bar(
            top_10_director[(top_10_director['type'].isin(value))],
            x='count',
            y='director',
            color='type',
            color_discrete_sequence=['#B7E0FF', '#E78F81'],
            labels={'count': 'Count', 'director': 'Director', 'type': 'Type'}
        )
    )

st.markdown(
    """
    <style>
    .main {
        background-color: rgba(0, 0, 0, 0);  /* Transparent background */
    }
    </style>
    """,
    unsafe_allow_html=True
)
