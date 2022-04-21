# Dependencies
import openpyxl


def save_to_excel(result):
    workbook_obj = openpyxl.load_workbook("odidata.xlsx")
    sheet_obj = workbook_obj.active
    for mtc in range(len(result)):
        sheet_obj.append(list(result.iloc[mtc]))
    workbook_obj.save("odidata.xlsx")