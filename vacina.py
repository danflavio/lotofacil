import json

print("Analisando o modelo matemático (Keras 3)...")

with open('model.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Função tática para varrer a matriz e traduzir o dialeto do Keras 3 para TFJS
def consertar_incompatibilidade(obj):
    if isinstance(obj, dict):
        if 'dtype' in obj and isinstance(obj['dtype'], dict) and obj['dtype'].get('class_name') == 'DTypePolicy':
            obj['dtype'] = obj['dtype']['config']['name']
        for v in obj.values():
            consertar_incompatibilidade(v)
    elif isinstance(obj, list):
        for item in obj:
            consertar_incompatibilidade(item)

# Aplica a vacina
consertar_incompatibilidade(dados)

# Sobrescreve o arquivo com a estrutura corrigida
with open('model.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, separators=(',', ':'))

print("Vacina aplicada com sucesso! O model.json agora é compatível com a Web.")