from flask import render_template

def render_export_html(template_name, context):
    return render_template(template_name, **context)
