from flask import session
import requests, base64
import pdb
from os import getenv


def flowershop_get_session(flower_user, flower_pass):
    """validates current cart_session id and session['cart_id']
    or get a new one from the API
    """
    print_test("REACHED flowershop_get_session", 1)

    if session.get('cart_id') is None:
        print_test("NO ID EXISTS:", 0)

        #create shopping cart
        session['cart_id'] = create_cart(flower_user, flower_pass)
        print_test('NEW ID CREATED:',session['cart_id'])

        return session['cart_id']

    #see if it's valid
    cart_id = session['cart_id']
    print_test("CURRENT cart_id", cart_id)

    cart_contents = requests.get(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}', auth=(flower_user, flower_pass))
    cart_contents = cart_contents.json()
    try:
        if cart_contents['errors'][0] == 'The sessionid does not exist':
            print_test("TRIED GETTING CONTENTS:cart_contents['errors'][0]", cart_contents['errors'][0])

            #no? then create a new one
            session['cart_id'] = create_cart(flower_user, flower_pass)
            print_test("'errors'returned from API so NEW cart_id =':", session['cart_id'])

    except KeyError:
        print_test("THREW KEY ERROR -> API RETURNED VALID cart_contents = ", cart_contents )
        print_test("CURRENT cart_id still valid = ", cart_id)

    
    return session['cart_id']


# def check_or_create_cart(flower_user, flower_pass):
    """ requests cart contents to see if session is valid
        if API session id is NOT VALID
            create cart - 
        if valid:
            flower_cart_flask_session_checker()
    
    """
    try:
        cart_contents = requests.get(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}', auth=(flower_user, flower_pass))
        cart_contents = cart_contents.json()
    except:
        cart_contents = "NO CART FOUND"
    
    if cart_contents == "NO CART FOUND":
        create_cart(flower_user, flower_pass)

    return cart_contents

def create_cart(flower_user, flower_pass):
    
    cart=requests.post('https://www.floristone.com/api/rest/shoppingcart',  auth=(flower_user, flower_pass))
    cart = cart.json()

    return cart['SESSIONID']

def get_flower_urls(cart_contents):
    """ 
    Since cart contents only has code and name of the flowers this brings up the picture URLs from the code#'s in the cart so they can be displayed
    """
    flower_urls=[]
    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')
    for item in cart_contents['products']:
        flower_code=item['CODE']

        flower_detail = requests.get(f'https://www.floristone.com/api/rest/flowershop/getproducts?code={flower_code}', auth=(flower_user, flower_pass))
        flower_detail=flower_detail.json()

        flower_urls.append({item['CODE']:flower_detail['PRODUCTS'][0]['SMALL']})

        # print("___________________________FLOWER URLS_________________________________")
        # print(flower_detail['PRODUCTS'][0]['SMALL'])

    # print('flower_urls:', flower_urls)

    return flower_urls 


def get_cart_contents(cart_id, flower_user, flower_pass):
    """ Get current cart contents from API return them and store in flask-session """
    cart_contents = requests.get(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}', auth=(flower_user, flower_pass))
    cart_contents = cart_contents.json()

    session['cart_contents'] = cart_contents

    return cart_contents

def get_authorizenet_key(flower_user, flower_pass):
    """ responds with a unique structure like this:
        {
        "USERNAME": "unique string 'o letters",
        "AUTHORIZENET_KEY": "unique string 'o letters",
        "AUTHORIZENET_URL": "https://jstest.authorize.net/v1/Accept.js"
        }
    Needed for the place order call which also returns a single-use token   
    """
    authorize_net = requests.get(f'https://www.floristone.com/api/rest/flowershop/getauthorizenetkey', auth=(flower_user, flower_pass))
    authorize_net = authorize_net.json()

    return authorize_net

def print_test(variable_name, foo):

    print("------------------------------------------------------------------------------")
    print(variable_name, foo)
    print("------------------------------------------------------------------------------")

