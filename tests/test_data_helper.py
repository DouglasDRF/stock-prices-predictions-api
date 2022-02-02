import datetime as dt
from stockpredictions.data import get_last_working_day

def test_get_model_instance():
    today = dt.datetime.today().date()
    result = get_last_working_day()
    assert today.day != result
    
       
