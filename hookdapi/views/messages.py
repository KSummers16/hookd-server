from django.http import JsonResponse
from django.core.mail import send_mail


def send_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            "Hook'd by Kim Contact FOrm Submission",
            f"Name: {name}\nEmail: {email}\nMessage: {message}",
            "hookdbykim@gmail.com",
            ["hookdbykim@gmail.com"],
            fail_silently=False,
        )

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
