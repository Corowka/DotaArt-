import requests
from bs4 import BeautifulSoup

def get_reviews_with_offset(n):
    url = f'https://steamcommunity.com/app/570/homecontent/?userreviewscursor=AoIIP2zPSneTyZsC&userreviewsoffset={(n-1)*10}&p={n}&workshopitemspage=10&readytouseitemspage=10&mtxitemspage={n}&itemspage={n}&screenshotspage={n}&videospage={n}&artpage={n}&allguidepage={n}&webguidepage={n}&integratedguidepage={n}&discussionspage={n}&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=570&appHubSubSection=10&appHubSubSection=10&l=english&filterLanguage=russian&searchText=&maxInappropriateScore=50&forceanon=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    reviews = []

    for review in soup.find_all("div", class_="apphub_Card modalContentLink interactable"):
        profile_info = review.find("div", class_="apphub_CardContentAuthorName")
        if profile_info:
            profile_name = profile_info.text.strip()
            reviews.append(profile_name)

    return reviews

if __name__ == "__main__":
    all_reviews = []
    for offset in range(0, 100, 10):  # Проходим по значениям offset с шагом 10 до 100
        reviews_with_offset = get_reviews_with_offset(offset)
        all_reviews.extend(reviews_with_offset)

    print("Профили, оставившие отзывы:")
    print(all_reviews)

