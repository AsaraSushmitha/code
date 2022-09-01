import csv
import glob
import json
import os
from datetime import datetime, date

data = []
def read_csv(bank_name, bank_file,specificationbank):
    with open(bank_file, encoding="utf-8-sig") as csv_file:
        csv_data = csv.DictReader(csv_file)
        for dict_data in csv_data:
            print("dict_data",dict_data)
            new_dict = {}
            for field in specificationbank[bank_name]['fields']:
                name = field['name']
                csv_value = dict_data[name]
                new_dict["bank_name"] = bank_name
                try:
                    if field['type'] == 'int':
                        new_dict[name] = int(csv_value)
                    elif field['type'] == 'float':
                        new_dict[name] = float(csv_value)
                    elif field['type'] == 'date':
                        dt_temp = datetime.strptime(csv_value, field['format'])
                        new_dict[name] = date(dt_temp.year,
                                              dt_temp.month,
                                              dt_temp.day)
                    else:
                        new_dict[name] = csv_value
                except:
                    return None
            data.append(new_dict)
            
    return data


def to_csv_file(bank_data, csv_spec, bankdetails, output_file):
    with open(output_file, 'w') as csv_file:
        header = []
        bank_name = list(bankdetails.keys())[0]
        print("bank_name",bank_name)
        for field in csv_spec[bank_name]["to_csv"]:
            print("field is",field)
            header.append(field['name'])
        csv_output = csv.writer(csv_file)
        csv_output.writerow(header)
        for bank_name in bankdetails.keys():
            for dict_fields in bank_data:
                data_list = []
                if bank_name == dict_fields["bank_name"]:
                    for field in csv_spec[bank_name]["to_csv"]:
                        data_list.append(dict_fields[field['field']])
                    csv_output.writerow(data_list)


def csvfile(dir):
    return {os.path.basename(file).split(".")[0]: file for file in glob.glob(dir + '/*.csv')}



def jsonload(json_file):
    with open(json_file) as f:
        data = json.load(f)

    return data


def convertto(data, transform_to, bank_name):
    for data_dict in data:
        if data_dict["bank_name"] == bank_name:
            for rule in transform_to:
                print("rule is",rule)
                name = rule[1]
                print("data_dict[name]",data_dict[name])
                print("name=",name)
                print("data_dict",data_dict)
                print("rule[2] is",rule[2])
                if rule[0] == 'add_fields':
                    print("in add fields block")
                    print(data_dict[rule[2]])
                    print(data_dict[name])
                    data_dict[name] = data_dict[name] + data_dict[rule[2]]
                elif rule[0] == 'divide':
                    print("individe block")
                    print(rule[2])
                    print("data_dict[name]",data_dict[name])
                    data_dict[name] = data_dict[name] / rule[2]


if __name__ == '__main__':
    bankdetails= csvfile("data")
    print(bankdetails)
    specification = "bank.json"
    print(specification)
    specificationbank = jsonload(specification)
    print(specificationbank)
    print("---------------------")
    for bank_name, bank_file in bankdetails.items():
        read_csv(bank_name, bank_file, specificationbank)

    for bank_name, bank_file in bankdetails.items():
        bank_data = specificationbank.get(bank_name)
        if bank_data and 'transform' in bank_data:
            print(bank_data['transform'])
            convertto(data, bank_data['transform'], bank_name)
    print("data is=========",data)
    print("\n")
    print("\n")
    print("\n")
    print("specificationbank is=========",specificationbank)
    print("\n")
    print("\n")
    print("bankdetails is=========",bankdetails)

    to_csv_file(data,specificationbank, bankdetails, "newfile.csv")
