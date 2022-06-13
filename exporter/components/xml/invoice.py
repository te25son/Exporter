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


# fmt: off
@dataclass
class Invoice:
    """
    Sets up the XML structure to be used for conversion.
    """
    root: XMLElement = XMLElement(Element("InvoiceRegisters"))
    invoices: XMLElement = XMLElement(SubElement(root.element, "Invoices"))
    payable: XMLElement = XMLElement(SubElement(invoices.element, "Payable"))
    invoice_number: XMLElement = XMLElement(SubElement(payable.element, "InvoiceNumber"))
    invoice_date: XMLElement = XMLElement(SubElement(payable.element, "InvoiceDate"))
    due_date: XMLElement = XMLElement(SubElement(payable.element, "DueDate"))
    total_amount: XMLElement = XMLElement(SubElement(payable.element, "TotalAmount"))
    notes: XMLElement = XMLElement(SubElement(payable.element, "Notes"))
    iban: XMLElement = XMLElement(SubElement(payable.element, "Iban"))
    amount: XMLElement = XMLElement(SubElement(payable.element, "Amount"))
    currency: XMLElement = XMLElement(SubElement(payable.element, "Currency"))
    vendor: XMLElement = XMLElement(SubElement(payable.element, "Vendor"))
    vendor_address: XMLElement = XMLElement(SubElement(payable.element, "VendorAddress"))
    details: XMLElement = XMLElement(SubElement(payable.element, "Details"))

    def to_byte_string(self) -> bytes:
        return base64.b64encode(tostring(self.root.element, encoding='utf8', method='xml'))


class InvoiceDetail():
    """
    Sets up the XML detail structure to be used for conversion.
    """
    def __init__(self, detail_element: XMLElement) -> None:
        self.detail: XMLElement = detail_element
        self.amount: XMLElement = XMLElement(SubElement(self.detail.element, "Amount"))
        self.account_id: XMLElement = XMLElement(SubElement(self.detail.element, "AccountId"))
        self.quantity: XMLElement = XMLElement(SubElement(self.detail.element, "Quantity"))
        self.notes: XMLElement = XMLElement(SubElement(self.detail.element, "Notes"))
# fmt: on
