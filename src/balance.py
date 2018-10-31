from pymemcache.client import base
import os

player1_coins = 300
player2_coins = 300
player3_coins = 300
player4_coins = 300
   
def AddCoinsToPlayer():

    global memcached

    memcached = base.Client(('127.0.0.1', 11211))
    memcached.set('list_balance_p1', player1_coins)
    memcached.set('list_balance_p2', player2_coins)

    return memcached

def getBalance(item_player):

    global balance

    if item_player == 'Impulsivo':
        balance = memcached.get('list_balance_p1')
        
    elif item_player == 'Exigente':
        balance = memcached.get('list_balance_p2')

    return int(balance)
    
def debitBalance(item_player,price_buy):

    global balance

    price_buy = int(price_buy)

    if item_player == 'Impulsivo':
        balance = int(getBalance(item_player)) - price_buy
        memcached.set('list_balance_p1', balance)
        
    elif item_player == 'Exigente':
        balance = int(getBalance(item_player)) - price_buy
        memcached.set('list_balance_p2', balance)

    return int(balance)

def creditBalance(item_player,price_rent):

    global balance

    price_rent = int(price_rent)

    if item_player == 'Impulsivo':
        balance = int(getBalance(item_player)) + price_rent
        memcached.set('list_balance_p1', balance)
        print(memcached.get('list_balance_p1'))
        
    elif item_player == 'Exigente':
        balance = int(getBalance(item_player)) + price_rent
        memcached.set('list_balance_p2', balance)
        print(memcached.get('list_balance_p2'))

    return int(balance)