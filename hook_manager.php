<?php
class HookManager {
    private static $json_file = "hooks.json";
    private static $hooks = [];

    public static function load_hooks() {
        if (file_exists(self::$json_file)) {
            self::$hooks = json_decode(file_get_contents(self::$json_file), true);
        }
    }

    public static function save_hooks() {
        file_put_contents(self::$json_file, json_encode(self::$hooks, JSON_PRETTY_PRINT));
    }

    public static function add_before_hook($hook_name, $function, $priority = 10) {
        if (!isset(self::$hooks[$hook_name])) {
            self::$hooks[$hook_name] = ["before" => [], "after" => []];
        }
        self::$hooks[$hook_name]["before"][] = ["function" => $function, "priority" => $priority];
        usort(self::$hooks[$hook_name]["before"], function($a, $b) {
            return $a["priority"] <=> $b["priority"];
        });
        self::save_hooks();
    }

    public static function add_after_hook($hook_name, $function, $priority = 10) {
        if (!isset(self::$hooks[$hook_name])) {
            self::$hooks[$hook_name] = ["before" => [], "after" => []];
        }
        self::$hooks[$hook_name]["after"][] = ["function" => $function, "priority" => $priority];
        usort(self::$hooks[$hook_name]["after"], function($a, $b) {
            return $a["priority"] <=> $b["priority"];
        });
        self::save_hooks();
    }

    public static function get_before_hooks($hook_name) {
        if (isset(self::$hooks[$hook_name]["before"])) {
            return array_map(function($hook) { return $hook["function"]; }, self::$hooks[$hook_name]["before"]);
        }
        return [];
    }

    public static function get_after_hooks($hook_name) {
        if (isset(self::$hooks[$hook_name]["after"])) {
            return array_map(function($hook) { return $hook["function"]; }, self::$hooks[$hook_name]["after"]);
        }
        return [];
    }

    // Função que envolve a chamada de uma função com os hooks automaticamente
    public static function call_hookable($hook_name, $callable, $args = []) {
        // Aplica os before hooks
        $before_hooks = self::get_before_hooks($hook_name);
        foreach ($before_hooks as $function) {
            if (function_exists($function)) {
                // Cada before hook recebe os argumentos e retorna um array com novos argumentos
                $new_args = call_user_func_array($function, $args);
                if (is_array($new_args)) {
                    $args = $new_args;
                }
            }
        }
        // Chama a função original com os parâmetros (possivelmente modificados)
        $result = call_user_func_array($callable, $args);
        // Aplica os after hooks
        $after_hooks = self::get_after_hooks($hook_name);
        foreach ($after_hooks as $function) {
            if (function_exists($function)) {
                $result = call_user_func($function, $result);
            }
        }
        return $result;
    }
}

// Carrega os hooks do JSON
HookManager::load_hooks();

//////////////////////////
// Função do Sistema
//////////////////////////
function sistema_processa_dados($dado) {
    echo "[SISTEMA] Processando dado: $dado\n";
    return "Resultado final: $dado";
}

//////////////////////////
// Plugin: Funções de Interceptação
//////////////////////////
function antes_plugin($dado) {
    echo "[PLUGIN] Executando before hook\n";
    // Exemplo: converte o dado para maiúsculas
    return [strtoupper($dado)];
}

function depois_plugin($resultado) {
    echo "[PLUGIN] Executando after hook\n";
    return $resultado . " [MODIFICADO PELO PLUGIN]";
}

// Registra os hooks
HookManager::add_before_hook("sistema_processa_dados", "antes_plugin", 5);
HookManager::add_after_hook("sistema_processa_dados", "depois_plugin", 10);

//////////////////////////
// Execução do Sistema via wrapper
//////////////////////////
$res = HookManager::call_hookable("sistema_processa_dados", "sistema_processa_dados", ["meu dado"]);
echo $res . "\n";
?>
