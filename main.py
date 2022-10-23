from module import google_map_review_scrapper

url = 'https://www.google.com/maps/place/National+Monument/@-6.1753924,106.8249641,17z/data=!4m7!3m6!1s0x2e69f5d2e764b12d:0x3d2ad6e1e0e9bcc8!8m2!3d-6.1753924!4d106.8271528!9m1!1b1'
scroll_limit = 10

scrapper = google_map_review_scrapper

page_content = scrapper.get_page_content(url, scroll_limit)
review = scrapper.get_review(page_content)
to_df = scrapper.to_dataframe(review)
print(to_df)
scrapper.to_csv(to_df)

