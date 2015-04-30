from views import get_pagination_page
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def pagination(request, p):

    items = get_pagination_page(p)
    render = render_to_string('patient/ajax.html', {'items': items})

    dajax = Dajax()
    dajax.assign('#pagination', 'innerHTML', render)
    return dajax.json()