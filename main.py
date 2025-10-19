from reasoning import Reasoning

if __name__ == '__main__':
    # Configurações conservadoras para distilgpt2
    thinker = Reasoning(
        max_depth=7,      # Reduzido de 10 para 3
        max_width=3,      # Reduzido de 5 para 2
        model="deepseek-v3.1:671b-cloud"
    )
    
    # Query mais específica e curta
    result = thinker.reasoning_step(
        "O problema 3SAT pode ser resolvido em tempo polinomial?", 
        "Você é um matemático renomado"
    )
