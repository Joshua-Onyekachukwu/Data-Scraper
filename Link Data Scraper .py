import requests
from bs4 import BeautifulSoup
import pprint

base_url = 'https://news.ycombinator.com/news'
headers = {'User-Agent': 'Mozilla/5.0'}

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    total_score = 0  # Variable to hold the total sum of scores
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.a.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            score = int(vote[0].getText().replace(' points', ''))
            if score > 99:
                hn.append({'title': title, 'link': href, 'votes': score})
                total_score += score  # Add the score to the total sum
            print(score)

    print(f"Total Score: {total_score}")  # Print the total score after the loop
    return hn

def scrape_hacker_news(pages=2):
    hn = []
    url = base_url
    page_count = 0  # Counter for the number of pages scraped

    while url and page_count < pages:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        links = soup.select('.titleline')
        subtext = soup.select('.subtext')

        # Scrape the current page
        hn.extend(create_custom_hn(links, subtext))

        # Find the next page URL
        next_link = soup.select('.morelink')
        if next_link:
            url = 'https://news.ycombinator.com/' + next_link[0].get('href')
        else:
            url = None  # No more pages to scrape

        page_count += 1  # Increment the page count

    return hn

# Scrape the stories and sort them by votes
hn_stories = scrape_hacker_news(pages=2)
sorted_stories = sort_stories_by_votes(hn_stories)

# Print sorted stories
pprint.pprint(sorted_stories)

print(f'Total number of scraped data points is {len(sorted_stories)}')
