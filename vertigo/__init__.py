import chainlit as cl
from openai import OpenAI
from config import Config
from prompts import query_writer_instructions, summarizer_instructions
from tavily import TavilyClient

import json

client = OpenAI(base_url=Config.AI_API_URL, api_key=Config.AI_API_KEY)



### Funzione chiamata da Chainlit

def llm(developer_prompt, user_prompt, temperature=0, response_format={"type":"json_object"}):
    # Crea una richiesta di completamento chat utilizzando il client OpenAI
    response = client.chat.completions.create(
        model=Config.LLM_MODEL_LOW,  # Specifica il modello da utilizzare
        messages=[
            {"role": "developer", "content": developer_prompt},  # Messaggio dal punto di vista dello sviluppatore
            {"role": "user", "content": user_prompt}  # Messaggio dal punto di vista dell'utente
        ],
        temperature=temperature,  # Imposta la casualità della risposta
        response_format=response_format  # Specifica il formato della risposta
    )
    # Restituisce il contenuto del primo messaggio nella risposta del modello
    return response.choices[0].message.content
    
def optimize_search_query(research_topic):
    formatted_instructions = query_writer_instructions.format(research_topic = research_topic)
    result = llm(formatted_instructions, "Genera una query ottimizzata per ricerca su internet:")
    obj = json.loads(result)
    return obj


def _format_content(result):
   return f"""
   Fonte: {result['title']}:\n===\n
   Titolo: {result['url']}:\n===\n
   Contesto: {result['content']}
   """

def web_research(search_query):
    tavily_api_key = "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"
    max_results = 20
    include_raw = False
    client = TavilyClient(tavily_api_key)
    
    response = client.search(
               query = search_query, 
               max_results = max_results, 
               include_raw_content = include_raw
    )
    results = response.get('results', [])
    titles = [result["title"] for result in results]
    contents = [_format_content(result) for result in results]
    return {
        "source_gathered": titles,
        "web_research_results": contents
    }
    
def summarize_sources(web_research_results, research_topic, running_summary = None):
    current_result = web_research_results[-1]
        
    if running_summary:
        message =( 
            f"Estendi questo riassunto: {running_summary}\n\n"
            f"Con questi nuovi risultati: {current_result}"
            f"Sul tema: {research_topic}"
        )
    else:
        message = ( 
            f"Riassumi i risultati ottenuti: {current_result}"
            f"Sul tema: {research_topic}"
        )

        output_formatter = None
        return llm(summarizer_instructions, message, 0.2, output_formatter)    
        
### Interagire con il tuo modello


@cl.on_message
async def main(message: cl.Message):
    # Fase 1 Generazione Iniziale della Query Iniziale   
    user_messages = message.content
    osq = optimize_search_query(user_messages)

    query, aspect, reason = osq['query'], osq['aspect'], osq['reason']
    
    running_summary = None


    # Messaggio dell'utente
    results = web_research(query)
    await cl.Message(author="system_assistant", content=f"Questi sono i risultati migliori che ho trovato:\n {query}.\n Mi sono soffermato su: {aspect}.\n per quanto riguarda: {reason}").send()
    # Fase 2 Riassunto
    summary = llm(
        summarizer_instructions,
        f"Riassumi i risultati ottenuti: {results['web_research_results']}",
        0.2, None
        )
    print(f"Riassumi i risultati ottenuti: {results['web_research_results']}")
    summary = summarize_sources(results['web_research_results'], query, running_summary)

    await cl.Message(author="system_assistant", content=f"Riassunto: {summary}").send()
