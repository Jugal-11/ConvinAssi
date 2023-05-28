# from google.oauth2 import credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from django.shortcuts import redirect
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.urls import reverse
# from urllib.parse import urlencode

# # class GoogleCalendarInitView(APIView):
# #     def get(self, request):
# #         flow = InstalledAppFlow.from_client_secrets_file(
# #             settings.GOOGLE_CLIENT_SECRET_FILE,
# #             scopes=['https://www.googleapis.com/auth/calendar.readonly']
# #         )
# #         flow.redirect_uri = request.build_absolute_uri(reverse('google-calendar-redirect'))
# #         auth_url, _ = flow.authorization_url(access_type='offline')
# #         return redirect(auth_url)

# class GoogleCalendarInitView(APIView):
#     def get(self, request):
#         # Construct the authorization URL
#         auth_url = 'https://accounts.google.com/o/oauth2/auth'
#         params = {
#             'client_id': settings.GOOGLE_CLIENT_ID,
#             'redirect_uri': request.build_absolute_uri(reverse('google-calendar-redirect')),
#             'response_type': 'code',
#             'scope': 'https://www.googleapis.com/auth/calendar.readonly',
#             'access_type': 'offline',
#             'prompt': 'consent',
#         }
#         auth_url += '?' + urlencode(params)

#         # Redirect the user to the authorization URL
#         return redirect(auth_url)


# class GoogleCalendarRedirectView(APIView):
#     def get(self, request):
#         flow = InstalledAppFlow.from_client_secrets_file(
#             settings.GOOGLE_CLIENT_SECRET_FILE,
#             scopes=['https://www.googleapis.com/auth/calendar.readonly']
#         )
#         flow.fetch_token(authorization_response=request.build_absolute_uri())
#         credentials = flow.credentials
#         service = build('calendar', 'v3', credentials=credentials)
#         events = service.events().list(calendarId='primary').execute()
#         return Response(events['items'])

from django.shortcuts import redirect, render
from django.conf import settings
from rest_framework.views import APIView
from django.urls import reverse
from urllib.parse import urlencode
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework.response import Response


class GoogleCalendarInitView(APIView):
    def get(self, request):
        auth_url = 'https://accounts.google.com/o/oauth2/auth'
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': request.build_absolute_uri(reverse('google-calendar-redirect')),
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/calendar.readonly',
            'access_type': 'offline',
            'prompt': 'consent',
        }
        auth_url += '?' + urlencode(params)
        return redirect(auth_url)


class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        authorization_code = request.GET.get('code')
        if authorization_code:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CLIENT_SECRET_FILE,
                scopes=['https://www.googleapis.com/auth/calendar.readonly'],
                redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
            )
            flow.fetch_token(authorization_response=request.build_absolute_uri(),
                             code=authorization_code)
            credentials = flow.credentials
            service = build('calendar', 'v3', credentials=credentials)
            events = service.events().list(calendarId='primary').execute()
            print('events', events['items'])
            context = {'events': events['items']}
            return render(request, 'google_calendar_redirect.html', context)
            # return Response(events['items'])
        else:
            return Response({'error': 'Authorization code missing'})
        
        
