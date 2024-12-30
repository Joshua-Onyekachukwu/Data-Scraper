# Data-Scraper
Hacker News Scraper Documentation


Overview

This script is designed to scrape stories from the Hacker News website, collect data about the title, URL, and votes, and then sort the stories by the number of votes they have received. The scraper can be configured to limit the number of pages it scrapes.
Requirements

    Python 3.x
    requests library
    beautifulsoup4 library

To install the required libraries, run:

    pip install requests beautifulsoup4



How It Works

The script scrapes stories from the Hacker News website (https://news.ycombinator.com/news) and processes them in the following steps:

    Scraping Pages: It starts by scraping the first page of Hacker News and continues to scrape subsequent pages until the specified number of pages has been processed or there are no more pages left.

    Collecting Data: For each page, it collects the following information:
        Title: The title of each story.
        Link: The URL of the story.
        Votes: The number of votes (points) the story has received.

    Filtering by Votes: The scraper only collects stories that have more than 99 votes. This helps filter out less popular stories.

    Sorting by Votes: After collecting the stories, they are sorted in descending order by the number of votes they have received.

    Limiting Scraped Pages: The script can be configured to scrape a specific number of pages by specifying the pages parameter. The default is 2 pages.

Functions
sort_stories_by_votes(hnlist)

This function sorts a list of stories (hnlist) by their vote count in descending order.
Parameters:

    hnlist: A list of dictionaries, where each dictionary represents a story. Each dictionary contains the following keys:
        title: The title of the story.
        link: The URL of the story.
        votes: The number of votes the story has received.

Returns:

    A sorted list of stories, with the most voted stories first.

create_custom_hn(links, subtext)

This function processes the HTML elements that contain the story titles, links, and votes. It extracts the relevant data for each story and adds it to a list if the story has more than 99 votes.
Parameters:

    links: A list of BeautifulSoup elements containing the titles and links of the stories.
    subtext: A list of BeautifulSoup elements containing the vote count for each story.

Returns:

    A list of dictionaries representing the stories, each with the following keys:
        title: The title of the story.
        link: The URL of the story.
        votes: The number of votes the story has received.

scrape_hacker_news(pages=2)

This is the main function that scrapes Hacker News. It begins at the base URL and continues to scrape pages until it reaches the specified number of pages or there are no more pages to scrape.
Parameters:

    pages: The number of pages to scrape. The default is 2 pages.

Returns:

    A list of dictionaries representing the stories scraped, each containing:
        title: The title of the story.
        link: The URL of the story.
        votes: The number of votes the story has received.

Example Usage

# Scrape 2 pages from Hacker News and sort stories by votes
hn_stories = scrape_hacker_news(pages=2)
sorted_stories = sort_stories_by_votes(hn_stories)

# Print the sorted stories
import pprint
pprint.pprint(sorted_stories)

# Print the total number of scraped stories
print(f'Total number of scraped data points is {len(sorted_stories)}')

Output:

    A sorted list of stories from Hacker News, displayed in descending order of votes.
    The total number of stories that were scraped.

Error Handling

The script is designed to handle basic errors, such as:

    Missing next page link: If there is no "next" page link, the script will stop scraping.
    Empty pages: If there are no stories on a page, it will still proceed to the next page.

How to Modify

    To change the number of pages scraped, simply modify the pages parameter in the scrape_hacker_news(pages=n) function call.
    To adjust the minimum vote threshold for collecting stories, modify the if score > 99: line in the create_custom_hn function.

Conclusion

This scraper is a simple yet effective tool to gather top stories from Hacker News. By customizing the number of pages scraped, you can control how much data to collect and how to analyze popular stories on the site.
