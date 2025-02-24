import json
import os
import functools

class HookManager:
    def __init__(self, json_file="hooks.json"):
        self.json_file = json_file
        self.hooks = self._load_hooks()

    def _load_hooks(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                return json.load(file)
        # Estrutura: { hook_name: { "before": [ { "function": nome, "priority": int }, ... ],
        #                            "after": [ { "function": nome, "priority": int }, ... ] } }
        return {}

    def _save_hooks(self):
        with open(self.json_file, "w") as file:
            json.dump(self.hooks, file, indent=4)

    def add_before_hook(self, hook_name, function, priority=10):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = {"before": [], "after": []}
        self.hooks[hook_name]["before"].append({"function": function.__name__, "priority": priority})
        self.hooks[hook_name]["before"].sort(key=lambda x: x["priority"])
        self._save_hooks()

    def add_after_hook(self, hook_name, function, priority=10):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = {"before": [], "after": []}
        self.hooks[hook_name]["after"].append({"function": function.__name__, "priority": priority})
        self.hooks[hook_name]["after"].sort(key=lambda x: x["priority"])
        self._save_hooks()

    def get_before_hooks(self, hook_name):
        if hook_name in self.hooks and "before" in self.hooks[hook_name]:
            return [hook["function"] for hook in self.hooks[hook_name]["before"]]
        return []

    def get_after_hooks(self, hook_name):
        if hook_name in self.hooks and "after" in self.hooks[hook_name]:
            return [hook["function"] for hook in self.hooks[hook_name]["after"]]
        return []

# Instância global do HookManager
hook_manager = HookManager()

def hookable(hook_name):
    """
    Decorator que intercepta a chamada de uma função:
      - Aplica _before hooks_ para modificar os parâmetros (cada hook deve retornar uma tupla (args, kwargs))
      - Chama a função original com os parâmetros modificados
      - Aplica _after hooks_ para modificar o retorno
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Aplica os before hooks (em ordem de prioridade)
            for hook_func_name in hook_manager.get_before_hooks(hook_name):
                if hook_func_name in globals():
                    hook_func = globals()[hook_func_name]
                    # O hook recebe (args, kwargs) e retorna (novos_args, novos_kwargs)
                    modified = hook_func(*args, **kwargs)
                    if isinstance(modified, tuple) and len(modified) == 2:
                        args, kwargs = modified
            # Chama a função original com os parâmetros (possivelmente modificados)
            result = func(*args, **kwargs)
            # Aplica os after hooks (em ordem de prioridade)
            for hook_func_name in hook_manager.get_after_hooks(hook_name):
                if hook_func_name in globals():
                    hook_func = globals()[hook_func_name]
                    result = hook_func(result)
            return result
        return wrapper
    return decorator

#########################################
# Função do Sistema (sem alteração interna)
#########################################
@hookable("sistema_processa_dados")
def sistema_processa_dados(dado):
    print(f"[SISTEMA] Processando dado: {dado}")
    return f"Resultado final: {dado}"

#########################################
# Plugin: funções de interceptação
#########################################
def antes_plugin(dado, *args, **kwargs):
    print("[PLUGIN] Executando before hook")
    # Por exemplo, converte o dado para maiúsculas
    new_dado = dado.upper()
    # Retorna os novos parâmetros (args deve ser uma tupla)
    return ((new_dado,), kwargs)

def depois_plugin(resultado):
    print("[PLUGIN] Executando after hook")
    # Adiciona uma marcação ao resultado
    return resultado + " [MODIFICADO PELO PLUGIN]"

# Registrando os hooks no HookManager
hook_manager.add_before_hook("sistema_processa_dados", antes_plugin, priority=5)
hook_manager.add_after_hook("sistema_processa_dados", depois_plugin, priority=10)

#########################################
# Execução do sistema
#########################################
res = sistema_processa_dados("meu dado")
print(res)
