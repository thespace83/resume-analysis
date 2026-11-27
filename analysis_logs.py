def find_first(key: str, lg: str) -> int:
    if key not in lg:
        raise
    i = 1
    while lg[lg.find(key) + len(key) + 1:lg.find(key) + len(key) + 1 + i].isdigit():
        i += 1
    return int(lg[lg.find(key) + len(key) + 1:lg.find(key) + len(key) + i])


file = open("app.log", "r", encoding="utf-8")
line = file.readline()
input_tokens = 0
max_input_tokens = 0
output_tokens = 0
max_output_tokens = 0
count = 0
while line:
    log = line.strip()
    if "DEBUG root: ParsedResponse" in log:
        count += 1
        log = log.replace("max_output_tokens", "")

        print(log)

        input_tokens += find_first("input_tokens", log)
        output_tokens += find_first("output_tokens", log)
        if find_first("input_tokens", log) > max_input_tokens:
            max_input_tokens = find_first("input_tokens", log)
        if find_first("output_tokens", log) > max_output_tokens:
            max_output_tokens = find_first("output_tokens", log)
        print(f"input_tokens: {find_first("input_tokens", log)}")
        print(f"output_tokens: {find_first("output_tokens", log)}")
    line = file.readline()

print()
print(f"В среднем input_tokens {input_tokens // count}. Цена {round(input_tokens / count / 1000 * .1, 2)} руб")
print(f"В среднем output_tokens {output_tokens // count}. Цена {round(output_tokens / count / 1000 * .1, 2)} руб")
print(f"Средняя цена: {round(input_tokens / count / 1000 * .1 + output_tokens / count / 1000 * .1, 2)} руб")
print(f"Максимальный input_tokens: {max_input_tokens}. Цена {round(max_input_tokens / 1000 * .1, 2)} руб")
print(f"Максимальный output_tokens: {max_output_tokens}. Цена {round(max_output_tokens / 1000 * .2, 2)} руб")
file.close()

# ParsedResponse(id='37ee5c69-7f99-4618-bed1-54e2a9538e3d', access_programs=None, created_at=1795795881.0, error=None,
#                incomplete_details=None,
#                instructions='\nВыведи машинно-читаемые данные без форматирования о кандидате в формате JSON. \nКлюч "name": ФИО кандидата, если не найдено, пустая строка. \nКлюч "age": возраст кандидата, если не найдено, -1. \nКлюч "gender": пол кандидата, если не найдено, пустая строка. \nКлюч "education": образование кандидата, если не найдено, пустая строка. \nКлюч "region": регион РФ в котором кандидат ищет работу, если не найдено пустая строка. \nКлюч "profession": профессия кандидата, если не найдено, пустая строка.\nКлюч "experience": количество лет работы кандидата, если не найдено, -1. \nКлюч "type-of-employment": тип работы кандидата, если не найдено, пустая строка. \nКлюч "info": вырезка из текста про личные качества кандидата, если не найдено, пустая строка. \nКлюч "knowledge-of-languages": список из словарей, где ключ название языка строчными буквами, а значение уровень владения языком, если язык родной, то указать "родной", если не найдено, пустой список. \nКлюч "driving-license-category": категория прав кандидата, если не найдено, пустая строка. \nКлюч "own-car": "да" если у кандидата есть своя машина, "нет" если у кандидата нет свей машины, если не найдено, пустая строка. \nКлюч "citizenship": название страны, гражданином которой является кандидат, если не найдено, пустая строка.\n',
#                metadata={}, model='gpt://b1gjsrfhh4f8o2ch3pkb/aliceai-llm-flash/latest', object='response', output=[
#         ParsedResponseOutputMessage(id='96bf76b3-5efe-4485-b557-e6b3f849b9ce', content=[
#             ParsedResponseOutputText(annotations=[],
#                                      text='{"profession": "старшая медицинская сестра стоматологии", "education": "высшее", "gender": "женщина", "own-car": "да", "citizenship": "Россия", "experience": 13, "knowledge-of-languages": [{"level": "родной", "language": "русский"}], "driving-license-category": "В", "name": "Грибанова Ольга Владимировна", "type-of-employment": "постоянная работа", "region": "Москва", "age": 44, "info": "коммуникабельность; способность быстро принимать решения; стрессоустойчивость; стремление к самосовершенствованию и развитию, умение ладить с коллективом, целеустремленность, отзывчивость, порядочность, пунктуальность"}',
#                                      type='output_text', logprobs=None, parsed=None)], role='assistant',
#                                     status='completed', type='message', phase=None)], parallel_tool_calls=False,
#                temperature=0.0, tool_choice='auto', tools=[], top_p=1.0, background=False, completed_at=None,
#                conversation=None, image=None,
#                input_transformations=None, = 65536, max_tool_calls = None, moderation = None, previous_response_id = None, prompt = None, prompt_cache_diagnostics = None, prompt_cache_key = None, prompt_cache_options = None, prompt_cache_retention = None, reasoning = None, safety_identifier = None, service_tier = 'default', status = 'completed', text = ResponseTextConfig(
#     format=ResponseFormatTextJSONSchemaConfig(name='resume_response',
#                                               schema_={'additionalProperties': False, 'type': 'object', 'strict': True,
#                                                        'properties': {'profession': {'type': 'string'},
#                                                                       'education': {'type': 'string',
#                                                                                     'enum': ['среднее',
#                                                                                              'средне специальное',
#                                                                                              'неоконченное высшее',
#                                                                                              'высшее', 'бакалавриат',
#                                                                                              'магистратура',
#                                                                                              'кандидат наук',
#                                                                                              'доктор наук', 'прочее',
#                                                                                              '']},
#                                                                       'gender': {'type': 'string',
#                                                                                  'enum': ['мужчина', 'женщина', '']},
#                                                                       'own-car': {'type': 'string',
#                                                                                   'enum': ['да', 'нет', '']},
#                                                                       'citizenship': {'type': 'string'},
#                                                                       'experience': {'type': 'integer'},
#                                                                       'knowledge-of-languages': {'type': 'array',
#                                                                                                  'items': {
#                                                                                                      'additionalProperties': False,
#                                                                                                      'type': 'object',
#                                                                                                      'properties': {
#                                                                                                          'level': {
#                                                                                                              'type': 'string',
#                                                                                                              'enum': [
#                                                                                                                  'A1',
#                                                                                                                  'A2',
#                                                                                                                  'B1',
#                                                                                                                  'B2',
#                                                                                                                  'C1',
#                                                                                                                  'C2',
#                                                                                                                  'родной']},
#                                                                                                          'language': {
#                                                                                                              'type': 'string'}},
#                                                                                                      'required': [
#                                                                                                          'language',
#                                                                                                          'level']}},
#                                                                       'driving-license-category': {'type': 'string',
#                                                                                                    'enum': ['А', 'В',
#                                                                                                             'С', 'D',
#                                                                                                             'E', '']},
#                                                                       'name': {'type': 'string'},
#                                                                       'type-of-employment': {'type': 'string', 'enum': [
#                                                                           'постоянная работа', 'подработка',
#                                                                           'стажировка', 'прочее', '']},
#                                                                       'region': {'type': 'string'},
#                                                                       'age': {'type': 'integer'},
#                                                                       'info': {'type': 'string'}},
#                                                        'required': ['name', 'age', 'gender', 'education', 'region',
#                                                                     'profession', 'experience', 'type-of-employment',
#                                                                     'info', 'knowledge-of-languages',
#                                                                     'driving-license-category', 'own-car',
#                                                                     'citizenship']}, type='json_schema',
#                                               description=None, strict=False),
#     verbosity=None), tool_usage = None, top_logprobs = None, truncation = 'disabled', usage = ResponseUsage(
#     input_tokens=887,
#     input_tokens_details=InputTokensDetails(cache_write_tokens=None, cached_tokens=0, cache_write_tokens_details=None,
#                                             tool_tokens=0), output_tokens=151,
#     output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=1038), user = None)
