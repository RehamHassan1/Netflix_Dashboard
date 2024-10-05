import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>Netflix Data Analysis</h1>", unsafe_allow_html=True)
st.divider()

# Function to load data with caching for performance
@st.cache_data
def load_data():
    return pd.read_csv('netflix1.csv')

# Load Data
df = load_data()

# Subset Dataframe for relevant columns
df2 = df[['show_id', 'title', 'country', 'type']]
df2.dropna(subset=['country'], inplace=True)

# Continent Mapping
continent_map = {
    # Africa
    'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa', 'Burkina Faso': 'Africa',
    # Add remaining country mappings for other continents...
}

# Map countries to continents
df2['continent'] = df2['country'].map(continent_map)

# Drop rows with NaN continents
df2.dropna(subset=['continent'], inplace=True)

# Layout for continents and category selection
Select_Continents, category_chart = st.columns([2, 1])

# Continent Selection & Pie Chart
with Select_Continents:
    selected_continents = st.multiselect('Select Continents', options=df2['continent'].unique())

    # If no continent selected, show all
    if not selected_continents:
        selected_continents = df2['continent'].unique()

    # Filter dataframe based on continent selection
    filtered_df2 = df2[df2['continent'].isin(selected_continents)]

    # Count types of shows
    types = filtered_df2['type'].value_counts().reset_index()
    types.columns = ['type', 'count']

    # Pie Chart & Trendline Layout
    Pie_chart, trendline_chart = st.columns([1.5, 3.5])

    with Pie_chart:
        st.subheader('Distribution of Movies and TV Shows')
        fig = px.pie(
            types,
            names='type',
            values='count',
            color_discrete_sequence=['lightblue', 'lightcoral']
        )
        fig.update_traces(textinfo='percent+label', pull=[0, 0.1], textfont_size=15,
                          marker=dict(line=dict(color='white', width=.5)))
        fig.update_layout(
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Arial'),
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig)

    with trendline_chart:
        st.subheader("Movies & TV Shows Trendline")
        df["date"] = pd.to_datetime(df["date_added"])
        df['year'] = df['date'].dt.year
        filtered_df = df[df['country'].map(continent_map).isin(selected_continents)]
        cnt_years = filtered_df.groupby(['type', 'year']).size().reset_index().rename(columns={0: 'count'})
        st.plotly_chart(
            px.line(cnt_years, x='year', y='count', color='type', markers=True, color_discrete_sequence=['#B7E0FF', '#E78F81'])
        )

# Category Chart
with category_chart:
    st.subheader('Most Common Categories in Movies and TV Shows by Type')

    # Split categories
    df_split = df.assign(category=df['listed_in'].str.split(', ')).explode('category')
    category_count = df_split.groupby(['type', 'category']).size().reset_index().rename(columns={0: 'count'})

    # Category multiselect filter
    category = st.multiselect('Select Category', category_count['category'])

    # Sort and filter categories based on selection
    category_df = pd.DataFrame()
    category_count = category_count.sort_values(['type', 'count'], ascending=False)
    if not category:
        category_df = category_count.groupby('type').head(10).reset_index(drop=True)
    else:
        category_df = category_count[category_count['category'].isin(category)]

    # Bar Chart for category distribution
    st.plotly_chart(
        px.bar(
            category_df,
            x='category', y='count', color='type', 
            labels={'count': 'Count', 'category': 'Category', 'type': 'Type'},
            barmode='group', color_discrete_sequence=['#B7E0FF', '#E78F81']
        )
    )

# Geo Chart and Top 10 Directors Layout
Geo_chart, Top_10_chart = st.columns(2)

# Geo Chart for country-based movie/shows distribution
with Geo_chart:
    st.subheader('Movies & Shows by Countries')

    # Continent Selection for Geo Chart
    selected_continent = st.selectbox('Select Continent', options=df2['continent'].unique())
    flag = bool(selected_continent)

    if not flag:
        selected_continent = df2['continent'].unique()

    # Filter data by selected continent
    filtered_data = df2[df2['continent'].isin([selected_continent])]
    country_count = filtered_data['country'].value_counts().reset_index()
    country_count.columns = ['country', 'count']

    # Geo Choropleth Map
    fig = px.choropleth(
        country_count, locations="country", locationmode="country names", color="count",
        hover_name="country", projection="natural earth", color_continuous_scale=px.colors.sequential.OrRd
    )

    # Update Geo Chart based on continent selection
    if flag:
        fig.update_geos(visible=False)

        # Update ranges based on continent
        if 'North America' in selected_continent:
            fig.update_geos(lonaxis=dict(range=(-170, -50)), lataxis=dict(range=(20, 50)))
        elif 'South America' in selected_continent:
            fig.update_geos(lonaxis=dict(range=(-80, -30)), lataxis=dict(range=(-60, 15)))
        elif 'Europe' in selected_continent:
            fig.update_geos(lonaxis=dict(range=(-30, 50)), lataxis=dict(range=(35, 70)))
        # Add ranges for other continents...

    fig.update_geos(
        showcoastlines=True, coastlinecolor="black", showcountries=True, countrycolor="gray",
        landcolor="lightgray", showocean=True, oceancolor="lightblue", showlakes=True, lakecolor="lightblue",
        showrivers=True, rivercolor="blue"
    )

    st.plotly_chart(fig, use_container_width=True)

# Top 10 Directors Chart
with Top_10_chart:
    st.subheader('Top 10 Directors')

    # Radio buttons for filtering by Movie/TV Show/Both
    value = st.radio('Select top 10 directors in', ['Both', 'Movie', 'TV Show'], horizontal=True)
    value = ['Movie', 'TV Show'] if value == 'Both' else [value]

    # Group by director and count
    director = df.groupby(['type', 'director']).size().reset_index().rename(columns={0: 'count'})
    top_10_director = director[(director['director'] != 'Not Given')].sort_values(['count', 'type'], ascending=False)
    top_10_director = top_10_director.groupby('type').head(10)

    # Bar Chart for top 10 directors
    st.plotly_chart(
        px.bar(
            top_10_director[(top_10_director['type'].isin(value))],
            x='count', y='director', color='type',
            color_discrete_sequence=['#B7E0FF', '#E78F81'],
            labels={'count': 'Count', 'director': 'Director', 'type': 'Type'}
        )
    )

# Styling for transparent background
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
