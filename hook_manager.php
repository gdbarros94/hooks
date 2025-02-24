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

    public static function add_action($hook_name, $function, $priority = 10) {
        if (!isset(self::$hooks[$hook_name])) {
            self::$hooks[$hook_name] = [];
        }
        self::$hooks[$hook_name][] = ["function" => $function, "priority" => $priority];
        usort(self::$hooks[$hook_name], function ($a, $b) {
            return $a["priority"] <=> $b["priority"];
        });
        self::save_hooks();
    }

    public static function do_action($hook_name, ...$args) {
        if (isset(self::$hooks[$hook_name])) {
            foreach (self::$hooks[$hook_name] as $hook) {
                $function = $hook["function"];
                if (function_exists($function)) {
                    call_user_func_array($function, $args);
                }
            }
        }
    }

    public static function apply_filters($hook_name, $value, ...$args) {
        if (isset(self::$hooks[$hook_name])) {
            foreach (self::$hooks[$hook_name] as $hook) {
                $function = $hook["function"];
                if (function_exists($function)) {
                    $value = call_user_func_array($function, array_merge([$value], $args));
                }
            }
        }
        return $value;
    }
}

// Carregando Hooks
HookManager::load_hooks();

// --- Função do Sistema ---
function sistema_processa_dados($dado) {
    echo "[SISTEMA] Processando dado original: $dado\n";
    $dado = HookManager::apply_filters("antes_do_sistema", $dado);
    $resultado = "Resultado do sistema com dado: $dado\n";
    $resultado = HookManager::apply_filters("depois_do_sistema", $resultado);
    return $resultado;
}

// --- Funções do Plugin ---
function intercepta_antes($dado) {
    echo "[PLUGIN] Interceptando antes do sistema...\n";
    return strtoupper($dado);
}

function intercepta_depois($resultado) {
    echo "[PLUGIN] Interceptando depois do sistema...\n";
    return $resultado . " [MODIFICADO PELO PLUGIN]\n";
}

// Registrando Hooks
HookManager::add_action("antes_do_sistema", "intercepta_antes", 5);
HookManager::add_action("depois_do_sistema", "intercepta_depois", 10);

// Executando o sistema
$res = sistema_processa_dados("meu dado");
echo "$res\n";
?>
