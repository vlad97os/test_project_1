import re
from pypdf import PdfReader
import pytest

reference_file_path = 'test_task.pdf'
verifiable_file_path = 'test_task1.pdf'


@pytest.fixture
def converter_pdf_to_dictionary(request):
    pdf_path = request.param
    file = PdfReader(pdf_path)
    page = file.pages
    text = page[0].extract_text()
    dictionary_from_file = {}
    regular_pattern = r"([^\n:]+)\s*:\s*(.*)"
    characteristics = re.findall(regular_pattern, text)
    for characteristic in characteristics:
        key = characteristic[0].strip()
        value = characteristic[1].strip()
        dictionary_from_file[key] = value
    return dictionary_from_file


@pytest.mark.parametrize('converter_pdf_to_dictionary', [reference_file_path], indirect=True)
def test_pdf_file(converter_pdf_to_dictionary, request):
    reference_dictionary = request.getfixturevalue('converter_pdf_to_dictionary')
    request.param = verifiable_file_path
    verifiable_dictionary = request.getfixturevalue('converter_pdf_to_dictionary')
    assert list(reference_dictionary.keys()) == list(verifiable_dictionary.keys())[:len(reference_dictionary)]
