import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
url = 'https://raw.githubusercontent.com/natelewis17/STAT386_Project/main/kanji.csv'
df = pd.read_csv(url)

# Sidebar with user input
st.sidebar.title('Wikiji: Kanji Explorer')
st.sidebar.markdown('This will take an input of a kanji or English meaning and then return a table with basic information for your input and then a table showing the frequencies of on Wikipedia, in newspapers, and in novels. (potential kanji that you can try: 水、証、遊、曜、年)')
user_input = st.sidebar.text_input('Enter a Kanji or an English Meaning', '水')

st.title(f'Kanji Explorer - Showing results for {user_input}')

# Filter the DataFrame based on user input
filtered_df = df[df['Kanji'].str.contains(user_input) | df['Meanings'].str.contains(user_input)]

# Display the filtered DataFrame or a message if there are no matches
if not filtered_df.empty:
    st.write(f"Showing results for: {user_input}")
    st.write(filtered_df)

    # More detailed information
    st.subheader('Details:')
    for index, row in filtered_df.iterrows():
        st.write(f"Kanji: {row['Kanji']}")
        st.write(f"Meanings: {row['Meanings']}")
        st.write(f"JLPT Level: N{row['JLPT']}")
        # Add more columns as needed
else:
    st.write(f"No matches found for: {user_input}. Please try something else.")

# Visualization of Wiki_Ranking, Novel_Ranking, Newspaper_Ranking
if not filtered_df.empty:
    st.subheader('Rankings Distribution')

    # Melt the DataFrame for Altair
    melted_df = pd.melt(filtered_df, id_vars=['Kanji'], value_vars=['Wiki_Ranking', 'Novel_Ranking', 'Newspaper_Ranking'],
                        var_name='Ranking Type', value_name='Ranking')

    # Create a grouped bar chart using Altair
    chart = alt.Chart(melted_df).mark_bar().encode(
        column='Ranking Type',
        x='Kanji',
        y='Ranking'
    ).properties(width=150)

    # Display the chart using Streamlit and Altair
    st.altair_chart(chart)

    # Sidebar with user input

# Sidebar with user input
st.sidebar.title('Wikiji: Wiki Kanji Frequency')
st.sidebar.markdown('You will select a grouping option and a plot will be returned showing the frequencies of different levels of that grouping on Wikipedia.')
group_by_option = st.sidebar.selectbox('Select grouping option', ['Stroke_Count', 'JLPT', 'Grade', 'In_Joyo'])

# Group by the selected option and sum Wiki_Counts
grouped_df = df.groupby(group_by_option)['Wiki_Count'].sum().reset_index()

# Display the big title
st.title(f'Wiki Kanji Frequency - Grouped by {group_by_option}')

# Plotting
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x=group_by_option, y='Wiki_Count', data=grouped_df, ci=None, ax=ax)
plt.title(f'Bar Plot of Frequency Grouped by {group_by_option}')
plt.xlabel(group_by_option)
plt.ylabel('Occurrences on Sampled Wikipedia Articles')

# Display the plot using st.pyplot(fig)
st.pyplot(fig)



# Sidebar for Top 20 Kanji
st.sidebar.title('Wikiji: Top 20 Kanji')
group_by_option_top20 = st.sidebar.selectbox('Select grouping option', ['Stroke_Count', 'JLPT', 'Grade', 'In_Joyo'], key='group_by_option_top20')

# Create a subcategory dropdown based on the selected grouping option
subcategory_options = None
if group_by_option_top20 == 'Stroke_Count':
    subcategory_options = st.sidebar.selectbox('Select Stroke Count Range', ['<5', '5-10', '10-15', '>15'], key='stroke_count_subcategory')
elif group_by_option_top20 == 'JLPT':
    subcategory_options = st.sidebar.selectbox('Select JLPT Level', ['1', '2', '3', '4', '5'], key='jlpt_subcategory')
elif group_by_option_top20 == 'Grade':
    subcategory_options = st.sidebar.selectbox('Select Grade Level', ['1', '2', '3', '4', '5', '6', '8', '9', '10'], key='grade_subcategory')
elif group_by_option_top20 == 'In_Joyo':
    subcategory_options = st.sidebar.selectbox('Select In_Joyo', ['Yes', 'No'], key='in_joyo_subcategory')

# Display the title for the Top 20 section
st.title(f'Wikiji: Top 20 Kanji - Grouped by {group_by_option_top20}')

# Filter the DataFrame based on the selected grouping option and subcategory
if group_by_option_top20 == 'Overall':
    top20_df = df.nlargest(20, 'Wiki_Count')
else:
    if group_by_option_top20 == 'Stroke_Count':
        if subcategory_options == '<5':
            filtered_top20_df = df[df['Stroke_Count'] < 5]
        elif subcategory_options == '5-10':
            filtered_top20_df = df[(df['Stroke_Count'] >= 5) & (df['Stroke_Count'] <= 10)]
        elif subcategory_options == '10-15':
            filtered_top20_df = df[(df['Stroke_Count'] > 10) & (df['Stroke_Count'] <= 15)]
        elif subcategory_options == '>15':
            filtered_top20_df = df[df['Stroke_Count'] > 15]
    elif group_by_option_top20 == 'JLPT':
        filtered_top20_df = df[df['JLPT'] == int(subcategory_options)]
    elif group_by_option_top20 == 'Grade':
        filtered_top20_df = df[df['Grade'] == int(subcategory_options)]
    elif group_by_option_top20 == 'In_Joyo':
        filtered_top20_df = df[df['In_Joyo'] == subcategory_options]

# Visualization of the Top 20 Kanji
if not filtered_top20_df.empty:
    st.subheader(f'Top 20 Kanji Distribution - Grouped by {group_by_option_top20}')

    # Create a bar plot for top 20 Kanji by Wiki_Count, using 'Meanings' on the y-axis
    top_n = 20
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Wiki_Count', y='Meanings', data=filtered_top20_df.head(top_n), palette='viridis', ax=ax)
    plt.title(f'Top {top_n} Kanji by Wiki_Count')
    plt.xlabel('Wiki_Count')
    plt.ylabel('Meanings')

    # Display the plot using st.pyplot(fig)
    st.pyplot(fig)

    # Add a thank you section at the bottom
st.sidebar.markdown("---")
st.sidebar.markdown("### Thank you for exploring my project!")
st.sidebar.markdown("If you're interested in more details about the project here's a link to my GitHub repo and blog:")
st.sidebar.markdown("[GitHub Repository](https://github.com/natelewis17/STAT386_Project)")
st.sidebar.markdown("[Blog](https://natelewis17.github.io/)")
