import re
import pandas as pd

def preprocess(data):
    pattern = "\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'User_messages': messages, 'message_date': dates})
    user = []
    Message = []
    for message in df['User_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            Message.append(entry[2])
        else:
            user.append('Group_notification')
            Message.append(entry[0])

    df['User'] = user
    df['message'] = Message
    # cnvert message date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period
    return df
