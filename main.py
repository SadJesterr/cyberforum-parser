from sql import create_db, insert_data
from forumParser import forumParser
import numpy as np
import pandas as pd
from utils import *

# Парсинг
parser = forumParser()
data = parser.parse_forum(PAGE_START=1,PAGE_STOP=2)

# Обработка данных
# print(data)

# Добавление данных в БД
# create_db()

# ['username', 'comments', 'datetime', 'rating', 'theme', 'link','user_id', 'theme_id', 'message_id', 'previous_message']
# theme_data, author_data, comment_data
mask = data['previous_message'] == -1

theme_data = data[mask][['theme', 'comments']].to_numpy()
author_data = data[mask]['username'].to_frame(name='username').to_numpy()
comment_data = data[['comments','datetime','rating']].to_numpy()

theme_id = data[mask][['theme', 'comments']].nunique().to_numpy()


# print(comment_data)
# insert_data(theme_data=theme_data, 
#             author_data=author_data,
#             comment_data=comment_data)


# Создание графика
make_plot(data)
print(data)