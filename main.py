import requests
from bs4 import BeautifulSoup
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}


def get_movies(url, i):
    print(url)
    req = requests.get(url, headers)
    with open(f"{i}.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    with open(f"{i}.html", encoding="utf-8") as file:
        src = file.read()
    
    try:
        soup = BeautifulSoup(src, "lxml")
        movies = soup.find_all('tr', attrs={'class': ['nb', 'even']})

        cinema_dict = {}
        m_dict = {}
        for item in movies: 
            
            movie_name = item.find('td', class_='title')
            movie_place = item.find('td', class_='place').find('a').text   
            movies_time = item.find('td', class_='time').find_all('span')
            
            times = []
            if movie_name:
                movie_name_check = movie_name.find('a').text
                cinema_dict = {}
            
            for t in movies_time:
                t = t.text
                if t not in times:
                    times.add(t.text)

            cinema_dict[movie_place] = sorted(times)
            m_dict[movie_name_check] = cinema_dict

        if len(m_dict):
            with open(f'{i}.json', 'w', encoding="utf-8") as file:
                json.dump(m_dict, file, indent=4, ensure_ascii=False)

    except Exception as ex:
        print(ex)
        print('Ouch...')


def main():

    url = 'https://www.afisha.uz/afisha/movies/?date=2022-01-11'
    req = requests.get(url, headers)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    with open("index.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    menu = soup.find('div', class_='schedule_menu')
    urls = menu.find_all('li')
    i = 0
    for url in urls:
        url = url.find('a')
        if url:
            i += 1
            url = url.get('href')
            get_movies(f"https://www.afisha.uz{url}", i)


if __name__ == "__main__":
    main()
