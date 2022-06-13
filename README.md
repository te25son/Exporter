### Exporter App 🚀

Recording of the app in action. To avoid showing secret data, the demo only uses users without privileges to export.

https://user-images.githubusercontent.com/39095798/173402737-ef557587-c4a4-44c4-a4fd-462a506c05f4.mov


To set this up locally, you'll need a new `.env` file and to set up some particular env vars. Here's the rundown:

FLASK_APP = location of the main app. In this case "exporter/app.py"

SECRET_KEY = 🙊

DATABASE_URI = ulr of database to be used. Currently the app only supports simple sqlite databases.

DEBUG = :bug::gun:

HASH = encryption method to be used when hashing passwords, e.g. sha256

DUMMY_ADMIN_USERNAME = username of user to automatically be added to the database upon creation. Will have export rights (sort of).

DUMMY_ADMIN_PASSWORD = the users password

API_USERNAME = username for authentication to the main endpoint

API_PASSWORD = password of user for authentication to the main endpoint

EXPORT_GET_ENDPOINT_BASE = base of the main endpoint

EXPORT_GET_ENDPOINT_END = end of the main endpoint

If it helps, the endpoint is constructed in the following way:

```py
endpoint = f"{settings.EXPORT_GET_ENDPOINT_BASE}{user defined queue id}{settings.EXPORT_GET_ENDPOINT_END}"
```

EXPORT_POST_ENDPOINT = endpoint for the final converted content to be posted to

VALID_ANNOTATION_ID = a valid annotation id (used for testing)

VALID_QUEUE_ID = a valid queue id (used for testing)
