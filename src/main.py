from fastapi import FastAPI
import uvicorn
from api import main_router

# processor = TextProcessor()
# create_tables()
# row = '''Кот сидел на ковре. Кот любит спать. На ковре было тепло и уютно.
# Кот — это домашнее животное. Собака тоже может быть домашним животным.
# Коты и собаки часто живут вместе. Кот мурлычет, а собака лает.
# На улице холодно, но кот всё равно гуляет. Собака бегает за котом.
# Кот прыгнул на диван, а собака легла рядом. Они друзья.'''


# text_schema = TextSchema(content=row, title='Кот')
# txt_id = insert_text(text=text_schema)
# words = processor.get_tokens(row)
# insert_words(words=words, text_id=txt_id)
app = FastAPI()
app.include_router(main_router)
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True,
    )