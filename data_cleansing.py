import pandas as pd
import emoji
import csv
import re
from datetime import date
import os


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

    removed_new_line = [review.replace('\n', '') for review in reviews]
    removed_date = [re.sub(re.compile('\d{2}.\d{2}.\d{4}'), '', review) for review in removed_new_line]
    removed_white_space = [review.lstrip() for review in removed_date]
    removed_dash_in_first_char = [review.replace('- ', '') if review[0] == '-' else review for review in removed_white_space]
    removed_emojis = [emoji.replace_emoji(review, replace='') for review in removed_dash_in_first_char]
    removed_text_before_parenthesis = [re.sub(r'.*((Diterjemahkan oleh Google)*[)])', '', review) for review in removed_emojis]
    lower_text_review = [review.lower() for review in removed_text_before_parenthesis]
    removed_quotation = [review.replace('"', '') for review in lower_text_review]
    cleaned_reviews = removed_quotation

    data = {
        'usernames': usernames,
        'reviews': cleaned_reviews
    }

    return data


def to_df(data):
    df = pd.DataFrame(data)
    return df


def drop_duplicate(data):
    data.drop_duplicates(subset='reviews', inplace=True, keep=False)
    df = data.reset_index(drop=True)

    return df


def to_csv(data):
    os.makedirs('dataset', exist_ok=True)
    file_name = f'dataset/clean/review-{date.today()}.csv'
    data.to_csv(file_name)


def main():
    reviews = clean_sentences(path)
    df = to_df(reviews)
    cleaned_df = drop_duplicate(df)
    to_csv(cleaned_df)
    return cleaned_df


if __name__ == '__main__':
    print(main())
