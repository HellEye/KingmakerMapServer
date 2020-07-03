from flask import request


def getFormattedData(data):
    columnString = ""
    if data is not None:
        columnString = "("
        for c in data:
            columnString += c + ','
        columnString = columnString[:-1]
        columnString += ")"
    return columnString


def getPostColumns(data, columns):
    if len(data) != len(columns):
        return ""
    out = ""
    for i in range(len(data) - 1):
        out += f"{columns[i]} = {data[i]}, "
    out += f"{columns[-1]} = {data[-1]}"
    return out


def getColumnString(columns):
    columnString = "*"
    if columns is not None:
        columnString = "("
        for c in columns:
            columnString += c + ','
        columnString = columnString[:-1]
        columnString += ')'
    return columnString


def getDataAndColumns(request: request):
    data = []
    columns = []
    for key in request.form:
        columns.append(key)
        if request.form[key].isnumeric():
            data.append(request.form[key])
        else:
            data.append(f"'{request.form[key]}'")
    return data, columns
