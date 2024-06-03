from job_manager import append_event
from tasks import Text_Processing_Task
from agents import Text_Processing_Agents
from crewai import Crew


class TextProcessingCrew:
    def __init__(self,job_id:str):
        self.job_id = job_id
        self.crew = None
    
    def setup_crew(self,input:str):
        print (
            f"Setting Up Crew For {self.job_id} with Text Inputed {input}"
        )
        agents = Text_Processing_Agents()
        tasks = Text_Processing_Task(job_id=self.job_id)
        

        # Create And Setup Agents
        TextProcessingAgents = agents.Text_Cleaning__agent(input)
        Research_agent = agents.Research_agent(TextProcessingAgents)
        Content_Generation_agent = agents.Content_Generation_agent(Research_agent)
        Quality_Assurance_Agent = agents.Quality_Assurance_Agent(Content_Generation_agent)
        Final_Assembly_Agent = agents.Final_Assembly_Agent(Research_agent,Content_Generation_agent,Quality_Assurance_Agent)


        # Create And Setup Tasks
        Clean_and_Normalize_Text_Tasks = tasks.Clean_and_Normalize_Text_Tasks(TextProcessingAgents)
        Perform_Web_Search_task = tasks.Perform_Web_Search_task(Research_agent)
        Content_Expansion_Task = tasks.content_expansion_task(Content_Generation_agent)
        quality_assurance_task = tasks.quality_assurance_task(Quality_Assurance_Agent)
        final_assembly_task = tasks.final_assembly_task(Final_Assembly_Agent)

        # Create Crew
        self.crew = Crew(
	    agents=[
		TextProcessingAgents,
        Research_agent,
        Content_Generation_agent,
        Quality_Assurance_Agent,
        Final_Assembly_Agent
	    ],
	    tasks=[
		Clean_and_Normalize_Text_Tasks,
        Perform_Web_Search_task,
        Content_Expansion_Task,
        quality_assurance_task,
        final_assembly_task
	    ]
        )


    def kickoff(self):
        if not self.crew:
            print(f"No crew found for {self.job_id}")
            return
        
        append_event(self.job_id, "CREW STARTED")
        try:
            print (f"""Running crew for {self
                                       .job_id}""")
            results = self.crew.kickoff()
            append_event(self.job_id,"Crew Completed")
            return results
        
        except Exception as e:
            append_event(self.job_id, f"""An error occurred: {e}""")
            return str(e)