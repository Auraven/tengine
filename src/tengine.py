import sys, os, time
from abc import abstractmethod
from typing import Callable
class PageItem:
    @abstractmethod
    def print(self):
        pass

class Page:
    def __init__(self, *page_items:PageItem) -> None:
        self.page_items:list[PageItem] = page_items
    def print(self) -> None:
        for page_item in self.page_items:
            page_item.print()

class Text(PageItem):
    def __init__(self, *lines:str) -> None:
        self.lines:list[str] = lines
    def print(self):
        for line in self.lines:
            print(line)

class LinkedText(PageItem):
    def __init__(self, output:Callable) -> None:
        self.output:Callable = output
    def print(self):
        print(self.output())   

class Menu(PageItem):
    def __init__(self, title:str, *options:tuple, prompt_text = '>') -> None:
        self.title:str = title
        self.options:list[tuple] = options
        self.prompt_text:str = prompt_text
        self.option_aliases:list[str] = []
        for option in options:
            self.option_aliases.append(option[0].split(' ')[0].lower())

    def print(self):
        print(self.title)
        for index, option in enumerate(self.options):
            print(f'[{index}] {option[0]}')
        option = None
        text = input(self.prompt_text).lower()
        for i, option_alias in enumerate(self.option_aliases):
            if text == option_alias[0] or text == option_alias:
                option = self.options[i]
                break
        if option is None:
            try:
                option = self.options[int(text)]
            except:
                option = None
        if option is not None:
            option[1]()
        else:
            print('Invalid Input')
            time.sleep(1)          


class PageManager:
    def __init__(self, *pages:Page) -> None:
        self.pages:list[Page] = pages
        self.index:int = 0
    def print(self):
        self.pages[self.index].print()
        os.system('cls')
    def get_active(self) -> Page:
        return self.pages[self.index]
    def set_active(self, index:int):
        self.index = index