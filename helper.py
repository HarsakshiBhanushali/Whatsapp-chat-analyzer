import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji

from collections import Counter
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user !='overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages= df[df['message'] == '<Media omitted>\n'].shape[0]
    #fetch links
    links =[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/ df.shape[0]) * 100, 2).reset_index().rename(columns ={'index': 'name', 'user':'percent'})
    return x,df

def remove_stopwords(text, stop_words):
    return " ".join([word for word in text.split() if word.lower() not in stop_words])

def create_wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    # ✅ Remove "<Media omitted>\n" and empty messages
    df = df[(df['message'] != '<Media omitted>\n') & (df['message'].str.strip() != '')]

    # ✅ Remove emojis
    df['message'] = df['message'].apply(remove_emojis)

    # ✅ Load stop words
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().split())  # Convert stop words to a set

    # ✅ Remove stop words from messages
    df['message'] = df['message'].apply(lambda text: remove_stopwords(text, stop_words))

    # ✅ Generate WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

import re
import pandas as pd
from collections import Counter

def remove_emojis(text):
    emoji_pattern = re.compile("["  
        "\U0001F600-\U0001F64F"  # Emoticons  
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs  
        "\U0001F680-\U0001F6FF"  # Transport & map symbols  
        "\U0001F700-\U0001F77F"  # Alchemical symbols  
        "\U0001F780-\U0001F7FF"  # Geometric shapes  
        "\U0001F800-\U0001F8FF"  # Supplemental arrows  
        "\U0001F900-\U0001F9FF"  # Supplemental symbols & pictographs  
        "\U0001FA00-\U0001FA6F"  # Chess symbols, etc.  
        "\U0001FA70-\U0001FAFF"  # Symbols for heads  
        "\U00002702-\U000027B0"  # Dingbats  
        "\U000024C2-\U0001F251"  # Enclosed characters  
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def most_common_words(selected_user, df):
    # Load stop words
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        message = remove_emojis(message)  # Remove emojis
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Create DataFrame with column names
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

    return most_common_df

# Use remove_emojis(message) before splitting words
def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([char for char in message if emoji.is_emoji(char)])  # Proper emoji detection

    if emojis:
        emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    else:
        emoji_df = pd.DataFrame(columns=['emoji', 'count'])  # Return empty dataframe if no emojis

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    # Corrected column names and fixed reset_index()
    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline










