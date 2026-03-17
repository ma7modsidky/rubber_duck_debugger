import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re


class ErrorAnalyzerService:
    def __init__(self):
        # Initialize Gemini via LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,  # Low temperature for technical accuracy
        )
        self.output_parser = StrOutputParser()

    @staticmethod
    def extract_error_title(traceback_text: str) -> str:
        """
        Extracts the last line of a traceback which usually contains
        'ErrorName: description'
        """
        if not traceback_text:
            return "Empty Traceback"

        lines = traceback_text.strip().split("\n")
        # We look at the last line first
        last_line = lines[-1]

        # Standard Python errors follow 'ErrorName: message'
        # This regex looks for a word ending in 'Error' followed by a colon
        match = re.search(r"([a-zA-Z]+Error|Exception):", last_line)
        if match:
            return last_line.strip()

        # Fallback: if the traceback is very long, the error might be
        # a few lines up (common in some frameworks)
        for line in reversed(lines):
            if any(err in line for err in ["Error:", "Exception:"]):
                return line.strip()

        return "General Python Error"

    def analyze_traceback(self, traceback_text: str, history_context: str = "") -> str:
        """
        Takes a raw Python traceback and optional user history,
        returns a structured fix.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an expert Python Debugger. Analyze the provided traceback "
                        "and provide a concise explanation of the root cause. "
                        "Include a 'Suggested Fix' section with the corrected code block. "
                        "If history context is provided, mention if this is a recurring error."
                    ),
                ),
                ("human", "Traceback: {traceback}\n\nPast Context: {context}"),
            ]
        )

        # Create the Chain (The "Lego" pieces connecting together)
        chain = prompt | self.llm | self.output_parser

        # Execute
        return chain.invoke({"traceback": traceback_text, "context": history_context})
