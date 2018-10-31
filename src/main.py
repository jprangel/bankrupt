import logging
import sys
import re
import random
import balance as blc
#from balance import list_balance_p1, list_balance_p2

dice_min = 1
dice_max = 6
player1 = 'Impulsivo'
player2 = 'Exigente'
player3 = 'Cauteloso'
player4 = 'Aleatorio'
list_players = [player1,player2]
player1_position = 0
player2_position = 0
player3_position = 0
player4_position = 0
player_position = 0
complete_round = 100
list_houses_owners = []
list_houses = []

def logger():

    global log

    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s [%(funcName)s] [%(levelname)-5.5s] %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
    
    return log

def readConf():
    
    global list_houses

    conf = open('cfg/gameConfig.txt','r')
    for line in conf:
        line = re.sub(' ', ';', line)
        line = re.sub(';;', ';', line)
        line = re.sub('\n', '', line)
        list_houses.append(line)

    return list_houses

def rollingDice(dice_min,dice_max):

    global value_dice

    value_dice = random.randint(dice_min, dice_max)
    log.info('Dado numero... '+ str(value_dice))

    return value_dice

def getPosition(value_dice,player):

    global player_position
    global item_house

    if player == 'Impulsivo':
        player_position = player1_position + value_dice
        log.info('Andando... '+ str(player_position)+' casas')

    elif player == 'Exigente':
        player_position = player2_position + value_dice
        log.info('Andando... '+ str(player_position)+' casas')
    
    item_house = value_dice-1
    player_position = value_dice-1

    return player_position
    return item_house

def priceToBuyHouse(value_position):

    global price_buy_house

    price_buy_house = list_houses[value_position].split(';')
    price_buy_house = price_buy_house[0]

    return price_buy_house

def priceToRentHouse(value_position):

    global price_rent_house

    price_rent_house = list_houses[value_position].split(';')
    price_rent_house = price_rent_house[1]

    return price_rent_house

def getOwnerHouse(value_position):

    global player_owner

    print(list_houses_owners)
    print(value_position)
    try:
        player_owner = list_houses_owners.index(value_position)
        print(player_owner)
    except ValueError:
        player_owner = 'Ninguem'
        print(player_owner)

    return player_owner

def buyHouse(item_player,value_position):

    price_buy = priceToBuyHouse(value_position)
    balance = blc.getBalance(item_player)
    
    if balance >= int(price_buy):

        balance = blc.debitBalance(item_player,price_buy)

        list_houses_owners.append(value_position)
        list_houses_owners.append(item_player)

        log.info('Jogador: ' + str(item_player) + ' - Comprando Casa: ' + str(value_dice) + ' - Valor: ' + str(price_buy) + ' - Saldo: ' + str(balance))
    else:
        log.info('Jogador: ' + str(item_player) + ' - Comprando Casa: ' + str(value_dice) + ' - Valor: ' + str(price_buy) + ' - Nao possui Saldo: ' + str(balance))

def rentHouse(item_player,value_position):

    price = priceToRentHouse(value_position)
    player_owner = getOwnerHouse(value_position)
    balance = blc.getBalance(item_player)
    

    if balance >= int(price):

        balance = blc.debitBalance(item_player,price)
        credit = blc.creditBalance(player_owner,price)

        log.info('Jogador: ' + str(item_player) + ' - Alugando Casa: ' + str(value_dice) + ' - Valor: ' + str(price) + ' - Saldo: ' + str(balance))
    else:
        log.info('Jogador: ' + str(item_player) + ' - Alugando Casa: ' + str(value_dice) + ' - Valor: ' + str(price) + ' - Nao possui Saldo: ' + str(balance))


def playBankrupt(list_players):
    
    max_sessions = 5

    for i in range(1,max_sessions):
        print('### Iniciando rodada: ' + str(i))
        for player in list_players:
            if player == player1:
                player = player1
                log.info(player1+' jogando' + ' - Saldo: ' + str(blc.getBalance(player1)))
                rollingDice(dice_min,dice_max)
                value_position = getPosition(value_dice,player)

                if value_position in list_houses_owners:
                    log.info('Essa propriedade ja tem dono')
                    rentHouse(player,value_position)
                else:
                    buyHouse(player,value_position)
            elif player == player2:
                player = player2
                log.info(player2+' jogando'  + ' - Saldo: ' + str(blc.getBalance(player2)))
                rollingDice(dice_min,dice_max)
                value_position = getPosition(value_dice,player)

                if value_position in list_houses_owners:
                    log.info('Essa propriedade ja tem dono')
                    rentHouse(player,value_position)
                elif priceToRentHouse(value_position) > str(50):
                    log.info('Essa propriedade custa '+ str(price_rent_house))
                    buyHouse(player,value_position)
                else:
                    log.info('Essa propriedade custa '+ str(price_rent_house))
                    rentHouse(player,value_position)
                    
if __name__ == '__main__':
    logger()
    readConf()
    blc.AddCoinsToPlayer()
    playBankrupt(list_players)
