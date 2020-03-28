# Project 3

Web Programming with Python and JavaScript

## Function of base.html
This is the base template with formatting that other pages extend

## Function of add_additions.html
This page allows you to select additions eg. toppings to a pizza. 

## Function of cart.html
This displays the current items in the customer's cart

## Function of create_account.html
This allows a customer to create a new account

## Function of index.html
This displays the main menu, the ability to add items to cart. Also depending on whether the user is logged in, it allows them to log in, log out, and create a new account.

## Function of message.html
This is a generic page to display a message eg. order completed.

## Function of pay.html
This is the page hosting the Square API for payments. Lots of js code to generate a nonce for the card, then charge the card.

## Function of models.py
This is the data structure of the app. It has 4 main tables:
1. Menu Item Additions: this contains the additions to a menu item, eg. a pizza topping

2. Menu Item: this is an item on the menu. It has a property to limit the max number of additions (eg. toppings) based on the item selected. If a customer selects a 2-topping pizza, then they can only choose 2 toppings

3. Order Item: this is a line item in a customer's order. It can contain a menu item and one or more additions

4. Order: this is the entire order for the customer

## Function of admin.py
This has some modifications to display order->order item relationships in the Order Admin table, as well as some UI customizations

## Function of views.py
This is the brains of the app - it has a method for all the functions that are needed in the requirements.  