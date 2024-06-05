# import json
# import os
# import stripe

# # This is your test secret API key.
# stripe.api_key = "sk_test_51PDtaxA9AMTZvu4DkKM0nrXO9EuQtAEDyb0mFKlFFw5qR12lQdjNuScCQsxe6T29pftONqPWjeH0vL4YJdhtbvkZ00nhjAcsZn"

# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required


# def calculate_order_amount(items):

#     return 1400


# @csrf_exempt
# @login_required
# def create_payment(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data["items"]),
#                 currency="usd",
#                 # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
#                 automatic_payment_methods={
#                     "enabled": True,
#                 },
#             )
#             return JsonResponse({"clientSecret": intent["client_secret"]})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=403)
