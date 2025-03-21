from utils import extract_news
import pprint
# Input company name
company = input("Enter a company name: ")

# Fetch news
news_data = extract_news(company)

# Print structured output
pprint.pprint(news_data)
'''
if news_data["Audio"]:
    os.system(f"start {news_data['Audio']}")  
'''