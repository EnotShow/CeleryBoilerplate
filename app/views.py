from django.shortcuts import render

from app.tasks import print_hello, add


def render_page(request):
    """Render app page"""
    print_hello.delay()
    add.delay(1, 2)
    return render(request, 'app/index.html')
