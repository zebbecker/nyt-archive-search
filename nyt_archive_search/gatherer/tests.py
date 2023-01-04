from django.test import TestCase, Client
import pandas as pd
import datetime
import sys, os
import json

import gatherer.gatherer as gatherer
import gatherer.nyt_gatherer as nyt_gatherer
import gatherer.melk_format as melk_format
import gatherer.config as config

TESTDATA_FILENAME = 'gatherer/fixtures/articlesearchresponse.json'



""" sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from . import gatherer, nyt_gatherer, config, melk_format """

# Run tests: ./manage.py test
# more docs: https://docs.djangoproject.com/en/4.1/topics/testing/overview/
# coverage: coverage run --source='.' manage.py test myapp
# view coverage: coverage report


class NewTestCase(TestCase):
    def testMethod(self):
        self.assertTrue(True)

class PagesLoadTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()

    def test_home_loads(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home')
    
    def test_about_loads(self):
        response = self.client.get('/about')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'about')


class FormSubmissionTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        query = {'keyword': 'Argentina', 'start_date': '2022-11-01', 'end_date': '2022-12-30', 'APIKey': ''}
        self.responseNoKey = self.client.post(path='/', data=query)
   
    # @tag('slow')
    def test_redirect(self):
        """
        @TODO test that redirects, then test that response data loads when available.
        """
        
        self.assertRedirects(self.responseNoKey, '/data')

    def test_response_no_APIKey(self):
        self.assertTrue(False)


#@TODO this test but through main gatherer
"""
Test that an example search returns a non-empty dataframe with appropriate columns and length. 
"""
class DataframeOKTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        """
        Note: uses demo/None API key. 
        We only want to do this once each time we run tests, because it 
        can take up to 6 seconds each time. 
        """
        self.df = nyt_gatherer.search_nyt("Argentina", datetime.date(2022, 11, 1), 
        datetime.date(2022, 12, 28), None)
        

    def test_columns_present(self):
        """
        DF is a dataframe passed in from NYT gatherer
        """
        
        for i in range(len(melk_format.melk_fields)):
            with self.subTest(i=i):
                header = melk_format.melk_fields[i]
                self.assertIn(header, self.df.columns, 'Missing header: ' + header)

    def test_not_empty(self):
        self.assertGreater(len(self.df), 0, 'Dataframe is empty')

    def test_rows_not_empty(self):
        row = self.df.get(0)
        for col in self.df.columns:
            # None, null, "", [], and 0 values are falsy
            self.assertTrue(row[col], 'Empty value for ' + col)

    def test_user_limit(self):
        self.assertLessEqual(len(self.df), config.NYT_DEFAULT_LIMIT, 
        'Demo search with no API key returned too many results. Num results: ' + len(self.df))


#@TODO this test but through main gatherer
"""
Test that an example search returns a non-empty dataframe with appropriate columns and length. 
This case uses an API key to return a longer file. 
"""
class LongDataframeOKTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        """
        @TODO store API key securely

        We only want to do this setup once each time we run tests, because it is slow. 
        """
        self.df = nyt_gatherer.search_nyt("Argentina", "2022-11-01", 
       "2022-12-28", config.NYT_API_KEY, 100)
        

    def test_columns_present(self):
        """
        DF is a dataframe passed in from NYT gatherer
        """
        
        for i in range(len(melk_format.melk_fields)):
            with self.subTest(i=i):
                header = melk_format.melk_fields[i]
                self.assertIn(header, self.df.columns, 'Missing header: ' + header)

    def test_not_empty(self):
        self.assertGreater(len(self.df), 0, 'Dataframe is empty')

    def test_not_capped(self):
        self.assertGreater(len(self.df), config.NYT_DEFAULT_LIMIT)

    def test_rows_not_empty(self):
        row = self.df.get(0)
        for col in self.df.columns:
            # None, null, "", [], and 0 values are falsy
            self.assertTrue(row[col], 'Empty value for ' + col)

    def test_user_limit(self):
        self.assertLessEqual(len(self.df), 100, 
        'Demo search with API key and user limit 100 returned too many results. Num results: ' + len(self.df))

class DateProcessingTestCase(TestCase):

    def test_valid_dates(self):
        self.assertIs(gatherer.validate_dates("2022-01-01", "2022-02-02")[0], datetime.date)
        self.assertEqual(gatherer.validate_dates("2022-01-01", "2022-02-02")[0], datetime.date(2022, 1, 1))
        self.assertIs(gatherer.validate_dates("2022-01-01", "2022-02-02")[1], datetime.date)
        self.assertEqual(gatherer.validate_dates("2022-01-01", "2022-02-02")[1], datetime.date(2022, 2, 2))

    def test_invalid_inputs(self):
        self.assertRaises(Exception, gatherer.validate_dates("1", "2"))
        self.assertRaises(Exception, gatherer.validate_dates("Another string", "2022-01-01"))
        self.assertRaises(Exception, gatherer.validate_dates("01/01/2022", "2022-02-01"))
        self.assertRaises(Exception, gatherer.validate_dates(None, None))
        self.assertRaises(Exception, gatherer.validate_dates("2022-40-40", "2022-01-01"))
    
class KeywordFormatTestCase(TestCase):

    def test_keyword_format(self):
        self.assertEqual("query+with+multiple+words", nyt_gatherer.format_keyword("query with multiple words"))

class ParseArticleTestCase(TestCase):

    def setUp(self):
        self.testfile = open(TESTDATA_FILENAME)
        self.testjson = json.load(self.testfile)

    def test_parse_article(self):
        data = []

        nyt_gatherer.parse_article(article=self.testjson, data=data, next_id=12)

        self.assertEqual(len(data), 1)
        row = data[0]
        self.assertEqual(row['ID'], 12)
        self.assertEqual(row['SECTION'], "World")
        self.assertEqual(row['SOURCE'], nyt_gatherer.SOURCE_NAME)
        self.assertEqual(row['SOURCE_URL'], "https://www.nytimes.com/2022/05/23/world/haitian-creole-history.html")
        self.assertEqual(row['DATE'], "2022-05-23 15:06:55")
        self.assertEqual(row['TITLE'], "A Story About Haitian History, in Haitian Creole.")
        #self.assertEqual(row['FULL_TEXT'], None)
        self.assertEqual(row['TYPE'], nyt_gatherer.TYPE)

    def tearDown(self):
        self.testfile.close()

class ScrapeArticleTextTestCase(TestCase):

    def test_scrape_body_text(self):
        # @TODO create example 
        url = "https://www.nytimes.com/2023/01/03/climate/california-flood-atmospheric-river.html"
        expected_content = None
        content = nyt_gatherer.scrape_body_text(url)
        self.assertEqual(content, expected_content)