import pandas as pd
# Steps:
# 1. Filter the file - return only the lines that contain the category
# 2. Slice the string - return a dictionary with the values
# 3. Create a new dataframe with the values


raw_data = [] # stores the raw data from text file, is later used to compare the result with the original data
categories = ["Dinkel", "Mohn","Semmel", "Käsestangerl", "Pizza", "Pizzen", "Kornspitz", "Salzstangerl", "Kipferl", "Krapfen", "Graham" ]

def contains_category(line):
    for category in categories:
        if category in line:
            return True
    return False



def filter_file(filePath):
    filteredTextFile = open("./FilesToConvert/new_data.txt", "w", encoding="utf-8")

    with open(filePath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if contains_category(line):
                # ---- replace ä with ae ----
                if "ä" in line:
                    line = line.replace("ä", "ae")
                filteredTextFile.write(line)
                # append raw_line_data
                raw_data.append(line)
    filteredTextFile.close()



def slice_string(string):
    """slice strings into a dictionary"""
    dict = {"classroom": "", "amount": 0, "product": ""}
    # if string starts with whitespace, we have to add the values differently
    # --- whitespace check ---
    if string.startswith(" "):
        string = string.replace(" ", "")
        dict["classroom"] = ""
        dict["amount"] = int(string[:1])
        dict["product"] = string[1:]
    else:
        # --- correct format check ---
        formatted_string = string.replace(" ", "")
        # --- check if the strings number is higher than 9
        check_string = formatted_string[2:4]
        if check_string.isdigit():
            dict["classroom"] = formatted_string[:2]
            dict["amount"] = int(formatted_string[2:4])
            dict["product"] = formatted_string[4:]
        else:
            # --- only one digit check ---
            dict["classroom"] = formatted_string[:2]
            dict["amount"] = int(formatted_string[2:3])
            dict["product"] = formatted_string[3:]
    return dict


def create_dataframe(file_path):
    class_room = []
    amount = []
    product = []
    raw_row_data = []

    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            row_data = slice_string(line)
            raw_row_data.append(row_data)
            class_room.append(row_data["classroom"])
            amount.append(row_data["amount"])
            product.append(row_data["product"].replace("\n", ""))

        data = {
            "Klasse": pd.Series(class_room),
            "Anzahl": pd.Series(amount),
            "Produkt": pd.Series(product),
            "Raw Data": pd.Series(raw_row_data)
        }
    return data


def get_product_amount(data, substring):

    global raw_data
    productName = []
    values = []
    raw_data_to_display = []
    idx = 0

    for index, row in data.iterrows():
        temp_product = row["Produkt"]
        if substring in temp_product:
            productName.append(temp_product)
            values.append(row["Anzahl"])
            raw_data_to_display.append(raw_data[index])

            # check if the product is already in the list
            # for row in raw_data:
            #     if not substring in row:
            #         raw_data.remove(row)

    raw_data = raw_data_to_display
    filtered_data = {
        "Filtered_Product": pd.Series(productName),
        "Filtered_Amount": pd.Series(values),
        "Raw_Data": pd.Series(raw_data)
    }

    return filtered_data


# ------------------filter txt file ------------------ #
filter_file("./FilesToConvert/waldschuleBestellung.txt")
print(raw_data)
# ------------------create dataframe ------------------ #
temp = create_dataframe("./FilesToConvert/new_data.txt")
values = pd.DataFrame(temp)
values["Anzahl"] = values["Anzahl"].astype(int)

# ------------------filter products and amount ------------------ #
# Dinkel", "Mohn","Semmel", "Käsestangerl", "Pizza", "Pizzen", "Kornspitz", "Salzstangerl", "Kipferl", "Krapfen", "Graham

f_df = get_product_amount(values, "Pizz")
filtered = pd.DataFrame(f_df)
sum_filtered = sum(filtered["Filtered_Amount"])

# ------------------Add Sum Column into Dataframe ------------------ #
sum_row = pd.DataFrame([{"Sum": sum_filtered}])
filtered = pd.concat([filtered, sum_row])

# to csv
filtered.to_csv("./FilesToConvert/filtered.csv", index=False, encoding="utf-8")
