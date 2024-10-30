from redactor import Redactor

def test_redact_names():
    # Testing the redaction of names, with sample name "Meghana Sairam"
    text = "Meghana Sairam attended the conference."
    redactor = Redactor()
    doc = redactor.nlp(text)
    redacted_doc = redactor.redact_names(doc)
    assert "Meghana" not in redacted_doc.text
    assert "Sairam" not in redacted_doc.text
    assert "attended the conference" in redacted_doc.text
