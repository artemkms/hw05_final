from django.shortcuts import render


def permission_denied_view(request, exception):
    return render(request, "core/403.html", status=403)


def page_not_found(request, exception):
    return render(request, "core/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "core/500.html", status=500)
