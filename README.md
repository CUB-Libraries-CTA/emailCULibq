emailCULibq Queue
======================

This task queue provides for an email service that can be utilized by CU Libraries. 

Requirements
------------
1. Cybercommons API
2. Task Queue intalled within API(This Repository)

Installation
------------

1. Update `cybercom` secret within kubernetes cluster

        CELERY_IMPORTS add `emailCULibq`

        CELERY_SOURCE add `git+https://github.com/culibraries/emailCULibq@main`

2. Redeploy `cybercom-celery` deployment

Run
----

Post to Celery Task URL with the following data.

        {
            "queue": "celery",
            "args": ["< receiver_email >","noreply@colorado.edu","test email"],
            "kwargs": {"template":"default_template.html.j2","template_data":{"name":"Mark"}},
            "tags": []
        }

Templates
--------

1. Set Template Name with html or plain

    name.< html or plain >.j2

2. Configure template --> Jinja2



