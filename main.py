from download_comments import get_news
from pathlib import Path
from datetime import datetime
import os
import enlighten
import json
import typer

app = typer.Typer()

def find_match(keywords:str, new):
    for i in new['tags']:
        if type(i) == str and not i.lower().find(keywords) == -1:
            return True
    if not new['title'].lower().find(keywords) == -1 or not new['summary'].lower().find(keywords) == -1:
        return True
    return False

@app.command()
def main(from_date: datetime, to_date: datetime, folder: Path = typer.Option(
    default = 'articles',
    exists=False,
    file_okay=False,
    dir_okay=True,
    resolve_path=True,
)):


    folder = str(folder)
    manager = enlighten.get_manager()
    ticks = manager.counter(desc='News', unit='news')

    for new in get_news(from_date.date(), to_date.date()):
        os.makedirs(os.path.join(folder, str(new['published'])), exist_ok=True)
        path = os.path.join(folder, str(new['published']), new['title']+'.json')
        json.dump(new, open(path, 'w'), indent=2,
                  default=str, ensure_ascii=False)
        print(f"{new['title']}-{new['published']}")
        ticks.update()

@app.command()
def search(keywords:str, from_date: datetime, to_date: datetime, folder: Path = typer.Option(
    default = 'articles',
    exists=False,
    file_okay=False,
    dir_okay=True,
    resolve_path=True,
)):
    
    folder = str(folder)
    manager = enlighten.get_manager()
    ticks = manager.counter(desc='News', unit='news')

    for new in get_news(from_date.date(), to_date.date()):
        if find_match(keywords,new):
            new['id'] = new['link']
            os.makedirs(os.path.join(folder, str(new['published'])), exist_ok=True)
            path = os.path.join(folder, str(new['published']), new['title']+'.json')
            json.dump(new, open(path, 'w'), indent=2,
                    default=str, ensure_ascii=False)
            print(f"{new['title']}-{new['published']}")
            ticks.update()

    
    

if __name__ == "__main__":
    app()
