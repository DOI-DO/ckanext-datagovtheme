# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
import re
from builtins import object

import pytest
import six


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config('ckan.plugins', 'harvest datagovtheme')
@pytest.mark.use_fixtures('with_plugins', 'clean_db')
class TestDatagovthemeServed(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_homepage_redirect(self, app):
        index_response = app.get('/')

        assert 'Welcome to Geospatial Data' not in index_response.body
        if six.PY2:
            assert ('You should be redirected automatically to target URL: <a href='
                    '"/dataset">/dataset</a>') in index_response.body
        else:
            assert 'datasets found' in index_response.body

    def test_datagovtheme_css_file(self, app):
        """Assert the correct version of CSS is served."""
        index_response = app.get('/dataset')

        # Note: in development/debug mode, this asset uses the output filename
        # in webassets.yml. In production mode, it is compiled to a different
        # name and may have addtional filters (e.g. minification) applied.
        assert 'datagovtheme.css' in index_response.body

    def test_datagovtheme_html_loads(self, app):
        index_response = app.get('/dataset')

        # assert "Search Data.Gov" in index_response.body
        assert "Search datasets..." in index_response.body
        assert "datasets found" in index_response.body

    def test_datagovtheme_navigation(self, app):
        index_response = app.get('/dataset')

        aboutElement = """
            <li style="display:inline;"><a style="display:inline;" href="//data.doi.gov/about">About</a></li>
        """
        openGov = """
            <li style="display:inline;"><a style="display:inline;" href="//www.data.gov/open-gov/">Open Government</a></li>
        """
        dataPolicy = """
            <li style="display:inline;"><a style="display:inline;" href="//www.data.gov/data-policy">Data Policy</a></li>
        """

        assert '<li style="display:inline;"><a style="display:inline;" href="//www.doi.gov/data">Open Data at DOI</a></li>' \
            in index_response.body
        assert '<li style="display:inline;"><a style="display:inline;" href="//usinterior.ideascale.com">Feedback</a></li>' \
               in index_response.body
        assert aboutElement in index_response.body
        assert openGov in index_response.body
        assert '<li style="display:inline;"><a style="display:inline;" href="//data.gov">data.gov</a></li>' \
            in index_response.body
        assert dataPolicy in index_response.body

    """
    DOI Has no topics drop down menu. This test is not necessary.
    """
    # def test_datagovtheme_topics(self, app):
    #     index_response = app.get('/dataset')

    #     assert '<li class="menu-agriculture">' in index_response.body
    #     assert '<li class="menu-climate">' in index_response.body
    #     assert '<li class="menu-energy">' in index_response.body
    #     assert '<li class="menu-local-government">' in index_response.body
    #     assert '<li class="menu-maritime">' in index_response.body
    #     assert '<li class="menu-ocean">' in index_response.body
    #     assert '<li class="menu-older-adults-health">' in index_response.body

    def test_datagovtheme_organizations(self, app):
        index_response = app.get('/organization')

        org_match = r'organizations? found'
        matches = re.findall(org_match, index_response.body)
        assert len(matches) > 0
        assert "Search organizations..." in index_response.body
        assert "What are organizations?" in index_response.body
