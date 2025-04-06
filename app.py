from praisonaiagents import Agent, Agents, MCP
import os
from rich import print
import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQL_API_KEY = os.getenv("GROQ_API_KEY")
brave_api_key = os.getenv("BRAVE_API_KEY")

# Literature Research Agent - Finds relevant scientific papers and research
literature_agent = Agent(
    instructions="Research scientific literature, academic papers, and research findings on specific topics",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": brave_api_key})
)

# Methodology Agent - Analyzes research methodologies and experimental designs
methodology_agent = Agent(
    instructions="Analyze scientific methodologies, experimental designs, and data collection techniques",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": brave_api_key})
)

# Data Analysis Agent - Evaluates statistical methods and results interpretation
data_agent = Agent(
    instructions="Evaluate data analysis approaches, statistical methods, and results interpretation",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": brave_api_key})
)

# Summary & Implications Agent - Synthesizes research and explains significance
summary_agent = Agent(
    instructions="Synthesize research findings, explain significance, and suggest future research directions",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": brave_api_key})
)

def generate_research_report(topic, scope, depth, focus_areas):
    """Generate a comprehensive research report using the AI agents
    
    Args:
        topic (str): The main research topic to investigate
        scope (str): The scope of the research (e.g., last 5 years, specific field)
        depth (str): The level of technical detail desired
        focus_areas (str): Specific aspects of the topic to emphasize
        
    Returns:
        str: Formatted research report
    """
    
    # Create the research query
    research_query = f"""Create a comprehensive research report on {topic} within the scope of {scope}.
    Technical Depth: {depth}
    Focus Areas: {focus_areas}
    
    Include:
    1. Current state of research and key findings
    2. Major methodological approaches
    3. Data analysis techniques and findings
    4. Synthesis of results and future research directions
    """
    
    # Initialize the agents team
    agents = Agents(agents=[literature_agent, methodology_agent, data_agent, summary_agent])
    
    try:
        # Generate the research report
        result = agents.start(research_query)
        
        # Format the output with clear sections
        formatted_result = f"""
=== SCIENCE RESEARCH REPORT: {topic} ===

Scope: {scope}
Technical Depth: {depth}
Focus Areas: {focus_areas}

{result}
"""
        
        return formatted_result
    except Exception as e:
        return f"Error generating research report: {str(e)}"

# Create the Gradio interface with an academic theme
with gr.Blocks(title="AI Science Research Assistant", theme="soft") as demo:
    gr.Markdown("# 🔬 AI Science Research Assistant")
    gr.Markdown("Generate comprehensive research reports with our specialized AI agents")
    
    with gr.Row():
        with gr.Column(scale=1):
            topic = gr.Textbox(label="Research Topic", placeholder="CRISPR gene editing applications", value="CRISPR gene editing applications")
            scope = gr.Textbox(label="Research Scope", placeholder="Last 5 years, medical applications", value="Last 5 years, medical applications")
            depth = gr.Textbox(label="Technical Depth", placeholder="Graduate level, include technical details", value="Graduate level, include technical details")
            focus_areas = gr.Textbox(
                label="Focus Areas", 
                placeholder="Clinical trials, ethical considerations, recent breakthroughs",
                value="Clinical trials, ethical considerations, recent breakthroughs"
            )
            submit_btn = gr.Button("Generate Research Report 🧪", variant="primary")
        
        with gr.Column(scale=2):
            output = gr.Markdown(label="Your Research Report")
    
    submit_btn.click(
        generate_research_report,
        inputs=[topic, scope, depth, focus_areas],
        outputs=output
    )
    
    gr.Markdown("### How to use")
    gr.Markdown("""
    1. Enter your research topic of interest
    2. Specify the scope of research to include
    3. Indicate the desired technical depth
    4. Share specific focus areas within the topic
    5. Click 'Generate Research Report'
    
    *Note: Generation may take a minute or two as our AI agents conduct thorough research.*
    """)

# Run the CLI version when script is run directly
if __name__ == "__main__":
    # Launch the Gradio interface
    demo.launch()
    
    # Example CLI usage (commented out when using Gradio)
    """
    topic = "CRISPR gene editing applications"
    scope = "Last 5 years, medical applications"
    depth = "Graduate level, include technical details"
    focus_areas = "Clinical trials, ethical considerations, recent breakthroughs"
    
    research_query = f"What are the latest findings on {topic} within {scope} at a {depth} level focusing on {focus_areas}?"
    agents = Agents(agents=[literature_agent, methodology_agent, data_agent, summary_agent])
    result = agents.start(research_query)
    print(f"\n=== RESEARCH REPORT: {topic} ===\n")
    print(result)
    """