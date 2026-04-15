import re

# Database for Lab Values
LAB_DB = {
    "BILIRUBIN": {"range": (0.1, 1.2), "unit": "mg/dL", "condition": "Jaundice"},
    "WBC": {"range": (4500, 11000), "unit": "cells/mcL", "condition": "Infection/Fever"},
    "CRP": {"range": (0, 10), "unit": "mg/L", "condition": "Inflammation"},
    "SGPT/ALT": {"range": (7, 55), "unit": "U/L", "condition": "Liver Health"},
}

def analyze_complex_report(text):
    text_lower = text.lower()
    findings, alerts, suggestions = [], [], []
    
    # 1. Check Lab Values (Jaundice/Fever)
    for marker, info in LAB_DB.items():
        pattern = rf"{marker.lower()}.*?(\d+\.?\d*)"
        match = re.search(pattern, text_lower)
        if match:
            val = float(match.group(1))
            low, high = info["range"]
            if val > high:
                alerts.append(f"HIGH {marker}: {val} {info['unit']}")
                if info['condition'] == "Jaundice":
                    suggestions.append("High Bilirubin detected. Avoid oily food and check for yellowing of eyes/skin.")
                if info['condition'] == "Infection/Fever":
                    suggestions.append("High WBC suggests the body is fighting an infection. Monitor temperature.")

    # 2. Keyword Detection (Cough/MRI/General)
    symptom_keywords = {
        "consolidation": "Potential Pneumonia/Lung infection (often linked to Cough).",
        "infiltration": "Fluid in lungs, common in severe Cough/Bronchitis.",
        "infarct": "Evidence of tissue death due to blood loss (Stroke risk).",
        "ischaemic": "Restricted blood flow to brain/heart.",
        "microbleeds": "Chronic small hemorrhages detected."
    }

    for key, desc in symptom_keywords.items():
        if key in text_lower:
            alerts.append(f"CRITICAL TERM: {key.upper()}")
            findings.append(desc)

    # 3. Contextual Diagnosis (The "Project" Intelligence)
    if "fever" in text_lower or "wbc" in str(alerts).lower():
        suggestions.append("Stay hydrated and rest. If fever persists >101°F, consult a doctor.")
    
    if "cough" in text_lower or "consolidation" in text_lower:
        suggestions.append("Respiratory distress noted. Chest X-ray or Pulmonologist visit advised.")

    # Final Summary
    if alerts:
        summary = "⚠️ Potential health issues detected requiring medical attention."
    else:
        summary = "✅ No critical biomarkers or pathological keywords were detected."

    return summary, findings, alerts, suggestions