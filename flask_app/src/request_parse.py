from flask import Flask, render_template, redirect, request, url_for

def request_parse(request,defaults):

    form_dict = {}
    if request.method == "POST":
        form_dict.update(request.form.to_dict())
    
    for k, v in defaults.items():
        if k not in form_dict:
            form_dict[k] = v

    if any(key in form_dict for key in ['submit', 'prev_submit', 'next_submit']):
        for radio_button in ['active_check','sold_check']:
            if radio_button in form_dict:
                form_dict[radio_button] = True
            else:
                form_dict[radio_button] = False
    else:
        form_dict['active_check'] = True
        form_dict['sold_check'] = False

    if 'prev_submit' in form_dict:
        form_dict['page'] = int(form_dict['page']) - 1
    elif 'next_submit' in form_dict:
        form_dict['page'] = int(form_dict['page']) + 1
    elif 'submit' in form_dict:
        form_dict['page'] = 1

    
    return form_dict