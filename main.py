import logging
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from numpy import imag
from email import encoders
import ssl
import smtplib
import logging
from setup import setup
from glob import glob
import pandas as pd
from styles import style

class AutoEmail():
    """
    Sends automatic emails.
    You must setup 2 variables, "sender_email" and "password", in an ".env" file in the main directory.
    receiver_email: email to send to
    title: title/subject of email
    body_text: body/text of email. Can be in html format or just plain old text. will be incorporated in a div in top of body.
    table: Do not assign any value if don't need. if you want to render a pandas DataFrame inside them email body as an html table (after text) and also attach it as an excel or csv file.
        example:
            {
                'df': pd.DataFrame({
                        'dates': [1,2,3],
                        'values': [1203,4034,3434],
                    }), 
                'name': 'some_long_data.csv',
                'max_len': 30,
                conditions: {'danger':'this is very wrong'}
            }
            where:
                - df is your pandas DataFrame (necessary)
                - name is the file name, with or without extension - .csv, .xlsx (defult will be .xlsx)
                - max_len is the maximum length of the table to be displayed in the body text. The full table will always be available as an attachment 
                - conditions: dict with KEYS - text that can be found in a cell of df that you want to format with a specific class and 
                                    VALUES - what class to format that text with ('danger', 'danger-back', 'success', ...) from the 'style" variable in the 'styles.py' file

    
    Atachements should be placed inside the 'attachments' folder.

    EXAMPLE:
        send_auto_email(
                    receiver_email='yourclientemail@gmail.com', 
                    title='download 15/06',
                    text='Today our sales increase here and decrease there mostly because of reasons.', 
                    df=<AS_SHOWN_ABOVE>,  
                    )
    """

    def __init__(self, receiver_email, title, body_text, table={}):    
        self.images_path, self.attachments_path = setup()
        logging.info('Setting up variables')
        self.receiver_email = receiver_email
        self.title = title
        self.body_text = body_text
        self.table = table
        

        load_dotenv()
        self.sender_email = os.environ.get("email")
        self.password = os.environ.get("password")
        if not self.sender_email or not self.password:
            logging.error(' "sender_email" and "password" variables not found in environment. You must setup this variables in an ".env" file in the main directory.')
        
        self.send_email()

    def df_to_txt(self):
        df = self.table.get('df', pd.DataFrame())
        df_name = self.table.get('name', 'table')
        max_len = self.table.get('max_len', None)
        conditions = self.table.get('conditions', None)
        if df.empty:
            self.df_fp = None
            return ''
        to_excel = True
        if df_name.endswith('.csv'):
            to_excel = False
        elif df_name.endswith('.xls'):
            df_name_ = df_name.split('.')[:-1]
            df_name = ''.join(df_name_)
            df_name = df_name + '.xlsx'
        elif not df_name.endswith('.xlsx'):
            df_name = df_name + '.xlsx'
            
        df_fp = os.path.join(self.attachments_path, f'{df_name}')
        if to_excel:
            df.to_excel(df_fp, index=False)
        else:
            df.to_csv(df_fp, index=False)
        self.df_fp = df_fp
        
        if max_len and len(df) > max_len:
            logging.info(f'Turning first {max_len} of df to text')
            df_txt = df.iloc[:max_len, :]
        else:
            df_txt = df
        
        if conditions:
            style_f = self.custom_style(self.conditions)
            df_txt = df_txt.to_html(
                formatters={d: style_f for d in df_txt.columns.tolist()}, classes='mystyle', escape=False)
        else:
            df_txt = df_txt.to_html(classes='mystyle', escape=False)

        return df_txt

    def custom_style(conditions):

        def style_f(x):
            for c_txt, c_class in conditions.items():
                if str(x).lower() == str(c_txt).lower():
                    return f'<span class={c_class}>{x}</span>'
            return str(x)

        return style_f

    def get_image(self, image_path):
        fp = open(image_path, 'rb')
        image = MIMEImage(fp.read())
        fp.close()
        image.add_header('Content-ID', '<Mailtrapimage>')
        return image

    def get_file_name(self, file_path):
        return os.path.split(file_path)[1]

    def main_html(self, body_text, df_txt=''):
        return f"""\
            <html>
            <head>
                <style>{style}</style>
            </head>
            
            <body>
                <h1>{self.title}</h1>
                <div>
                {body_text}

                </div>
                <div>
                {df_txt}
                </div>
            </body>
            </html>
        """

    def build_message(self):
        logging.info('Building message')
        body_text = self.body_text
        message = MIMEMultipart()
        message["Subject"] = self.title
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        df_txt = self.df_to_txt()
        
        images_paths = glob(f'{self.images_path}/*')
        if len(images_paths) > 0:
            body_text = body_text + '<img src="cid:Mailtrapimage" >'

        images = []
        for image_path in images_paths:
            logging.info(f'adding inline image {self.get_file_name(image_path)}')
            images.append(self.get_image(image_path))

        html = self.main_html(body_text, df_txt)
        message.attach(MIMEText(html, "html"))
    
        for image in images:
            message.attach(image)
        
        attachments_files = glob(f'{self.attachments_path}/*')
        for attachment_path in attachments_files:
            attachement_name = self.get_file_name(attachment_path)
            logging.info(f'Attaching file {attachement_name}')
            with open(attachment_path, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                attach_section = MIMEBase("application", "octet-stream")
                attach_section.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(attach_section)
            
            # Add header as key/value pair to attachment part
            attach_section.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachement_name}",
            )
            message.attach(attach_section)
        

        return message


    def send_email(self):
        
        message = self.build_message()
        # return
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(
                    self.sender_email, self.receiver_email, message.as_string()
                )
        except Exception as e:
            print(f"Not possible to send email: {e}")

        logging.info('Email sent!')

        if self.df_fp:
            os.remove(self.df_fp)

