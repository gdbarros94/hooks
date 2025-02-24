Sistema de Hooks e Actions com Plugins

Este projeto demonstra uma arquitetura modular para aplicações, inspirada no modelo do WordPress, onde é possível interceptar e modificar os parâmetros e retornos de funções do sistema através de hooks.
Os hooks são persistidos em um arquivo JSON, possuem hierarquia (prioridades) e permitem que plugins adicionem funcionalidades sem modificar o código principal.
Funcionalidades

    Hooks persistentes: Os hooks são salvos e carregados de um arquivo JSON, permitindo persistência e fácil configuração.
    Interceptação automática: Usamos uma camada de interceptação para que funções do sistema sejam automaticamente envolvidas por before hooks (executados antes) e after hooks (executados depois), sem alterar o corpo da função.
    Prioridades: Cada hook pode ser registrado com uma prioridade, definindo a ordem de execução.
    Plugins: Funções externas podem ser registradas para modificar os parâmetros (antes) e o retorno (depois) de funções críticas do sistema.

Como Funciona
1. Camada de Interceptação

Para interceptar as chamadas sem alterar o código do sistema, usamos um decorator em Python. Um decorator é uma função que envolve outra função, permitindo executar código adicional antes e/ou depois da função original. Assim, podemos modificar os parâmetros de entrada ou o resultado sem precisar editar a função principal.
O que é um Decorator em Python?

Imagine que você tem uma função que faz algo importante, mas você quer adicionar um comportamento extra (como logar, validar dados, ou modificar parâmetros) sempre que essa função for chamada.
Um decorator é uma função que recebe outra função como argumento, estende seu comportamento e retorna uma nova função "decorada".
Por exemplo:
```python
def meu_decorator(func):
    def wrapper(*args, **kwargs):
        print("Antes de chamar a função")
        resultado = func(*args, **kwargs)
        print("Depois de chamar a função")
        return resultado
    return wrapper

@meu_decorator
def minha_funcao(x):
    return x * 2

print(minha_funcao(5))
```
Ao usar @meu_decorator, o Python transforma minha_funcao na função wrapper definida dentro do decorator. Dessa forma, sempre que minha_funcao é chamada, o código dentro de wrapper é executado, permitindo adicionar comportamentos sem alterar o código original.
2. Sistema de Hooks com Decorator

No nosso sistema, o decorator @hookable envolve a função do sistema. Ele executa automaticamente:

    Before hooks: Funções registradas que podem modificar os parâmetros antes da execução da função original.
    After hooks: Funções registradas que podem modificar o retorno após a execução da função original.

Veja um trecho de código da implementação em Python:
```python
def hookable(hook_name):
    """
    Decorator que intercepta a chamada de uma função:
      - Aplica before hooks para modificar os parâmetros;
      - Chama a função original;
      - Aplica after hooks para modificar o retorno.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Aplica os before hooks
            for hook_func_name in hook_manager.get_before_hooks(hook_name):
                if hook_func_name in globals():
                    hook_func = globals()[hook_func_name]
                    modified = hook_func(*args, **kwargs)
                    if isinstance(modified, tuple) and len(modified) == 2:
                        args, kwargs = modified
            # Chama a função original
            result = func(*args, **kwargs)
            # Aplica os after hooks
            for hook_func_name in hook_manager.get_after_hooks(hook_name):
                if hook_func_name in globals():
                    hook_func = globals()[hook_func_name]
                    result = hook_func(result)
            return result
        return wrapper
    return decorator

@hookable("sistema_processa_dados")
def sistema_processa_dados(dado):
    print(f"[SISTEMA] Processando dado: {dado}")
    return f"Resultado final: {dado}"
```
3. Registro e Execução dos Plugins

Os plugins registram funções que serão chamadas automaticamente como before ou after hooks. Por exemplo:
```python
def antes_plugin(dado, *args, **kwargs):
    print("[PLUGIN] Executando before hook")
    return ((dado.upper(),), kwargs)

def depois_plugin(resultado):
    print("[PLUGIN] Executando after hook")
    return resultado + " [MODIFICADO PELO PLUGIN]"

hook_manager.add_before_hook("sistema_processa_dados", antes_plugin, priority=5)
hook_manager.add_after_hook("sistema_processa_dados", depois_plugin, priority=10)
```
Dessa forma, quando sistema_processa_dados("meu dado") é chamado, o decorator intercepta a chamada:

    Before hooks: antes_plugin transforma o dado para maiúsculas.
    A função original processa o dado modificado.
    After hooks: depois_plugin modifica o resultado retornado pela função do sistema.

4. Implementação em PHP

Uma mecânica similar é implementada em PHP, usando uma função call_hookable que:

    Aplica os before hooks para modificar os parâmetros.
    Chama a função do sistema.
    Aplica os after hooks para modificar o retorno.

Confira o trecho de código em PHP:
```python
function call_hookable($hook_name, $callable, $args = []) {
    $before_hooks = HookManager::get_before_hooks($hook_name);
    foreach ($before_hooks as $function) {
        if (function_exists($function)) {
            $new_args = call_user_func_array($function, $args);
            if (is_array($new_args)) {
                $args = $new_args;
            }
        }
    }
    $result = call_user_func_array($callable, $args);
    $after_hooks = HookManager::get_after_hooks($hook_name);
    foreach ($after_hooks as $function) {
        if (function_exists($function)) {
            $result = call_user_func($function, $result);
        }
    }
    return $result;
}

$res = HookManager::call_hookable("sistema_processa_dados", "sistema_processa_dados", ["meu dado"]);
echo $res;
```
Resumo

    O que é um decorator?
    Um decorator em Python é uma função que recebe outra função, estende seu comportamento e retorna uma nova função, permitindo a injeção de código antes e depois da execução da função original.

    Como funciona o sistema de hooks?
    As funções do sistema são envolvidas por uma camada de interceptação que aplica os hooks registrados:
        Before hooks: Modificam os parâmetros antes da função principal.
        After hooks: Modificam o retorno depois que a função principal é executada.

    Vantagens:
        Permite a criação de um sistema modular e extensível.
        Plugins podem ser adicionados sem alterar o código principal.
        A persistência via JSON facilita a configuração e manutenção dos hooks.

Esse sistema demonstra como é possível criar uma arquitetura dinâmica, onde funcionalidades podem ser alteradas ou estendidas sem tocar no núcleo da aplicação, inspirando a criação de plugins e frameworks altamente configuráveis.
