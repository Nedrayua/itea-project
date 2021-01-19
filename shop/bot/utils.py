import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def processing_iterable(tag, iterable, id_field='id', text_fields='title', add_text=None):
    buttons = []
    for i in iterable:
        json_data = json.dumps({
            id_field: str(getattr(i, id_field)),
            'tag': tag
        })
        if add_text:
            text = add_text + getattr(i, text_fields)
        else:
            text = getattr(i, text_fields)
        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=json_data
            )
        )
    return buttons


def inline_kb_from_iterable(
        tag,
        iterable,
        back_way=None,
        id_field='id',
        text_fields='title',
        row=0

):
    text = 'Вернуться в: '
    if back_way:
        buttons = processing_iterable(tag, iterable, id_field, text_fields)
        buttons.append(processing_iterable(tag, [back_way], id_field, text_fields, add_text=text)[0])
    else:
        buttons = processing_iterable(tag, iterable, id_field, text_fields)
    if row:
        kb = InlineKeyboardMarkup(row_width=row)
    else:
        kb = InlineKeyboardMarkup()
    kb.add(*buttons)
    return kb


def inline_kb(callback_dict, text, without_kb=False):
    json_data = json.dumps(callback_dict)
    button = InlineKeyboardButton(
        text=text,
        callback_data=json_data
    )
    kb = InlineKeyboardMarkup()
    kb.add(button)
    if without_kb:
        return button
    else:
        return kb


def return_content_args(name, argument, message=None):
    """
    :name: Имя, для форматирования
    :argument: подставленное значение
    :message: сообщение в случае пустого аргумента
    """
    if message:
        data = f'{name}: {argument}' if argument else f'{name}: {message}'
    else:
        data = f'{name}: {argument}' if argument else ""
    return data
