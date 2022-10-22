from module import google_map_review_scrapper

url = 'https://www.google.com/maps/place/Gn.+Galunggung/@-7.2666665,108.0716667,15z/data=!4m7!3m6!1s0x2e6f52ad6cc52ec7:0x46410a2c9ef6157d!8m2!3d-7.2666667!4d108.0716667!9m1!1b1'
scroll_limit = 10

scrapper = google_map_review_scrapper

page_content = scrapper.get_page_content(url, scroll_limit)
review = scrapper.get_review(page_content)
to_df = scrapper.to_dataframe(review)
print(to_df)

