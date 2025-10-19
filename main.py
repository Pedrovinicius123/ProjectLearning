from reasoning import Reasoning

if __name__ == '__main__':
    # Configurações conservadoras para distilgpt2
    thinker = Reasoning(
        max_depth=15,      # Reduzido de 10 para 3
        max_width=4,      # Reduzido de 5 para 2
        model="deepseek-v3.1:671b-cloud",
        log_dir="logs_2_try"
    )

    # Query mais específica e curta
    result = thinker.reasoning_step(
        "Demonstre *matematicamente* a Conjectura de Goldbach",
        "Você é um pesquisador renomado",
        '0',
    )
