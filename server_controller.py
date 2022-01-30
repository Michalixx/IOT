from audioop import add
import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
import random
from question_db import get_questions
from students_db import get_map
import pygame as pg




broker = "localhost"

client = mqtt.Client()

players = {}

map_id = get_map()

#questions = [["Pyt1", "a", "b", "c", "d", "a"], ["Pyt2", "a", "b", "c", "d", "a"], ["Pyt3", "a", "b", "c", "d", "a"], ["Pyt4", "a", "b", "c", "d", "a"], ["Pyt5", "a", "b", "c", "d", "a"]]
questions = get_questions()

counter = 0

current_answer = 1

questions_number = 5
time_for_answer = 30


#pygame
pg.init()
screen = pg.display.set_mode([1280, 720])
font_30 = pg.font.SysFont('Comic Sans MS', 30)
font_50 = pg.font.SysFont('Comic Sans MS', 50)
bg_color = (0,0,0)
text_color = (255,255,255)
button_color = (0,0,128)
button_color_noactive = (0,0,48)

def simple_gui():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.collidepoint(pg.mouse.get_pos()):
                    manage_gui()

        screen.fill(bg_color)
        button = pg.draw.rect(screen, button_color, pg.Rect(350,420,580,100))
        button_text = font_30.render("Rozpocznij Quiz", False, text_color)
        screen.blit(button_text, (520,450))
        label_text = font_50.render("Aktualnie graczy: " + str(len(players)), False, text_color)
        screen.blit(label_text, (400,200))
        pg.display.update()

def manage_gui():
    questions_counter = 1
    button_state = 2
    q = send_question()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and counter == len(players):
                if button.collidepoint(pg.mouse.get_pos()):
                    
                    if button_state == 1:
                        button_state = 2
                        if questions_counter < questions_number:
                            questions_counter += 1
                            q = send_question()
                        else:
                            pg.display.quit()
                            running = False
                    elif button_state == 2:
                        send_ranking(q)
                        button_state = 1


        
        screen.fill(bg_color)
        if(counter == len(players)):
            button = pg.draw.rect(screen, button_color, pg.Rect(350,420,580,100))
        else:
            button = pg.draw.rect(screen, button_color_noactive, pg.Rect(350,420,580,100))
        if questions_counter != questions_number:
            if(button_state == 1):
                button_text = font_30.render("Zadaj kolejne pytanie", False, text_color)
            elif button_state == 2:
                button_text = font_30.render("Wyślij ranking", False, text_color)
        else:
            button_text = font_30.render("Zakończ quiz", False, text_color)
        screen.blit(button_text, (520,450))
        label_text = font_50.render("Aktualne pytanie " + str(questions_counter) + "/" + str(questions_number), False, text_color)
        screen.blit(label_text, (400,200))
        label_text_2 = font_50.render("Aktualnie odpowiedziało " + str(counter) + "/" + str(len(players)), False, text_color)
        screen.blit(label_text_2, (400,300))
        pg.display.update()



def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split("|")
    
    if(message_decoded[0] == "A"):
        add_player(message_decoded[1])
    elif(message_decoded[0] == "Q"):
        global counter
        counter += 1
        if(message_decoded[2] == current_answer):
            if(int(message_decoded[3]) < 0): message_decoded[3] = "0"
            players[message_decoded[1]] +=  int(message_decoded[3])



        
    
    
def add_player(ID):
    if not ID in map_id:
        send_mess("A|"+ID+"|ERROR|1")
    elif not ID in players:
        players[ID] = 0
        send_mess("A|"+ID+"|"+map_id.get(ID))
    else:
        send_mess("A|"+ID+"|ERROR|2")
    
     



def send_mess(mess):
    client.publish("quiz/server", mess,)


def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    # Send message about conenction.
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("quiz/player")

def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()

def temp():
    s = input()
    while s != "start":
        s = input()
    start_game(5, 10)

def send_question():
    global counter, current_answer
    q = random.choice(questions)
    questions.remove(q)
    tmp = "Q|"
    for i in range(5):
        tmp += q[i]
        tmp += "|"
    send_mess(tmp+str(time_for_answer))
    current_answer = q[5]
    counter = 0
    return q

def start_game(n, t):
    global counter, current_answer
    for _ in range(n):
        q = random.choice(questions)
        questions.remove(q)
        tmp = "Q|"
        for i in range(5):
            tmp += q[i]
            tmp += "|"
        send_mess(tmp+str(t))
        current_answer = q[5]
        counter = 0
        s = input("Wpisz next na nowe pytanie")
        while s != "next" or counter != len(players):
            s = input("Wpisz next na nowe pytanie")
        send_ranking(q)

def send_ranking(q):
    tmp = "R|" + current_answer
    # if current_answer == "a": tmp += q[1]
    # elif current_answer == "b": tmp += q[2]
    # elif current_answer == "c": tmp += q[3]
    # else: tmp += q[4]
    tmp += "|"
    sort = dict(sorted(players.items(), key=lambda x:x[1], reverse=True))
    for item in sort:
        tmp += map_id[item] + "|" + str(sort[item]) + "|"
    tmp = tmp[:-1]
    print(tmp)
    send_mess(tmp)



        





def run_receiver():
    connect_to_broker()
    print("Czekam na graczy...")
    simple_gui()
    #temp()
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
