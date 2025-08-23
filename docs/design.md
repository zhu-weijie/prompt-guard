# PromptGuard Design Documentation

This document contains a series of diagrams that describe the architecture, data flow, and user interaction of the PromptGuard application. The diagrams are generated using Mermaid.

## 1. Class Diagram

This diagram shows the main classes in the `prompt_guard` application and their relationships. It highlights the modular design, where the `PromptAnalyzer` uses a collection of `Detector` classes to perform its analysis.

```mermaid
classDiagram
    direction LR

    class PromptAnalyzer {
        - _detectors: list~Detector~
        + analyze(prompt: str): AnalysisResult
    }

    class Detector {
        <<interface>>
        + run(prompt: str): Iterator~Vulnerability~
    }

    class MarkdownImageExfiltrationDetector {
        + run(prompt: str): Iterator~Vulnerability~
    }
    class DnsExfiltrationDetector {
        + run(prompt: str): Iterator~Vulnerability~
    }
    class ConfigFileWriteDetector {
        + run(prompt: str): Iterator~Vulnerability~
    }
    class InvisibleCharacterDetector {
        + run(prompt: str): Iterator~Vulnerability~
    }

    class schemas {
        <<module>>
    }

    class AnalysisResult {
        <<Pydantic Model>>
        + vulnerabilities: list~Vulnerability~
    }

    class Vulnerability {
        <<Pydantic Model>>
        + category: str
        + description: str
        + confidence: float
    }

    PromptAnalyzer o-- "1..*" Detector : uses
    Detector <|-- MarkdownImageExfiltrationDetector
    Detector <|-- DnsExfiltrationDetector
    Detector <|-- ConfigFileWriteDetector
    Detector <|-- InvisibleCharacterDetector

    %% --- Refinement: Added a dependency from Detector to Vulnerability ---
    Detector ..> Vulnerability : creates

    PromptAnalyzer ..> AnalysisResult : creates
    AnalysisResult "1" -- "0..*" Vulnerability : contains

    schemas ..> AnalysisResult
    schemas ..> Vulnerability
```

---

## 2. C4 Component Diagram

The C4 model helps to visualize the software architecture at different levels of detail. A Component Diagram is perfect for showing the major building blocks of the `PromptGuard` system.

```mermaid
C4Component
    title Component Diagram for PromptGuard

    Container(web_browser, "Web Browser", "HTML, CSS, JavaScript", "The client-side user interface for submitting prompts.")

    Container_Boundary(api_container, "PromptGuard API Container") {
        Component(fastapi_app, "FastAPI Web Server", "Python", "Handles HTTP requests, serves the UI, and provides the /analyze endpoint.")
        Component(analyzer, "Prompt Analyzer", "Python", "Orchestrates the analysis by invoking all registered detectors.")
        Component(detectors, "Detector Modules", "Python", "A collection of modules, each responsible for finding a specific type of vulnerability.")
    }

    Rel(web_browser, fastapi_app, "Makes API calls to /analyze", "HTTPS")
    Rel(fastapi_app, analyzer, "Calls analyze() method")
    Rel(analyzer, detectors, "Invokes run() on each detector")
```

---

## 3. Sequence Diagram

This diagram illustrates the sequence of interactions that occur when a user submits a prompt for analysis, from the web browser to the individual detectors.

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant FastAPI
    participant PromptAnalyzer
    participant Detectors

    User->>Browser: Enters prompt and clicks "Analyze"
    Browser->>FastAPI: POST /analyze with prompt JSON
    activate FastAPI
    FastAPI->>PromptAnalyzer: analyze(prompt)
    activate PromptAnalyzer

    %% --- Refinement: Using a loop fragment to be more explicit ---
    loop for each detector
        PromptAnalyzer->>Detectors: run(prompt)
        activate Detectors
        Detectors-->>PromptAnalyzer: Yields found vulnerabilities
        deactivate Detectors
    end

    PromptAnalyzer-->>FastAPI: Returns AnalysisResult object
    deactivate PromptAnalyzer
    FastAPI-->>Browser: Responds with JSON of vulnerabilities
    deactivate FastAPI
    Browser->>User: Renders formatted results
```

---

## 4. User Journey Map

This diagram provides a high-level overview of the user's experience, from discovering the tool to understanding the results of their prompt analysis.

```mermaid
journey
    title User Journey for Prompt Analysis
    section Discovery and Usage
      User wants to check a prompt for security risks: 5: User
      Opens the PromptGuard URL in a browser: 5: User
      Pastes a potentially malicious prompt into the text area: 5: User
      Clicks the "Analyze" button: 5: User
    section Analysis and Results
      The UI shows an "Analyzing..." message: 4: System
      The results are displayed in formatted cards: 5: System
      User reads the detected vulnerabilities and their descriptions: 5: User
      User decides to modify the prompt based on the feedback: 5: User
```

---

## 5. State Diagram

A State Diagram is useful for objects with complex, defined states. In our application, the `PromptAnalyzer` itself is stateless (it doesn't change based on previous requests). However, we can model the state of the *UI* during the analysis process.

```mermaid
stateDiagram-v2
    direction LR
    [*] --> Idle
    Idle --> Analyzing: User clicks "Analyze"
    Analyzing --> ResultsDisplayed: API call succeeds
    Analyzing --> Error: API call fails
    ResultsDisplayed --> Idle: User enters new prompt
    Error --> Idle: User dismisses error
```
