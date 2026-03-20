# Directive: TruthLens - Misinformation Detection System

## Objective
Build an AI system that detects misinformation from messy real-world inputs and provides actionable insights.

## Inputs
- **Image**: e.g., WhatsApp forward screenshots, memes with text, photos of documents.
- **Text**: e.g., news headlines, social media posts, direct claims.
- **Voice**: (Optional) audio clips converted to text via speech-to-text.

## Outputs
A structured JSON response containing:
- **Truth score**: Numeric representation from 0 (completely false) to 100 (verifiably true).
- **Claim summary**: A clear, concise restatement of the core claim being analyzed.
- **Verdict**: Categorical classification (True / Misleading / False / Unverifiable).
- **Explanation**: A short paragraph explaining the reasoning behind the verdict.
- **Supporting fact-check insights**: Bullet points providing context, sources, or factual corrections.
- **Confidence level**: Categorical classification of how confident the system is in its assessment (High, Medium, Low).

## Constraints
- **Infrastructure**: Must strictly use Google services (Gemini for reasoning/parsing, Firebase for storage/hosting).
- **Deployment**: Must be fully deployable as a cloud-based service (e.g., Cloud Functions or Cloud Run).
- **Architecture**: Must follow a 3-layer architecture (Directive, Orchestration, Execution).
- **Code Quality**: Must be modular, independent, testable components.

## Edge Cases
- **No clear claim**: The input is an opinion, greeting, or nonsense string. (Should return Unverifiable/Not Applicable verdict).
- **Image text not readable**: Low resolution, corrupted images, or heavily obscured text. (Should return an error or prompt for clearer input).
- **Ambiguous claims**: Claims that mix truth and falsehood, or rely on missing context. (Should be marked as Misleading with a nuanced explanation).
- **No reliable sources found**: Search or fact-checking APIs return zero relevant context. (Should be marked as Unverifiable with low confidence).
