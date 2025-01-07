import requests
import csv

URL = "http://172.20.241.9/luedataa_kannasta_groupid_csv.php"
GROUP_ID = "212" 


CSV_FILE = "data.csv"

def fetch_and_save_data():
    try:

        params = {"groupid": GROUP_ID}
        response = requests.get(URL, params=params)


        if response.status_code == 200:
            print("Data haettu onnistuneesti!")
            

            data = response.text
            rows = data.splitlines()


            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                for row in rows:
                    csv_writer.writerow(row.split(","))  
                
            print(f"Data tallennettu tiedostoon {CSV_FILE}")



    except Exception as e:
        print(f"Tapahtui virhe: {e}")


fetch_and_save_data()

