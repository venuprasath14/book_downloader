import os
import msvcrt
import subprocess
import requests as req
from termcolor import colored
from bs4 import BeautifulSoup
from downloader import download_file


class BookStore:

    def __init__(self):
        self.base_url = 'https://www.pdfdrive.com'
        self.book_locator = 'div.file-right a h2'
        self.book_download = 'div.file-right a'
        self.book_info = 'div.file-info'
        self.category_locator = 'div.categories-list ul li a'
        self.category_link = 'div.categories-list ul li a'

    def get_html_page(self, url: str) -> object:
        try:
            page = BeautifulSoup(req.get(url).content, 'html.parser')
        except Exception as err:
            print(err, 'No Internet connection / Incorrect URL / Try again later')
            quit()
        return page
    
    def categories(self) -> dict:
        url = self.base_url
        page = self.get_html_page(self.base_url)
        cname = [i.text.strip() for i in page.select(self.category_locator)]
        links = [i['href'] for i in page.select(self.category_link)]
        return {'name': cname, 'link': links}
    
    def books_data(self, urls: str) -> dict:
        url = self.base_url + urls 
        page = self.get_html_page(url)
        books = [i.text.strip() for i in page.select(self.book_locator, limit=None)]
        info = [i.text.strip().replace('·', ' | ') for i in page.select(self.book_info, limit=None)]
        links = [i['href'] for i in page.select(self.book_download, limit=None)]
        return {'name': books, 'info': info, 'link': links, 'rqlink': url}

    def download(self, name: str, url: str) -> bool:
        link = self.base_url + url
        return download_file(name, link)

        
if __name__ == "__main__":
    
    subprocess.call('', shell=True)
    books = BookStore()
    years= {'1': '1990', '2': '2000', '3': '2005', '4': '2010', '5': '2015', '6': ''}
    pages = {'1': '1-24', '2': '25-50', '3': '51-100', '4': '100-*', '5': ''}
    
    while True:
        stop = False
        nxt = 1
        q = input("\n\tBook-Universe\n\n Press S :: Search by Bookname\n Press A :: Advance BookSearch \n Press C :: Category-wise books\n Press Q :: Quit\n\n Your Choice : ")
        if q.lower() == 's':
            query = '+'.join(list(map(str, input('\nEnter the book/author name : ').split())))
            if not query:
                print(colored('Invalid book name ...', 'red'))
                continue
            link = f'/search?q={query}&pagecount=&pubyear=&searchin=&em=&more=true'
            data = books.books_data(link)

        elif q.lower() == 'c':
            cats = books.categories()
            print(*[f'{i} :: '.rjust(6, ' ')+j for i,j in enumerate(cats['name'], 1)], sep='\n')
            choice = int(input('\n Your choice : '))
            data = books.books_data(cats['link'][choice-1])
            
        elif q.lower() == 'a':
            name = '+'.join(list(map(str, input('Enter the book name(*) : ').split())))
            year = input(f'\n < 1. After 1990>\n < 2. After 2000>\n < 3. After 2005>\n < 4. After 2010>\n < 5. After 2015>\n < 6. Any year  >({colored("Deafult", "green")})\n Select the book release year : ')
            count = input(f'\n < 1.  1 -   24 >\n < 2. 25 -   50 >\n < 3. 51 -  100 >\n < 4. 100+      >\n < 5. Any pages >({colored("Default", "green")})\n Select the page-count of book : ')
            exm = input(f'\n < 1. False >({colored("Default", "green")})\n < 2. True  >\n Exact match :')
            if exm and not exm.isnumeric():
                print(colored("Invalid option!!!", "red"))
            if not name:
                print(colored('Invalid book name ...', 'red'))
                continue
            link = f'/search?q={name}&pagecount={pages.get(count, "")}&pubyear={years.get(year, "")}&searchin=en&em={0 if not exm else int(exm) - 1}&more=true'
            data = books.books_data(link)
            
        elif q.lower() == 'q':
            print('\nThanks for Visiting Books Universe !!!')
            break
            
        else:
            print(colored('\nInvalid Option!!!', 'red'))
            continue
        print(colored('\n Note : Press q to stop print more books.', 'red'))
        for i, j in enumerate(zip(data['name'], data['info']), 1):
            print(f'{i}.'.rjust(3, ' '), (j[0], j[1]))
            if not i%10:
                print('--More--\r', end='')
                while True:
                    if msvcrt.kbhit():
                        if msvcrt.getch() == b'q':
                            stop = True
                        print('        \r', end='')
                        break
                if stop:
                    break
                else:
                    try:
                        if (len(data['name'])-i) <= 10:
                            nxt += 1
                            print('Loading... \r',end='')
                            if q.lower() in ['a', 's']:
                                bk = books.books_data(f'{data["rqlink"]}&page={nxt}')
                            elif q.lower() == 'c':
                                bk = books.books_data(f'{data["rqlink"]}/p{nxt}/')
                            data['name'].extend(bk['name'])
                            data['info'].extend(bk['info'])
                            data['link'].extend(bk['link'])
                    except:
                        print('No-more-books',end='\r')
        while True:
            sel = (input('\t\t\t\nYour choice : '))
            if sel.lower() == 'q':
                break
            elif (sel.isnumeric() and int(sel) > i) or (not sel.isnumeric()):
                print(colored('Invalid option !!!', 'red'))
            else:
                lnk = data['link'][int(sel)-1][::-1].replace('e', 'd', 1)
                books.download(data['name'][int(sel)-1], lnk[::-1])
                break
