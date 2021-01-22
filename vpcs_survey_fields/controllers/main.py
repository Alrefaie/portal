# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey
from odoo import SUPERUSER_ID

ADDRESS_FIELDS = ['street', 'street2', 'city', 'zip', 'state_id', 'country_id']
NAME_FIELDS = ['first_name', 'middle_name', 'last_name']


class VpsSurvey(Survey):

    @http.route(['/survey/cprefill/<string:survey_token>/<string:answer_token>'],
                type='http', auth='public', website=True)
    def custom_prefill(self, survey_token, answer_token, page_or_question_id=None, **post):
        if not answer_token:
            answer_token = None
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
        if access_data['validity_code'] is not True and access_data['validity_code'] != 'answer_done':
            return {}

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']
        try:
            page_or_question_id = int(page_or_question_id)
        except:
            page_or_question_id = None

        # Fetch previous answers
        if survey_sudo.questions_layout == 'one_page' or not page_or_question_id:
            previous_answers = answer_sudo.user_input_line_ids
        elif survey_sudo.questions_layout == 'page_per_section':
            previous_answers = answer_sudo.user_input_line_ids.filtered(lambda line: line.page_id.id == page_or_question_id)
        else:
            previous_answers = answer_sudo.user_input_line_ids.filtered(lambda line: line.question_id.id == page_or_question_id)

        # Return non empty answers in a JSON compatible format
        ret = {}
        for answer in previous_answers:
            if not answer.skipped:
                answer_data = answer.read()[0]
                answer_tag = '%s_%s' % (answer.survey_id.id, answer.question_id.id)
                if answer.answer_type == 'name':
                    for f_name in NAME_FIELDS:
                        ret.update({answer_tag + '_' + f_name: answer_data.get(f_name)})
                elif answer.answer_type == 'm2o':
                    answer_value = int(answer.value_m2o)
                    ret.update({answer_tag: answer_value})
                elif answer.answer_type == 'address':
                    for f_name in ADDRESS_FIELDS:
                        f_val = answer_data.get(f_name)
                        if '_id' in f_name and f_val:
                            f_val = answer_data.get(f_name, [False])[0]
                        ret.update({answer_tag + '_' + f_name: f_val})
                elif answer.answer_type == 'text' and answer.question_id.question_type == 'textbox':
                    answer_value = answer.value_text
                    ret.update({answer_tag: answer_value})
                elif answer.answer_type == 'binary':
                    answer_value = answer.attachment_id.name
                    ret.update({answer_tag: answer_value})
                elif answer.answer_type == 'sign':
                    answer_value = answer.img_sign
                    ret.update({answer_tag: answer_value.decode('utf-8')})
        return json.dumps(ret)

    def _get_graph_data(self, question, current_filters=None):
        current_filters = current_filters if current_filters else []
        Survey = request.env['survey.survey']

        if question.question_type == 'm2o':
            result = Survey.prepare_result(question, current_filters)['answers']
            return json.dumps(result)
        if question.question_type == 'address':
            result = Survey.prepare_result(question, current_filters)['answers']
            return json.dumps(result)
        return super(VpsSurvey, self)._get_graph_data(question, current_filters=None)
