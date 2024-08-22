from typing import Iterable, List, Tuple
import xml.etree.ElementTree as ET

def load_doc(data: str) -> ET.Element:
    return ET.fromstring(data)

def find_currency_rates(data: str, currency: Iterable) -> List[Tuple[str, str, str]]:
    doc = load_doc(data)
    result = []
    for element in doc.findall(f'./Valute'):
        char_code = element.find('CharCode').text
        if char_code in currency:
            result.append((char_code, element.find('Name').text, element.find('Value').text))

    return result
