from download_comments import get_news
from pathlib import Path
from datetime import datetime
import os
import enlighten
import json
import typer


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
        os.makedirs(os.path.join(folder, str(new['date'])), exist_ok=True)
        path = os.path.join(folder, str(new['date']), new['title']+'.json')
        json.dump(new, open(path, 'w'), indent=2,
                  default=str, ensure_ascii=False)
        print(f"{new['title']}-{new['date']}")
        ticks.update()



if __name__ == "__main__":
    typer.run(main)
