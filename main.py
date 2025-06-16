import os
import getpass
from typing import TypedDict
from textwrap import dedent
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph

# Environment setup
def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}: ")

_set_if_undefined("OPENAI_API_KEY")

# Prompts
TARGET_DOMAIN = dedent("""
        As a Domain Analysis Specialist, extract the core innovation domain from the user query.
        Instructions:
        1. Analyze the user's input
        2. Identify the primary domain requiring innovation
        3. Classify it within standard innovation categories
        Output Format:
        Target Domain: [Clear, specific domain label]
        Be very detailed and specific in your response and do not generalize. Respond ONLY with the name of the domain, do NOT include ANY other text like 'Target Domain:'.
        User query: {user_query}
""").strip()

PROBLEM_LANDSCAPE = dedent("""
        You are a Problem Landscape Analyst. Your task is to map out the concrete challenges within the target domain identified.
        Instructions:
        1. Identify 3-5 core problems or challenges currently present in this domain.
        2. For each problem, provide:
        - Problem: A short, clear title.
        - Description: 2-3 sentences explaining what the problem is and why it matters.
        - Context: Briefly state the circumstances or environment where this problem occurs.
        - Stakeholders: List the main groups or individuals affected.
        - Root Causes: Identify 1-3 underlying causes, if known.
        - Impact: State the significance of the problem (e.g., social, economic, technical).
        - Current Approaches: How is this problem currently addressed?
        - Limitations: What are the shortcomings of current approaches?
        - Success Metrics: How would you measure if this problem is solved?
        - Interconnections: Note if this problem is linked to or influenced by other problems.
        Output Format:
        Present your findings as a structured list or JSON array, with each problem fully described as above.
        Important:
        - Focus on clarity and completeness.
        - Avoid abstracting or generalizing; stay concrete and domain-specific.
        - Do not propose solutions; only describe the current problem landscape.
        Target domain: {target_domain}
""").strip()

ABSTRACTION = dedent("""
You are a TRIZ Methodology Expert. Transform domain-specific problems into universal contradictions.
        Process:
        1. For each problem in the problem landscape
        - Abstract to universal parameters (what improves vs. what worsens)
        - Express as 'When we improve X, Y worsens'
        - Ensure parameters are domain-agnostic
        2. Identify 3-4 core contradictions:
        - Select the most fundamental tensions
        - Map to TRIZ contradiction matrix
        - Note applicable inventive principles
        Output:
        # Core Contradictions:
        1. Improving [parameter] vs. Worsening [parameter]
        - TRIZ Principles: [1-3 relevant principles]
        - Innovation Potential: [High/Medium/Low]
        - Universal Application: [Brief example from another domain]
        Focus on contradictions that, if resolved, would create breakthrough value.

        Problem landscape: {problem_landscape}
""").strip()

BASE_DOMAIN = dedent("""
        You are a Cross-Domain Search Specialist.
        For each contradiction provided, identify two distinct source domains (fields or industries) where this contradiction has been successfully addressed.
        The domains should have A CONCEPTUAL DISTANCE OF AT LEAST 2 DISTINCT HOPS FROM WHAT IMMEDIATELY COMES TO MIND. Be creative! It can be domains within spheres like natural, physical, social, artistic, anything.
        For each domain, briefly explain why it is relevant to the contradiction. Do not describe specific solutions-only list the domains and your rationale.
        Output:
        A list for each contradiction, naming two relevant domains with a one-sentence rationale for each.

        Contradictions: {contradictions}
""").strip()

BASE_SOLUTIONS = dedent("""
        You are a Solution Pattern Extractor. You are provided with an input with 2 base domains identified per contradiction.
        For each of these identified base domains, identify one specific, well-documented solution pattern within the domain that effectively resolves the contradiction.
        For each solution pattern:
        - The original base domain identified
        - The name or label of the solution pattern
        - A detailed description of the core mechanism or principle involved and how it addressed the domain's contradiction
        - The context or situation in the domain where this pattern is applied
        Do not generalize or adapt the solution-simply describe how the contradiction is addressed within each source domain.
        Output:
        For each of the provided domain, list the base domain name, solution pattern name, a detailed description of its mechanism, and the context in which it is used.

        Input: {input}
""").strip()

ANALOGICAL_TRANSFER = dedent("""
You are an Analogical Transfer Specialist.

Your task is to propose how solution patterns used to resolve abstracted contradictions in various base domains might inspire solution framings for the original target domain.

Input:
1. A list of abstracted contradictions, each with two base domains and their associated solution patterns (including how each contradiction was resolved in those domains).
2. The original target domain.

Instructions:
For each contradiction, review the solution patterns from both base domains. For each pattern:
- Analyze the core mechanism or principle behind the solution.
- Map and adapt this mechanism conceptually to the target domain, considering the specific context and needs of the target domain.
- Clearly describe how this analogical transfer could frame a potential solution in the target domain.
- Highlight any key adaptations, considerations, or limitations that would be relevant when applying this pattern to the target domain.

Output:
For each contradiction and base domain solution pattern, provide a comprehensive description of a proposed solution framing for the target domain, including:
- The original contradiction addressed
- The source domain and solution pattern
- A detailed explanation of how the pattern could inspire or inform a solution in the target domain
- Any important adaptations or considerations for successful transfer

Input:
- List of abstracted contradictions: {contradictions_solutions}
- Original target domain: {target_domain}
""").strip()

# Graph state
class ReasoningState(TypedDict):
    user_query: str
    target_domain: str
    problem_landscape: str
    abstraction: str
    base_domain: str
    base_solutions: str
    analogical_transfer: str
    solution: str

# Initialize LLM
llm = init_chat_model("openai:gpt-4o")

# Agent functions
def target_domain_agent(state: ReasoningState):
    u = state['user_query']
    msg = llm.invoke(TARGET_DOMAIN.format(user_query=u))
    return {"target_domain": msg.content}

def problem_landscape_agent(state: ReasoningState):
    t = state['target_domain']
    msg = llm.invoke(PROBLEM_LANDSCAPE.format(target_domain=t))
    return {"problem_landscape": msg.content}

def abstraction_agent(state: ReasoningState):
    p = state['problem_landscape']
    msg = llm.invoke(ABSTRACTION.format(problem_landscape=p))
    return {"abstraction": msg.content}

def base_domain_agent(state: ReasoningState):
    a = state['abstraction']
    msg = llm.invoke(BASE_DOMAIN.format(contradictions=a))
    return {"base_domain": msg.content}

def base_solution_agent(state: ReasoningState):
    b = state['base_domain']
    msg = llm.invoke(BASE_SOLUTIONS.format(input=b))
    return {"base_solutions": msg.content}

def analogical_transfer_agent(state: ReasoningState):
    if "base_solutions" not in state:
        raise ValueError("Missing 'base_solutions' key. Check if previous node returned it.")
    b = state['base_solutions']
    t = state['target_domain']
    msg = llm.invoke(ANALOGICAL_TRANSFER.format(contradictions_solutions=b, target_domain=t))
    return {"analogical_transfer": msg.content}

def synthesis_agent(state: ReasoningState):
    msg = llm.invoke(
        f"Evaluate the proposed analogical solutions. Find the best one that balances practicality with innovation. Then, provide a detailed, well-structured response that addresses all aspects of the query.\n\n"
        f"Problem: {state['user_query']}\n"
        f"Analogical Solutions: {state['analogical_transfer']}"
        f"In your output, remember to abstract away the analogy itself such that it is focused on responding to the user input."
    )
    return {"solution": msg.content}

# Construct the workflow
def create_workflow():
    workflow = StateGraph(ReasoningState)
    
    workflow.add_node("target", target_domain_agent)
    workflow.add_node("landscape", problem_landscape_agent)
    workflow.add_node("abstract", abstraction_agent)
    workflow.add_node("base", base_domain_agent)
    workflow.add_node("base_soln", base_solution_agent)
    workflow.add_node("analogy", analogical_transfer_agent)
    workflow.add_node("synthesis", synthesis_agent)
    
    workflow.set_entry_point("target")
    
    # Define edges
    workflow.add_edge("target", "landscape")
    workflow.add_edge("landscape", "abstract")
    workflow.add_edge("abstract", "base")
    workflow.add_edge("base", "base_soln")
    workflow.add_edge("base_soln", "analogy")
    workflow.add_edge("analogy", "synthesis")
    
    workflow.set_finish_point("synthesis")
    
    return workflow.compile()

def process_query(user_query: str) -> str:
    """Process a user query through the analogical reasoning pipeline."""
    graph = create_workflow()
    input_state = {"user_query": user_query}
    final_state = graph.invoke(input_state)
    return final_state["solution"]

# For testing
if __name__ == "__main__":
    test_query = input("Enter your query: ")
    result = process_query(test_query)
    print("\n" + "="*50)
    print("ANALOGICAL REASONING RESULT:")
    print("="*50)
    print(result)