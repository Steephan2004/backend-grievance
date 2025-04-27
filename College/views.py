from django.shortcuts import render
# import view sets from the REST framework
from rest_framework import viewsets
from django.middleware.csrf import get_token
from django.http import JsonResponse,HttpResponse
from vonage import Client, Sms #It's for SMS Api
# import the TodoSerializer from the serializer file
from .serializers import *
import json
# import the Todo model from the models file
from .models import *
from twilio.rest import Client
from email import encoders
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import csv
from io import StringIO
from bs4 import BeautifulSoup
from decouple import config


# create a class for the Todo model viewsets
class LoginView(viewsets.ModelViewSet):

	# create a serializer class and 
	# assign it to the TodoSerializer class
	serializer_class = LoginSerializer

	# define a variable and populate it 
	# with the Todo list objects
	queryset = Login.objects.all()


class GuestLoginView(viewsets.ModelViewSet):

	serializer_class = GuestLoginSerializer
	queryset = GuestLogin.objects.all()
 
class AdminLoginView(viewsets.ModelViewSet):

	serializer_class = AdminLoginSerializer
	queryset = AdminLogin.objects.all()
    

class QueryFormView(viewsets.ModelViewSet):
      serializer_class=QueryFormSerializer
      queryset=QueryForm.objects.all()
      
      
def get_data(request):
    if request.method == 'GET':
        data = QueryForm.objects.values()  # Retrieve data from your model
        return JsonResponse(list(data), safe=False)
    

def update_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            item_id = int(data.get('id'))
            new_status = data.get('status')
            new_remark=data.get('remark')
            

            # Update the status in your database here
            # Example:
            item = QueryForm.objects.get(id=item_id)
            item.Status = new_status
            item.Remark=new_remark
            item.save()
            if new_status=="COMPLETED":
                phone(item.MobileNumber)

            return JsonResponse({'message': 'Status updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
def phone(MobileNumber):
    
    account_sid = config('ACCOUNT_SID')
    auth_token = config('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_='+19562908942', body='From Grievance App-Your reported problem is solved', to='+916383765373')
    
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

def check(request):
    if request.method == 'GET':
        print(request.GET.keys())
        print("name:",request.GET['name'])
        print("password:",request.GET['password'])
        try:
            user = AdminLogin.objects.get(UserName=request.GET['name'],Password=request.GET['password'])
            print("User logined ",user)
            if user:
                return JsonResponse({"status":True,"userId":user.id})
                
            else:
                return JsonResponse({"status":False})
        except:
            pass
          # Retrieve data from your model
        return JsonResponse({"status":False})
def sendEmail(request):
  if request.method == 'GET':
    try:
      Title = request.GET['title']
      Venue = request.GET['venue']
      RoomNo = request.GET['RoomNo']
      Floor = request.GET['floor']
      Complaint = request.GET['complaint']
      Mail = request.GET['mail']
      print(Mail, Venue)
    except KeyError as e:
      return HttpResponse(f'Missing parameter: {str(e)}', status=400)

    # Determine the main receiver email
    receiver_email = {
      'Computer': 'rsteephan85@gmail.com',
      'Civil': 'steephan383@gmail.com',
      'Electrical': 'steephan383@gmail.com',
      'Plumbing': 'steephan383@gmail.com'
    }.get(Mail, 'rsteephan85@gmail.com')

    hod_email = {
      'CSE': 'rsteephan85@gmail.com',
      'EEE': 'steephan383@gmail.com',
      'ECE': 'steephan383@gmail.com',
      'MECH': 'steephan383@gmail.com',
      'NCC': 'steephan383@gmail.com',
      'HOSTEL': 'steephan383@gmail.com',
      'CANTEEN': 'steepha383@gmail.com',
    }.get(Venue, 'rsteephan85@gmail.com')

    # Add an additional email to the list
    additional_email = "steverogers03062004@gmail.com"
    receiver_emails = [receiver_email, additional_email, hod_email]

    # Email credentials (replace with your credentials)
    email = config('EMAIL')
    password = config('PASSWORD')  # Don't store passwords in plain text

    # Email details
    sender_email = email
    subject = 'Grievance App'

    # Build HTML content
    html_content = f"""
    <p>A Problem Arised</p>
    <ul>
      <li>Venue: {Venue}</li>
      <li>RoomNo: {RoomNo}</li>
      <li>Floor: {Floor}</li>
      <li>Complaint: {Complaint}</li>
    </ul>
    """

    # Create a multipart message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    # Create the plain text and HTML versions of the message body
    text_part = MIMEText(f'A Problem Arised\n\nVenue: {Venue}\nRoomNo: {RoomNo}\nFloor: {Floor}\nComplaint: {Complaint}', 'plain')
    html_part = MIMEText(html_content, 'html')

    # Attach both parts to the message
    msg.attach(text_part)
    msg.attach(html_part)

    try:
      # Connect to Gmail's SMTP server
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        # Log in to your Gmail account
        server.login(email, password)
        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())

      print('Email sent successfully')
      return HttpResponse('Email sent successfully', status=200)
    except smtplib.SMTPException as e:
      print(f'Failed to send email: {str(e)}')
      return HttpResponse(f'Failed to send email: {str(e)}', status=500)


def fetch_and_generate_html_table():
    # Fetch data from QueryForm model
    query_data = QueryForm.objects.filter(Status='PROCESSING')

    # Create an HTML table structure
    html_table = """
    <html>
    <body>
        <h2>Weekly Query Report</h2>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Mobile Number</th>
                    <th>Department</th>
                    <th>Venue</th>
                    <th>Floor</th>
                    <th>Room No</th>
                    <th>Complaint</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Remark</th>
                </tr>
            </thead>
            <tbody>
    """

    # Create CSV structure in parallel
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)
    
    # Write CSV header
    csv_writer.writerow(['Name', 'Mobile Number', 'Department', 'Venue', 'Floor', 'Room No', 'Complaint', 'Status', 'Date', 'Remark'])

    for query in query_data:
        html_table += f"""
        <tr>
            <td>{query.Name}</td>
            <td>{query.MobileNumber}</td>
            <td>{query.Department}</td>
            <td>{query.Venue}</td>
            <td>{query.Floor}</td>
            <td>{query.RoomNo}</td>
            <td>{query.Complaint}</td>
            <td>{query.Status}</td>
            <td>{query.Date}</td>
            <td>{query.Remark}</td>
        </tr>
        """
        
        # Write the same data into CSV
        csv_writer.writerow([query.Name, query.MobileNumber, query.Department, query.Venue, query.Floor, query.RoomNo, query.Complaint, query.Status, query.Date, query.Remark])
    
    html_table += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Get CSV content
    csv_output.seek(0)
    csv_content = csv_output.getvalue()

    # Return raw HTML table string and CSV content
    return html_table, csv_content

def updateDataEmail():
    receiver_email = "steephan383@gmail.com"

    # Email credentials (use environment variables for security)
    email = 'steephan383@gmail.com'
    password = 'afsbgcqpxarauljc'  # Use environment variables for security

    # Email details
    sender_email = email
    subject = 'Weekly Report'

    # Get HTML content and CSV content
    html_content, csv_content = fetch_and_generate_html_table()

    # Create a multipart message
    msg = MIMEMultipart('mixed')  # 'mixed' is used to attach files
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the HTML part to the email
    html_part = MIMEText(html_content, 'html')
    # msg.attach(html_part)

    # Create the CSV attachment
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_content.encode('utf-8'))
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="query_report.csv"')

    # Attach the CSV file to the email
    msg.attach(part)

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Log in to your Gmail account
            server.login(email, password)
            # Send email
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully')
        return HttpResponse('Email sent successfully', status=200)
    except smtplib.SMTPException as e:
        print(f'Failed to send email: {str(e)}')
        return HttpResponse(f'Failed to send email: {str(e)}', status=500)