import base64

from dataclasses import dataclass
from xml.etree.ElementTree import Element, SubElement, tostring


@dataclass
class XMLElement:
    """
    Helper class that allows us to more concisely set the value
    of elements.

    Using the helper we're able to set an element in the following
    way:

    >>> sample = XMLElement(Element("sample"))
    >>> sample.element.set_text("some text")

    The alternative without this helper is:

    >>> sample = Element("sample")
    >>> sample.text = "some text"
    """
    element: Element

    def set_text(self, text: str | None = None) -> None:
        self.element.text = text

    def add_sub_element(self, tag: str) -> 'XMLElement':
        return XMLElement(SubElement(self.element, tag))


# fmt: off
@dataclass
class Invoice:
    """
    Sets up the XML structure to be used for conversion.
    """
    root: XMLElement = XMLElement(Element("InvoiceRegisters"))
    invoices: XMLElement = root.add_sub_element("Invoices")
    payable: XMLElement = invoices.add_sub_element("Payable")
    invoice_number: XMLElement = payable.add_sub_element("InvoiceNumber")
    invoice_date: XMLElement = payable.add_sub_element("InvoiceDate")
    due_date: XMLElement = payable.add_sub_element("DueDate")
    total_amount: XMLElement = payable.add_sub_element("TotalAmount")
    notes: XMLElement = payable.add_sub_element("Notes")
    iban: XMLElement = payable.add_sub_element("Iban")
    amount: XMLElement = payable.add_sub_element("Amount")
    currency: XMLElement = payable.add_sub_element("Currency")
    vendor: XMLElement = payable.add_sub_element("Vendor")
    vendor_address: XMLElement = payable.add_sub_element("VendorAddress")
    details: XMLElement = payable.add_sub_element("Details")

    def to_byte_string(self) -> bytes:
        return base64.b64encode(tostring(self.root.element, encoding='utf8', method='xml'))


class InvoiceDetail():
    """
    Sets up the XML detail structure to be used for conversion.
    """
    def __init__(self, detail_element: XMLElement) -> None:
        self.detail: XMLElement = detail_element
        self.amount: XMLElement = self.detail.add_sub_element("Amount")
        self.account_id: XMLElement = self.detail.add_sub_element("AccountId")
        self.quantity: XMLElement = self.detail.add_sub_element("Quantity")
        self.notes: XMLElement = self.detail.add_sub_element("Notes")
# fmt: on
