# EvidenceLab

EvidenceLab är ett stegvis portfolio-projekt för att lära sig bygga och
utvärdera system för dokumentsökning och RAG.

Den första versionen är en liten Python-applikation utan ramverk. Den:

- delar ett dokument i ord-baserade chunks
- räknar ordens förekomster
- jämför varje chunk med en fråga med cosinuslikhet
- returnerar den mest relevanta chunken

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
Most relevant chunk: hund springer
```

## Köra tester

```powershell
python -m pytest
```
