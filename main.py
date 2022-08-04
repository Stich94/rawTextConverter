import pandas as pd

# Steps:
# 1. Filter the file - return only the lines that contain the category
# 2. Slice the string - return a dictionary with the values
# 3. Create a new dataframe with the values


raw_data = [] # stores the raw data from text file, is later used to compare the result with the original data
categories = ["Dinkel", "Mohn","Semmel", "Käsestangerl", "Pizza", "Kornspitz", "Salzstangerl", "Kipferl", "Krapfen", "Graham" ]

def contains_category(line):
    for category in categories:
        if category in line:
            return True
    return False



def filter_file(filePath):
    filteredTextFile = open("./FilesToConvert/new_data.txt", "w")

    with open(filePath, "r") as f:
        lines = f.readlines()
        for line in lines:
            if contains_category(line):
                filteredTextFile.write(line)
                # append raw_line_data
                raw_data.append(line)
    filteredTextFile.close()


def slice_string(string):

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


def get_product_amount(data, search_product):

    productName = []
    values = []

    for index, row in data.iterrows():
        temp = row["Produkt"]
        if search_product in temp:
            productName.append(temp)
            values.append(row["Anzahl"])

            # check if the product is already in the list
            for row in raw_data:
                if not search_product in row:
                    raw_data.remove(row)
    filtered_data = {
        "Filtered_Product": pd.Series(productName),
        "Filtered_Amount": pd.Series(values),
        "Raw_Data": pd.Series(raw_data)
    }
    return filtered_data


# ------------------filter txt file ------------------ #
filter_file("./FilesToConvert/waldschuleBestellung.txt")

# ------------------create dataframe ------------------ #
temp = create_dataframe("./FilesToConvert/new_data.txt")
values = pd.DataFrame(temp)
values["Anzahl"] = values["Anzahl"].astype(int)

# ------------------filter products and amount ------------------ #
f_df = get_product_amount(values, "Krap")
filtered = pd.DataFrame(f_df)
sum_filtered = sum(filtered["Filtered_Amount"])

# ------------------Add Sum into Dataframe ------------------ #
sum_row = pd.DataFrame([{"Sum": sum_filtered}])
filtered = pd.concat([filtered, sum_row])

# to csv
filtered.to_csv("./FilesToConvert/filtered.csv", index=False)
