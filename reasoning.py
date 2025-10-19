from api import *
import os


class Reasoning:
    def __init__(self, max_depth:int, max_width:int,  model:str="deepseek-r1:7b", log_dir:str="logs"):
        #self.core = Client()
        self.max_depth = max_depth
        self.max_width = max_width
        self.model = model
        self.log_dir = log_dir

    def reasoning_step(self, query:str, context:str, current_label:str, depth:int=0, init=True, use_cloud=True):
        path_logging = os.path.join(".", self.log_dir)

        if depth <= self.max_depth:
            prompt = query

            if init:
                prompt = f"""
                Analise este problema passo a passo:

                PROBLEMA: {query}

                PENSE EM VOZ ALTA:
                1. Quebre o problema em partes menores
                2. Identifique o que precisa ser verificado
                3. Sugira próximos passos (mostrando, também, PROGRESS ou SOLVED, para progresso e finalização, respectivamente)
                4. Deve ser sugerido ao máximo {self.max_width} alternativas de passos

                RACIOCÍNIO:
                """

            response = make_request_to_ollama_reasoning(self.model, context, prompt, 10000, use_cloud=use_cloud)
            if not os.path.exists(path_logging):
                os.makedirs(path_logging)

            with open(os.path.join(".",self.log_dir,f"log{current_label}.md"), 'w', encoding='utf-8') as file:
                #file.write(query+'\n\n')
                file.write(response)

            current_pos_tree = f"{depth}-"

            if "PROGRESS" in response.upper():
                context_resp = query + "\n\n" + response
                query_progress = f"""

                ETAPA {depth}

                Escolha, dentre os passos mais recentes sugeridos, o melho para implementar,
                focando no analítico ao invés do computacional
                Sugira também novos passos consecutivos também limitados a {self.max_width}
                Tenha em mente escrever PROGRESS para progresso ou apenas SOLVED para um resultado efetivo para a questão.
                """

                self.reasoning_step(
                    query=query_progress,
                    context=context_resp,
                    current_label = str(depth),
                    depth=depth+1,
                    init=False
                )

            if "não" in response.lower() and "SOLVED" in response.upper():
                context += "\n\n" + query

                response_query = make_request_to_ollama_compile(self.model, context, 500000, use_cloud=use_cloud)
                #print(response_query[0]["generated_text"])
                with open(os.path.join(".","output.md"), 'w', encoding='utf-8') as file:
                    file.write(response_query)
