import  re
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    # 1. fetch number of messages
    num_messages = df.shape[0]
    # 2. number of words
    word = []
    for i in df['message']:
        word.extend(i.split())
    # 3. number of merdia
    num_media_msg =df[df['message'] == '<Media omitted>\n'].shape[0]
    # 4. number of links
    urls = []
    for i in df['message']:
        urls.extend(re.findall(r'(https?://[^\s]+)', i))

    return num_messages,len(word),num_media_msg,len(urls)

def most_busy_user(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df['User'].shape[0]) * 100, 2).reset_index().rename(columns={'User': 'name', 'count': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    temp = df[df['User'] != 'Group_notification']
    df = temp[temp['message'] != '<Media omitted>\n']
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'Group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    word = []
    for message in temp['message']:
        word.extend(message.split())

    return_df = pd.DataFrame(Counter(word).most_common(20))
    return return_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    activity_map = df.pivot_table(index='day_name',columns = 'period',values='message',aggfunc='count').fillna(0)
    return activity_map





