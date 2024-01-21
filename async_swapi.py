import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from models import Session, SwapiPeople, close_db, init_db

CHUNK_SIZE = 10


async def insert_people(people_list):
    people_list = [SwapiPeople(**person) for person in people_list if person.get('detail')!= 'Not found']
    async with Session() as session:
        session.add_all(people_list)
        await session.commit()


async def get_person(person_id):
    session = aiohttp.ClientSession()
    f_dict = {'films':'title', 'species':'name','starships':'name','vehicles':'name'}
    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    json_response = await response.json()
    if json_response.get('detail') != 'Not found':
        json_body = {key:json_response.get(key) for key in SwapiPeople.__table__.columns.keys() if key != 'ID'} 
        for field in f_dict.keys():
            result = []
            coros = [get_linked_name(i, f_dict[field],session) for i in json_body.get(field)]
            result += await asyncio.gather(*coros)
            json_body[field] = ", ".join(result)
    else:
        json_body = json_response
    await session.close()
    return json_body

async def get_linked_name(link, name_field, session: aiohttp.ClientSession):
    response = await session.get(link)
    json_response = await response.json()
    return json_response[name_field]



async def main():
    await init_db()

    for person_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
        coros = [get_person(person_id) for person_id in person_id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_people(result))
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)
    await close_db()


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
