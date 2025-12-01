# Architecture Diagram

To generate the architecture diagram, you can use tools like:

1. **Draw.io** (https://app.diagrams.net/)
2. **Mermaid** (included below)
3. **Lucidchart**
4. **Excalidraw**

## Mermaid Diagram Code
```mermaid
graph TD
    User[User] -->|Policy + Document| Orchestrator[Orchestrator Agent]
    
    Orchestrator -->|Policy Text| PolicyExtractor[Policy Extractor Agent]
    PolicyExtractor -->|Structured Requirements| Orchestrator
    
    Orchestrator -->|Document + Requirements| Scanner[Document Scanner Agent]
    Scanner -->|Violation List| Orchestrator
    
    Orchestrator -->|Each Violation| Analyzer[Violation Analyzer Agent]
    Analyzer -->|Severity + Remediation| Orchestrator
    
    Orchestrator -->|CRITICAL/HIGH Violations| Rewriter[Rewrite Agent]
    Rewriter -->|Compliant Rewrites| Orchestrator
    
    Orchestrator -->|Final Report| User
    
    style Orchestrator fill:#667eea,stroke:#333,stroke-width:3px,color:#fff
    style PolicyExtractor fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
    style Scanner fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
    style Analyzer fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
    style Rewriter fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
```

## To Generate PNG

1. Copy the Mermaid code above
2. Go to https://mermaid.live/
3. Paste the code
4. Download as PNG
5. Save as `architecture_diagram.png` in this directory
````