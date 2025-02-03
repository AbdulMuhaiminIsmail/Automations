import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

def update_sheet(sheet_name, rankings_1d, start_col):
    try:
        print("Updating google sheet")

        # Load credentials from the downloaded JSON key file
        creds = Credentials.from_service_account_file(r"D:\SEO Automations\script\creds.json", scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])

        # Refresh token if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Authorize the client
        client = gspread.authorize(creds)

        # Open the Google Sheet (by name or by URL)
        sheet = client.open(sheet_name).sheet1  # Access first sheet

        # Write data to specific cells
        rankings = []
        for rank in rankings_1d:
            if rank > 100:
                temp = ["N/A"]
            elif rank == 0:
                temp = ["Error"]
            else:
                temp = [rank]
            rankings.append(temp)

        sheet.update(rankings, start_col)  

        print("Sheet updated successfully!")
    except Exception as e:
        print(f"An error occurred while updating sheet: {e}")


rankings = [2, 3, 5, 0, 0, 5, -1, 7]
update_sheet("Automated Ranking", rankings, "E2")
