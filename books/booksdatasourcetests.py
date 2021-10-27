'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
   Altered by Elliot Hanson and Avery Hall, 27 September 2021
'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass
    
    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == booksdatasource.Author('Pratchett', 'Terry'))

    def test_authors_bronte(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors == [booksdatasource.Author('Brontë', 'Ann'), booksdatasource.Author('Brontë', 'Charlotte'), booksdatasource.Author('Brontë', 'Emily')])
 

    def test_author_nonexistent(self):
        authors = self.data_source.authors('ghjk')
        self.assertTrue(len(authors) == 0)
    
    def test_author_emptyString(self):
        authors = self.data_source.authors('')
        self.assertTrue(len(authors) == 22)
        self.assertTrue(authors[0] == booksdatasource.Author('Austen', 'Jane'))
        self.assertTrue(authors[21] == booksdatasource.Author('Wodehouse', 'Pelham Grenville'))
        
    def test_author_partial(self):
        authors = self.data_source.authors('or')
        self.assertTrue(authors[0] == booksdatasource.Author('Morrison', 'Toni'))
        self.assertTrue(authors[2] == booksdatasource.Author('Orenstein', 'Peggy'))
        
    
    def test_unique_title(self):
        titles = self.data_source.books('The Fire Next Time')
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0] == booksdatasource.Book('The Fire Next Time'))
        self.assertTrue(titles[0].authors[0] == booksdatasource.Author('Baldwin', 'James'))

    def test_title_option_n(self):
        titles = self.data_source.books('and', 'title')
        self.assertTrue(len(titles) == 7)
        self.assertTrue(titles[1] == booksdatasource.Book('Boys and Sex'))
        self.assertTrue(titles[5] == booksdatasource.Book('Sense and Sensibility'))
        self.assertTrue(titles[1].authors[0] == booksdatasource.Author('Orenstein', 'Peggy'))
        self.assertTrue(titles[6] == booksdatasource.Book('The Life and Opinions of Tristram Shandy, Gentleman'))

    def test_unique_title_option_y(self):
        titles = self.data_source.books('and', 'year')
        self.assertTrue(len(titles) == 7)
        self.assertTrue(titles[0] == booksdatasource.Book('The Life and Opinions of Tristram Shandy, Gentleman'))
        self.assertTrue(titles[1].authors[0] == booksdatasource.Author('Austen','Jane'))
        self.assertTrue(titles[6] == booksdatasource.Book('Boys and Sex'))
    
    def test_title_nonexistent(self):
        titles = self.data_source.books('asdf', 'title')
        self.assertTrue(len(titles) == 0)

    def test_title_emptyString(self):
        titles = self.data_source.books('')
        self.assertTrue(len(titles) == 41)
        self.assertTrue(titles[0] == booksdatasource.Book('1Q84'))
        self.assertTrue(titles[40] == booksdatasource.Book('Wuthering Heights'))

    def test_title_partial(self):
        titles = self.data_source.books('wo')
        self.assertTrue(len(titles) == 2)
        self.assertTrue(titles == [booksdatasource.Book('Hard-Boiled Wonderland and the End of the World'), booksdatasource.Book('The Code of the Woosters')])
        #Hard-Boiled... has 2 instances of the "wo" so tests for that too
     
    def test_title_option_y_small_set(self):
        self.data_source = booksdatasource.BooksDataSource('bookstest1.csv')
        titles = self.data_source.books('', 'year')
        self.assertEqual(titles, [booksdatasource.Book('And Then There Were None'), booksdatasource.Book('Beloved'), booksdatasource.Book('Schoolgirls'), booksdatasource.Book('To Say Nothing of the Dog'), booksdatasource.Book('All Clear'), booksdatasource.Book('Blackout')])
     
    def test_title_option_n_small_set(self):
        self.data_source = booksdatasource.BooksDataSource('bookstest1.csv')
        titles = self.data_source.books('', 'title')
        self.assertEqual(titles, [booksdatasource.Book('All Clear'), booksdatasource.Book('And Then There Were None'), booksdatasource.Book('Beloved'), booksdatasource.Book('Blackout'), booksdatasource.Book('Schoolgirls'), booksdatasource.Book('To Say Nothing of the Dog')])
 
    def test_betweenyrs_unique(self):
        titles = self.data_source.books_between_years(1920,1921)
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles == [booksdatasource.Book('Main Street')])
    
    def test_betweenyrs_same_year(self):
        titles = self.data_source.books_between_years(1920,1920)
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles == [booksdatasource.Book('Main Street')])
    
    def test_betweenyrs_group(self):
        titles = self.data_source.books_between_years(1920,1927)
        self.assertTrue(len(titles) == 3)
        self.assertTrue(titles == [booksdatasource.Book('Main Street'), booksdatasource.Book('Leave it to Psmith'), booksdatasource.Book('Elmer Gantry')])
    
    def test_betweenyrs_tie(self):
        self.data_source = booksdatasource.BooksDataSource('bookstest1.csv')
        books = self.data_source.books_between_years(2009,2030)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books == [booksdatasource.Book('All Clear'), booksdatasource.Book('Blackout')])
        
    def test_betweenyrs_empty(self):
        books = self.data_source.books_between_years(None,None)
        self.assertTrue(len(books) == 41)
        self.assertTrue(books[0] == booksdatasource.Book('The Life and Opinions of Tristram Shandy, Gentleman'))
        self.assertTrue(books[40] == booksdatasource.Book('The Invisible Life of Addie LaRue'))
    
    def test_betweenyrs_no_start_date(self):
        self.data_source = booksdatasource.BooksDataSource('bookstest1.csv')
        titles = self.data_source.books_between_years(None,1995)
        self.assertTrue(len(titles) == 3)
        self.assertTrue(titles == [booksdatasource.Book('And Then There Were None'), booksdatasource.Book('Beloved'), booksdatasource.Book('Schoolgirls')])
    
       
    def test_betweenyrs_no_end_date(self):
        self.data_source = booksdatasource.BooksDataSource('bookstest1.csv')
        titles = self.data_source.books_between_years(2005,None)
        self.assertTrue(len(titles) == 2)
        self.assertTrue(titles == [booksdatasource.Book('All Clear'), booksdatasource.Book('Blackout')])
       
    

if __name__ == '__main__':
    unittest.main()
