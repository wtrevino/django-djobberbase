# -*- coding: utf-8 -*-

import unittest
from djobberbase.models import Job, Type, Category, City
from djobberbase.conf import settings
from django.test.client import Client
from django.core.urlresolvers import reverse

class JobTestCase(unittest.TestCase):

    def setUp(self):
        ''' Set up test objects.
        '''

        # Creating a set of job categories
        self.category_1 = Category.objects.create(name='Genetic Engineering')
        self.category_2 = Category.objects.create(name='Eye Design', 
                                                            var_name='eyes')
        self.category_3 = Category.objects.create(name='Bounty Hunting', 
                                                            category_order=4)
        self.category_4 = Category.objects.create(name='Origami')

        # Creating a set of job types
        self.job_type_1 = Type.objects.create(name='Full time', 
                                                        var_name='fulltime')
        self.job_type_2 = Type.objects.create(name='Part time')
        self.job_type_3 = Type.objects.create(name='Freelance')

        # Creating a couple of cities
        self.city_1 = City.objects.create(name='Los Angeles', 
                                                        ascii_name='la')
        self.city_2 = City.objects.create(name='San Francisco')

        # Creating a job
        self.job_1 = Job.objects.create(category=self.category_1, 
                jobtype=self.job_type_1, 
                title='Genetist needed', 
                description='A new job', 
                company='Tyrell Corporation', 
                city=self.city_1, 
                poster_email='hr@tyrellcorp.com')

        # Creating a job with outside location
        self.job_2 = Job.objects.create(category=self.category_2, 
                jobtype=self.job_type_1, 
                title='WANTED: Eye Designer', 
                description='Must be able to put up with low temperatures.', 
                company='Tyrell Corp.', 
                city=None, 
                outside_location='Las Vegas', 
                poster_email='hr@tyrellcorp.com')

        # Set up a Client
        self.client = Client()

    def tearDown(self):
        ''' Tear down everything.
        '''
        self.category_1.delete()
        self.category_2.delete()
        self.category_3.delete()
        self.category_4.delete()
        self.job_type_1.delete()
        self.job_type_2.delete()
        self.job_type_3.delete()
        self.city_1.delete()
        self.city_2.delete()
        self.job_1.delete()
        self.job_2.delete()
        del self.client

    def testSlugs(self):
        # Test category slugs
        self.assertEqual(self.category_1.var_name, 'genetic-engineering')
        self.assertEqual(self.category_2.var_name, 'eyes')
        self.assertEqual(self.category_3.var_name, 'bounty-hunting')
        self.assertEqual(self.category_4.var_name, 'origami')

        # Test job type slugs
        self.assertEqual(self.job_type_1.var_name, 'fulltime')
        self.assertEqual(self.job_type_2.var_name, 'part-time')
        self.assertEqual(self.job_type_3.var_name, 'freelance')

        # Test city slugs
        self.assertEqual(self.city_1.ascii_name, 'la')
        self.assertEqual(self.city_2.ascii_name, 'san-francisco')

        # Test job slugs
        self.assertEqual(self.job_1.joburl, 
          'genetist-needed-'+settings.DJOBBERBASE_AT_URL+'-tyrell-corporation')
        self.assertEqual(self.job_2.joburl, 
             'wanted-eye-designer-'+settings.DJOBBERBASE_AT_URL+'-tyrell-corp')

        # Test company slugs
        self.assertEqual(self.job_1.company_slug, 'tyrell-corporation')
        self.assertEqual(self.job_2.company_slug, 'tyrell-corp')

    def testCategoryOrder(self):
        self.assertEqual(self.category_1.category_order, 0)
        self.assertEqual(self.category_2.category_order, 1)
        self.assertEqual(self.category_3.category_order, 4)
        self.assertEqual(self.category_4.category_order, 5)

    def testInitialJobStatus(self):
        ''' Ensure that initial job status is Job.TEMPORARY.
        '''
        self.assertEqual(self.job_1.status, Job.TEMPORARY)
        self.assertEqual(self.job_2.status, Job.TEMPORARY)

    def testActivateJob(self):
        ''' Test activation.
        '''
        self.job_1.activate()
        self.assertEqual(self.job_1.status, Job.ACTIVE)
        self.job_2.activate()
        self.assertEqual(self.job_2.status, Job.ACTIVE)

    def testDeactivateJob(self):
        ''' Test deactivation.
        '''
        self.job_1.deactivate()
        self.assertEqual(self.job_1.status, Job.INACTIVE)
        self.job_2.deactivate()
        self.assertEqual(self.job_2.status, Job.INACTIVE)

    def testApprovedEmail(self):
        ''' Activate job_1 and making sure job_2 will be automatically
            published.
        '''
        self.job_1.activate()
        self.assertEqual(self.job_2.email_published_before(), True)

    def testIndexView(self):
        response = self.client.get(reverse('djobberbase_job_list'))
        # Check that the response is 200 OK
        self.failUnlessEqual(response.status_code, 200)
        # Assert that number of categories is correct
        self.assertEqual(len(response.context['categories']), 4)

    def testActivateView(self):
        response = self.client.post(self.job_1.get_activation_url())
        # Check that the response is 200 OK
        self.failUnlessEqual(response.status_code, 200)
        # Assert that job status has been changed
        self.assertEqual(response.context['page_type'], 'activate')

    def testDeactivateView(self):
        response = self.client.get(self.job_1.get_deactivation_url())
        # Check that the response is 200 OK.
        self.failUnlessEqual(response.status_code, 200)
        # Assert that job status has been changed
        self.assertEqual(response.context['page_type'], 'deactivate')

