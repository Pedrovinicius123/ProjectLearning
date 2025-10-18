from transformers import pipeline
import torch
import os


class Reasoning:
    def __init__(self, max_depth:int, max_width:int,  model:str="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"):
        
        self.generator = pipeline("text-generation", model=model)
        self.max_depth = max_depth
        self.max_width = max_width

    def reasoning_step(self, query:str, context:str, depth:int=0, current_pos:int=0, tree=None):
        if tree is None:
            tree = {}

        if depth <= self.max_depth:
            tree[query] = {}
            prompt = f"""
            Analise este problema passo a passo:

            PROBLEMA: {query}

            CONTEXTO: {context}
            
            PENSE EM VOZ ALTA:
            1. Quebre o problema em partes menores
            2. Identifique o que precisa ser verificado
            3. Sugira próximos passos (escrevendo, além deles, PROGRESS ou SOLVED)
            
            RACIOCÍNIO:
            """
            message = [
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "system",
                    "content": context

                }
            
            ]

            response = self.generator(
                message,
                max_new_tokens=600,
                temperature=0.5,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id,
                num_return_sequences=1
            )

            print(response[0]["generated_text"])
            with open(os.path.join(".","logs",f"log{depth}-{current_pos}.md"), 'w') as file:
                file.write(query+'\n\n')
                file.write(response[0]["generated_text"])

            if "PROGRESS" in response[0]["generated_text"].upper(): 
                context_resp = query + "\n\n" + response[0]['generated_text']
                for i in range(self.max_width):
                    current_pos += 1
                    query_progress = f"""
                    Contexto anterior: {context_resp}
                    
                    [System]
                    Elabore uma nova possibilidade de pergunta sob o contexto, a qual possibilitará
                    progresso no raciocínio.
                    
                    Elabore uma pergunta que poderá ser respondida por 'sim' ou 'não', 
                    se não houver uma resposta clara, siga em frente.
                    [/System]
                    
                    """

                    message = [
                        {
                            "role": "user",
                            "content": query_progress
                        },
                        {
                            "role": "system",
                            "content": context_resp

                        }
                    
                    ]

                    response_query_progress = self.generator(
                        message,
                        max_new_tokens=100,
                        temperature=0.5,
                        do_sample=True,
                        pad_token_id=self.generator.tokenizer.eos_token_id,
                        num_return_sequences=1
                    )

                    result_query = response_query_progress[0]["generated_text"]
                    result = self.reasoning_step(result_query, context_resp, depth+1, current_pos, tree[query])

                    tree[query_progress] = result
                    if result:
                        return result

                    context += f"\n\n{i+1}." + result_query

            elif "CONCLUSION" in response[0]['generated_text'].upper():
                tree[query] = response.choices[0].message.content
                prompt = f"""
                Contexto anterior: {context + "\n\n" + query}
                
                [System]
                Com base no contexto anterior de raciocínio, gere uma demonstração rigorosa e clara, citando a
                (DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter, [Sanh, Victor and Debut, Lysandre and Chaumond, Julien and Wolf, Thomas], 2019) bem como outros artigos relacionados.
                Enfatize o uso de Inteligência Artificial no processo.            
                [/System]
                """

                message = [
                    {
                        "role": "user",
                        "content": prompt
                    },
                    {
                        "role": "system",
                        "content": context

                    }
                
                ]

                response_query = self.generator(
                    message,
                    max_new_tokens=10000,
                    temperature=0.5,
                    do_sample=True,
                    pad_token_id=self.generator.tokenizer.eos_token_id,
                    num_return_sequences=1
                )


                print(response_query[0]["generated_text"])
                with open(os.path.join(".","output.md"), 'w') as file:
                    file.write(query+'\n\n')
                    file.write(response_query[0]["generated_text"])
