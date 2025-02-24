import json
import os

class HookManager:
    def __init__(self, json_file="hooks.json"):
        self.json_file = json_file
        self.hooks = self._load_hooks()

    def _load_hooks(self):
        """Carrega os hooks do JSON."""
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                return json.load(file)
        return {}

    def _save_hooks(self):
        """Salva os hooks no JSON."""
        with open(self.json_file, "w") as file:
            json.dump(self.hooks, file, indent=4)

    def add_action(self, hook_name, function, priority=10):
        """Adiciona uma ação a um hook com prioridade."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append({"function": function.__name__, "priority": priority})
        self.hooks[hook_name] = sorted(self.hooks[hook_name], key=lambda x: x["priority"])
        self._save_hooks()

    def do_action(self, hook_name, *args, **kwargs):
        """Executa todas as funções associadas a um hook."""
        if hook_name in self.hooks:
            for hook in sorted(self.hooks[hook_name], key=lambda x: x["priority"]):
                function_name = hook["function"]
                if function_name in globals():
                    globals()[function_name](*args, **kwargs)

    def apply_filters(self, hook_name, value, *args, **kwargs):
        """Permite que funções modifiquem um valor antes de ser retornado."""
        if hook_name in self.hooks:
            for hook in sorted(self.hooks[hook_name], key=lambda x: x["priority"]):
                function_name = hook["function"]
                if function_name in globals():
                    value = globals()[function_name](value, *args, **kwargs)
        return value


# Criando um gerenciador de hooks
hooks = HookManager()

# --- Funções do Sistema ---
def sistema_processa_dados(dado):
    """Função do sistema que recebe um dado e retorna uma resposta"""
    print(f"[SISTEMA] Processando dado original: {dado}")
    dado = hooks.apply_filters("antes_do_sistema", dado)  # Modifica antes da execução
    resultado = f"Resultado do sistema com dado: {dado}"
    resultado = hooks.apply_filters("depois_do_sistema", resultado)  # Modifica depois da execução
    return resultado


# --- Funções que Interceptam Hooks ---
def intercepta_antes(dado):
    """Intercepta antes do sistema e modifica o dado"""
    print("[PLUGIN] Interceptando antes do sistema...")
    return dado.upper()

def intercepta_depois(resultado):
    """Intercepta depois do sistema e modifica a resposta"""
    print("[PLUGIN] Interceptando depois do sistema...")
    return resultado + " [MODIFICADO PELO PLUGIN]"

# Registrando Hooks
hooks.add_action("antes_do_sistema", intercepta_antes, priority=5)
hooks.add_action("depois_do_sistema", intercepta_depois, priority=10)

# Executando o sistema com hooks aplicados
res = sistema_processa_dados("meu dado")
print(res)
