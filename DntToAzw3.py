import os
import platform

from bs4 import BeautifulSoup


def get_calibre_path():
    res = platform.architecture()
    if '32bit' in res[0]:
        return 'C:/PROGRA~2/Calibre2'
    return 'C:/PROGRA~1/Calibre2'


def get_course_files(soup_content):
    links = soup_content.find_all('a', href=True)
    return [item.get('href') for item in links]


def get_course_titles(book):
    course_info = os.path.join(book, 'path.html')
    with open(course_info, mode='r', encoding='utf-8') as book_title:
        ls = ['نقشه راه']
        soup = BeautifulSoup(book_title, 'html.parser')
        all_titles = soup.findAll('h2')
        for title in all_titles:
            this_title = str(title.text).replace(' ', '-').replace('.', '')
            ls.append(this_title)
        return ls


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


def end_body():
    return '''
                </body>
                </html>
           '''


def write_book(courses, title, article_dir, course_out_dir):
    start_body_section = "class='main'"
    comment_section = '<h3>نظرات</h3>'
    course_file_name = '{0}.html'.format(title).replace('  ', '')
    write_mode = False

    course_file = open(os.path.join(course_out_dir, course_file_name), 'w', encoding='utf-8')
    course_file.write(body_section(title))

    for course in courses:
        this_book = os.path.join(article_dir, course)
        if not course.endswith('.html') or title is None:
            continue
        with open(this_book, 'r', encoding='utf-8') as book_content:
            for line in book_content.readlines():
                this_line = str(line).strip()
                if comment_section in this_line:
                    write_mode = False
                    course_file.write('<br><br><br>')
                    break
                if start_body_section in this_line:
                    write_mode = True
                if write_mode:
                    course_file.write(this_line + '\n')

    course_file.write(end_body())
    course_file.close()
    print('task  {0} complete'.format(title), '=' * 40)


def get_articles_content(articles_dir, out_book_dir):
    if not os.path.exists(out_book_dir):
        os.mkdir(out_book_dir)
    course_info = os.path.join(articles_dir, 'path.html')
    with open(course_info, mode='r', encoding='utf-8') as course_info:
        content = course_info.read().split('<h2>')
        titles = get_course_titles(articles_dir)
        for part in content:
            soup = BeautifulSoup(part, 'html.parser')
            course_files = get_course_files(soup)
            course_title = titles.pop(0)
            write_book(course_files, course_title, articles_dir, out_book_dir)


def convert_to_azw3(articles_dir):
    out_files = os.listdir(articles_dir)
    for file in out_files:
        if '.html' in file:
            file_path = os.path.join(articles_dir, file)
            out_file_path = os.path.join(articles_dir, file[:-4] + 'azw3')
            if not os.path.exists(out_file_path):
                try:
                    cmd = '{0}/ebook-convert.exe {1} {2}'.format(get_calibre_path(), file_path, out_file_path)
                    os.system(cmd)
                except Exception as e:
                    print(e, 'error!!!!')


if __name__ == '__main__':
    articles = 'C:/Users/masiha/Desktop/dnt-1399-10-16/OPF/articles'
    book_out_dir = 'C:/Users/masiha/Desktop/dnt-1399-10-16/final_book_farsi_final22323'
    get_articles_content(articles, book_out_dir)
    convert_to_azw3(book_out_dir)
    print('complete all tasks!')
