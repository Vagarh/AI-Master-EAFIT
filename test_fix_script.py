with open("Proyecto_Agente/test/test_agent.py", "r") as f:
    content = f.read()

content = content.replace('GEMINI_API_KEY', 'HUGGING_FACE_API_KEY')
content = content.replace('API key for Gemini not found', 'API key for Hugging Face not found')
content = content.replace('gemini/gemini-pro', 'huggingface/together/deepseek-ai/DeepSeek-R1')
content = content.replace('Error al contactar el modelo de lenguaje: Error de red simulado', 'Error al procesar la solicitud con el agente: Error de red simulado')

content = content.replace('mock_response.choices[0].message.content = "Respuesta simulada de la IA"', 'mock_response.choices[0].message.tool_calls = None\n        mock_response.choices[0].message.content = "Respuesta simulada de la IA"')

with open("Proyecto_Agente/test/test_agent.py", "w") as f:
    f.write(content)

print("Applied quick-fixes to test_agent.py to make tests pass given the implementation was actually previously changed to HuggingFace DeepSeek.")
