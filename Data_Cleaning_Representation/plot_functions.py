import pandas as pd
import os

def clean_data():
    '''Function to clean the input data.'''

    # Load the dataset
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, '230609_Interview_Dataset_Reels_Assets_v1.csv')
    data = pd.read_csv(csv_path)

    # Convert data types
    data['Comments'] = data['Comments'].astype('Int64')
    data['Influencer Type'] = data['Influencer Type'].astype('category')
    data['Likes'] = data['Likes'].astype('Int64')
    data['Plays'] = data['Plays'].astype('Int64')
    data['Views'] = data['Views'].astype('Int64')

    # Date just has two values, so we can convert it to a category
    data['Date'] = pd.Categorical(data['Date'], categories=['12 2022', '1 2023'], ordered=True)

    # Only IG Reels in dataset, so we can erase this column
    data = data.drop(columns = ['Post Type', 'Social Channel'])

    # IG Reels not longer than 3 minutes
    data = data[data['Video Duration'] <= 180]

    # Missing in play and views 0.1% -> delete these rows
    data = data.dropna(subset=['Views', 'Plays'])

    # To view Reel you have to play it -> plays must be greater than views
    data = data[data['Views'] <= data['Plays']]

    # 5.6% likes are missing and 1.5% comments are missing -> additional column
    # fill with 0

    data['Unknown Comments'] = data['Comments'].isna()
    data['Comments'] = data['Comments'].fillna(0)
    data['Unknown Likes'] = data['Likes'].isna()
    data['Likes'] = data['Likes'].fillna(0)

    return data



def total_kpis(cleaned_data):
    ''' Function return total KPIs of the dataset.'''

    # Total KPIs
    total_comments = cleaned_data['Comments'].sum()
    total_likes = cleaned_data['Likes'].sum()
    total_plays = cleaned_data['Plays'].sum()
    impressions = cleaned_data['Views'].sum()

    # Engagement Rate
    data_like_and_comments_known = cleaned_data[(~cleaned_data['Unknown Likes']) & (~cleaned_data['Unknown Comments'])]
    engagement_rate = (data_like_and_comments_known['Comments'].sum() + data_like_and_comments_known['Likes'].sum()) / data_like_and_comments_known['Views'].sum()

    return {
        'Total Comments': total_comments,
        'Total Likes': total_likes,
        'Total Plays': total_plays,
        'Total Views': impressions,
        'Engagement Rate': engagement_rate}


def grouped_data_influencer(cleaned_data):
    ''' Function return grouped data by influencer type.'''

    # Total and Average Values per Influencer
    total_values_per_influencer = cleaned_data[['Influencer ID',
                                    'Comments',
                                    'Likes',
                                    'Plays',
                                    'Views',
                                    'Post ID',
                                    'Followers on Postday',
                                    'Influencer Type',
                                    'Video Duration'
                                   ]].groupby('Influencer ID', as_index=False).agg(
                                {
                                    'Comments' : ['mean','sum'],
                                    'Likes' : ['mean','sum'],
                                    'Plays' : ['mean','sum'],
                                    'Views' : ['mean','sum'],
                                    'Post ID' : 'count',
                                    'Followers on Postday': ['mean', 'std'],
                                    'Influencer Type': 'first',
                                    'Video Duration' : 'mean'
                                })

    total_values_per_influencer.columns = [
        'Influencer ID',
        'Average Comments per post',
        'Total Comments',
        'Average Likes per post',
        'Total Likes',
        'Average Plays per post',
        'Total Plays',
        'Average Views per post',
        'Total Views',
        'Total number of posts',
        'Average number of followers',
        'Standard deviation of number of followers',
        'Influencer Type',
        'Average video duration in s'
    ]

    # Engagement Rate per Influencer without any Missing values in Likes and Comments
    data_like_and_comments_known = cleaned_data[(~cleaned_data['Unknown Likes']) & (~cleaned_data['Unknown Comments'])]

    engagement_per_influencer = data_like_and_comments_known[['Influencer ID',
                                                          'Comments',
                                                          'Likes',
                                                          'Plays',
                                                          'Views',
                                                          'Post ID',
                                                          'Followers on Postday',
                                                          'Influencer Type',
                                                          'Video Duration']].groupby('Influencer ID', as_index=False).agg(
                                                            {
                                                            'Comments' : 'sum',
                                                            'Likes' : 'sum',
                                                            'Plays' : 'sum',
                                                            'Views' : 'sum',
                                                            'Post ID' : 'count',
                                                            'Followers on Postday': 'mean',
                                                            'Influencer Type': 'first',
                                                            'Video Duration' : 'mean'
                                                            })

    engagement_per_influencer.columns = [
        'Influencer ID',
        'Total Comments',
        'Total Likes',
        'Total Plays',
        'Total Views',
        'Total number of posts',
        'Average number of followers',
        'Influencer Type',
        'Average video duration in s'
    ]

    engagement_per_influencer['Engagement rate'] = (engagement_per_influencer['Total Comments'] + engagement_per_influencer['Total Likes'])/(engagement_per_influencer['Total Views'])

    return {
        'Total Values per Influencer': total_values_per_influencer,
        'Engagement per Influencer': engagement_per_influencer
    }



def grouped_data_brand(cleaned_data):
    ''' Function return grouped data by brand.'''

    total_values_per_brand = cleaned_data[['Influencer Type',
                                    'Comments',
                                    'Likes',
                                    'Plays',
                                    'Views',
                                    'Post ID'
                                   ]].groupby('Influencer Type', as_index=False).agg(
                                {
                                    'Comments' : 'sum',
                                    'Likes' : 'sum',
                                    'Plays' : 'sum',
                                    'Views' : 'sum',
                                    'Post ID' : 'count',
                                })

    total_values_per_brand.columns = [
        'Influencer Type',
        'Total Comments',
        'Total Likes',
        'Total Plays',
        'Total Views',
        'Total number of posts'
    ]

    return total_values_per_brand


def grouped_data_date(cleaned_data):
    ''' Function return grouped data by date.'''

    total_values_per_date = cleaned_data[['Date',
                                    'Comments',
                                    'Likes',
                                    'Plays',
                                    'Views',
                                    'Post ID'
                                   ]].groupby('Date', as_index=False).agg(
                                {
                                    'Comments' : 'sum',
                                    'Likes' : 'sum',
                                    'Plays' : 'sum',
                                    'Views' : 'sum',
                                    'Post ID' : 'count',
                                })


    total_values_per_date.columns = [
        'Date',
        'Total Comments',
        'Total Likes',
        'Total Plays',
        'Total Views',
        'Total number of posts'
    ]

    return total_values_per_date




if __name__ == "__main__":
    # Load the cleaned dataset
    cleaned_data = clean_data()
    print(cleaned_data.head())
    print(len(cleaned_data))

    # Test total kpis
    print(total_kpis(cleaned_data))


    # Test grouped data by influencer
    grouped_data_inf = grouped_data_influencer(cleaned_data)
    total_values_per_influencer = grouped_data_inf['Total Values per Influencer']
    engagement_per_influencer = grouped_data_inf['Engagement per Influencer']

    min_comment = total_values_per_influencer['Average Comments per post'].min()
    max_comment = total_values_per_influencer['Average Comments per post'].max()
    min_like = total_values_per_influencer['Average Likes per post'].min()
    max_like = total_values_per_influencer['Average Likes per post'].max()
    min_views = total_values_per_influencer['Average Views per post'].min()
    max_views = total_values_per_influencer['Average Views per post'].max()
    min_plays = total_values_per_influencer['Average Plays per post'].min()
    max_plays = total_values_per_influencer['Average Plays per post'].max()


    print('Min Avg Comments: ', min_comment)
    print('Max Avg Comments: ', max_comment)
    print('Min Avg Like: ', min_like)
    print('Max Avg Like: ', max_like)
    print('Min Avg Views: ', min_views)
    print('Max Avg Views: ', max_views)
    print('Min Avg Plays: ', min_plays)
    print('Max Avg Plays: ', max_plays)

    min_engagement_rate = engagement_per_influencer['Engagement rate'].min()
    max_engagement_rate = engagement_per_influencer['Engagement rate'].max()

    print('Minimum Engagement rate: ', min_engagement_rate)
    print('Maximum Engagement rate: ', max_engagement_rate)
