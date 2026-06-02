"""
    Implementacao de um padrao de resiliência: Circuit Breaker

    Propriedades de estado:
    state: CLOSED, OPEN, HALF-OPEN
    failure_threshold: O número máximo de falhas consecutivas permitida
    failure_count: O contador de falhas consecutivas atuais. Se o circuito estiver CLOSED e esse número atingir o failure_threshold, o circuito abre. Se uma requisição funcionar, esse contador zera.
    recovery_timeout: O tempo (em segundos) que o circuito deve permanecer no estado OPEN antes de transicionar para HALF-OPEN
    last_failure_time: Armazena o timestamp em que o circuito abriu.
"""
from typing import Any, Callable
from datetime import datetime
class CircuitBreakerOpenException(Exception):
    """Exceção genérica para erros de provedor de IA."""
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: int) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.last_failure_time = None
        self.failure_count = 0
        self.state = "CLOSED"
    def before_call(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            time_passed = datetime.now() - self.last_failure_time
            gap_time = time_passed.total_seconds()
            if gap_time < self.recovery_timeout:
                raise CircuitBreakerOpenException(f"Circuito ABERTO. Bloqueando chamada. Tempo restante: {self.recovery_timeout - gap_time:.1f}s")
            self.state = "HALF-OPEN"
            return True
        return True
    def record_failure(self):
        self.failure_count += 1
        if self.state == "HALF-OPEN":
            self.last_failure_time = datetime.now()
            self.state = "OPEN"
        elif self.state == "CLOSED":
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_failure_time = datetime.now()
    def record_success(self):
        if self.state == "HALF-OPEN":
            self.state = "CLOSED"
            self.failure_count = 0

    def __call__(self, func: Callable[..., Any]) -> Callable[...,Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.before_call()
            try:
                result = func(*args, **kwargs)

                self.record_success()
                return result
            except Exception as e:
                self.record_failure()
                raise e

        return wrapper

"""
Se você quiser rodar um teste para ver o que acontece com o Circuit Breaker.
Descomente esse trecho de código e rode esse arquivo.
"""
#if __name__ == "__main__":
#    import time
#    # Instanciamos um disjuntor rígido: aguenta 2 falhas e fica 5 segundos de castigo
#    db_breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=5)
#    # Criamos uma função simulada que SEMPRE falha (como uma API fora do ar)
#    @db_breaker
#    def conectar_api_instavel():
#        print("-> Tentando conectar à API...")
#        raise ConnectionError("Falha de rede na API externa!")
#    # Vamos forçar chamadas para ver a máquina de estados agir:
#    print(f"=== Estado Inicial: {db_breaker.state} ===")
#    for i in range(1, 5):
#        print(f"\n--- Tentativa {i} ---")
#        try:
#            conectar_api_instavel()
#        except Exception as erro:
#            print(f"Capturado no main: {erro}")
#            print(f"Estado atual do Disjuntor: {db_breaker.state} (Falhas: {db_breaker.failure_count})")