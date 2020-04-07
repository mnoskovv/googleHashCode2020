import sys
from pprint import pprint

class Library:
    def __init__(self, id, totalBooksInLib, daysToSignUp, booksPerDay, booksInLib):
        self.id = id
        self.totalBooksInLib = int(totalBooksInLib)
        self.daysToSignUp = int(daysToSignUp)
        self.booksPerDay = int(booksPerDay)
        self.booksInLib = booksInLib
        self.signedUp = False
        self.total_points = 0
        self.omega = 0
        self.potential_points = 0

    def set_omega(self):
        """
        Считает коэффицент полезности либы (он будет важен при сортировке).
        """
        self.omega = (self.total_points / self.daysToSignUp)
    
    def set_total_points(self):
        """
        Считает максимально доступное количество очков за все книги в либе.
        """
        total = 0
        for k, v in self.booksInLib.items():
            total += v
        self.total_points = total 

class UsedLib:
    def __init__(self, id, used_books):
        self.id = id
        self.used_books = used_books

def print_libs(libraries):
    """
    @libraries - список либ, заполненных данными

    Печатает весь переданный список библиотек с отформатированным выводом
    """
    print ("__________")
    for lib in libraries:
        print(f'id: {lib.id}\ntotal books: {lib.totalBooksInLib}\ndays to sign: {lib.daysToSignUp}'\
            f'\nbooks per day: {lib.booksPerDay}\nbooks: {lib.booksInLib}\ntotal points: {lib.total_points}')

def get_potential_points(lib, total_days):
    potential = 0
    maxbooks = lib.booksPerDay * total_days
    for book in lib.booksInLib.values():
        if maxbooks <= 0:
            break
        potential += book
    return potential

def solve(libraries, total_days, filename):
    """
    @libraries - список либ, заполненных данными
    @total_days - количество доступных дней
    @filename - название входного файла (чтобы пришить к нему '.out')

    Главный метод, решающий задачу,регистируя библиотеки и сканируя максимальное к-во книг за отведенное время.
    """
    libs_used = []

    for lib in libraries:             # идем по либам
        used_books = []               # в начале итерации очищаем список юзанных книг в либе
        if (total_days <= 0):         # прекращаем сканить либы если закончились дни
            break

        # lib.potential_points = get_potential_points(lib, total_days)
        # libraries.sort(key=lambda x: x.potential_points)

        
        # sign Up lib
        if lib.signedUp == False:  
            total_days -= lib.daysToSignUp 
            lib.signedUp = True


        books_to_add = lib.booksPerDay * total_days    # считаем сколько книг может отсканить наша либа за оставшиеся дни
        
        # цикл сканирования книг
        for book in lib.booksInLib.keys():            # идем по книгам
            if books_to_add <= 0:                     # если закончился лимит добавления книг то стопаем
                break
            used_books.append(book)
            books_to_add -= 1

        if len(used_books) > 0:                                    # считаем либу использованной если мы взяли хоть одну книгу из нее
            libs_used.append(UsedLib(lib.id, used_books)) # add used lib to array 


    # генерим аутпут
    with open(filename + '.out', 'w') as f_obj:
        f_obj.write(f'{len(libs_used)} \n')
        
        for lib in libs_used:
            if len(lib.used_books) > 0:
                f_obj.write(f'{lib.id} {len(lib.used_books)} \n')

                for book in lib.used_books:
                    f_obj.write(f'{book} ')
                f_obj.write('\n')
        


def remove_duplicates(libraries, books):
    """
    @libraries - список библиотек, заполненных данными
    @books - список книг и их значений

    @@global_books - словарь {id книг и id библиотек} в которых они лежат, без дублирования друг друга.
    """
    # формируем словарь global_books {id книг и id библиотек} в которых они лежат, без дублирования друг друга.
    for lib in libraries:
        for book in lib.booksInLib.keys():
            try:
                if global_books[book]: # если книга есть в словаре - ничего не делаем
                    pass
            except KeyError:           # если нет - добавляем книгу
                global_books[book] = lib.id

    # удаляем дубликаты из всех библиотек
    for lib in libraries:
        lib.booksInLib = {} # удаляем все книги что были раньше
        for bookId, libId in global_books.items():
            if libId == lib.id:
                lib.booksInLib[bookId] = books[bookId] # записываем в либу {bookId: bookValue}

        lib.set_total_points() # пересчитываем тотал поинты за каждую либу, без дублирующих книг
 
def prepare_libs(content, books):
    """
    @content - строки считанного файла
    @libraries - пустой список библиотек
    @books - список всех книг и из скоров

    Заполняет библиотеки книгами, сортирует их по убыванию очков за них. Формирует спиок библиотек.
    """
    libraries = []
    _len = len(content)
    _id_counter = 0
    for i in range(2, _len - 1 , 2):
        f_line = content[i].split(' ')
        # обьявляем словарь  книг вида ключ-значение {key: Id книги, value: Очки за книгу}
        booksInLib = {}
        booksInLibKeys = [int(b) for b in content[i + 1].split(' ')] 
        booksInLibVals = [books[v] for v in booksInLibKeys]
        booksInLib = dict(zip(booksInLibKeys, booksInLibVals))
        booksInLib = {k: v for k, v in sorted(booksInLib.items(), key=lambda item: item[1], reverse = True)} # обединяем словарь и сортируем по спадению Очков за книгу

        # заполняем либу даными (id, к-во книг, к-во дней для сайнапа, книг в день, словарь книг)
        libraries.append(Library(id = _id_counter, totalBooksInLib = f_line[0],
                                daysToSignUp = f_line[1], booksPerDay = f_line[2], booksInLib = booksInLib))
        _id_counter += 1
    
    return libraries

def main(file):
    content = file.readlines()
    first_line = content[0].split(' ')
    total_days = first_line[2]
    books = [int(b) for b in content[1].split(' ')]
    
    # заполняем данными библиотеки
    libraries = prepare_libs(content, books)

    # сортируем по дням для удаления дубликатов
    libraries.sort(key=lambda x: x.daysToSignUp)
    remove_duplicates(libraries, books)

    libraries.sort(key=lambda x: x.total_points, reverse = True)
    libraries = [x for x in libraries if x.total_points > 0]            
    
    for lib in libraries:
        lib.set_omega()
    
    libraries.sort(key=lambda x: x.omega, reverse = True)

    # print_libs(libraries)
    solve(libraries, int(total_days), f_obj.name)


if __name__ == "__main__":

    global_books = {} # {book Id : lib id}
    with open(sys.argv[1]) as f_obj:
        main(f_obj)
