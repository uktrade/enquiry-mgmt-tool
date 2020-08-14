import random
import requests_mock

from datetime import datetime
from django.conf import settings
from django.forms.models import model_to_dict
from django.test import TestCase
from faker import Faker

from app.enquiries.models import Enquiry, Enquirer
from app.enquiries.common.as_utils import fetch_and_process_enquiries

faker = Faker()

# relevant table from the complete html body
table_template = """
<p>See below for your submitted form:</p>
<div class="form-table">
    <table>
        <tr>
            <td>Given name</td>
            <td>{first_name}</td>
        </tr>

        <tr>
            <td>Family name</td>
            <td>{last_name}</td>
        </tr>

        <tr>
            <td>Job title</td>
            <td>CEO</td>
        </tr>

        <tr>
            <td>Email address</td>
            <td>{email}</td>
        </tr>

        <tr>
            <td>Phone number</td>
            <td>{phone}</td>
        </tr>

        <tr>
            <td>Company name</td>
            <td>{company_name}</td>
        </tr>

        <tr>
            <td>Company website</td>
            <td>https://example.com</td>
        </tr>

        <tr>
            <td>Company HQ address</td>
            <td>Far, far away</td>
        </tr>

        <tr>
            <td>Country</td>
            <td>US</td>
        </tr>

        <tr>
            <td>Industry</td>
            <td>AEROSPACE</td>
        </tr>

        <tr>
            <td>
                Which of these best describes how you feel about expanding to the UK?
            </td>
            <td>I’m still exploring where to expand my business and would like to know more about\
 the UK’s offer.</td>
        </tr>

        <tr>
            <td>Tell us about your investment</td>
            <td>This is a test message sent via automated tests</td>
        </tr>

        <tr>
            <td>Would you like to arrange a call?</td>
            <td>{arrange_call}</td>
        </tr>

        <tr>
            <td>When should we call you?</td>
            <td></td>
        </tr>

        <tr>
            <td>How did you hear about us?</td>
            <td>LinkedIn</td>
        </tr>

        <tr>
            <td>I would like to receive additional information by email</td>
            <td>{email_consent}</td>
        </tr>

        <tr>
            <td>
                I would like to receive additional information by telephone
            </td>
            <td>{phone_consent}</td>
        </tr>
    </table>
</div>

"""


def get_enquiries_data():
    response = {"hits": {"hits": []}}
    details = []
    for i in range(3):
        item = {
            "_source": {
                "object": {
                    "submission_data": {"html_body": ""},
                    "url": "/international/invest/contact/",
                    "published": datetime.now().isoformat(),
                }
            },
            "sort": [12345, "submission_type"],
        }

        arrange_call = random.choice(["yes", "no", "yes", "yes", "no", "yes"])
        email_consent = random.choice(["True", "False", "False", "True", "True", "True"])
        phone_consent = random.choice(["True", "False", "False", "True", "True", "True"])
        detail = {
            "company_name": faker.company(),
            "first_name": faker.name(),
            "last_name": faker.name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "arrange_call": arrange_call,
            "email_consent": email_consent,
            "phone_consent": phone_consent,
            "skip": False,
        }
        html_body = table_template.format(**detail)
        item["_source"]["object"]["submission_data"]["html_body"] = html_body
        # make one item with incorrect url so that it gets skipped
        if i == 1:
            item["_source"]["object"]["url"] = "/international/trade/contact/"
            detail["skip"] = True

        response["hits"]["hits"].append(item)
        details.append(detail)

    return response, details


class ActivityStreamIntegrationTests(TestCase):
    def test_fetch_new_enquiries(self):
        """
        Test that fetches sample enquiries data, parses them and creates
        Enquiry objects and asserts data matches with input data

        Checks that for enquiries which come through activity stream the
        date_received field is populated with the date of creation.
        """
        with requests_mock.Mocker() as m:
            url = settings.ACTIVITY_STREAM_SEARCH_URL
            data, details = get_enquiries_data()
            m.get(url, json=data)

            self.assertEqual(Enquiry.objects.count(), 0)
            fetch_and_process_enquiries()
            self.assertEqual(Enquiry.objects.count(), 2)
            enquiry = Enquiry.objects.all().first()
            assert enquiry.date_received == enquiry.created

            for detail in details:
                if not detail["skip"]:
                    enquiry = model_to_dict(
                        Enquiry.objects.filter(company_name=detail["company_name"]).first()
                    )
                    enquirer = model_to_dict(Enquirer.objects.get(id=enquiry["enquirer"]))
                    for k, v in detail.items():
                        if k == "arrange_call":
                            v = True if v == "yes" else False
                        if k in ["email_consent", "phone_consent"]:
                            v = True if v == "True" else False
                        if k in enquiry.keys():
                            self.assertEqual(enquiry[k], v)
                        if k in enquirer.keys():
                            self.assertEqual(enquirer[k], v)
                else:
                    self.assertEqual(
                        Enquiry.objects.filter(company_name=detail["company_name"]).count(), 0
                    )
