from textwrap import dedent
from crewai import Task
from langchain_community.tools import DuckDuckGoSearchRun

from job_manager import append_event

search_tool = DuckDuckGoSearchRun()

class Text_Processing_Task():
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        append_event(self.job_id, task_output.exported_output)
        
    def Clean_and_Normalize_Text_Tasks(self,agent):
        return Task(
            description=dedent(f"""\
				Removes irrelevant characters, corrects formatting inconsistencies, and standardizes the text. 
                Identifies key concepts, characters, locations, and other relevant entities within the text."""),
			expected_output=dedent("""\
				The transformed version of the original text, which includes:

				All characters converted to lowercase.
				Removal of punctuation marks.
				Removal of numeric characters.
				Elimination of special symbols.
				Reduction of multiple spaces to a single space.
				Trimming of any leading and trailing whitespace.
				The output should be a structured JSON object containing both the original and the cleaned text, ensuring the input text is standardized and ready for subsequent processing stages.
                Keywords:
				Definition: A list of significant words or phrases that capture the essential topics or themes of the input text.
				Characteristics:
				Excludes common stop words.
				Includes important terms relevant to the context.
				Entities:
				Definition: A dictionary where keys are entity types (such as PERSON, ORGANIZATION, LOCATION, etc.) and values are lists of entities of that type extracted from the input text.
				Characteristics:
				Recognizes and categorizes named entities.
				Distinguishes between different types of entities (e.g., names of people, places, organizations)."""),
			agent=agent
		)
    def Perform_Web_Search_task(self,agent):
        return Task(
            description=dedent(f"""\
			Uses the extracted keywords and entities to search for relevant information online.
            Filters and extracts details that are relevant to the input text."""),
			expected_output=dedent("""\
			Keywords and Entities Used: The output should specify the keywords and entities extracted from the input text that were used to formulate the web search query.
			Search Query: The constructed query string or set of queries based on the keywords and entities.
            Number of Results: The total count of search results retrieved from the web search.
			Results Details: A list of search results, where each result includes:
			Title: The title of the web page or document.
			URL: The URL of the web page or document.
			Snippet: A brief snippet or summary of the content from the search result that indicates its relevance to the query.
			Source: The domain or source of the web page or document.
            The title of the relevant information.
            A brief summary of the relevant content.
            The URL or source from which the information was extracted.
            Keywords or phrases related to the extracted content.
            Named entities (e.g., people, organizations) identified in the content."""),
			agent=agent
		)
    def content_expansion_task(self,agent):
        return Task(
            description=dedent(f"""\
			Adds details, explanations, and examples to the input text.
            Ensures the expanded content maintains a consistent tone and style.
            Organizes the content logically and ensures smooth transitions between sections.    """),
			expected_output=dedent("""\
			The output should provide a more comprehensive and informative version of the input text.
			The expanded content should seamlessly blend with the original text in terms of tone, style, and coherence.
			The revised text should be ready for further processing or publication, maintaining the quality and integrity of the original content."""),
			agent=agent
		)
    def quality_assurance_task(self,agent):
        return Task(
            description=dedent(f"""\
			Adds details, explanations, and examples to the input text.
            Ensures the expanded content maintains a consistent tone and style.
            Organizes the content logically and ensures smooth transitions between sections.    """),
			expected_output=dedent("""\
			Employ Natural Language Processing (NLP) techniques and tools to identify and correct grammatical errors and spelling mistakes.
			Use fact-checking APIs or databases to verify the accuracy of factual information presented in the text.
			Offer clear and specific feedback on each aspect of the text, including grammar, spelling, style, and factual accuracy.
			Include explanations and references to support the suggested changes and fact-checking results.
            Maintain a consistent tone and style throughout the text.
			Ensure logical coherence and smooth transitions between sentences and paragraphs.
			"""),
			agent=agent
		)
    def final_assembly_task(self,agent):
        return Task(
            description=dedent(f"""\
			Combines the processed content into a single document.
            Applies consistent formatting and styles according to specified guidelines.
            Prepares the final document for different formats like articles, scripts, or social media posts                      """),
			expected_output=dedent("""\
			The compiled final document should include all the relevant information gathered from various sources, structured in a logical and coherent manner. It should have a clear title, organized sections, and proper headings and subheadings.
			The content of the final document should be properly formatted according to predefined style guidelines. This includes consistent font styles, sizes, margins, alignments, and other visual elements to ensure readability and professionalism.
			The finalized and formatted document should be exported into the desired format, such as Word document (.docx), PDF file (.pdf), HTML file (.html), or any other specified format. The exported document should accurately reflect the compiled and formatted content.
			"""),
			agent=agent
		)
    