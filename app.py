import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import Data_Cleaning_Representation.plot_functions as pf

# Load and clean data
cleaned_data = pf.clean_data()

# Grouped data
influencer_data = pf.grouped_data_influencer(cleaned_data)
total_values_per_influencer = influencer_data['Total Values per Influencer']
engagement_per_influencer = influencer_data['Engagement per Influencer']
brand_data = pf.grouped_data_brand(cleaned_data)
date_data = pf.grouped_data_date(cleaned_data)

# Streamlit App
st.set_page_config(layout="wide")

st.title("Case Study: IG Reels Analysis")

# Layout: 2 Spalten pro Zeile
col1, col2 = st.columns(2)
with col1:
    st.write("## Total KPIs")
    total_kpis = pf.total_kpis(cleaned_data)

    for kpi, value in total_kpis.items():
        string_value = f"{value:,}" if kpi != 'Engagement Rate' else f"{value:.3f}"
        st.metric(label=kpi, value=string_value)

with col2:
    st.write("## Grouped Data by Influencer Type")
    categories1 = ['Average Comments per post',
                  'Average Likes per post',
                  'Average Plays per post',
                  'Average Views per post',
                  'Standard deviation of number of followers',
                  'Engagement rate']

    plot_category1 = st.selectbox("Choose a category", categories1)
    plot_data1 = engagement_per_influencer if  plot_category1 == 'Engagement rate' else total_values_per_influencer

    plot_ascending1 = st.checkbox("Sort by ascending order", value=False)
    plot_diagonal1 = st.checkbox("Show diagonal line", value=True)

    color_categories1 = ['Total number of posts', 'Influencer Type', 'Average video duration in s']
    plot_color1 = st.selectbox("Color by category", color_categories1)

    amount1 = st.slider(
        "Amount of data to display (%)",
        min_value=0.01,
        max_value=100.0,
        value=0.01,
        step=0.01,
        format="%.2f"
    )
    number_rows1 = int(len(plot_data1) * (amount1 / 100))


    total_values_per_influencer_sorted_ammount1 = plot_data1.sort_values(by=plot_category1,
                                                                        ascending = plot_ascending1).head(number_rows1)

    fig1 = px.scatter(total_values_per_influencer_sorted_ammount1, x='Average number of followers', y=plot_category1, color=plot_color1,
                    hover_name='Influencer ID', color_continuous_scale=px.colors.sequential.Viridis )

    # Plot diagonal line
    if plot_diagonal1:
        max_plot_category = plot_data1[plot_category1].max()
        max_avg_follower =  plot_data1['Average number of followers'].max()
        line_border = plot_category1 if (max_plot_category < max_avg_follower) else 'Average number of followers'

        fig1.add_shape(
            type='line',
            x0=total_values_per_influencer_sorted_ammount1[line_border].min(),
            y0=total_values_per_influencer_sorted_ammount1[line_border].min(),
            x1=total_values_per_influencer_sorted_ammount1[line_border].max(),
            y1=total_values_per_influencer_sorted_ammount1[line_border].max(),
            line=dict(color='Red', dash='dash')  # color and dash style
        )

    st.plotly_chart(fig1, use_container_width=True)


col3, col4 = st.columns(2)

with col3:
    st.write("## Grouped Data by brand and date")

    categories2 = ['Total Comments',
                  'Total Likes',
                  'Total Plays',
                  'Total Views',
                  'Total number of posts']
    plot_category2 = st.selectbox("Choose a category", categories2)

    pie_categories2 = ['Brand', 'Date']
    plot_pie_category2 = st.selectbox("Choose a pie category", pie_categories2)

    plot_data2 = brand_data if plot_pie_category2 == 'Brand' else date_data
    plot_theme2 =  'Influencer Type' if plot_pie_category2 == 'Brand' else 'Date'

    fig2 = px.pie(plot_data2, names=plot_theme2, values=plot_category2, title=plot_category2,color_discrete_sequence=px.colors.qualitative.Safe)

    st.plotly_chart(fig2, use_container_width=True)


with col4:
    st.write("## Top Influencers")

    categories3 = ['Total Comments',
                  'Total Likes',
                  'Total Plays',
                  'Total Views',
                  'Engagement rate']
    plot_category3 = st.selectbox("Choose a category", categories3, key ="plot_category3")

    plot_data3 = engagement_per_influencer if  plot_category3 == 'Engagement rate' else total_values_per_influencer

    plot_ascending3 = st.checkbox("Sort by ascending order", value=False, key="plot_ascending3")

    color_categories3 = ['Total number of posts', 'Influencer Type', 'Average video duration in s']
    plot_color3 = st.selectbox("Color by category", color_categories3, key="plot_color3")

    amount3 = st.slider(
        "Amount of data to display (%)",
        min_value=0.01,
        max_value=1.0,
        value=0.01,
        step=0.01,
        format="%.2f",
        key="amount3"
    )
    number_rows3 = int(len(plot_data3) * (amount3 / 100))


    total_values_per_influencer_sorted_ammount3 = plot_data3.sort_values(by=plot_category3,
                                                                        ascending = plot_ascending3).head(number_rows3)


    fig3 = px.bar(total_values_per_influencer_sorted_ammount3,
                x='Influencer ID',
                y=plot_category3,
                color=plot_color3,
                category_orders={'Influencer ID': total_values_per_influencer_sorted_ammount3['Influencer ID'].tolist()},
                color_continuous_scale=px.colors.sequential.Viridis
                )

    st.plotly_chart(fig3, use_container_width=True)
