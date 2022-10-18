
from gcsa.google_calendar import GoogleCalendar

calendar = GoogleCalendar('monishsai.pv@gmail.com',credentials_path='/Users/monishpalisetti/Desktop/webdev/appointment_booking/client_secret_597137240518-1ttco94aen2ajvlm7qq0snjdm2u27vkh.apps.googleusercontent.com.json',authentication_flow_port=8910)
'''
booked_slots = []
DATE = '2022-02-24T'
for event in calendar:
    e = str(event)
    if DATE[:10]==e[:10]:
        booked_slots.append(int(e[11:13]))
print(booked_slots)
from cal_setup import get_calendar_service
NAME = 'testmon'
NUMBER = '123'
DATE = '2022-02-23T'
start = '06:30:00.000Z'
end = '08:30:00.000Z'
MAIL = 'abc@test.company'
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
'''