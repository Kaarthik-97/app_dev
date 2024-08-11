import flet as ft
from flet import *
import pandas as pd
import requests
# from nselib.libutil import *
# from nselib.constants import *
# from nselib import capital_market
from bs4 import BeautifulSoup as bs
import regex as re


def headers(df : pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]

def rows(df : pd.DataFrame) -> list:
    rows = []
    for index, row in df.iterrows():
        rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
    return rows


def main_page(page: Page):
    page.title = "KD_Stock"
    page.vertical_alignment = "center"
    hf = ft.HapticFeedback()
    page.overlay.append(hf)
    text_field = TextField( value="0",text_align = "center")
    cur_value = ft.Text()
    tb2 = ""
    error_dlg = ft.AlertDialog(
    title = ft.Text("Please Enter the Correct Name",color=ft.colors.RED,bgcolor=ft.colors.BLACK,size = "15",text_align="center"))
    # lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    # bar_search = SearchBar(bar_hint_text="enter the company name here", on_change=check_company,bar_leading=IconButton(icon="search"))

    def realtime_stock(e):
        comp_name = tb1.value
        url = f"https://www.google.com/finance/quote/{comp_name}:NSE"
        webpage = requests.get(url)
        html_text = bs(webpage.text, 'html.parser')
        class_value = html_text.find(class_="YMlKec fxKbKc")
        try:
            value = class_value.text
            cur_value.value = value
            hf.heavy_impact()
            page.update(cur_value)
            return cur_value
        except:
            page.open(error_dlg)
            cur_value.value = None
            page.update(cur_value)
        
    # market_list = capital_market.equity_list()
    # company_list = market_list["NAME OF COMPANY"].to_list()

    # datatable = ft.DataTable(
    #     columns=headers(market_list),
    #     rows=rows(market_list))

    def remove_me(e):
        text_field.value = int(text_field.value)-1 if (text_field.value != int("0")) else int("0")
        page.update(text_field)
        return text_field
    
    def add_me(e):
        text_field.value = int(text_field.value)+1
        page.update(text_field)
        return text_field
    
    # def check_company():
    #     # company_list_to_display = []
    #     for company in company_list:
    #         if tb1.value in company:
    #             # company_list_to_display.append(company)
    #             # lv.controls.append(ft.Text(company))
    #             pass
            
    tb1 = TextField(label = "Please Enter the Stock Name",text_align = "center") #,on_change=check_company()

    page.add(ft.Row
             (
                 [  
                     ft.Container(content = tb1),
                     ft.Container(content = ft.ElevatedButton(text="OK",on_click= realtime_stock)),
                     ft.Container(content = cur_value)
                #   datatable
    ],
    alignment = "center"
    ),
    ft.Row([

    ])
    )
    

ft.app(main_page)