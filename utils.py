import matplotlib.pyplot as plt
import logging


logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', encoding='utf-8', filemode='w', filename='logs.txt', level="INFO",format='%(levelname)s %(asctime)s: %(message)s')

def log_info(log):
    logging.info(log)

def log_error(log):
    logging.error(log)

def make_plot(df):
    plt.figure(figsize=(12, 6))

    avg_comments_by_theme = df.groupby('theme_id').mean()
    plt.subplot(3, 1, 1)
    plt.bar(avg_comments_by_theme.index, avg_comments_by_theme['message_id'])
    plt.xlabel('Номер треда')
    plt.ylabel('Среднее значение')
    plt.title('Среднее количество комментариев')

    count_comments_by_theme = df.groupby('theme_id').count()-1
    plt.subplot(3, 1, 2)
    plt.bar(count_comments_by_theme.index, count_comments_by_theme['message_id'])
    plt.xlabel('Номер треда')
    plt.ylabel('Количество')
    plt.title('Количество комментариев-ответов')

    mask = df['message_id'] > 4
    user_comments_count  = df[mask].groupby('theme_id').count()
    plt.subplot(3, 1, 3)
    plt.bar(user_comments_count.index, user_comments_count['message_id'])
    plt.xlabel('Номер треда')
    plt.ylabel('Количество')
    plt.title('Кол-во комментариев пользователей, которые оставили под темой больше 3-х комментариев')

    plt.tight_layout()
    plt.savefig('plot.png')
    log_info("График создан и сохранён в рабочую директорию под именем plot.png")