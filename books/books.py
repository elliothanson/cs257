'''
   books.py
   Elliot Hanson and Avery Hall, 2 October 2021
   Revised by Avery Hall and Elliot Hanson, 11 October 2021
'''
import argparse
import booksdatasource

def display_usage():
    '''Prints out the usage statement for books.py'''
    f = open('usage.txt', 'r')
    usage_statement = f.read()
    print(usage_statement)
    f.close()
                
def display_titles(list_of_books_to_display):
    '''Prints out information about books from an input list of book objects.
        For example:
        "Right Ho, Jeeves", Pelham Greenville Wodehouse, 1934
     '''
    if len(list_of_books_to_display) == 0:
        print('No titles were found to include the given search string.')
    else:
        for book in list_of_books_to_display:
            authors_name_string = create_authors_string(book)

            print('"' +book.title + '"' + ', ' + authors_name_string + ', ' + book.publication_year)

def display_authors(list_of_authors_to_display):
    '''Prints out information about authors from an input list of author objects.
        For example:
        Wodehouse, Pelham Grenville (1881-1975):
          "Leave it to Psmith" (1923)
          "Right Ho, Jeeves" (1934)
          "The Code of the Woosters" (1938)
     '''
    if len(list_of_authors_to_display) == 0:
        print('No authors were found to include the given search string.')
        
    else:    
        for author in list_of_authors_to_display:
            author_name = author.surname + ', ' + author.given_name
            author_life_span = ' (' + author.birth_year + '-' + author.death_year + '):'
            print(author_name + author_life_span)

            for book in author.author_works:
                print('  "' + book.title + '" (' + book.publication_year + ')')

            print()

def display_range_list(list_of_books_to_display):
    '''Prints out information about books from an input list of book objects
        For example:
        "Right Ho, Jeeves", Pelham Grenville Wodehouse, (1934)
     '''
    if len(list_of_books_to_display) == 0:
        print('No titles were found within the given range.')
        
    else:    
        for book in list_of_books_to_display:
            authors_names_string = create_authors_string(book)
            print('"' + book.title + '", ' + authors_names_string + ', (' + book.publication_year + ')')
        
def create_authors_string(book):
    '''Returns a string that contains the full names of all of a book object's authors.
        For example:
        Pelham Grenville Wodehouse
        Neil Gaiman and Terry Pratchett
    '''
    authors_string = ''
    
    for i in range(len(book.authors)):
        author = book.authors[i]
        if i > 0 and i < len(book.authors):
            authors_string += ' and '
        authors_string += author.given_name + ' ' + author.surname
        
    return authors_string

    
def main():
    data_source = booksdatasource.BooksDataSource('books1.csv')

    parser = argparse.ArgumentParser(add_help = False)

    parser.add_argument('-t', '--title', type = str, default = '', dest = 'title_search', nargs = '?')
    parser.add_argument('-n', action = 'store_true', dest = 'sort_by_title')
    parser.add_argument('-y', action = 'store_true', dest = 'sort_by_year')
    parser.add_argument('-a', '--author', type = str, default = '', dest = 'author_search', nargs = '?')
    parser.add_argument('-r', '--range', action = 'store_true', dest = 'search_by_year_range')
    parser.add_argument('-h', '-?', '--help', action = 'store_true', dest = 'request_help')
    parser.add_argument('-s', '--start_yr', type = int, dest = 'start_yr')
    parser.add_argument('-e', '--end_yr', type = int, dest = 'end_yr')

    args = parser.parse_args()

    if args.request_help:
        display_usage()
        
    elif args.title_search != '':
        if args.sort_by_year == True:
            book_list = data_source.books(args.title_search, 'year')
            display_titles(book_list)
        else:
            book_list = data_source.books(args.title_search, 'title')
            display_titles(book_list)

    elif args.author_search != '':
        author_list = data_source.authors(args.author_search)
        display_authors(author_list)

    elif args.search_by_year_range:
        year_list = data_source.books_between_years(args.start_yr,args.end_yr)
        display_range_list(year_list)

    else:
        display_usage()


if __name__ == '__main__':
    main()