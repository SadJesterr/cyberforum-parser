from bs4 import BeautifulSoup
import requests
import re
import os
import pandas as pd
import numpy as np
from utils import *

class forumParser:
    def __init__(self):
        self.headers = {
            'Accept': "text/html",
            'User-Agent': os.getenv('USER_AGENT')
            # st_useragent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
            #         "Safari/537.36")
        }

    # проверка работы запроса
    def get_status_code(self, response):
        return response.status_code

    # получение ссылок на страницы
    def get_cyberforum_pages_links(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')

        pages = soup.find('div', class_='pagenav').findAll('td', class_='alt1') 
        links = []
        for href in pages:
            links.append(href.a.get("href"))
        return links[0]

    # получение названий тем форума
    def get_cyberforum_thread_title(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')
        pages = soup.find_all('a', id=re.compile('^thread_title'))

        links = []
        for link in pages:
            title = link.text
            links.append(title)
        return links

    # получение ссылок на темы форума
    def get_cyberforum_thread_links(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')
        pages = soup.find_all('a', id=re.compile('^thread_title'))
        links = []
        for link in pages:
            url = link['href']
            links.append(url)
        return links

    # смена текущей страницы
    def change_current_page(self, url = ''):
        new_url = re.sub(r'page(\d+)\.html', 
                        lambda match: f'page{int(match.group(1))+1}.html', url)
        return new_url

    # 
    def get_cyberforum_thread_comment(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')
        postMessage = soup.find_all('div', id=re.compile('^post_message'))

        comments = []
        for comment in postMessage:
            title = comment.text
            title = re.sub(r'[\n\t\r]', '', title)
            comments.append(title)

        return comments

    def get_cyberforum_thread_author(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')
        
        authorMessage = soup.find_all('table', id=re.compile('^post'))
        
        authors = []
        for author in authorMessage:
            name = author.text
            name = re.sub(r'[\n\t\r]', '', name).split()
            authors.append(name[0])
        return authors

    def get_cyberforum_thread_comments_date(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')
        
        commentsDate = soup.find_all('table', id=re.compile('^post'))
        
        dates = []
        for date in commentsDate:
            currentDate = date.text
            currentDate = re.sub(r'[\n\t\r]', '', currentDate)
            datetimeMatch = re.search(r'(\d{2}\.\d{2}\.\d{4}, \d{2}:\d{2})', currentDate)
            if datetimeMatch:
                datetime = datetimeMatch.group(1)
                dates.append(datetime)
        return dates

    def get_cyberforum_thread_comments_rate(self, response):
        src = response.text
        soup = BeautifulSoup(src, 'html.parser')
        
        commentsRate = soup.find_all('table', id=re.compile('^post'))
        # commentsRate = soup.find_all('span', 'thumbs-post-rate')

        rates = []
        for rate in commentsRate:
            currentRate = rate.text
            currentRate = re.sub(r'[\n\t\r]', '', currentRate).split()
            rateMatch = re.search(r'(\d+)$', currentRate[-1])
            if rateMatch:
                rates.append(rateMatch.group(1))
        return rates


    def parse_forum(self):
        PAGE_START = 1
        PAGE_STOP = 21
        # все комментарии с ссылки
        currentComments = []
        # все авторы комментариев
        currentAuthor = []
        # все даты написания комментариев
        currentDateComments = []
        # все оценки комментариев
        currentRateComments = []

        # текущая страница
        currentPage = []
        # все темы со страницы
        currentTheme = []
        # все ссылки на темы со страниц
        currentThemeLinks = []

        url = 'https://www.cyberforum.ru/python-web/'
        # url = f'https://www.cyberforum.ru/python-web-page{PAGE}.html'


        data = []
        for page in range(PAGE_START, PAGE_STOP):
            # получение html
            response = requests.get(url=url, 
                                    headers=self.headers)

            # t = self.get_status_code(response)
            print(self.get_status_code(response))
            src = response.text
            soup = BeautifulSoup(src, 'html.parser')

            currentPage.append(self.get_cyberforum_pages_links(response))
            currentTheme.append(self.get_cyberforum_thread_title(response))
            currentThemeLinks.append(self.get_cyberforum_thread_links(response))

            # print(currentPage)
            # print(change_current_page(currentPage))
            # print(currentTheme)
            # print(currentThemeLinks)
            log_info(f'Обрабатывается страница {page}')

            for link in range(len(currentThemeLinks[-1])):
                themeLink = currentThemeLinks[-1][link]

                if (themeLink.find('https://www.cyberforum.ru/') < 0):
                    themeLink = 'https://www.cyberforum.ru/' + themeLink

                # print('Обрабатывается ссылка: '+themeLink)
                log_info('Обрабатывается ссылка: '+themeLink)

                response = requests.get(url=themeLink, 
                                    headers=self.headers)
                currentComments.append(self.get_cyberforum_thread_comment(response))
                currentAuthor.append(self.get_cyberforum_thread_author(response))
                currentDateComments.append(self.get_cyberforum_thread_comments_date(response))
                currentRateComments.append(self.get_cyberforum_thread_comments_rate(response))

                themeLink = currentThemeLinks[-1][link]

                arrs = [
                    currentAuthor[-1],
                    currentComments[-1],
                    currentDateComments[-1],
                    currentRateComments[-1],
                    [currentTheme[-1][link] for i in range(len(currentComments[-1])+1)]
                        ]
                
                # data = []
                for i in range(len(arrs[0])):
                    for arr in arrs:
                        data.append(arr[i])
                    data.append(themeLink)

                # print(data)
                # data = np.array(data).reshape(6, len(data)//6) 
                # print(data)
                
                # break

            url = self.change_current_page(url)
            # print(f'Обработано вопросов: {len(currentTheme[-1])*len(currentTheme)}')
            log_info(f'Обработано вопросов: {len(currentTheme[-1])*len(currentTheme)}')


        # COLUMNS = ['username', 'user_id', 'theme', 'theme_id', 'message', 'prev_message', 'message_id', 'raiting', 'link', 'datatime']
        columns = ['username', 'comments', 'datetime', 'rating', 'theme', 'link']
        data = np.array(data).reshape(len(data)//6, 6)
        df = pd.DataFrame(data, columns=columns)
        df['user_id'] = pd.factorize(df['username'])[0]

        df['theme_id'] = pd.factorize(df['theme'])[0]

        # Создаем столбец с id для каждого сообщения
        # df['message_id'] = range(1, len(df) + 1)
        df['message_id'] = df.groupby('theme_id').cumcount() + 1

        # Группируем по темам и применяем метод shift() для создания столбца previous_message
        df['previous_message'] = df.groupby('theme')['message_id'].shift()

        # Заполняем пропуски в previous_message значением -1 (или другим, по вашему выбору)
        df['previous_message'] = df['previous_message'].fillna(-1).astype(int)

        log_info('Создан датафрейм')

        return df