# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Surveys',
    'version': '3.0',
    'category': 'Marketing/Survey',
    'description': """
Create beautiful surveys and visualize answers
==============================================

It depends on the answers or reviews of some questions by different users. A
survey may have multiple pages. Each page may contain multiple questions and
each question may have multiple answers. Different users may give different
answers of question and according to that survey is done. Partners are also
sent mails with personal token for the invitation of the survey.
    """,
    'summary': 'Create surveys and analyze answers',
    'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'auth_signup',
        'http_routing',
        'mail',
        'web_tour',
        'gamification'],
    'data': [
        'views/survey_question_views.xml',
        'views/survey_user_views.xml',
        'survey_templates.xml',
    ],
}
