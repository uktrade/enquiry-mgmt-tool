# Local troubleshooting

This document was created to provide solutions to common issues that occur when running Enquiry Management. The issues are categorised by the method used to bring up the application.

When updating this document please use the following template:

```
### Issue title
[brief description of issue]

Screenshot or text:

![image-title](./Troubleshooting/[image-name].png)

**Solution** If there is a single permanent fix for this issue enter it here.

**Short-term fix** If there is a temporary workaround or some of 'sticky-tape' solution enter it here.

**Long-term fix** If there is a permanent fix for the issue (or if one is being worked on) enter it here.
```

## Docker issues

This section should include issues that occur when running Enquiry Management in Docker.

### TypeError at /enquiries/14/company-search 'NoneType' object is not subscriptable

This occurs when the connection to Data Hub is setup but the browser isn't logged in to the Django admin on http://localhost:8000/admin/.

```
TypeError at /enquiries/14/company-search
'NoneType' object is not subscriptable
solution: login to Django admin on http://localhost:8000/admin/
Request Method:	POST
Request URL:	http://localhost:8001/enquiries/14/company-search
Django Version:	3.1.14
Exception Type:	TypeError
Exception Value:	'NoneType' object is not subscriptable
Exception Location:	/usr/src/app/app/enquiries/common/datahub_utils.py, line 63, in dh_request
Python Executable:	/usr/local/bin/python
Python Version:	3.8.14
Python Path:	['/usr/src/app',
 '/usr/src/app',
 '/usr/local/lib/python38.zip',
 '/usr/local/lib/python3.8',
 '/usr/local/lib/python3.8/lib-dynload',
 '/usr/local/lib/python3.8/site-packages']
Server time:	Thu, 22 Sep 2022 11:28:44 +0000
```

**Solution** login to Django admin on http://localhost:8000/admin/


## Native issues

### TypeError at /enquiries/14/company-search 'NoneType' object is not subscriptable

This occurs when the connection to Data Hub is setup but the browser isn't logged in to the Django admin on http://localhost:8000/admin/.


This section should be used for native issues that occur regardless of what API you are using.

### There is a problem. Referral Advisor: Error validating your identity in DataHub

```
There is a problem.
Referral Advisor: Error validating your identity in DataHub
```

**Solution** Update/renew the MOCK_SSO_TOKEN from DataHub. (//[your-datahub-api]/admin/add-access-token/)
