import csv
import os 
from collections import  Counter
from datetime import timedelta, datetime

BASE_DIR = os.path.dirname(__file__)
TICKETS_FILE_PATH = os.path.join(BASE_DIR,"tickets.csv")

REQUIRED_COLUMNS = {
    "ticket_id",
    "title",
    "priority",
    "status",
    "created_date",
    "assigned_team",
}

def read_tickets(file_path:str) -> list[dict] :
    try:
        with open(file_path, mode='r',newline='',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing_columns:
                raise ValueError(
                    f"CSV is missing required columns : {sorted(missing_columns)}"
                )
            tickets = list(reader)
            for ticket in tickets:
                ticket["priority"] = ticket["priority"].strip().upper()
                ticket["status"] = ticket["status"].strip().title()

            return tickets

                
    except FileNotFoundError as nf:
        raise FileNotFoundError("File is not present:",nf)
    except csv.Error as e:
        raise csv.Error("Some Error occured while reading the csv file:",e)

def get_count_priority_ticket() -> dict:
    priority_dic = Counter()
    csv_data = read_tickets(TICKETS_FILE_PATH)
    for data in csv_data:
        # if d['priority'] in dic:
        #     dic[d['priority']] += 1
        # else:
        #     dic[d['priority']] = 1
        priority_dic[data['priority']] += 1
    return priority_dic


def find_old_tickets(days: int, reference_date : datetime|None = None) -> list:
    if reference_date is None:
        reference_date = datetime.today()
    if days < 0 :
        raise ValueError("Days must be zero or greater")
    days_difference = reference_date - timedelta(days)
    csv_data = read_tickets(TICKETS_FILE_PATH)
    old_tickets = []
    for data in csv_data:
        try:
            ticket_date = datetime.strptime(data['created_date'],"%Y-%m-%d")
        except ValueError:
            continue
        if ticket_date <= days_difference:
            old_tickets.append(data['ticket_id'])

    return old_tickets

    
def write_ticket_summary(priority_counts: list[dict[str,str | int]], old_tickets: list[dict[str,str | int]]) -> None:
    try:
        output_file_path = os.path.join(os.path.dirname(__file__),'ticket_summary.csv')
        with open(output_file_path,"w",encoding="utf-8",newline='') as f:
            field_header = ['report_type','value','count']
            writer = csv.DictWriter(f,fieldnames=field_header) 
            writer.writeheader()
            writer.writerows(priority_counts)
            writer.writerows(old_tickets)

    except OSError as err:
        print("Some error occured while writing into file : ",err)


if __name__ == "__main__":
    print("Priority counts:")
    priority_dic = []
    for priority, count in get_count_priority_ticket().items():
        print(f"{priority}: {count}")
        priority_dic.append({'report_type':'priority','value':priority,'count':count})

    print("\nOld tickets:")
    old_tickets = find_old_tickets(7)

    old_tickets_dic = []
    if old_tickets:
        for ticket_id in old_tickets:
            print(ticket_id)
            old_tickets_dic.append({'report_type':'old_tickets','value':ticket_id})
    else:
        print("No tickets found older than 7 days.")
   
    write_ticket_summary(priority_dic,old_tickets_dic)

