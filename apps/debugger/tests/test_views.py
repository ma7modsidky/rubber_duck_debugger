import pytest
from django.urls import reverse
from apps.debugger.models import DebugLog

@pytest.mark.django_db
class TestDebuggerViews:

    def test_home_page_loads(self, client):
        """Test that the home page is accessible."""
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_successful_analysis_redirects(self, client, mocker):
        """Test that a valid POST redirects to the detail page (PRG Pattern)."""
        # Mock the service so we don't call Gemini
        mocker.patch("apps.debugger.services.ai_handler.ErrorAnalyzerService.analyze_traceback", 
                     return_value="Fixed code here.")
        
        url = reverse('home')
        data = {'traceback': "ZeroDivisionError: division by zero"}
        response = client.post(url, data)
        
        # Check for redirect (302)
        assert response.status_code == 302
        assert DebugLog.objects.count() == 1

    def test_invalid_input_shows_error(self, client):
        """Test that short/empty input doesn't trigger AI and shows error."""
        url = reverse('home')
        response = client.post(url, {'traceback': 'short'})
        
        # Should redirect back to home
        assert response.status_code == 302
        assert DebugLog.objects.count() == 0
    
    def test_non_traceback_input_fails(self, client):
        """Ensure random text like 'hello world' is rejected by the view."""
        url = reverse('home')
        # This should be caught by our new validation gate
        response = client.post(url, {'traceback': 'hello world this is not a python traceback or error'})
        
        assert response.status_code == 302
        assert DebugLog.objects.count() == 0 # No log should be created