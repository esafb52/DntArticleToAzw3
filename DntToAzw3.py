import os
import platform

from bs4 import BeautifulSoup


def get_calibre_path():
    res = platform.architecture()[0]
    calibre_path = 'C:/PROGRA~2/Calibre2'
    if '32bit' not in res:
        calibre_path = 'C:/PROGRA~1/Calibre2'
    if os.path.exists(calibre_path):
        return calibre_path
    return None


def get_article_files(soup_content):
    links = soup_content.find_all('a', href=True)
    return [item.get('href') for item in links]


def get_articles_title(book):
    course_info = os.path.join(book, 'path.html')
    with open(course_info, mode='r', encoding='utf-8') as book:
        soup = BeautifulSoup(book, 'html.parser')
        all_titles = soup.findAll('h2')
        return [str(title.text).replace(' ', '-') for title in all_titles]


def get_articles_content(art_dir):
    course_info = os.path.join(art_dir, 'path.html')
    with open(course_info, mode='r', encoding='utf-8') as course_info:
        content = course_info.read().split('<h2>')[1:]
        return content


def body_section(book_title):
    return '''
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <title>{0}</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <link type="text/css" rel="stylesheet" href="styles.css">
            </head>
            <body dir='rtl'>
            '''.format(book_title)


def end_body_section():
    return '''
                </body>
                </html>
           '''


def write_book(courses, title, article_dir, save_dir):
    start_body_section = "class='main'"
    comment_section = '<h3>نظرات</h3>'
    course_file_name = '{0}.html'.format(title)
    write_mode = False
    new_course = os.path.join(save_dir, course_file_name)

    with open(new_course, 'w', encoding='utf-8') as file:
        file.write(body_section(title))
        for course in courses:
            if not course.endswith('.html') or title is None:
                continue
            with open(os.path.join(article_dir, course), 'r', encoding='utf-8') as book_content:
                for line in book_content.readlines():
                    this_line = str(line).strip()
                    if comment_section in this_line:
                        write_mode = False
                        file.write('<br><br><br>')
                        break
                    if start_body_section in this_line:
                        write_mode = True
                    if write_mode:
                        file.write(this_line + '\n')
        file.write(end_body_section())
        print('task  {0} complete'.format(title))


def merge_and_convert_articles_content_to_html(articles_dir, out_book_dir):
    content = get_articles_content(articles_dir)
    titles = get_articles_title(articles_dir)
    for part in content:
        try:
            soup = BeautifulSoup(part, 'html.parser')
            course_files = get_article_files(soup)
            course_title = titles.pop(0)
            write_book(course_files, course_title, articles_dir, out_book_dir)
        except Exception as e:
            print(e, 'error!!!')


def convert_html_article_to_azw3(articles_dir):
    if get_calibre_path() is not None:
        html_book_files = os.listdir(articles_dir)
        for file in html_book_files:
            if file.endswith('.html'):
                html_book_file = os.path.join(articles_dir, file)
                azw3_file = os.path.join(articles_dir, file[:-4] + 'azw3')
                if not os.path.exists(azw3_file):
                    try:
                        cmd = '{0}/ebook-convert.exe {1} {2}'.format(get_calibre_path(), html_book_file, azw3_file)
                        os.system(cmd)
                    except Exception as e:
                        print(e, 'error!!!!')
    else:
        print('calibre is not install on this pc !!!')


if __name__ == '__main__':

    print('=' * 10, 'start !!!', '=' * 10)
    articles = 'C:/Users/masiha/Desktop/dnt-1399-10-16/OPF/articles'
    book_out_dir = 'C:/Users/masiha/Desktop/dnt-1399-10-16/final_bbc2000'

    if not os.path.exists(book_out_dir):
        os.mkdir(book_out_dir)

    merge_and_convert_articles_content_to_html(articles, book_out_dir)
    convert_html_article_to_azw3(book_out_dir)
    print('=' * 10, 'complete all tasks  !!!', '=' * 10)
