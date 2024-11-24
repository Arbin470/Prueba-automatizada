from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from jinja2 import Template
from selenium.webdriver.edge.service import Service  
import os

driver_path = r"C:\Users\oca20\Desktop\edgedriver_win64\msedgedriver.exe"


service = Service(driver_path)


driver = webdriver.Edge(service=service)


BASE_URL = "http://127.0.0.1:5000"


results = []

def take_screenshot(test_name):
  
    if not os.path.exists("capturas"):
        os.makedirs("capturas")
    
    screenshot_path = f"capturas/{test_name}.png"
    driver.save_screenshot(screenshot_path)
    return screenshot_path

def test_carga_pagina():
    try:
        driver.get(BASE_URL)
        time.sleep(2)  
        assert "Calculadora" in driver.title
        screenshot = take_screenshot("carga_pagina")
        results.append({"test": "Carga de página", "resultado": "Éxito", "screenshot": screenshot})
    except Exception as e:
        screenshot = take_screenshot("carga_pagina")
        results.append({"test": "Carga de página", "resultado": f"Fallido - {e}", "screenshot": screenshot})

def test_formulario():
    try:
        driver.get(BASE_URL)
        
        
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")
        driver.find_element(By.ID, "operacion").send_keys("suma")
        driver.find_element(By.TAG_NAME, "button").click()
        
        time.sleep(2)  
        
       
        resultado = driver.find_element(By.TAG_NAME, "h2").text
        assert "Resultado: 15.0" in resultado
        screenshot = take_screenshot("formulario_funcional")
        results.append({"test": "Formulario funcional", "resultado": "Éxito", "screenshot": screenshot})
    except Exception as e:
        screenshot = take_screenshot("formulario_funcional")
        results.append({"test": "Formulario funcional", "resultado": f"Fallido - {e}", "screenshot": screenshot})

def test_operaciones():
    operaciones = {
        "suma": "15.0",
        "resta": "5.0",
        "multiplicacion": "50.0",
        "division": "2.0"
    }

    for operacion, resultado_esperado in operaciones.items():
        try:
            driver.get(BASE_URL)
            
            
            driver.find_element(By.ID, "num1").send_keys("10")
            driver.find_element(By.ID, "num2").send_keys("5")
            driver.find_element(By.ID, "operacion").send_keys(operacion)
            driver.find_element(By.TAG_NAME, "button").click()
            
            time.sleep(2)
            
            
            resultado = driver.find_element(By.TAG_NAME, "h2").text
            assert f"Resultado: {resultado_esperado}" in resultado
            screenshot = take_screenshot(f"operacion_{operacion}")
            results.append({"test": f"Operación {operacion}", "resultado": "Éxito", "screenshot": screenshot})
        except Exception as e:
            screenshot = take_screenshot(f"operacion_{operacion}")
            results.append({"test": f"Operación {operacion}", "resultado": f"Fallido - {e}", "screenshot": screenshot})


test_carga_pagina()
test_formulario()
test_operaciones()


reporte_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        img { width: 300px; }
    </style>
</head>
<body>
    <h1>Reporte de Pruebas Automatizadas</h1>
    <table>
        <thead>
            <tr>
                <th>Prueba</th>
                <th>Resultado</th>
                <th>Captura de Pantalla</th>
            </tr>
        </thead>
        <tbody>
            {% for result in results %}
            <tr>
                <td>{{ result.test }}</td>
                <td>{{ result.resultado }}</td>
                <td><img src="{{ result.screenshot }}" alt="Captura de Pantalla"></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""


template = Template(reporte_template)
reporte_html = template.render(results=results)


with open("reporte_pruebas.html", "w", encoding="utf-8") as f:
    f.write(reporte_html)


driver.quit()

print("Pruebas completadas. Revisa el archivo 'reporte_pruebas.html'")

