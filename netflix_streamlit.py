import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>Netflix Data Analysis</h1>", unsafe_allow_html=True)
st.divider()
df= pd.read_csv('netflix1.csv')
df2 = df[['show_id', 'title', 'country', 'type']]
df2.dropna(subset=['country'], inplace=True)
types = df2['type'].value_counts().reset_index()
types.columns = ['type', 'count']
col2,  category_chart,col1=st.columns([2,2,1])
trendline_chart,bar2=st.columns(2)
with col1:
    st.subheader('Distribution of Movies and TV Shows')
    fig, ax = plt.subplots(figsize=(4, 4))  
    fig.patch.set_alpha(0)  
    ax.pie(types['count'], 
           labels=types['type'], 
           autopct='%1.2f%%', 
           explode=[0, 0.1], 
           colors=['lightblue', 'lightcoral'],
           textprops={'color': 'white', 'fontsize': 10})  
    #plt.gca().set_title("Movies vs TV Shows", color='white', fontsize=11, family='Arial') 
    ax.set_facecolor('none') 
    st.pyplot(fig)
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
                         #title="Movies & Shows by Countries",
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
            bgcolor="rgba(0, 0, 0, 0)"  
        ),
        #title_font=dict(size=14 , color="white", family="Arial")  
    )
    st.plotly_chart(fig, use_container_width=True)  
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

with category_chart:
    st.subheader('Most Common Categories in Movies and TV Shows by Type')
    #split the data in listed column and add category column to database to descibe each category
    df_split=df.assign(category=df['listed_in'].str.split(', ')).explode('category')
    #get the count of each category
    category_count=df_split.groupby(['type','category']).size().reset_index().rename(columns={0: 'count'})
    #select the category
    category=st.multiselect('Select Category',category_count['category'])
    category_df=pd.DataFrame();
    category_count=category_count.sort_values(['type','count'],ascending=False)
    if not category:
        category_df=category_count.groupby('type').head(10).reset_index(drop=True)
    else:
        category_df=category_count[category_count['category'].isin(category)]
    #draw plot
    st.plotly_chart(
    px.bar(category_df,
                x='category',
                y='count',
                color='type', 
                labels={'count': 'Count', 'category': 'Category','type':'Type'}, 
                barmode='group',
                color_discrete_sequence=['#B7E0FF', '#E78F81'],
                ))

with trendline_chart:
    st.subheader("Movies & TV shows trendline")
    #convert date form str to datatime
    df["date"] = pd.to_datetime(df["date_added"])
    df['year']=df['date'].dt.year
    
    cnt_years=df.groupby(['type', 'year']).size().reset_index().rename(columns={0: 'count'})
    #draw plot 
    st.plotly_chart(
        px.line(cnt_years,
                x='year',
                y='count',
            
                color='type',
                markers=True,
                color_discrete_sequence=['#B7E0FF', '#E78F81'],
                )
    )
with bar2:
    st.subheader('Top 10 Directors')
    value=st.radio('Select top 10 directors in',['Both','Movie','TV Show'],horizontal=True)
    if (value=='Both'):
        value=['Movie','TV Show']
    else:
        value=[value]
    director=df.groupby(['type','director']).size().reset_index().rename(columns={0:'count'})
    top_10_director=director[(director['director']!='Not Given')].sort_values(['count','type'],ascending=False)
    top_10_director=top_10_director.groupby('type').head(10)

    st.plotly_chart(
        px.bar(
            top_10_director[(top_10_director['type'].isin(value))],
            x='count',
            y='director',
            color='type',
            color_discrete_sequence=['#B7E0FF', '#E78F81'],
            labels={'count': 'Count', 'director': 'Director','type':'Type'},
           
        ))
