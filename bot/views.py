from django.shortcuts import render,HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import datetime, timedelta
from cal_setup import get_calendar_service
from gcsa.google_calendar import GoogleCalendar



CLIENT_ID = 'c8f2c8ae-943f-41ed-b274-22448503cb64'
SECRET_ID = '3NG7Q~PFGzDyJ.A02Bi-Ar3qLhJrwj-Isvjta'
account_sid = 'ACeaf344cbda950e2aa828c052aa811fa6'
auth_token = 'bfae9bebd8fd7f866f5b278a0f3b93a2'
client = Client(account_sid, auth_token)
DATE,start,NAME,NUMBER,MAIL,end = '','','','','',''
date_visited,time_visited,name_visited,number_visited,mail_visited,startmsg_visited = True,True,True,True,True,True

@csrf_exempt
def bot(request):
    global startmsg_visited,date_visited,time_visited,name_visited,number_visited,mail_visited
    global DATE,start,NAME,NUMBER,MAIL,end
    datedict = {'2022-02-22T':'22-Feb','2022-02-23T':'23-Feb','2022-02-24T':'24-Feb','2022-02-25T':'25-Feb'}
    timedict12 = {'04:30:00.000Z':'10am','06:30:00.000Z':'12pm','08:30:00.000Z':'2pm','10:30:00.000Z':'4pm','12:30:00.000Z':'6pm'}
    timedict24 = {10:'10am',12:'12pm',14:'2pm',16:'4pm',18:'6pm'}
    try:
        message = request.POST['Body']
        sender_name = request.POST['ProfileName']
        sender_number = request.POST['From']
        if message not in ['1','2','3','4'] and startmsg_visited:
            startmsg_visited = False
            client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='Hello! '+sender_name+', Please choose your date of appointment:\n1. 22-Feb\n2. 23-Feb\n3. \
                                    24-Feb\n4. 25-Feb',
                                to=sender_number,
                            )
        elif date_visited:
            date_visited=False
            if message=='1':
                DATE = '2022-02-22T'
            elif message=='2':
                DATE = '2022-02-23T'
            elif message=='3':
                DATE = '2022-02-24T'
            elif message=='4':
                DATE = '2022-02-25T'
            calendar = GoogleCalendar('monish.notbot@gmail.com',credentials_path='/Users/monishpalisetti/Desktop/webdev\
                /appointment_booking/client_secret_385471400639-5nbhm1ddje9r5d7v818od2vaq01u160t.apps.googleusercontent.com.json')
            slottime_string = 'Please choose from the available time slots:\n'
            booked_slots = []
            for event in calendar:
                e = str(event)
                if DATE[:10]==e[:10]:
                    booked_slots.append(int(e[11:13]))
            i=1
            for key in sorted(timedict24.keys()):
                if key not in booked_slots and key!=18:
                    slottime_string=slottime_string+str(i)+'. '+timedict24[key]+' to '+timedict24[key+2]+' (available)\n'
                elif key in booked_slots and key!=18:
                    slottime_string=slottime_string+str(i)+'. '+timedict24[key]+' to '+timedict24[key+2]+' (not available)\n'
                i+=1
            
            client.messages.create(
                                from_='whatsapp:+14155238886',
                                body= slottime_string,
                                to=sender_number,
                            )
        elif time_visited:
            time_visited = False
            if message == '1':
                start = '04:30:00.000Z'
                end = '06:30:00.000Z'
            elif message == '2':
                start = '06:30:00.000Z'
                end = '08:30:00.000Z'
            elif message == '3':
                start = '08:30:00.000Z'
                end = '10:30:00.000Z'
            elif message == '4':
                start = '10:30:00.000Z'
                end = '12:30:00.000Z'
    
            client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='Okay,great can we have your name?',
                                to=sender_number,
                            )
        elif name_visited:
            name_visited = False
            NAME = message
            client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='To complete your appointment,may we have your phone number to confirm?',
                                to=sender_number,
                            )
        elif number_visited:
            number_visited = False
            NUMBER = message
            client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='Lastly, can we also have your email address?',
                                to=sender_number,
                            )
        elif mail_visited:
            mail_visited = False
            MAIL = message
            client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='Thank you so much , for all the details!\n\nAre these all the final details?\n\nPhone: \
                                    '+NUMBER+'\nEmail: '+MAIL+'\nDate: '+datedict[DATE]+'\nTime: '+timedict12[start]+' to \
                                        '+timedict12[end]+'\n1. Yes\n2. No',
                                to=sender_number,
                            )
        elif date_visited==False and time_visited==False and name_visited==False and number_visited==False and mail_visited==False \
            and startmsg_visited==False:
            if message=='1':
                service = get_calendar_service()
                event_result = service.events().insert(calendarId='primary',
                        body={
                        "summary": 'Appointment with '+NAME,
                        "description": 'Phone number of attendee: '+NUMBER,
                        "start": {"dateTime": DATE+start},
                        "end": {"dateTime": DATE+end},
                        'attendees': [
                                            {'email': MAIL},
                                        ],
                            
                    },
                sendNotifications=True).execute()

                date_visited,time_visited,name_visited,number_visited,mail_visited,startmsg_visited = True,True,True,True,True,True
                client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='Thank you! for the booking,\nEvent with name: Appointment with '+NAME+' is created for \
                                    '+MAIL+'\nOur human will get in in touch with you soon',
                                to=sender_number,
                            )
            elif message=='2':
                date_visited,time_visited,name_visited,number_visited,mail_visited = True,True,True,True,True
                client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='Hello! '+sender_name+', Please choose your date of appointment:\n1. 17-Feb\n2. 18-Feb\n3. \
                                    19-Feb\n4. 20-Feb',
                                to=sender_number,
                            )
    except Exception:
        pass
    return HttpResponse('The bot is working')

