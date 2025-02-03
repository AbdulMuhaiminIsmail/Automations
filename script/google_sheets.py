import gspread
from google.oauth2.service_account import Credentials

def update_sheet(sheet_name, rankings_1d, start_col):
    try:
        # Load credentials from the downloaded JSON key file
        creds = Credentials.from_service_account_file("e:/Programming/SEO Automation/script/creds.json", scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])

        # Authorize the client
        client = gspread.authorize(creds)

        # Open the Google Sheet (by name or by URL)
        sheet = client.open(sheet_name).sheet1  # Access first sheet

        # Write data to specific cells
        rankings = []
        for rank in rankings_1d:
            if rank > 100:
                temp = ["N/A"]
            elif rank == -1:
                temp = ["Error"]
            else:
                temp = [rank]
            rankings.append(temp)

        sheet.update(rankings, start_col)  

        print("Sheet updated successfully!")
    except Exception as e:
        print(f"An error occurred while updating sheet: {e}")
