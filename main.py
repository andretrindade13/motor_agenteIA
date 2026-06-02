##Implementar um agente de IA focado em chamadas de ferramentas (Tool Calling).
#Esse projeto aplica fundamentos de engenharia de software rididos como boas práticas, Desacoplamento
#Resiliências e Observabilidade. Esses são principios norteadores de qualquer projeto que seja projetado
#para ambientes de producao

"""
Esse Projeto visa evoluir para uma ferramenta mult tooling, você escolhe a ferramenta e a funcao do seu agente e ele
responde adequadamente de acordo com sua funcao atual
"""
from google.genai.errors import ClientError, ServerError

from AIAssistantStrategy import AIAssistant, AIProviderType
from src.providers.GeminiProvider import AIProviderError
from src.utils.resilience import CircuitBreakerOpenException


def main() -> None:
    aiassistant = AIAssistant()
    prompt = "Eu quero saber sobre os emails que eu recebi desde de a ultima quinta-feira, selecione apenas os emails que precisam de alguma acao, e me sugira uma acao necessaria para cada um deles"
    #prompt = "me explique como a ia funciona em poucas palavras "
    try:

       aiassistant.set_provider(AIProviderType.GEMINI)
       response = aiassistant.generate_response(prompt)
       print (f"Resposta do OPEN: {response}")
    except AIProviderError as e:
        print(f"Erro: {e}")
    except CircuitBreakerOpenException as e:
        # Captura o bloqueio do SEU Circuit Breaker
        print(f"\n[SISTEMA PROTEGIDO] {e}")

    except ClientError as e:
        # Captura o erro 429 (Limite de requisições atingido)
        print(f"\n[LIMITE DE COTA] Você atingiu o limite de requisições gratuitas do Gemini.")
        print("O Circuit Breaker registrou essa falha e vai proteger o sistema.")

    except ServerError as e:
        # Captura erros 500/503 (Instabilidade da Google)
        print(f"\n[PROVEDOR INDISPONÍVEL] O servidor do Gemini está instável.")

    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")

if __name__ == "__main__":
    main()