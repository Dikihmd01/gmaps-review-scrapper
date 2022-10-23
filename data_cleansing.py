import pandas as pd
import emoji
import csv
import re

path = './dataset/review.csv'
# print(data)

def clean_sentences(path):
    usernames = []
    reviews = []

    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            usernames.append(row[1])
            reviews.append(row[2])
    
    removed_new_line = [sentence.replace('\n', '') for sentence in reviews]
    removed_date = [re.sub(re.compile('\d{2}.\d{2}.\d{4}'), '', review) for review in removed_new_line]
    removed_diterjemahkan_oleh = [
        review.replace('(Diterjemahkan oleh Google)', '') for review in removed_date
    ]
    removed_white_space = [review.lstrip() for review in removed_diterjemahkan_oleh]
    removed_dash_in_first_char = [
        review.replace('- ', '') if review[0] == '-' else review for review in removed_white_space
    ]
    removed_emojis = [emoji.replace_emoji(review, replace='') for review in removed_dash_in_first_char]
    cleaned_reviews = removed_emojis

    data = {
        'username': usernames,
        'review': cleaned_reviews
    }
    
    return data

def to_df(data):
    df = pd.DataFrame(data)
    return df

def drop_duplicate(data):
    data.drop_duplicates(subset='review', inplace=True, keep=False)
    df = data.reset_index(drop=True)

    return df

def main():
    reviews = clean_sentences(path)
    df = to_df(reviews)
    cleaned_df = drop_duplicate(df)
    return cleaned_df

if __name__ == '__main__':
    print(main())

