import asyncio
import time
from typing import List
from core.config import DATA
from core.types import RequestData
from core.funcs import login, get_data, parse_2_bottext, send_message


print("Bot ishga tushmoqda ...")
session = login()
DATA["session"] = session

if session:
    print("Muffaqiyatli login bo'ldi !")
    while True:
        data: List[RequestData] = get_data(DATA["session"])
        if data != []:
            if DATA["data"] is None:
                DATA["data"] = data
            else:
                old_data_ids = {item["load_id"] for item in DATA['data']}
                result = [item for item in data if item["load_id"] not in old_data_ids]
                if result != []:
                    for item in result:
                        text = parse_2_bottext(item)
                        if text:
                            asyncio.run(
                                send_message(text), 
                            )
                DATA["data"] = data
                time.sleep(60)
else:
    print("Login amalga oshmadi !")
