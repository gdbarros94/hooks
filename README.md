# Sistema de Hooks e Actions em Python e PHP

Este projeto demonstra como criar um sistema modular de hooks e actions, semelhante ao funcionamento do WordPress, permitindo a adição de funcionalidades sem modificar o código principal do sistema.

## Funcionalidades
✅ **Hooks persistentes** armazenados em JSON.  
✅ **Hierarquia e níveis de execução** com prioridade definida para cada hook.  
✅ **Interceptação de parâmetros antes da execução da função**.  
✅ **Modificação do retorno após a execução da função**.  
✅ **Possibilidade de criação de plugins sem alterar o código principal**.  

---

## Estrutura do Projeto

O projeto consiste em dois arquivos principais, um para Python e outro para PHP, cada um implementando um sistema de hooks modular.

- `hooks.json`: Armazena as configurações de hooks e suas funções associadas.
- `hook_manager.py`: Implementação do sistema de hooks em Python.
- `hook_manager.php`: Implementação do sistema de hooks em PHP.
- `plugin.py` e `plugin.php`: Exemplos de plugins adicionando funcionalidades ao sistema.

---

## Como Funciona?

### 1. Adicionando Hooks e Actions
Os hooks podem ser adicionados dinamicamente ao sistema, associando funções a um nome específico e atribuindo uma prioridade de execução. Isso permite que múltiplas funções sejam executadas antes ou depois de uma determinada função principal do sistema.

### 2. Execução dos Hooks
Quando um hook é acionado, todas as funções associadas a ele são executadas na ordem definida pela prioridade.

### 3. Modificação de Parâmetros e Retornos
- Hooks "antes" permitem modificar os parâmetros antes da função principal ser executada.
- Hooks "depois" permitem modificar o retorno da função principal.

---

## Exemplo de Uso (Python)

### Criando um Hook Manager
```python
hooks = HookManager()
```

### Criando uma Função do Sistema
```python
def sistema_processa_dados(dado):
    dado = hooks.apply_filters("antes_do_sistema", dado)
    resultado = f"Resultado: {dado}"
    resultado = hooks.apply_filters("depois_do_sistema", resultado)
    return resultado
```

### Criando um Plugin que Modifica os Dados
```python
def intercepta_antes(dado):
    return dado.upper()

def intercepta_depois(resultado):
    return resultado + " [MODIFICADO PELO PLUGIN]"

hooks.add_action("antes_do_sistema", intercepta_antes, priority=5)
hooks.add_action("depois_do_sistema", intercepta_depois, priority=10)
```

### Executando o Sistema
```python
res = sistema_processa_dados("meu dado")
print(res)
```
Saída esperada:
```
[SISTEMA] Processando dado original: meu dado
[PLUGIN] Interceptando antes do sistema...
[PLUGIN] Interceptando depois do sistema...
Resultado: MEU DADO [MODIFICADO PELO PLUGIN]
```

---

## Exemplo de Uso (PHP)

### Criando um Hook Manager
```php
HookManager::load_hooks();
```

### Criando uma Função do Sistema
```php
function sistema_processa_dados($dado) {
    $dado = HookManager::apply_filters("antes_do_sistema", $dado);
    $resultado = "Resultado: " . $dado;
    $resultado = HookManager::apply_filters("depois_do_sistema", $resultado);
    return $resultado;
}
```

### Criando um Plugin que Modifica os Dados
```php
function intercepta_antes($dado) {
    return strtoupper($dado);
}
function intercepta_depois($resultado) {
    return $resultado . " [MODIFICADO PELO PLUGIN]";
}
HookManager::add_action("antes_do_sistema", "intercepta_antes", 5);
HookManager::add_action("depois_do_sistema", "intercepta_depois", 10);
```

### Executando o Sistema
```php
$res = sistema_processa_dados("meu dado");
echo "$res\n";
```
Saída esperada:
```
[SISTEMA] Processando dado original: meu dado
[PLUGIN] Interceptando antes do sistema...
[PLUGIN] Interceptando depois do sistema...
Resultado: MEU DADO [MODIFICADO PELO PLUGIN]
```

---

## Conclusão
Este sistema permite que aplicações sejam estendidas sem modificar o código-fonte principal, tornando-as altamente flexíveis e modulares. Com esse conceito, é possível criar **frameworks**, **sistemas de plugins**, e **softwares altamente configuráveis**.

