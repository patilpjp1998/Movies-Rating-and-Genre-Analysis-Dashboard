# Import necessary libraries
import pandas as pd # for data manipulation
import numpy as np # for numerical operations
import seaborn as sns #  for building interactive web applications
import matplotlib.pyplot as plt # for creating static visualizations
import plotly.express as px # for creating interactive plots
import plotly.graph_objects as go # for more detailed plotting
import streamlit as st #  for building interactive web applications
import preprocessor 


# Reading the data
df = pd.read_csv("cleaned_n_moviess.csv")

# Page title
st.set_page_config(
    page_title="'Movies Analysis Dashboard",
    page_icon="🎞",
    layout="wide", 
    initial_sidebar_state="expanded")

### =========================================================================================================================================================##

# Dashboard Title and description
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            color: #FF204E;  /* Title color */
            font-size: 45px;
            font-weight: bold;
            margin-top: 20px;
        }
        .description {
            text-align: center;
            font-size: 20px;
            margin-top: 20px;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True
)

# Title with custom styling
st.markdown('<div class="title">🎦 Movies Dataset Analysis Dashboard </div>', unsafe_allow_html=True)

# Project description
st.markdown('<div class="description">Explore movie ratings, genres, and trends to gain insights into the movie industry dynamics.</div>', unsafe_allow_html=True)


st.markdown("---")

## =========================================================================================================================================================##

# Sidebar filters
st.sidebar.image("logo.jpg", width = 280)
st.sidebar.title("🔍 Filters")
selected_Year = preprocessor.multiselect("Select Year", df["Year"].sort_values().unique())
selected_Genre = preprocessor.multiselect("Select Genre", df['Genre'].unique())
selected_rating = st.sidebar.slider('Select Rating Range', 0.0, 10.0, (0.0, 10.0))


# Apply Filters
filtered_df = df.copy()  # Create a copy of the original DataFrame to apply filters

# Apply filters only if they have been selected (to avoid errors when filters are empty)
if len(selected_Year) > 0:  # Check if any year has been selected
    filtered_df = filtered_df[filtered_df["Year"].isin(selected_Year)]

if len(selected_Genre) > 0:  
    filtered_df = filtered_df[filtered_df["Genre"].isin(selected_Genre)]


if selected_rating:  
    filtered_df = filtered_df[filtered_df["Rating"].between(selected_rating[0], selected_rating[1])]

## =========================================================================================================================================================##

# KPI - Key Performance Indicator 
st.subheader("Key Performance Indicators(KPI's)")
col1, col2, col3, col4 = st.columns(4)

# Average Rating
with col1:
    st.metric(label='Average Rating', value = round(filtered_df['Rating'].mean(), 2))

# Total Movies 
with col2:
    st.metric(label ='Total Movies', value = len(filtered_df))

# Year with most Movies 
with col3:
    # Safely access mode() result
    year_mode = filtered_df['Year'].mode()
    year_most_movies = year_mode[0] if not year_mode.empty else "N/A"
    st.metric(label='Year with Most Movies', value = year_most_movies)

# Total Votes
with col4:
    st.metric(label = 'Total Votes', value = filtered_df['Votes'].sum())

# Shortest Time Duration
with col1:
    st.metric(label = 'Shortest Time Duration', value = filtered_df['Duration'].min())

# Longest Time Duration
with col2:
    st.metric(label = 'Longest Time Duration', value = filtered_df['Duration'].max())

# Most Popular Genre
with col3:
    genre_mode = filtered_df['Genre'].mode()
    most_popular_genre = genre_mode[0] if not genre_mode.empty else "N/A"
    st.metric(label = 'Most Popular Genre', value = most_popular_genre)

st.markdown("---")

## =========================================================================================================================================================##
# Visuaization

st.markdown('<h3> 📊Average Ratings by Certification</h3>', unsafe_allow_html=True)
# Calculate average ratings by certificate
avg_ratings_cert = (
    filtered_df.groupby('Certificate')['Rating']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
# Check for empty DataFrame to avoid errors
if not avg_ratings_cert.empty:
    # Create an interactive bar chart using Plotly
    fig1 = px.bar(
        avg_ratings_cert,
        x=avg_ratings_cert.values,
        y=avg_ratings_cert.index,
        orientation='h',  # Horizontal bar chart
        labels={'x': 'Average Rating', 'y': 'Certificate'},
        color=avg_ratings_cert.values, 
        color_continuous_scale='dense'
    )
    # Update layout for better readability
    fig1.update_layout(
        xaxis_title='Average Rating',
        yaxis_title='Certification',
        yaxis=dict(categoryorder='total ascending'),
        template='plotly_white',
        height=500,
    )
    # Render the interactive plot in Streamlit
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.write("No data available for the selected filters.")

# Graph related summary 
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
     The bar chart compares the average viewer ratings across different movie certifications. It highlights how ratings vary by certification, providing insights into audience preferences and the perceived quality of films within each category.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

## =========================================================================================================================================================##
## 2. Distribution of Ratings
st.markdown('<h3> 📊Distribution of Ratings</h3>', unsafe_allow_html=True)

if not filtered_df.empty and 'Rating' in filtered_df.columns:
    # Create an interactive histogram using Plotly
    fig2 = px.histogram(
        filtered_df,
        x='Rating',
        nbins=30,
        color_discrete_sequence=px.colors.sequential.Sunset  
    )

    # Add edge color effect by outlining the bars
    fig2.update_traces(
        marker=dict(
            line=dict(color='black', width=1)  
        )
    )

    # Update layout for better readability
    fig2.update_layout(
        xaxis_title='Ratings',
        yaxis_title='Counts',
        template='plotly_white',
        height=500
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.write("No ratings data available for the selected filters.")


st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        The bar chart is showing how movie ratings are spread across the dataset. It highlights the most frequent rating ranges and provides
        insights into audience sentiment, such as whether most movies have high, average, or low ratings.   </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

### ## =========================================================================================================================================================##
# 3. Genre Popularity

st.markdown('<h3>📈 Genre Popularity</h3>', unsafe_allow_html=True)

# Split genres from the 'Genre' column in the filtered DataFrame
split_genres_filtered = []
for sublist in filtered_df['Genre'].dropna():
    if isinstance(sublist, str):
        split_genres_filtered.extend([genre.strip() for genre in sublist.split(',')])

# Calculate genre counts
genre_popularity = pd.Series(split_genres_filtered).value_counts()

# Streamlit visualization
if not genre_popularity.empty:
    fig3 = px.pie(
        names=genre_popularity.index, 
        values=genre_popularity.values,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig3.update_layout(
        template='plotly_white',
        height=500
    )
    st.plotly_chart(fig3)
else:
    st.write("No genres to display for the selected filters.")

# Graph related summary
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
         This pie chart illustrates the popularity of each genre by showing the proportion of movies belonging to each genre in the dataset.

    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")
## ========================================================================================================================================================##
# 4. Movies Released Per Year

st.markdown('<h3>📉 Movies Released Per Year</h3>', unsafe_allow_html=True)

year_counts = filtered_df['Year'].value_counts().sort_index()

if not year_counts.empty:
    # Ensure data is in a DataFrame format
    year_counts_df = year_counts.reset_index()
    year_counts_df.columns = ['Year', 'Count'] 

    # Create the plot using the corrected DataFrame
    fig4 = px.line(
        year_counts_df,
        x='Year', 
        y='Count', 
        markers=True,  # This adds markers to the plot
        color_discrete_sequence=['blue'] 
    )

    fig4.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of Movies',
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig4, use_container_width=True)
else:
    st.write("No yearly data to display for the selected filters.")


# Graph related summary 
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
         The line chart shows the yearly distribution of movie releases over a specific time period. It highlights trends, such as peaks and declines, indicating periods of increased or decreased cinematic production. This visualization offers insights into the evolution of the film industry.
    </div>
    """,
    unsafe_allow_html=True
)

st.write('---')

## =========================================================================================================================================================##

# 5. Relationship between the Year and Rating
st.markdown('<h3>📉 Relationship between Year and Rating</h3>', unsafe_allow_html=True)

# Scatter plot showing the relationship between Year and Rating
fig5 = px.scatter(
    filtered_df, 
    x='Year', 
    y='Rating', 
    # title="Relationship between Year and Rating",
    labels={'Year': 'Year', 'Rating': 'Rating'},
    color='Rating', 
    color_continuous_scale='Viridis',  
    template='plotly_white'
)

# Customize the scatter plot for better readability
fig5.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
fig5.update_layout(
    xaxis_title='Year',
    yaxis_title='Rating',
    height=500
)

# Render the chart in Streamlit
st.plotly_chart(fig5, use_container_width=True)

# Graph related summary
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        This scatter plot shows the relationship between the year of release and the rating of movies. Each point represents an individual movie, 
        with its position determined by the year of release and its rating. This allows us to visually explore how movie ratings have evolved over time.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")

# ==========================================================================================================================================================##
st.markdown('<h3>📉 Average Rating Per Year</h3>', unsafe_allow_html=True)
average_rating_per_year = filtered_df.groupby('Year')['Rating'].mean()

if not average_rating_per_year.empty:
    # Create the line plot using Plotly Express
    fig6 = px.line(
        x=average_rating_per_year.index, 
        y=average_rating_per_year.values, 
        labels={'x': 'Year', 'y': 'Average Rating'}, 
        markers=True,  # Adds markers at data points
        color_discrete_sequence=['red'] 

    )
    
    # Update layout for better readability and style
    fig6.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Rating',
        yaxis=dict(showgrid=True,),
        template='plotly_white',
        height=500,
        font=dict(size=12),
    )
    
    # Render the chart in Streamlit
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.write("No data available for the selected filters.")
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        This line chart visualizes the average movie ratings over time, with each point representing the mean rating of movies released in a specific year. It highlights trends in audience sentiment, showing fluctuations in movie quality and reception, and provides insights into how movie ratings have evolved over the years.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# ===========================================================================================================================================================

## Add footer
st.markdown(
    """
    <style>
        footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background-color: #f8f9fa;
            margin-top: 50px;
            border-top: 1px solid #ddd;
        }
        .footer-left {
            flex: 1;
            font-size: 14px;
            color: #555;
        }
        .footer-left b {
            color: #FF204E;
        }
        .footer-text {
            font-size: 14px;
            color: #777;
            margin-top: 20px;
        }
        .footer-text a {
            color: #FF204E;
            text-decoration: none;
        }
        .footer-text a:hover {
            text-decoration: underline;
        }
        .gif-container {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .gif-container img {
            width: 250px;
            height: auto;
            border-radius: 8px;
        }
        .credits-container {
            text-align: center;
            margin-top: 30px;
            font-size: 18px;
            color: #333;
        }
        .credits-container b {
            font-size: 22px;
            color: #FF204E;
        }
        .contact-info {
            text-align: center;
            margin-top: 20px;
            font-size: 16px;
            color: #333;
        }
        .contact-info b {
            font-size: 18px;
            color: #007BFF;
        }
        .contact-info a {
            text-decoration: none;
            color: #007BFF;
        }
        .contact-info a:hover {
            text-decoration: underline;
        }
    </style>

    <footer>
        <div class="footer-left">
            <p><b>Project Code:</b> B41_DA_011_Data Wranglers | 
               <b>Data Source:</b> <a href="https://www.kaggle.com/datasets/narayan63/netflix-popular-movies-dataset" target="_blank">Kaggle</a>
            </p>
            <div class="footer-text">
                <p>Want to explore more? Check out our other projects or visit our <a href="https://www.kaggle.com/">Kaggle profile</a>.</p>
            </div>
        </div>
        <div class="gif-container">
            <img src="https://media.tenor.com/zDZRlH-tT1sAAAAM/despicable-me-minions.gif" />
        </div>
    </footer>

    <div class="credits-container">
        <b>✨ Dashboard Created By:</b><br>
        1. Tejas Patil <br>
        2. Chandra Yamuna <br>
        3. Prashant Patil
    </div>

    <div class="contact-info">
        📧 For any inquiries or feedback, feel free to reach us at: 
        <b><a href="mailto:team.dashboard@example.com">team.dashboard@example.com</a></b>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")


# ===========================================================================================================================================================
