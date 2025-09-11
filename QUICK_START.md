# ⚡ Quick Start - Comandos Essenciais

## 🔧 Setup (uma vez só)
```powershell
python setup.py
```

## 🎬 Teste inicial
```powershell
python demo.py
```

## 📝 Adicionar informações
```powershell
# Texto simples
python cli.py --texto "sua anotação aqui"

# Com contexto
python cli.py --texto "reunião sobre projeto X" --tags "trabalho,projeto-x"
```

## 📋 Ver "onde parei"
```powershell
python cli.py --contexto "trabalho"
python cli.py --contexto "estudos"
python cli.py --contexto "projeto X"
```

## 🔔 Verificar lembretes
```powershell
python cli.py --nudges
```

## ❓ Perguntas rápidas
```powershell
python cli.py --pergunta "o que fazer hoje?"
python cli.py --pergunta "onde estou travado?"
```

## 🤔 Reflexão semanal
```powershell
python cli.py --reflexao "semana"
```

## 📊 Menu completo
```powershell
python cli.py
```

---

**💡 Dica**: Use tags consistentes como "trabalho", "estudo", "pessoal" para organizar melhor suas memórias.

**🎯 Meta**: Use 5 minutos por dia adicionando informações importantes. O agente fará o resto!
