from datetime import datetime

from ticket_priority_count import (
    read_tickets, 
    get_count_priority_ticket,
    find_old_tickets,
    TICKETS_FILE_PATH
)


def test_read_csv_returns_25_tickets():

    tickets = read_tickets(TICKETS_FILE_PATH)
    assert isinstance(tickets,list)
    assert len(tickets) == 25

def test_priority_counts():
    counts = get_count_priority_ticket()

    assert counts["P1"] == 7
    assert counts["P2"] == 8
    assert counts["P3"] == 5
    assert counts["P4"] == 5

def test_find_old_tickets():

    reference_date = datetime(2026,8,26)
    old_tickets = find_old_tickets(7,reference_date)
    assert "INC-1003" in old_tickets
    assert "INC-1024" in old_tickets
    assert "INC-1022" not in old_tickets