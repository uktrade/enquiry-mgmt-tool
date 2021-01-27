from app.enquiries.utils import str2bool


def create_consent_update_task(data: dict):
    """
    Utility function to create consent update tasks from passed dictionary of data.

    :param data:
    {
        "email": "test@local.host",
        "phone": "+112222333444",
        "email_consent": "true",
        "phone_consent": "true",
    }
    """
    from app.enquiries import tasks

    email = data.get("email") or None
    phone = data.get("phone") or None
    email_consent = str2bool(data.get("email_consent"))
    phone_consent = str2bool(data.get("phone_consent"))

    if email:
        tasks.update_enquirer_consents.apply_async(kwargs={"key": email, "value": email_consent})
    if phone:
        tasks.update_enquirer_consents.apply_async(kwargs={"key": phone, "value": phone_consent})
