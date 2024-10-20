import pandas as pd
import plotly.express as px
import streamlit as st


import pandas as pd

# Load data
df = pd.read_csv('Bikes.csv')

# Remove duplicates and unnecessary columns
df.drop(['holiday', 'workingday', 'season'], axis=1, inplace=True)

# Create a date range and extract additional date-related information
date_range = pd.date_range(start='1/1/2011', end='9/9/2012', freq='D')
date = pd.DataFrame({
    'date': date_range,
    'value': range(1, len(date_range) + 1)  # Example values for each date
})

# Extract year, month, day, day name, and month name
date['year'] = date['date'].dt.year
date['month'] = date['date'].dt.month
date['day'] = date['date'].dt.day
date['day_name'] = date['date'].dt.day_name()
date['month_name'] = date['date'].dt.month_name()

# Function to determine the quarter based on the month
def q_fun(x):
    if x in [1, 2, 3]:
        return 'Q1'
    elif x in [4, 5, 6]:
        return 'Q2'
    elif x in [7, 8, 9]:
        return 'Q3'
    else:
        return 'Q4'

date['quarter'] = date['month'].apply(q_fun)

# Convert datetime column to separate date and time columns
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['date'] = pd.to_datetime(df['date'])
df['time'] = df['datetime'].dt.time

# Drop the original datetime column
df.drop(['datetime'], axis=1, inplace=True)

# Merge the date information with the main DataFrame
data = pd.merge(left=date, right=df, left_on='date', right_on='date', how='left')

# Define working day based on day name
data['workingDay'] = data['day_name'].apply(lambda x: False if x in ['Saturday', 'Sunday'] else True)

# Function to determine the season based on the date
def get_season(date):
    """Extract the season from a given date."""
    month = date.month
    day = date.day

    if (month == 12 and day >= 21) or (month <= 3 and (month != 3 or day <= 19)):
        return 'Winter'
    elif (month == 3 and day >= 20) or (month <= 6 and (month != 6 or day <= 20)):
        return 'Spring'
    elif (month == 6 and day >= 21) or (month <= 9 and (month != 9 or day <= 22)):
        return 'Summer'
    else:
        return 'Autumn'

# Apply the function to extract the season
data['season'] = data['date'].apply(get_season)

# Function to determine the period of the day based on the hour
def get_day_period(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

# Extract hour and day period information
data['hour'] = data['time'].apply(lambda x: x.hour if type(x) != float else x)
data['day_period'] = data['hour'].apply(get_day_period)
data = data.dropna(subset=['weather'])


# Calculate the required metrics
Total_Profit = round(data['Profit'].sum(), 2)
Total_Registered_Bikes = data['registered'].sum()
Total_Causal_Bikes = data['casual'].sum()
Total_Rented_Bikes = data['rented_bikes_count'].sum()




##st.set_page_config(page_title="Bikes Analysis dashboard",layout='wide')
##st.image('C:/Users/Ahmed Kodira/Plotly/bike.jpg')
##st.header(<h1 style = 'text-align : center ; color : red;'> Bikes Analysis Dashboard </h1> ,divider = True )
##st.markdown("<h1 style='text-align: center; color: red;'>Bikes Analysis Dashboard</h1>", unsafe_allow_html=True)
##st.markdown("---")



st.set_page_config(page_title="Bikes Analysis dashboard",layout='wide')
st.markdown("<h1 style='text-align: center; color: red;'>Bikes Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")
st.sidebar.title('Filter Pane')



col1, col2, col3, col4 = st.columns(4)


with col1:
    Total_Profit = round(data['Profit'].sum(), 2)  
    profit_value = f"${Total_Profit:,.2f}"  
    st.markdown(f"<h3 style='color: black; font-size: 14px; text-align: center;'>Total Profit</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 14px; text-align: center; font-weight: bold;'>{profit_value}</p>", unsafe_allow_html=True)

with col2:
    Total_Registered_Bikes = round(data['registered'].sum(), 0) 
    registered_value = f"{Total_Registered_Bikes:,.0f}"  
    st.markdown(f"<h3 style='color: black; font-size: 14px; text-align: center;'>Total Registered Bikes</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 14px; text-align: center; font-weight: bold;'>{registered_value}</p>", unsafe_allow_html=True)

with col3:
    Total_Causal_Bikes = round(data['casual'].sum(), 0)  
    causal_value = f"{Total_Causal_Bikes:,.0f}"  # Format with thousands separator
    st.markdown(f"<h3 style='color: black; font-size: 14px; text-align: center;'>Total Causal Bikes</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 14px; text-align: center; font-weight: bold;'>{causal_value}</p>", unsafe_allow_html=True)

with col4:
    Total_Rented_Bikes = round(data['rented_bikes_count'].sum(), 0)  # Round total rented bikes to 0 decimal places
    rented_value = f"{Total_Rented_Bikes:,.0f}"  # Format with thousands separator
    st.markdown(f"<h3 style='color: black; font-size: 14px; text-align: center;'>Total Rented Bikes</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 14px; text-align: center; font-weight: bold;'>{rented_value}</p>", unsafe_allow_html=True)



def page1():
    col1, col2 = st.columns(2)

    with col1:
        
        filtered_data = data.copy()

        if selected_year != 'Select':
            filtered_data = filtered_data[filtered_data['year'] == selected_year]
        if selected_month:  
            filtered_data = filtered_data[filtered_data['month_name'].isin(selected_month)]
        if selected_quarter != 'Select':
            filtered_data = filtered_data[filtered_data['quarter'] == selected_quarter]
        if selected_day:  
            filtered_data = filtered_data[filtered_data['day_name'].isin(selected_day)]
        if selected_season != 'Select':
            filtered_data = filtered_data[filtered_data['season'] == selected_season]
        if selected_weather != 'Select':
            filtered_data = filtered_data[filtered_data['weather'] == selected_weather]

        profit_by_year = filtered_data.groupby('year')['Profit'].sum().reset_index()
        max_year_profit = profit_by_year['Profit'].max()
        min_year_profit = profit_by_year['Profit'].min()
        year_colors = ['green' if value == max_year_profit else 'red' if value == min_year_profit else 'lightgray' for value in profit_by_year['Profit']]
        
        st.plotly_chart(px.bar(data_frame=profit_by_year, x='year', y='Profit', text_auto=True)
                 .update_traces(marker_color=year_colors)
                 .update_layout(
                     title_text='Total Profit by Year',
                     showlegend=False,
                     xaxis=dict(
                         tickmode='array',
                         tickvals=profit_by_year['year'],
                         ticktext=profit_by_year['year'].astype(str)
                     ),
                     yaxis={'showticklabels': False}
                 ))
    

        profit_by_quarter =  filtered_data.groupby('quarter')['Profit'].sum().reset_index()
        max_quarter_profit = profit_by_quarter['Profit'].max()
        min_quarter_profit = profit_by_quarter['Profit'].min()
        quarter_colors = ['green' if value == max_quarter_profit else 'red' if value == min_quarter_profit else 'lightgray' for value in profit_by_quarter['Profit']]
    
        st.plotly_chart(px.pie(data_frame=profit_by_quarter, 
                                names='quarter', 
                                values='Profit', 
                                title='Total Profit by Quarter',
                                hole=0.3,  #
                                color_discrete_sequence=quarter_colors)
                         .update_traces(textposition='inside', textinfo='label+percent')  
                         .update_layout(title_text='Total Profit by Quarter'))

    with col2:
        
        profit_by_month = filtered_data.groupby('month')['Profit'].sum().reset_index()
        max_month_profit = profit_by_month['Profit'].max()
        min_month_profit = profit_by_month['Profit'].min()
        month_colors = ['green' if value == max_month_profit else 'red' if value == min_month_profit else 'lightgray' for value in profit_by_month['Profit']]
        
        st.plotly_chart(px.bar(data_frame=profit_by_month, x='month', y='Profit', text_auto=True)
                 .update_traces(marker_color=month_colors)
                 .update_layout(
                     title_text='Total Profit by Month',
                     showlegend=False,
                     xaxis=dict(
                         tickmode='array',
                         tickvals=profit_by_month['month'],
                         ticktext=profit_by_month['month'].astype(str),
                         tickangle=-45  # Rotate labels for better readability
                     ),
                     yaxis={'showticklabels': False}
                 ))
    
        
        profit_by_day_name = filtered_data.groupby('day_name')['Profit'].sum().reset_index()
        max_day_profit = profit_by_day_name['Profit'].max()
        min_day_profit = profit_by_day_name['Profit'].min()
        day_colors = ['green' if value == max_day_profit else 'red' if value == min_day_profit else 'lightgray' for value in profit_by_day_name['Profit']]
        
        st.plotly_chart(px.bar(data_frame=profit_by_day_name, x='day_name', y='Profit', text_auto=True)
                         .update_traces(marker_color=day_colors)  # Set bar colors
                         .update_layout(title_text='Total Profit by Day', showlegend=False)  # Hide legend
                         .update_layout(yaxis={'showticklabels': False}))


def page2():
    tab1, tab2, tab3 = st.tabs(['Season', 'Temperature', 'Hour'])
       
    with tab1:
        filtered_data = data.copy()

        if selected_year != 'Select':
            filtered_data = filtered_data[filtered_data['year'] == selected_year]
        if selected_month:  
            filtered_data = filtered_data[filtered_data['month_name'].isin(selected_month)]
        if selected_quarter != 'Select':
            filtered_data = filtered_data[filtered_data['quarter'] == selected_quarter]
        if selected_day:  
            filtered_data = filtered_data[filtered_data['day_name'].isin(selected_day)]
        if selected_season != 'Select':
            filtered_data = filtered_data[filtered_data['season'] == selected_season]
        if selected_weather != 'Select':
            filtered_data = filtered_data[filtered_data['weather'] == selected_weather]
            
        profit_by_season = filtered_data.groupby('weather')['rented_bikes_count'].sum().reset_index()
        st.plotly_chart(px.bar(profit_by_season, x='weather', y='rented_bikes_count',color='weather', title='Total Rented Bikes', text_auto=True,
                                labels={'rented_bikes_count': 'Total Rented Bikes', 'weather': 'Weather'})
                         .update_layout(yaxis={'showticklabels': False}))

        rentedbikes_by_year = filtered_data.groupby('year')['rented_bikes_count'].sum().reset_index()
        st.plotly_chart(px.bar(rentedbikes_by_year, x='year', y='rented_bikes_count', text_auto=True)
                 .update_layout(
                     title_text='Rented Bikes by Year',
                     xaxis=dict(
                         tickmode='array',
                         tickvals=rentedbikes_by_year['year'],
                         ticktext=rentedbikes_by_year['year'].astype(str)
                     ),
                     yaxis={'showticklabels': False},
                     xaxis_title='Year',
                     yaxis_title='Rented Bikes'
                 ))

    with tab2:
        temp_analysis = filtered_data.groupby('temp')['rented_bikes_count'].sum().reset_index()
        def get_point_colors(values):
            
            max_value = max(values)
            min_value = min(values)
            return ['green' if v == max_value else 'red' if v == min_value else 'lightgrey' for v in values]

        point_colors = get_point_colors(temp_analysis['rented_bikes_count'])

        st.plotly_chart(px.scatter(temp_analysis, x='temp', y='rented_bikes_count')
                 .update_traces(marker=dict(color=point_colors, size=8))
                 .update_layout(
                     title_text='Temperature vs Rented Bikes',
                     xaxis_title='Temperature (°C)',
                     yaxis_title='Total Rentals',
                     yaxis={'showticklabels': False}
                 ))
        
        st.plotly_chart(px.pie(data, names='weather', values='rented_bikes_count').update_traces(textinfo='value+percent')
                        .update_layout(title_text='Rented Bikes by Weather'))
        
        weather_analysis = filtered_data.groupby('weather')['rented_bikes_count'].sum().reset_index()
        st.plotly_chart(px.histogram(weather_analysis, x='rented_bikes_count', y='weather',color='weather', title='Weather vs Rented Bikes',text_auto=True,
             labels={'weather': 'Weather Condition'}).update_layout(xaxis={'showticklabels': False}))
    
    with tab3:
        data['hour'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour
        rented_bikes_by_hour = filtered_data.groupby('hour')['rented_bikes_count'].sum().reset_index()
        st.plotly_chart(px.line(rented_bikes_by_hour, x='hour', y='rented_bikes_count')
                 .update_traces(
                     line_color='red',
                     mode='lines+markers+text',  # Include text on the line with markers
                     marker=dict(color='green', size=8),
                     text=rented_bikes_by_hour['rented_bikes_count'],  # Display numbers on the line
                     textposition='top center'  # Position the text at the top of markers
                 )
                 .update_layout(
                     title_text='Total Rented Bikes by Hour of Day',
                     xaxis_title='Hour',
                     yaxis_title='Total Rentals',
                     xaxis=dict(tickmode='linear', tick0=0, dtick=1),  # Show all hours on x-axis
                     yaxis={'showticklabels': False}  # Hide y-axis tick labels if needed
                 ))



        rented_bikes_by_time = filtered_data.groupby('time')['rented_bikes_count'].sum().reset_index()
        max_rented_bikes = rented_bikes_by_time['rented_bikes_count'].max()
        min_rented_bikes = rented_bikes_by_time['rented_bikes_count'].min()
        time_colors = ['green' if value == max_rented_bikes else 'red' if value == min_rented_bikes else 'lightgray' for value in rented_bikes_by_time['rented_bikes_count']]
        st.plotly_chart(px.bar(rented_bikes_by_time, x='time', y='rented_bikes_count', text_auto=True,
              title='Total Rented Bikes by Time of Day', 
              labels={'rented_bikes_count': 'Total Rentals', 'time': 'Time'}).update_layout(yaxis={'showticklabels': False}).update_traces(marker_color=time_colors))

def page3():
        filtered_data = data.copy()
        if selected_year != 'Select':
            filtered_data = filtered_data[filtered_data['year'] == selected_year]
        if selected_month:  
            filtered_data = filtered_data[filtered_data['month_name'].isin(selected_month)]
        if selected_quarter != 'Select':
            filtered_data = filtered_data[filtered_data['quarter'] == selected_quarter]
        if selected_day:  
            filtered_data = filtered_data[filtered_data['day_name'].isin(selected_day)]
        if selected_season != 'Select':
            filtered_data = filtered_data[filtered_data['season'] == selected_season]
        if selected_weather != 'Select':
            filtered_data = filtered_data[filtered_data['weather'] == selected_weather]
            
        user_analysis = filtered_data.groupby('month_name')[['casual', 'registered']].sum().reset_index()
        st.plotly_chart(px.bar(user_analysis, x='month_name', y=['casual', 'registered'], text_auto=True, barmode='group',
                            title='Casual vs Registered Users by Month', 
                            labels={'value': 'Number of Users', 'month_name': 'Month'})
                     .update_layout(yaxis={'showticklabels': False}))

        st.plotly_chart(px.pie(filtered_data, names='day_period', values='Profit').update_traces(textinfo='value+percent')
                   .update_layout(title_text='Profit Distribution by Day Period'))


pgs = {
    'Analysis By Time': page1,
    'Season': page2,
    'Types': page3
}


pg = st.sidebar.radio('Navigate pages', options=pgs.keys())

selected_year = st.sidebar.selectbox('Select Year', options=['Select'] + list(data['year'].unique()))
selected_month = st.sidebar.multiselect('Select Month', options=list(data['month_name'].unique()))
selected_quarter = st.sidebar.selectbox('Select Quarter', options=['Select'] + list(data['quarter'].unique()))
selected_day = st.sidebar.multiselect('Select Day', options=list(data['day_name'].unique()))
selected_season = st.sidebar.radio('Select Season', options=['Select'] + list(data['season'].unique()))
selected_weather = st.sidebar.radio('Select Weather', options=['Select'] + list(data['weather'].unique()))

pgs[pg]()

