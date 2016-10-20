#!flask/bin/python


class ErrorHelper:

    @staticmethod
    def make_response_for_code(code):
        return {
            'code': code,
            'description': default_texts[code]
        }


class StatusCode:
    ok = 21

    already_exists = 1201
    not_found = 1604

    group_is_busy = 2101
    room_is_busy = 2102
    lector_is_busy = 2103


default_texts = {
    StatusCode.ok: '',
    StatusCode.already_exists: 'Trying to add alreay existing item.',
    StatusCode.not_found: 'Item not found in database.',
    StatusCode.group_is_busy: 'Selected group is busy at this time.',
    StatusCode.room_is_busy: 'Another group already has lesson in this room',
    StatusCode.lector_is_busy: 'This lector already has another lesson at this time.'
}
