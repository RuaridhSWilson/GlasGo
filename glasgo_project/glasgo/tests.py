import os
import re
import importlib
from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from glasgo.models import Attraction, Vote

#from populate_glasgo import populate

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD Test Failure =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class AboutPageTests(TestCase):
    """
    Tests to check the about view.
    We check whether the view exists and the response is correct.
    Also tests if the link for the page is present in every page other than itself.
    """

    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()

        return template_str

    def setUp(self):
        self.views_module = importlib.import_module('glasgo.views')
        self.views_module_listing = dir(self.views_module)

    def test_view_exists(self):
        name_exists = 'AboutView' in self.views_module_listing
        is_callable = callable(self.views_module.AboutView)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}Couldn't find the view for the about view!{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Can't execute the about view{FAILURE_FOOTER}")

    def test_response(self):
        
        response = self.client.get(reverse('glasgo:about'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "About Us", msg_prefix=f"{FAILURE_HEADER}The about view did not respond with the expected message.{FAILURE_FOOTER}")

    def test_for_about_hyperlink_in_about_page(self):
        """
        checks to see if block in about page overrides the footer block
        """
        
       # populate()
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'glasgo')

        mapping = {
            reverse('glasgo:about') : {'block_footer_pattern': r'{% block footer_block %}(\s*|\n*){% (endblock|endblock footer_block) %}',
                                        'template_filename' : 'about.html'},
        }

        for url in mapping.keys():
            template_filename = mapping[url]['template_filename']
            block_footer_pattern = mapping[url]['block_footer_pattern']

            request = self.client.get(url)
            content = request.content.decode('utf-8')
            template_str = self.get_template(os.path.join(template_base_path, template_filename))

            self.assertTrue(re.search(block_footer_pattern, template_str), f"{FAILURE_HEADER}When looking at the response of template '{template_filename}', we couldn't find the template block.{FAILURE_FOOTER}")

    def test_for_about_hyperlink_in_base_html(self):
        """
        check to see if link for about page is present in base html
        """

        template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'glasgo', 'base.html'))

        look_for = '<a href="{% url \'glasgo:about\' %}">About Us</a>'

        self.assertTrue(look_for in template_str, f"{FAILURE_HEADER}In base.html, we couldn't find the hyperlink for the about page.{FAILURE_FOOTER}")

class HomePageTests(TestCase):
    def test_for_all_attractions_sorted_being_displayed(self):
        response = self.client.get(reverse('glasgo:home'))

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Home page requested is not same as expected{FAILURE_FOOTER}")
        
        #NEED TO CHECK IF HOMEPAGE ACTUALLY DISPLAYS WHAT ITS SUPPOSED TO 


#class AttractionPageTests(TestCase):
    """
    Tests if the attraction page has the following: image, address, votes, date added, title, description and price tag
    """

#class AddAttractionPageTests(TestCase):
    """
    If signed out, tests if it redirects to login page
    If signed in, tests if it has the following fields: title, website, add image, description, location, price range, accessibility, start / end date, tags
    """

#class SearchPageTests(TestCase):
    """
    Tests if attractions appear when a valid attraction name entered
    """

#class NavBarTests(TestCase):
    """
    Tests if it visible in all pages and includes the favicon, home buttons, search button and add attraction.
    If signed in, also tests if a "hi" message to the user, change password button and logout button are visible
    If signed out, also tests if login/register button is visible
    """

#class SideBarTests(TestCase):
    """
    Tests if it is visible in every page, have heading "Top 10 Attractions", be solved by top 10 votes, contain thumbnail, title and vote number
    """
    
#    def test_for_existance_of_top_10_attraction_sidebar(self):

#class LoginPageTests(TestCase):
    """
    Tests if it includes username and password field
    """

#class RegisterPageTests(TestCase):
    """
    Tests if it includes username, email and password fields
    """
