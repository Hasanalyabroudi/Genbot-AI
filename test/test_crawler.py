import pytest
from unittest.mock import patch, MagicMock
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from crawler.Crawler import Crawler 

class TestCrawler:
    """Test suite for the Crawler class"""
    
    def setup_method(self):
        """Setup method that runs before each test"""
        self.crawler = Crawler()
        
    def test_init(self):
        """Test the initialization of Crawler"""
        # Test default initialization
        crawler = Crawler()
        assert crawler.urls == []
        assert crawler.visited == []
        assert crawler.to_visit == []
        assert len(crawler.IDxURL) == 0
        
        # Test initialization with URLs
        test_urls = ["https://example.com", "https://test.org"]
        crawler = Crawler(urls=test_urls)
        assert crawler.urls == test_urls
        
    @patch('requests.get')
    def test_check_url_valid(self, mock_get):
        """Test check_url method with a valid URL"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><a href='https://example.com'>Link</a></body></html>"
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_get.return_value = mock_response
        
        # Test URL that hasn't been visited
        url = "https://example.com"
        soup, is_pdf = self.crawler.check_url(url)
        
        # Verify results
        assert soup is not None
        assert is_pdf is False
        mock_get.assert_called_once_with(url, timeout=5)
        
    @patch('requests.get')
    def test_check_url_pdf(self, mock_get):
        """Test check_url method with a PDF URL"""
        # Setup mock response for PDF
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/pdf'}
        mock_response.get_text = MagicMock(return_value="PDF content")
        mock_get.return_value = mock_response
        
        # Test PDF URL
        url = "https://example.com/document.pdf"
        content, is_pdf = self.crawler.check_url(url)
        
        # Verify results
        assert content == "PDF content"
        assert is_pdf is True
        
    @patch('requests.get')
    def test_check_url_error(self, mock_get):
        """Test check_url method with request error"""
        # Make requests.get raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Test exception")
        
        # Test URL with error
        url = "https://example.com/error"
        result = self.crawler.check_url(url)
        
        # Verify results
        assert result == (None, False)
        
    @patch('requests.get')
    def test_check_url_already_visited(self, mock_get):
        """Test check_url method with already visited URL"""
        # Add URL to visited list
        url = "https://example.com/visited"
        self.crawler.visited.append(url)
        
        # Test already visited URL
        result = self.crawler.check_url(url)
        
        # Verify results
        assert result == (None, False)
        # Ensure requests.get was not called
        mock_get.assert_not_called()
        
    def test_get_domaine_name(self):
        """Test get_domaine_name method"""
        # Test valid URLs
        assert self.crawler.get_domaine_name("https://example.com/page") == "example.com"
        assert self.crawler.get_domaine_name("http://www.test.org/path") == "www.test.org"
        assert self.crawler.get_domaine_name("https://subdomain.domain.net/path?query=value") == "subdomain.domain.net"
        
        # Test invalid URL
        assert self.crawler.get_domaine_name("invalid-url") is None
        
    def test_check_url_syntax(self):
        """Test check_url_syntax method"""
        # Test valid URLs
        assert self.crawler.check_url_syntax("https://example.com") is True
        assert self.crawler.check_url_syntax("http://www.test.org") is True
        
        # Test invalid URLs
        assert self.crawler.check_url_syntax("example.com") is False
        assert self.crawler.check_url_syntax("/relative/path") is False
        
    @patch.object(Crawler, 'check_url')
    def test_get_internal_links(self, mock_check_url):
        """Test get_internal_links method"""
        # Setup mock response
        html = """<html><body>
                <a href="https://example.com/page1">Page 1</a>
                <a href="https://example.com/page2">Page 2</a>
                <a href="https://external.com">External</a>
                <a href="/relative/path">Relative</a>
                <a href="#">Anchor</a>
                </body></html>"""
        soup = BeautifulSoup(html, 'html.parser')
        mock_check_url.return_value = (soup, False)
        
        # Set up crawler for test
        self.crawler.set_starting_url("https://example.com")
        
        # Test get_internal_links
        links, result_soup = self.crawler.get_internal_links("https://example.com")
        
        # Verify results
        assert soup == result_soup
        assert "https://example.com/page1" in links
        assert "https://example.com/page2" in links
        # Verify the URL was added to visited
        assert "https://example.com" in self.crawler.visited
        
    def test_add_url(self):
        """Test add_url method"""
        # Test adding a new URL
        url = "https://example.com"
        self.crawler.add_url(url)
        
        assert url in self.crawler.urls
        assert url in self.crawler.to_visit
        
        # Test adding a duplicate URL
        self.crawler.add_url(url)
        # Should still only appear once in to_visit
        assert self.crawler.to_visit.count(url) == 1
        
        # Test adding a visited URL
        visited_url = "https://example.com/visited"
        self.crawler.visited.append(visited_url)
        self.crawler.add_url(visited_url)
        
        assert visited_url not in self.crawler.to_visit
        
    def test_add_urls(self):
        """Test add_urls method"""
        # Test adding multiple URLs
        urls = ["https://example.com", "https://test.org"]
        self.crawler.add_urls(urls)
        
        for url in urls:
            assert url in self.crawler.urls
            assert url in self.crawler.to_visit
            
    def test_add_to_visited(self):
        """Test add_to_visited method"""
        url = "https://example.com"
        self.crawler.add_to_visited(url)
        
        assert url in self.crawler.visited
        
    def test_set_starting_url(self):
        """Test set_starting_url method"""
        url = "https://example.com/page"
        self.crawler.set_starting_url(url)
        
        assert url in self.crawler.to_visit
        assert self.crawler.original_domaine == "example.com"
        
    