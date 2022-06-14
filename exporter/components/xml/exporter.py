from datetime import datetime
from typing import Dict, List
from xml.etree.ElementTree import Element, ParseError, fromstring, SubElement
from .invoice import Invoice, InvoiceDetail, XMLElement


class InvoiceExporter:
    def __init__(self, response_content: bytes) -> None:
        try:
            self.content = fromstring(response_content)
        except ParseError as e:
            raise Exception(f"Invalid xml content. Unable to parse. {e.msg}")

        self.datapoints = self._get_datapoint_text_by_schema_ids(self.content)
        self.detail_items = self._get_detail_items()

    def create_export_xml(self) -> bytes:
        """
        Sets the text values of all elements in the Invoice class.
        Returns the invoice as a byte string.
        """
        invoice = Invoice()

        # fmt: off
        invoice.invoice_number.set_text(self._get_datapoint_value("document_id"))
        invoice.invoice_date.set_text(self._get_datapoint_value("date_issue"))
        invoice.due_date.set_text(self._get_datapoint_value("date_due"))
        invoice.total_amount.set_text(self._get_datapoint_value("amount_total"))
        invoice.notes.set_text(self._get_datapoint_value("notes"))
        invoice.iban.set_text(self._get_datapoint_value("iban"))
        invoice.amount.set_text(self._get_datapoint_value("amount_total_base"))
        invoice.currency.set_text(self._get_datapoint_value("currency"))
        invoice.vendor.set_text(self._get_datapoint_value("sender_name"))
        invoice.vendor_address.set_text(self._get_datapoint_value("sender_address"))

        for item in self.detail_items:
            detail = InvoiceDetail(detail_element=XMLElement(SubElement(invoice.details.element, "Detail")))

            detail.amount.set_text(item.get("item_total_base"))
            detail.account_id.set_text()
            detail.quantity.set_text(item.get("item_quantity"))
            detail.notes.set_text(item.get("item_description"))
        # fmt: on

        return invoice.to_byte_string()

    def _get_detail_items(self) -> List[Dict[str, str | None]]:
        """
        Gets all line items to be used as detail items in the xml conversion
        as a list of dictionaries.

        The line items are found in the content's tuple elements. If no
        tuple elements are found, and/or if no tuple elements contain a
        schema_id equal to line_item, and empty list is returned.
        """
        return [
            self._get_datapoint_text_by_schema_ids(tuple_element)
            for tuple_element in self.content.iter("tuple")
            if tuple_element.attrib.get("schema_id") == "line_item"
        ]

    def _get_datapoint_value(self, key: str) -> str | None:
        """
        Gets the value of the datapoint using the given key.
        If no key is found, returns None.
        """
        return self.datapoints.get(key)

    def _get_datapoint_date_value(self, key: str) -> str | None:
        """
        Gets the value of the datapoint using the given key. Converts
        the value (if present) into a valid ISO 8601 datetime string.
        Otherwise returns None.
        """
        to_iso = lambda d: datetime.strptime(d, "%Y-%m-%d").isoformat()
        return to_iso(date) if (date := self._get_datapoint_value(key)) else None

    @staticmethod
    def _get_datapoint_text_by_schema_ids(element: Element) -> Dict[str, str | None]:
        """
        Gets all datapoint elements in the given element and creates a
        dictionary using the datapoint's schema_id as the key and
        the datapoint's text as a value.

        If no datapoints are found, and/or if no datapoints contain
        a schema_id, an empty dictionary will be returned.
        """
        return {
            schema_id: datapoint.text
            for datapoint in element.iter("datapoint")
            if (schema_id := datapoint.attrib.get("schema_id")) is not None
        }
