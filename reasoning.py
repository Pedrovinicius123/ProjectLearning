from api import make_request_to_ollama
import torch
import os


class Reasoning:
    def __init__(self, max_depth:int, max_width:int,  model:str="deepseek-r1:7b"):
        #self.core = Client()
        self.max_depth = max_depth
        self.max_width = max_width
        self.model = model

    def reasoning_step(self, query:str, context:str, depth:int=0, current_pos:int=0, tree=None):
        path_logging = os.path.join(".", "logs")
        if tree is None:
            tree = {}

        if depth <= self.max_depth:
            tree[query] = {}
            prompt = f"""
            Analise este problema passo a passo:

            PROBLEMA: {query}
            
            PENSE EM VOZ ALTA:
            1. Quebre o problema em partes menores
            2. Identifique o que precisa ser verificado
            3. Sugira próximos passos (escrevendo, além deles, PROGRESS ou SOLVED)
            
            RACIOCÍNIO:
            """

            response = make_request_to_ollama(self.model, prompt, context)
            if not os.path.exists(path_logging):
                os.makedirs(path_logging)

            with open(os.path.join(".","logs",f"log{depth}-{current_pos}.md"), 'w') as file:
                file.write(query+'\n\n')
                file.write(response)

            if "PROGRESS" in response.upper(): 
                context_resp = query + "\n\n" + response
                for i in range(self.max_width):
                    current_pos += 1
                    query_progress = f"""                    
                    Elabore uma nova possibilidade de pergunta sob o contexto, a qual possibilitará
                    progresso no raciocínio.
                    
                    Elabore uma pergunta que poderá ser respondida por 'sim' ou 'não', 
                    se não houver uma resposta clara, siga em frente.
                    
                    """

                    response_query_progress = make_request_to_ollama(self.model, context_resp, prompt)
                    result = self.reasoning_step(response_query_progress, context_resp, depth+1, current_pos, tree[query])

                    tree[query_progress] = result
                    if result:
                        return result

                    context += f"\n\n{i+1}." + result_query

            elif "SOLVED" in response.upper():
                tree[query] = response
                context += "\n\n" + query

                prompt = f"""
                
                Com base no contexto anterior de raciocínio, gere uma demonstração rigorosa e clara, citando a
                o Ollama API bem como outros artigos acadêmicos de outros autores.
                Enfatize o uso de Inteligência Artificial no processo.            
                
                """

                response_query = make_request_to_ollama(self.model, context, prompt)
                #print(response_query[0]["generated_text"])
                with open(os.path.join(".","output.md"), 'w') as file:
                    file.write(query+'\n\n')
                    file.write(response_query)
