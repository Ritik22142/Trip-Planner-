# Imports
from flask import Flask, render_template, request
import places as ps
import hotels as h
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import warnings
warnings.filterwarnings("ignore")
import final_scrapping

app = Flask(__name__)


#Home Page

@app.route("/")
def home():
    return render_template("index.html")


#Flight Page

@app.route("/flights")
def flight():
    return render_template("flight.html")


#Function for flight search

@app.route("/search_flights" , methods=['GET', 'POST'])
def flight_search():
    if request.method == 'POST':
        value1 = request.form.getlist('src')
        source = value1[0]

        value2 = request.form.getlist('dst')
        destination = value2[0]

        value3 = request.form.getlist('src_date')
        depart_date = value3[0]

        value4 = request.form.getlist('dst_date')
        return_date = value4[0]

        option = request.form.getlist('flexRadioDefault')
        radio_options= option[0]

        # detail emailing feature is optional. So, we put it in try except blocks
        try: 
            email_checkbox = request.form.getlist('email_subsribed')
            email_checkbox_status = email_checkbox[0]
        
            email = request.form.getlist('subsriber_email')
            email_address= email[0]
        except:
            pass

    print("\n\nForm Data entered by the user:\n\n")
    try:
        print("Source: ",source, "\nDestination: ", destination, "\nDeparture date: ",
                    depart_date, "\nReturn date: ", return_date,"\nFilter choosed: ", 
                    radio_options,"\nCheckbox status: ", email_checkbox_status,
                     "\nE-mail entered: ", email_address
                     )
    except:
        print("Source: ",source, "\nDestination: ", destination, "\nDeparture date: ",
                    depart_date, "\nReturn date: ", return_date,"\nFilter choosed: ", 
                    radio_options
                     )
        

    # radio_options:['best','cheapest', 'quickest' ]

    # calling the "start_kayak" function from imported python script "flight_scrapping.py" here

    list_of_df=final_scrapping.start_kayak(source, destination, depart_date, return_date)

    # list_of_df[0]=best , list_of_df[1]=cheap , list_of_df[2]=fast. This is the order in which dataframes are returned
    # print("\n--------------------------------------------------------------\n")
    # print(list_of_df[0])
    # print(type(df))
    # print("\n--------------------------------------------------------------\n")

    if radio_options=='best':
        df= list_of_df[0].copy()
    elif radio_options=='cheapest':
        df= list_of_df[1].copy()
    elif radio_options=='quickest':
        df= list_of_df[2].copy()

    
    # checking e-mail subsribed button status:
    try: 
        if email_checkbox_status =='email_subsribed':
            
            # call e-mail function
            # receiver's email address in "email_address"
            print("\nReceiver's email:", email_address)      
            from1 = 'adityarajsingh705@outlook.com'
            print("\nSender's email:", email_address)      

            to = email_address
            message = MIMEMultipart()

            message['From'] = from1
            message['To'] = to
            message['Subject'] ="Flight Details"
            body_email = "Check attachements."
            message.attach(MIMEText(body_email, 'plain'))

            filename = "file1.csv"
            attachment = open("file1.csv", "rb")


            x = MIMEBase('application', 'octet-stream')
            x.set_payload((attachment).read())
            encoders.encode_base64(x)

            x.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            message.attach(x)

            s_e = smtplib.SMTP('smtp.outlook.com', 587)
            s_e.starttls()

            s_e.login(from1, "#TripPlanner17")
            text = message.as_string()
            # print("\n\n------------------------------text\n\n", text)
            try:
                s_e.sendmail(from1, to, text)
                print("\n\nMail sent to user successfully.\n\n")
                print("Note: Since this is system-generated email, first time it will be marked as spam\n\n")

            except smtplib.SMTPDataError:
                pass  # ignore email errors 
                print("\n\nSMTP Error:Mail not sent\n\n")
            
            s_e.quit()
    except:
        pass


    return render_template("flight.html", source=source, destination=destination,depart_date=depart_date,
                           return_date=return_date, tables=[df.to_html(classes='data', index=False)],
                           titles=df.columns.values)


# @app.route("/receive_emails" , methods=['GET', 'POST'])
# def receive_emails():
#     if request.method == 'POST':
#         value1 = request.form.getlist('email')

#     return render_template("flight.html")


#Cab Page

@app.route("/cabs")
def cabs():
    return render_template("cabs.html")


#Hotels Page

@app.route("/hotels")
def hotels():
    return render_template("hotels.html")

#Function for hotel search

@app.route("/search_hotels", methods=("POST", "GET"))
def best_hotels():
    if request.method == 'POST':
        vals = request.form.getlist('city')
        destination_city = vals[0]
        print("City selected:", destination_city)

    # calling the "search_hotel" function from imported python script "hotels.py" here

    df = h.search_hotel(destination_city)
    return render_template("hotels.html", destination=destination_city, tables=[df.to_html(classes='data', index=False)],
                           titles=df.columns.values)


#Places Page

@app.route("/places")
def places():
    return render_template("places.html")


#Function for places search



@app.route("/search_places", methods=['GET', 'POST'])
def best_places():
    if request.method == 'POST':
        vals = request.form.getlist('destination_places')
       
        destination1 = vals[0]

        print("City entered by user: ", destination1)

    # calling the "search_places" function from imported python script "places.py" here

    df = ps.search_places(destination1)
    print(df)
    return render_template("places.html", destination=destination1, tables=[df.to_html(classes='data', index=True)],
                           titles=df.columns.values)


#Contact Page

@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/contact_us", methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        username = request.form.getlist('username')
        user_name = username[0]

        useremail = request.form.getlist('useremail')
        user_email = useremail[0]

        userphone = request.form.getlist('userphone')
        user_phone = userphone[0]

        usermessage = request.form.getlist('usermessage')
        user_message = usermessage[0]
        try:
            Recipient_name=user_name
            Recipient_mobile_no =user_phone
            Recipient_msg = user_message
            sender = user_email
            to = "adityarajsingh705@outlook.com"
            message = MIMEMultipart()

            message['From'] = sender
            message['To'] = to
            message['Subject'] ="User's Query"
            body_email = f"Recipient_name {Recipient_name} \n Recipient_mobile_no {Recipient_mobile_no} \n Recipient msg:-\n{Recipient_msg}"
            message.attach(MIMEText(body_email, 'plain'))

        

            s_e = smtplib.SMTP('smtp.outlook.com', 587)
            s_e.starttls()

            s_e.login(sender, "ritik@1234")
            text = message.as_string()
            # print("\n\n------------------------------text\n\n", text)
            try:
                s_e.sendmail(sender, to, text)
                print("\n\nMail sent to user successfully.\n\n")
                print("Note: Since this is system-generated email, first time it will be marked as spam\n\n")

            except smtplib.SMTPDataError:
                pass  # ignore email errors 
                print("\n\nSMTP Error:Mail not sent\n\n")

            s_e.quit()

            print("\n-----------------------------------------------------------\n")
            print("\nUser-name: ", user_name,"\nUser-email: ", user_email,"\nUser-phone: ", user_phone,"\nUser-message: ", user_message )
            print("\n-----------------------------------------------------------\n")
        except:
            print("Error")



    return render_template("contact.html",user_name=user_name, user_email= user_email, user_phone=user_phone, user_message=user_message )



#About Page

@app.route("/about")
def about():
    return render_template("about.html")


# debug = True is like hot reload feature
# app.run(debug=True)

# Running the application on this system as host server. All the device connected with the same network can access the application remotely on their device.
app.run(debug=True, host="0.0.0.0", port=8003)
# app.run(debug=True, host="143.244.135.235",port=8003)


