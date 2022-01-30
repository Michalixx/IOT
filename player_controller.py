import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
import pygame as pg
import asyncio
import sys
from multiprocessing import Process
from threading import Thread

broker = "localhost"
client = mqtt.Client()

pg.init()
screen = pg.display.set_mode([1280, 720])
font_30 = pg.font.SysFont('calibri', 30)
font_50 = pg.font.SysFont('calibri', 50)
bg_color = (0, 0, 0)
text_color = (255, 255, 255)
wrong_answ_color = (105, 105, 105)
button_color = (0, 0, 128)
button_color_noactive = (0, 0, 48)

message = "Przyłóż kartę"
message_old = ""

ID = None
gui_type = 0
rank = []
currentQuestion = "asdasdadsad"

def process_message(client, userdata, messageW):
    # Decode message.
    message_decoded = (str(messageW.payload.decode("utf-8"))).split("|")
    global gui_type, currentQuestion, rank, message, message_old
    if message_decoded[0] == "A" and message_decoded[1] == ID:
        if (message_decoded[2] == "ERROR"):
            if (message_decoded[3] == "1"):
                gui_type = 1
                message = "Brak danych w bazie"
            elif (message_decoded[3] == "2"):
                gui_type = 1
                message = "Już zalogowano"
            #authorization()
        else:
            print("Mój nick to", message_decoded[2])
            gui_type = 1
            message = "Oczekiwanie na rozpoczęcie"
            print("Czekam na rozpoczęcie gry")
    elif (message_decoded[0] == "Q"):
        gui_type = 2
        currentQuestion = message_decoded[1]
        message = message_decoded
    elif (message_decoded[0] == "R"):
        rank.clear()
        print(message_decoded)
        gui_type = 3
        for i in range(2, len(message_decoded)):
            rank.append(message_decoded[i])
        message_old = message
        message = message_decoded




def playerGui():
    global gui_type, currentQuestion, rank
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if gui_type == 0:
            screen.fill(bg_color)
            label_text = font_50.render(message, False, text_color)
            screen.blit(label_text, (270, 300))
            pg.display.update()

        elif gui_type == 1:
            screen.fill(bg_color)
            label_text = font_50.render(message, False, text_color)
            screen.blit(label_text, (270, 300))
            pg.display.update()

        elif gui_type == 2:
            screen.fill(bg_color)
            q = splitQuestion(currentQuestion, 700).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, text_color)
                text_rect = question.get_rect(center=(440, 30 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("A: " + message[2], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, text_color)
                text_rect = question.get_rect(center=(200, 200 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("B: " + message[3], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, text_color)
                text_rect = question.get_rect(center=(700, 200 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("C: " + message[4], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, text_color)
                text_rect = question.get_rect(center=(200, 450 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("D: " + message[5], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, text_color)
                text_rect = question.get_rect(center=(700, 450 + 30 * i))
                screen.blit(question, text_rect)

            pg.draw.line(screen, (255,255,255), (900, 0), (900, 720))
            ranking = font_50.render("Ranking:", False, text_color)
            pos = 150
            for i in range(0,len(rank)-1,2):
                r = font_30.render(rank[i] + " " + rank[i+1], False, text_color)
                screen.blit(r, (1050, pos))
                pos += 70
            screen.blit(ranking, (1000, 50))
            pg.display.update()

        elif gui_type == 3:
            screen.fill(bg_color)
            correct = message[1]
            q = splitQuestion(currentQuestion, 700).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, text_color)
                text_rect = question.get_rect(center=(440, 30 + 30 * i))
                screen.blit(question, text_rect)
            colorA = wrong_answ_color
            colorB = wrong_answ_color
            colorC = wrong_answ_color
            colorD = wrong_answ_color
            
            if correct == 'a':
                colorA = text_color
            elif correct == 'b':
                colorB = text_color
            elif correct == 'c':
                colorC = text_color
            elif correct == 'd':
                colorD = text_color

            q = splitQuestion("A: " + message_old[2], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, colorA)
                text_rect = question.get_rect(center=(200, 200 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("B: " + message_old[3], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, colorB)
                text_rect = question.get_rect(center=(700, 200 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("C: " + message_old[4], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, colorC)
                text_rect = question.get_rect(center=(200, 450 + 30 * i))
                screen.blit(question, text_rect)

            q = splitQuestion("D: " + message_old[5], 500).split('\n')
            for i in range(len(q)):
                question = font_30.render(q[i], False, colorD)
                text_rect = question.get_rect(center=(700, 450 + 30 * i))
                screen.blit(question, text_rect)
            

            

            pg.draw.line(screen, (255,255,255), (900, 0), (900, 720))
            ranking = font_50.render("Ranking:", False, text_color)
            pos = 150
            for i in range(0,len(rank)-1,2):
                r = font_30.render(rank[i] + " " + rank[i+1], False, text_color)
                screen.blit(r, (1050, pos))
                pos += 70
            screen.blit(ranking, (1000, 50))
            pg.display.update()

def splitQuestion(question, n):
    message = question.split()
    q = ""
    flag = ""
    for i in range(len(message) - 1):
        q += message[i] + " "
        flag += message[i] + " "
        answerA = font_30.render("Pytanie: " + flag + message[i+1], False, text_color)
        if(answerA.get_size()[0] > n):
            flag = ""
            q += '\n'
    q += message[len(message) - 1]
    return q

def question(md):
    print("Pytanie:", md[1])
    print("A:", md[2])
    print("B:", md[3])
    print("C:", md[4])
    print("D:", md[5])
    start_time = time.time()
    tmp = input("Wpisz odpowiedź")
    points = int(md[6]) - (time.time() - start_time)
    send_mess("Q|" + ID + "|" + tmp + "|" + str(int(points * 100)))


def send_mess(mess):
    client.publish("quiz/player", mess, )


def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    # Send message about conenction.
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("quiz/server")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def temp():
    s = input()
    while s != "quit":
        send_mess(s)
        s = input()


def authorization():
    global ID
    ID = input("Wpisz swoje ID:")
    send_mess("A|" + ID)
    print("Czekam na odpowiedź serwera")

    flag = True
    while True:
        if gui_type == 3:
            flag = True
        if gui_type == 2 and flag:
            flag = False
            start_time = time.time()
            tmp = input("Wpisz odpowiedź")
            points = int(message[6]) - (time.time() - start_time)
            send_mess("Q|" + ID + "|" + tmp + "|" + str(int(points * 100)))
            time.sleep(1)


    #startWait() #tutaj mam do testu jakkolwiek, ale chyba lepiej, zeby bylo przy otrzymaniu wiadomosci mqtt

def run_receiver():
    connect_to_broker()
    thread1 = Thread(target = authorization)
    thread1.start()
    #thread1.join()
    playerGui()
    #thread2 = Thread(target=playerGui, args=("Przyłóż kartę", ))
    #thread2.start()
    #thread2.join()
    temp()
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
    #gui_type = 2
    #playerGui("Przyłóż karte")
    #playerGui(["Pyt1", "a", "basd", "c", "dasd", "a"])
    #questionGui(["Pyt1", "a", "b", "c", "d", "a"])