from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from square.client import Client
import uuid
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        username = None
    else:
        username = request.user

    context = {
        "items": MenuItem.objects.all(),
        "additions": MenuItemAddition.objects.all(),
        "username": username
    }

    return render(request, "orders/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    context = {
        "items": MenuItem.objects.all(),
        "message": "invalid password"
    }

    return render(request, "orders/index.html", context)

def logout_view(request):
    logout(request)

    context = {
        "items": MenuItem.objects.all(),
        "message": "logged out"
    }
    return render(request, "orders/index.html", context)

def create_account(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(username, email, password)
            return HttpResponseRedirect(reverse("index"))
        except:
            return HttpResponse("User already exists")

    else:
        return render(request, "orders/create_account.html")

def add_to_cart_item(request, menu_item_id):
    try:
        item = MenuItem.objects.get(pk=menu_item_id)
    except:
        raise Http404("Item does not exist")

    try: 
        Order.objects.get(customer=request.user, is_placed="N")
    except Order.DoesNotExist:
        Order.objects.create(customer=request.user, is_placed="N")

    currentOrder = Order.objects.get(customer=request.user, is_placed="N")
    
    newOrderItem = OrderItem.objects.create(menu_item=item, order=currentOrder)
    
    if newOrderItem.menu_item.max_num_of_additions == 0:
        return render(request, "orders/message.html", {"message": "Added to Cart", "item":item})

    context = {
        "max_additions": range(newOrderItem.menu_item.max_num_of_additions),
        "additions": MenuItemAddition.objects.filter(category="Topping"),
        "order_item": newOrderItem
    }
    return render(request, "orders/add_additions.html", context)

def add_to_cart_addition(request, order_item_id):
    try:
        order_item = OrderItem.objects.get(pk=order_item_id)
    except:
        raise Http404("Item does not exist")
    
    try:
        addition1 = int(request.POST["addition 0"])
        order_item.menu_item_addition.add(addition1) 
    except:
        pass

    try:
        addition2 = int(request.POST["addition 1"])
        order_item.menu_item_addition.add(addition2) 
    except:
        pass
    
    try:
        addition3 = int(request.POST["addition 2"])
        order_item.menu_item_addition.add(addition3) 
    except:
        pass

    try:
        addition4 = int(request.POST["addition 3"])
        order_item.menu_item_addition.add(addition4) 
    except:
        pass
    
    return HttpResponseRedirect(reverse("index"))

def view_cart(request):

    try:
        current_order = Order.objects.get(customer=request.user, is_placed="N")
    except:
        return render(request, "orders/message.html", {"message": "Your cart is empty!"})
    
    current_order_items = OrderItem.objects.filter(order=current_order)

    grand_total = 0.00

    for oi in current_order_items:
        grand_total += float(oi.menu_item.price)

    current_order.grand_total = grand_total
    current_order.save()

    context = {
        "order_items": current_order_items,
        "grand_total": "{0:.2f}".format(grand_total)
    }
    
    return render(request, "orders/cart.html", context)

def order_confirmation(request, order_id):
    try:
        current_order = Order.objects.get(pk=order_id)
    except:
        return render(request, "orders/message.html", {"message": "No such order!"})
    
    context = {
        "message": "Your order has been placed!",
        "grand_total": current_order.grand_total,
    }

    return render(request, "orders/message.html", context)

def pay(request):
    try:
        current_order = Order.objects.get(customer=request.user, is_placed="N")
    except:
        return render(request, "orders/message.html", {"message": "Your cart is empty!"})

    # current_order = Order.objects.filter(customer=request.user, is_placed="Y").first()

    context = {
        "grand_total": current_order.grand_total,
    }

    if request.method == "POST":
        # Create an instance of the API Client 
        # and initialize it with the credentials 
        # for the Square account whose assets you want to manage
        
        client = Client(
            access_token='EAAAEDjhGlYSsPaPl8t01AzkGgY9nKZoI-z8vuqX8oSHXsQJ4O7qK6jGC2LudLpg',
            environment='sandbox',
        )
        
        # Get an instance of the Square API you want call
        payments_api = client.payments
        
        # Call list_locations method to get all locations in this Square account
        # result = api_locations.list_locations()

        cents_charged = int(current_order.grand_total * 100)
        nonce = request.POST["nonce"]

        body = {
            "source_id": nonce,
            "idempotency_key": str(uuid.uuid1()),
            "amount_money": {"amount": cents_charged, "currency": "USD"}
        }

        payment_results = payments_api.create_payment(body)

        # Call the success method to see if the call succeeded
        if payment_results.is_success():
            # The body property is a list of locations
            response = payment_results.body['payment']
            # Iterate over the list
            # print(context)
            
            current_order.is_placed = "Y"
            current_order.save()

            order_pk = {
                # "order_message": "Your order has been placed!",
                # "grand_total": current_order.grand_total,
                "order_pk": current_order.id,
            }

            response.update(order_pk)

            return JsonResponse(response)
            
        # Call the error method to see if the call failed
        elif payment_results.is_error():
            print('Error calling payment API')
            context = payment_results.errors
            errors = payment_results.errors
            # An error is returned as a list of errors
            # for error in errors:
            #     # Each error is represented as a dictionary
            #     for key, value in error.items():
            #         print(f"{key} : {value}")
            #     print("\n")
            print(errors)

    return render(request, "orders/pay.html", context)