import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Run tests with the following command...
# $ python manage.py test <app_name>

def create_question(question_text, days):
    """ 
        Creates a question with the given text and days offset.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTest(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """ 
            Should return False for question whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
            Should return false for questions whose pud_date is older than one day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            Should return True for questions whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """ 
            If no questions exist, an appropiate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available...")

    def test_past_questions(self):
        """ 
            Questions with a pub_date in the past are displayed on the index page
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_questions(self):
        """ 
            Questions with pub_date in the future are not shown
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available...")
