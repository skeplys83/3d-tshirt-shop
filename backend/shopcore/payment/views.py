import logging

logger = logging.getLogger(__name__)
import json
from django.views import View
from .stripe_service import stripe
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decouple import config
from orders.models import Order
from datetime import datetime, timezone
from django.core.mail import send_mail
from products.models import Product

stripe.api_key = config('STRIPE_SECRET_KEY')

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order_data = data.get('order')
            line_items = order_data.get('line_items')
            selected_products = order_data.get('selectedProducts', {})

            if not line_items:
                return JsonResponse({'error': 'line_items not provided'}, status=400)

            for item in selected_products:
                product_id = item['id']
                ordered_size = item.get('size')
                ordered_quantity = item['quantity']

                try:
                    product = Product.objects.get(id=product_id)

                    product_quantity = product.stock.get(ordered_size)
                    logger.info(f"Product: {product}")
                    logger.info(f"Available quantity in selected Size: {product_quantity}")
                    if product_quantity is None or product_quantity < ordered_quantity:
                        logger.info(f"Stock nicht mehr vorhanden")
                        return JsonResponse({
                            'message': f"Insufficient stock for product {product.name}, only {product_quantity} left in"
                                       f" size {ordered_size}"
                        }, status=400)

                    product.stock[ordered_size] -= ordered_quantity
                    product.save()
                    logger.info(f"Stock updated for product {product.name} (size {ordered_size}): -{ordered_quantity}")

                except Product.DoesNotExist:
                    return JsonResponse({'error': f"Product with ID {product_id} does not exist."}, status=404)

            order = Order.objects.create(
                email=order_data.get('email'),
                totalPrice=order_data.get('totalPrice'),
                status='new',
                selectedProducts=order_data.get('selectedProducts', {}),
                salutation=order_data.get('salutation'),
                first_name=order_data.get('firstName'),
                last_name=order_data.get('lastName'),
                phone_number=order_data.get('phoneNumber'),
                street_and_number=order_data.get('streetAndNumber'),
                city=order_data.get('city'),
                postal_code=order_data.get('postalCode'),
                country=order_data.get('country'),
                alternative_address=order_data.get('alternativeAddress', {}),
                differentShippingAddress=order_data.get('differentShippingAddress', False),
                termsAccepted=order_data.get('termsAccepted', False),
            )

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=config('STRIPE_SITE_URL') + 'paymentSuccess/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=config('STRIPE_SITE_URL') + 'paymentFailed/?canceled=true',
            )

            order.stripe_session_id = checkout_session['id']
            if request.user.is_authenticated:
                order.orderPlacedByUserWithId = request.user.id
            order.save()
            logger.info(f"Order created by: {order.email}")
            logger.info(f"Order updated with stripe_session_id: {order.stripe_session_id}")
            logger.info(f"Hier wird die Session ID zurückgeeimert: {checkout_session.url}")
            return JsonResponse({'url': checkout_session.url})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)

        except Exception as e:
            return JsonResponse({'message': 'Something went wrong when creating checkout session: ' + str(e)},
                                status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = config('STRIPE_WEBHOOK_SECRET_KEY')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            try:
                order = Order.objects.get(stripe_session_id=session.get('id'))
                order.payedStatus = True
                order.payed_at = datetime.now(timezone.utc).isoformat(timespec='microseconds')
                order.save()
                logger.info(f"Order payment succeeded for: {order.email}")

                if order.differentShippingAddress:
                    # Alternative Adresse verwenden
                    address_line1 = order.alternative_address.get('street_and_number', '')
                    city = order.alternative_address.get('city', '')
                    postal_code = order.alternative_address.get('postal_code', '')
                    country = order.alternative_address.get('country', '')
                else:
                    # Standardadresse verwenden
                    address_line1 = order.street_and_number
                    city = order.city
                    postal_code = order.postal_code
                    country = order.country

                products_str = "\n".join([
                    f"- {item['quantity']} x {item['name']} ({item.get('size', 'N/A')}): {item['price']}€"
                    for item in order.selectedProducts
                ])

                send_mail(
                    subject=f'We received your order ({order.id})',
                    message=(
                        f"Thank you {order.salutation} {order.last_name}!\n"
                        f"Your payment method was accepted and our team will proceed with your order ASAP!\n"
                        f"Here are the details of your order:\n\n"
                        f"{products_str}\n\n"
                        f"Total Price: {order.totalPrice:.2f}€\n\n"
                        "Delivery Address:\n"
                        f"{address_line1}\n"
                        f"{city}, {postal_code}\n"
                        f"{country}\n\n"
                        "Thank you for shopping with us!\n\n\n"
                        f"For support questions (email to: shopcore.info@gmail.com), reference your "
                        f"order ID: {order.id}"
                    ),
                    from_email=config('DEFAULT_FROM_EMAIL'),
                    recipient_list=[order.email],
                    fail_silently=False,
                )
                logger.info(f"Confirmation email sent to: {order.email}")
            except Order.DoesNotExist:
                logger.error("Order not found for stripe_session_id: " + session.get('id'))

        elif event['type'] in ['checkout.session.expired']:
            session = event['data']['object']
            try:
                order = Order.objects.get(stripe_session_id=session.get('id'))
                order.status = 'cancelled'
                order.save()
                logger.info(f"Order payment failed or canceled for: {order.email}")

                for item in order.selectedProducts:
                    product_id = item['id']
                    ordered_size = item.get('size')
                    ordered_quantity = item['quantity']

                    try:
                        product = Product.objects.get(id=product_id)

                        if ordered_size in product.stock:
                            product.stock[ordered_size] += ordered_quantity
                            product.save()
                            logger.info(f"Restocked product {product.name} (size {ordered_size}): +{ordered_quantity}")

                    except Product.DoesNotExist:
                        logger.error(f"Product with ID {product_id} does not exist for restocking.")

                send_mail(
                    subject=f'We did not received your payment ({order.id})',
                    message=(
                        f"Hello {order.salutation} {order.last_name}!\n"
                        f"Your payment method was not accepted, therefore we cannot proceed your order...\n"
                        "Please contact our support to quickly solve the problem. The ordered items you have chosen"
                        "are only reserved for 24 hours!\n"
                        f"For support questions (email to: shopcore.info@gmail.com), reference your "
                        f"order ID ({order.id}) in the subject of the mail. Otherwise we cannot recognize your message!"
                    ),
                    from_email=config('DEFAULT_FROM_EMAIL'),
                    recipient_list=[order.email],
                    fail_silently=False,
                )

            except Order.DoesNotExist:
                logger.error("Order not found for stripe_session_id: " + session.get('id'))

        return JsonResponse({'status': 'success'}, status=200)
