import pytest
from redactor import Redactor

@pytest.fixture(scope="session")
def redactor():
    return Redactor()

def test_redact_dates(redactor):
    text = "The event is on April 20, 2022."
    doc = redactor.nlp(text)
    redacted_doc = redactor.redact_dates(doc)
    assert "April 20, 2022" not in redacted_doc.text
    assert "The event is on" in redacted_doc.text

def test_redact_phones(redactor):
    text = "Call me at 123-456-7890 or (987) 654-3210."
    doc = redactor.nlp(text)
    redacted_doc = redactor.redact_phones(doc)
    assert "123-456-7890" not in redacted_doc.text
    assert "(987) 654-3210" not in redacted_doc.text

def test_redact_address(redactor):
    text = "Mothish lives in New York City."
    doc = redactor.nlp(text)
    redacted_doc = redactor.redact_address(doc)
    assert "New York City" not in redacted_doc.text
    assert "Mothish lives in" in redacted_doc.text

def test_redact_concepts(redactor):
    text = "Praneeth discussed important topics about children."
    doc = redactor.nlp(text)
    redacted_doc = redactor.redact_concepts(doc, ["children"])
    assert "Praneeth discussed important topics about children" not in redacted_doc.text
