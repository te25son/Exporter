import httpx
import json

from exporter import settings
from .xml.exporter import InvoiceExporter


class ExportComponent:
    """
    Component that acts a separator between the view and the logic.
    Deals specificaly with logic related to exporting.
    """

    @staticmethod
    def try_export(queue_id: str, annotation_id: str) -> bool:
        """
        Main export function used by the /export endpoint.
        Using the validated queue and annotation ids (currently only
        validated as positive integers), will attempt to get a
        valid response from the export endpoint in the settings.

        If a valid response is received, it will then attempt to covert
        the response to a new XML format and again convert the new XML
        to a byte64 string.

        The byte64 string is then json serialized along with the annotation id,
        and both are passed to the post endpoint in settings.

        If all goes well, the method will return True. If any erros occur, it
        will return False.
        """
        try:
            endpoint = f"{settings.EXPORT_GET_ENDPOINT_BASE}{queue_id}{settings.EXPORT_GET_ENDPOINT_END}"
            get_params = {"format": "xml", "id": annotation_id}

            with httpx.Client(
                auth=(settings.API_USERNAME, settings.API_PASSWORD), params=get_params
            ) as client:
                response = client.get(endpoint)

            if not response.status_code == 200:
                raise Exception(
                    f"Response status code was not correct. Expected 200 but was {response.status_code}."
                )

            invoice_content = (
                InvoiceExporter(response.content).create_export_xml().decode()
            )
            post_params = json.dumps(
                {"annotaionId": annotation_id, "content": invoice_content}
            )

            # with httpx.Client(params=post_params) as client:
            #     client.post(settings.EXPORT_POST_ENDPOINT)

            return True

        except Exception as ex:
            return False
