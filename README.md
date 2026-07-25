# EvidenceLab

EvidenceLab är ett portfolio projekt för dokumentsökning och utvärdering av retrieval system.

Projektet:

- delar dokument i ord-baserade chunks
- räknar ordfrekvenser
- jämför chunks med en fråga genom cosinuslikhet
- returnerar de mest relevanta chunkarna i rankad ordning
- erbjuder retrieval genom både terminalen och ett REST API
- utvärderar flera sökningar med två metrics: Hit Rate och Mean Reciprocal Rank (MRR)

## Starta programmet

Aktivera den virtuella miljön och kör följande från projektmappen i PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m evidence_lab.main
```

Exempel på inmatning:

```text
Document: katt sover hund springer
Query: hund
Chunk size: 2
Number of Chunks: 1
Most relevant chunks: ['hund springer']
```

## Starta REST-API:t

Kör följande från projektmappen i PowerShell:

```powershell
.\.venv\Scripts\python.exe -m uvicorn evidence_lab.api:app --app-dir src --reload
```

API:t är sedan tillgängligt på:

- http://127.0.0.1:8000
- interaktiv dokumentation: http://127.0.0.1:8000/docs

Här skapar vi ett PowerShell objekt med "document", "query", "chunk_size" och "num_chunks". Sedan omvandlar vi objektet till JSON format.

```powershell
$body = @{
    document = "katt sover hund springer"
    query = "hund"
    chunk_size = 2
    num_chunks = 1
} | ConvertTo-Json
```

Sedan skickar vi JSON till POST /retrieve med Invoke-RestMethod.

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/retrieve" `
    -ContentType "application/json" `
    -Body $body
```

När man kör följande kod får man:

```text
best_chunks
-----------
{hund springer}
```

Här skapar vi ett Powershell objekt med "document", "queries", "relevant_chunks", "chunk_size" och "num_chunks", för att sedan omvandla det till JSON-format. Endpointen kör flera queries mot samma dokument och sammanfattar kvaliten på retrievalen vi utför med 2 metrics, Hit Rate och Mean Reciprocal Rank (MRR).

```powershell
$evaluationBody = @{
    document = "hund springer katt sover"
    queries = @("hund", "katt")
    relevant_chunks = @("hund springer", "katt sover")
    chunk_size = 2
    num_chunks = 1
} | ConvertTo-Json
```

Sedan skickar vi JSON till POST /evaluate med Invoke-RestMethod.

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/evaluate" `
    -ContentType "application/json" `
    -Body $evaluationBody |
    ConvertTo-Json
```

När man kör följande kod får man:

```json
{
  "hit_rate": 1.0,
  "mean_reciprocal_rank": 1.0
}
```

## Köra tester

```powershell
python -m pytest
```

## Teknikval

- **FastAPI** används för att ta emot och validera HTTP-anrop med JSON.
- **Uvicorn** kör FastAPI-applikationen som en lokal webbserver.
- **HTTPX2** används av API-testerna för att skicka testanrop utan att starta
  servern manuellt.

Projektet använder dessa små, avgränsade verktyg i stället för ett större
webbramverk. Retrieval logiken förblir vanlig Python och kan användas utan API:t.
