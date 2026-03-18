import pytest
from apps.debugger.services.ai_handler import ErrorAnalyzerService
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import AIMessage

@pytest.mark.django_db(transaction=False) # No DB needed for pure logic tests
class TestErrorAnalyzer:
    
    def test_extract_error_title_valid(self):
        """Test that we correctly pull the error name from a traceback."""
        traceback = "File 'main.py', line 1\nZeroDivisionError: division by zero"
        title = ErrorAnalyzerService.extract_error_title(traceback)
        assert title == "ZeroDivisionError: division by zero"

    def test_extract_error_title_fallback(self):
        """Test fallback for messy inputs."""
        assert ErrorAnalyzerService.extract_error_title("") == "Empty Traceback"

    def test_analyze_traceback_mocked(self, mocker):
        """
        Test the service without calling Google. 
        We mock the 'invoke' method of the chain.
        """
        service = ErrorAnalyzerService()
        
        # Mock the LangChain 'invoke' call
        mock_response = "Mocked AI Resolution: Fix the import."
        mocker.patch("langchain_core.runnables.base.RunnableSequence.invoke", return_value=mock_response)
        
        result = service.analyze_traceback("NameError: name 'x' is not defined")
        
        assert "Mocked AI Resolution" in result
        
    def test_extract_error_title_non_traceback(self):
        """Test how we handle text that isn't a traceback at all."""
        weird_text = "Hello, I am just a random sentence."
        title = ErrorAnalyzerService.extract_error_title(weird_text)
        # Based on your regex, it should hit the fallback
        assert title == "General Python Error"

    def test_analyze_traceback_api_failure(self, mocker):
        """Test that the service propagates exceptions when the API fails."""
        service = ErrorAnalyzerService()
        # Mock a connection error or rate limit
        mocker.patch("langchain_core.runnables.base.RunnableSequence.invoke", 
                    side_effect=Exception("API Quota Exceeded"))
        
        with pytest.raises(Exception) as excinfo:
            service.analyze_traceback("NameError: x")
        assert "API Quota Exceeded" in str(excinfo.value)    