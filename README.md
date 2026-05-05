# 📊 Manipulação de Dados com Hadoop e MapReduce

**Aluno:** Ana Rosimeire Ferreira da Silva  
**Disciplina:** Ciência de Dados 

---

## 📌 Descrição da Atividade

Esta atividade tem como objetivo aplicar conceitos de Engenharia de Dados utilizando o ecossistema Hadoop e o modelo de programação MapReduce.

Foi utilizado o dataset **MovieLens 100k**, contendo avaliações de filmes, para realizar o processamento distribuído e extrair métricas estatísticas relevantes.

---

## 🧰 Tecnologias Utilizadas

- Docker
- Hadoop (HDFS + MapReduce)
- Python (Hadoop Streaming)
- VS Code

---

## 📁 Estrutura do Projeto

```
aula-hadoop/
├── Dockerfile
├── docker-compose.yml
├── analise_filmes.py
├── u.data
└── u.item
```

---

## ⚙️ Configuração do Ambiente

### 1. Build da imagem Docker

```bash
docker build -t hadoop-master-python .
```

### 2. Subir o cluster Hadoop

```bash
docker compose up -d
```

### 3. Verificar containers

```bash
docker ps
```

---

## 📥 Preparação dos Dados

### Copiar arquivos para o container

```bash
docker cp u.data hadoop-master:/tmp/u.data
docker cp u.item hadoop-master:/tmp/u.item
docker cp analise_filmes.py hadoop-master:/tmp/analise_filmes.py
```

### Criar diretório no HDFS

```bash
docker exec -it hadoop-master hdfs dfs -mkdir -p /data/movielens
```

### Enviar dataset para o HDFS

```bash
docker exec -it hadoop-master hdfs dfs -put /tmp/u.data /data/movielens/
```

---

## 🚀 Execução do MapReduce

### Remover saída anterior

```bash
docker exec -it hadoop-master hdfs dfs -rm -r /data/output_final
```

### Executar o job

```bash
docker exec -it hadoop-master hadoop jar \
  /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
  -input /data/movielens/u.data \
  -output /data/output_final \
  -mapper "python3 /tmp/analise_filmes.py --mapper" \
  -reducer "python3 /tmp/analise_filmes.py --reducer"
```

---

## 📊 Visualização dos Resultados

```bash
docker exec -it hadoop-master hdfs dfs -cat /data/output_final/part-00000 | more
```

**Exemplo de saída:**

```
1    Toy Story (1995)    3.88    5.0    452
100  Fargo (1996)        4.16    5.0    508
```

---

## 🔍 Lógica do Processamento

### Mapper
- Extrai pares `(ID do filme, nota)`

### Reducer
- Agrupa por filme
- Calcula:
  - Média das avaliações
  - Nota máxima
  - Quantidade de avaliações
- Associa o nome do filme via `u.item`

---

## 📈 Análise dos Dados

- Filmes com maior número de avaliações apresentam resultados mais confiáveis
- Filmes com poucas avaliações podem ter médias altas, porém com baixa significância estatística
- Alguns filmes aparecem como **"Desconhecido"**, devido à ausência de correspondência no arquivo `u.item`

---

## 🏁 Conclusão

O uso do Hadoop permitiu o processamento eficiente de dados em larga escala. A abordagem com MapReduce possibilitou a extração de métricas importantes e o enriquecimento dos dados, tornando a análise mais completa e significativa.

---

## 🌐 Interface Web do Hadoop

A interface web pode ser acessada em:

```
http://localhost:9870
```

---

## 📌 Observação Final

Esta atividade demonstra na prática conceitos fundamentais de:

- Processamento distribuído
- Engenharia de Dados
- Análise estatística em larga escala
