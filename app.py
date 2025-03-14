import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)

        st.title('Top Statistics')
        col1, col2, col3, col4 =st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        #Timeline
        st.title('Monthly timeline')
        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], marker='o', linestyle='-')  # Added markers for clarity
        plt.xticks(rotation='vertical')
        plt.xlabel('Month-Year')
        plt.ylabel('Message Count')
        plt.title('Monthly Message Timeline')
        st.pyplot(fig)

        #finding busiest users in the group
        if selected_user == 'overall':
            st.title('Most Busy users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)

        # ✅ Fix: Use column names instead of numerical indexing
        fig, ax = plt.subplots()
        ax.bar(most_common_df['Word'], most_common_df['Frequency'])
        plt.xticks(rotation=90)  # Rotate labels for better readability
        st.title('Most common words')
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)

        st.title('Emoji Analysis')

        # Use st.columns() instead of st.beta_columns()
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df['count'].head(),
                    labels=emoji_df['emoji'].head(),
                    autopct='%1.1f%%',
                    startangle=90,
                    wedgeprops={'edgecolor': 'white'}
                )
                st.pyplot(fig)
            else:
                st.write("No emojis found in the chat.")


