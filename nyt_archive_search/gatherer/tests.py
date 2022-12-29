from django.test import TestCase, Client
import pandas as pd
import datetime

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
        query = {'keyword': 'Argentina', 'start_date': '2022-11-01', 'end_date': '2022-12-30', 'APIKey': None}
        self.responseNoKey = self.client.post(path='/', data=query)
   
    # @tag('slow')
    def test_redirect(self):
        """
        @TODO test that redirects, then test that response data loads when available.
        """
        
        self.assertRedirects(self.responseNoKey, '/data')

    def test_response_no_APIKey(self):
        self.assertTrue(False)


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
        self.df = gatherer.main(keyword="Argentina", start_date="2022-11-01", 
        end_date="2022-12-28", APIKey=None)
        

    def test_columns_present(self):
        """
        DF is a dataframe passed in from NYT gatherer
        """
        
        for i in range(len(FIELDS)):
            with self.subTest(i=i):
                self.assertIn(FIELDS[i], self.df.columns, 'Missing header: ' + header)

    def test_not_empty(self):
        self.assertGreater(len(self.df), 0, 'Dataframe is empty')

    def test_rows_not_empty(self):
        row = self.df.get(0)
        for col in self.df.columns:
            # None, null, "", [], and 0 values are falsy
            self.assertTrue(row[col], 'Empty value for ' + col)

    def test_user_limit(self):
        self.assertLessEqual(len(self.df), gatherer.DEFAULT_LIMIT, 
        'Demo search with no API key returned too many results. Num results: ' + len(self.df))


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
        self.df = gatherer.main(keyword="Argentina", start_date="2022-11-01", 
        end_date="2022-12-28", APIKey=secret.NYT_API_KEY, limit=100)
        

    def test_columns_present(self):
        """
        DF is a dataframe passed in from NYT gatherer
        """
        
        for i in range(len(gatherer.FIELDS)):
            with self.subTest(i=i):
                self.assertIn(gatherer.FIELDS[i], self.df.columns, 'Missing header: ' + header)

    def test_not_empty(self):
        self.assertGreater(len(self.df), 0, 'Dataframe is empty')

    def test_not_capped(self):
        self.assertGreater(len(self.df), gatherer.DEFAULT_LIMIT)

    def test_rows_not_empty(self):
        row = self.df.get(0)
        for col in self.df.columns:
            # None, null, "", [], and 0 values are falsy
            self.assertTrue(row[col], 'Empty value for ' + col)

    def test_user_limit(self):
        self.assertLessEqual(len(self.df), 100, 
        'Demo search with API key and user limit 100 returned too many results. Num results: ' + len(self.df))

class DateProcessingTestCase(TestCase):

    def test_valid_date(self):
        self.assertIs(gatherer.validate_date("2022-01-01"), datetime.date)
        self.assertEqual(gatherer.validate_date("2022-01-01"), datetime.date(2022, 1, 1))
    
    def test_invalid_inputs(self):
        self.assertRaises(Exception, gatherer.validate_date(1))
        self.assertRaises(Exception, gatherer.validate_date("Another string"))
        self.assertRaises(Exception, gatherer.validate_date("01/01/2022"))
        self.assertRaises(Exception, gatherer.validate_date(None))
    
class KeywordFormatTestCase(TestCase):

    def test_keyword_format(self):
        self.assertEqual("query+with+multiple+words", gatherer.format_keyword("query with multiple words"))

class ParseArticleTestCase(TestCase):

    def test_parse_article(self):
        # @TODO store example JSON response and input expected values
        json = None
        data = []

        gatherer.parse_article(article=json, data=data, next_id=12)

        self.assertEqual(len(data), 1)
        row = data[0]
        self.assertEqual(row.ID, 12)
        self.assertEqual(row.SECTION, None)
        self.assertEqual(row.SOURCE, None)
        self.assertEqual(row.SOURCE_URL, None)
        self.assertEqual(row.DATE, None)
        self.assertEqual(row.TITLE, None)
        self.assertEqual(row.FULL_TEXT, None)
        self.assertEqual(row.TYPE, None)

class ScrapeArticleTextTestCase(TestCase):

    def test_scrape_body_text(self):
        # @TODO create example 
        url = None
        expected_content = None
        content = gatherer.scrape_body_text(url)
        self.assertEqual(content, expected_content)
