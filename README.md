# :e-mail: Auto Email

Sends an email, from a specific **sender email** to a certain **receiver email**.

## Setup

- get code and setup environment
```
    git clone https://github.com/FranMacedo/autoemail
    cd  autoemail
    .\venv\scripts\activate
    pip install -r requirements.txt    
```

- Make sure your sender email address allows for remote usage (if it is gmail, you need to [allow less secure apps](https://myaccount.google.com/lesssecureapps)). 
- You must setup 2 variables, `sender_email` and `password` (of that `sender_email`), in an `.env` file in the main directory. check the `.env.preset` file for the correct format.

## Run
 
```python
    python run.py
```
logs will be written in files inside the `logs` directory. Each file will have the date and time of the run.

## Arguments


### Styles
Edit the `style` variable in the `styles.py` file with your custom css code.


### Run
Edit the file `run.py` with your custom variables:

- `receiver_email`: email to send to
- `title`: title/subject of email
- `body_text`: body/text of email. Can be in html format or just plain old text. will be incorporated in a div in top of body.
- `table`: if you want to render a pandas DataFrame inside them email body as an html table (after text) and also attach it as an excel or csv file. **Do not assign** any value if don't need. Example:
    ```python
        table = {
            'df': pd.DataFrame({
                    'dates': [1,2,3],
                    'values': [1203,4034,3434],
                }), 
            'name': 'some_long_data.csv',
            'max_len': 30,
            conditions: {'danger':'this is very wrong'}
        }
    ```
    - `df` is your pandas DataFrame (necessary)
    - `name` is the file name, with or without extension - .csv, .xlsx (defult will be .xlsx)
    - `max_len` is the maximum length of the table to be displayed in the body text. The full table will always be available as an attachment 
    - `conditions`: dictionary with:
        - **KEYS** - text that can be found in a cell of `df` that you want to format with a specific class and 
        - **VALUES** - what class to format that text with ('danger', 'danger-back', 'success', ...) from the `style` variable in the `styles.py` file.


## Images and Atachements

- Atachements should be placed inside the `attachments` folder.
- Images to show inline of the email should be placed inside the `images` folder. They will **not** show up as attachements _unless_ they are placed inside the `attachments` folder. 


## Example
```python
send_auto_email(
            receiver_email='yourclientemail@gmail.com', 
            title='download 15/06',
            text='Today our sales increase here and decrease there mostly because of reasons.', 
            df=<AS_SHOWN_ABOVE>,  
            )
```
