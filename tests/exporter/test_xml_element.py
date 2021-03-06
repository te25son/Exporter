import pytest

from xml.etree.ElementTree import Element, fromstring, tostring
from exporter.components.xml.invoice import XMLElement
from exporter.components.xml.exporter import InvoiceExporter


class TestElements:
    # fmt: off
    @pytest.fixture
    def valid_xml(self) -> bytes:
        return b"""<?xml version="1.0" encoding="utf-8"?>
        <result>
            <datapoint schema_id="id">12345</datapoint>
            <datapoint>No schema id here</datapoint>
            <tuple schema_id="line_item">
                <datapoint schema_id="first_name">First</datapoint>
                <datapoint schema_id="last_name">Last</datapoint>
            </tuple>
            <tuple schema_id="line_item">
                <datapoint schema_id="age">55</datapoint>
            </tuple>
            <tuple schema_id="line_item">
                <datapoint schema_id="number">123456789</datapoint>
                <datapoint schema_id="no_text"></datapoint>
                <datapoint>No schema id here either</datapoint>
            </tuple>
            <tuple>
                <datapoint schema_id="birth_date">1990-03-31</datapoint>
                <datapoint schema_id="birth_date_invalid">1990-03-31T00:00:00</datapoint>
            </tuple>
        </result>
        """

    @pytest.fixture
    def valid_multi_element(self, valid_xml) -> Element:
        return fromstring(valid_xml)

    @pytest.fixture
    def xml_element(self) -> XMLElement:
        return XMLElement(Element("New"))

    @pytest.fixture
    def exporter(self, valid_xml: bytes) -> InvoiceExporter:
        return InvoiceExporter(valid_xml)

    def test_can_create_xml_element_from_existing_element(self, valid_multi_element: Element):
        assert XMLElement(valid_multi_element).element == valid_multi_element

    def test_can_create_xml_element_from_new_element(self):
        assert XMLElement(new_element := Element("New")).element == new_element

    def test_can_add_sub_element(self, xml_element: XMLElement):
        assert xml_element.add_sub_element("Sub").element.tag == "Sub"

    def test_can_set_element_text(self, xml_element: XMLElement):
        xml_element.set_text(text := "Sample")
        assert xml_element.element.text == text

    def test_can_set_text_from_dictionary(self, xml_element: XMLElement, exporter: InvoiceExporter):
        (first_name := xml_element.add_sub_element("FirstName")).set_text(first_name_text := exporter._get_datapoint_value("first_name"))
        (last_name := xml_element.add_sub_element("LastName")).set_text(last_name_text := exporter._get_datapoint_value("last_name"))
        (birth_date := xml_element.add_sub_element("BirthDate")).set_text(birth_date_text := exporter._get_datapoint_date_value("birth_date"))
        (birth_date_invalid := xml_element.add_sub_element("BirthDateInvalid")).set_text(birth_date_invalid_text := exporter._get_datapoint_date_value("birth_date_invalid"))

        byte_string = tostring(xml_element.element, encoding='utf8', method='xml')

        assert first_name.element.text == first_name_text
        assert last_name.element.text == last_name_text
        assert birth_date.element.text == birth_date_text
        assert birth_date_invalid.element.text == birth_date_invalid_text
        assert byte_string == b"<?xml version='1.0' encoding='utf8'?>\n<New><FirstName>First</FirstName><LastName>Last</LastName><BirthDate>1990-03-31T00:00:00</BirthDate><BirthDateInvalid /></New>"

    def test_invoice_exporter(self, exporter: InvoiceExporter):
        assert exporter.datapoints == {
            'id': '12345',
            'first_name': 'First',
            'last_name': 'Last',
            'age': '55',
            'number': '123456789',
            'no_text': None,
            'birth_date': '1990-03-31',
            'birth_date_invalid': '1990-03-31T00:00:00'
        }
        assert exporter.detail_items == [
            {'first_name': 'First', 'last_name': 'Last'},
            {'age': '55'},
            {'number': '123456789', 'no_text': None}
        ]
    # fmt: on
