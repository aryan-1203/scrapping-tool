from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys

short_wait = 1

# Set headless Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Create headless driver
driver = webdriver.Chrome(options=options)

def open_website():
    driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")
    driver.implicitly_wait(short_wait)

def select_something(XPATH_dropdown_list, XPATH_list_item):
    driver.find_element(By.XPATH, XPATH_dropdown_list).click()
    driver.find_element(By.XPATH, XPATH_list_item).click()

def click_something(XPATH):
    driver.find_element(By.XPATH, XPATH).click()

def E2W(two_wheeler_nt_path, two_wheeler_t_path):
    click_something(two_wheeler_nt_path)
    print("Log: 2W NT selected")
    sys.stdout.flush()
    click_something(two_wheeler_t_path)
    print("Log: 2W T selected")
    sys.stdout.flush()

def E3W(three_wheeler_nt_path, three_wheeler_t_path):
    click_something(three_wheeler_nt_path)
    print("Log: 3W NT selected")
    sys.stdout.flush()
    click_something(three_wheeler_t_path)
    print("Log: 3W T selected")
    sys.stdout.flush()

def en_date(list_of_dates, meta_year):
    match meta_year:
        case "2024" | "2028":
            feb_day = 29
        case _:
            feb_day = 28
    dates = {
        "JAN": f"01-31",
        "FEB": f"02-{feb_day}",
        "MAR": "03-31",
        "APR": "04-30",
        "MAY": "05-31",
        "JUN": "06-30",
        "JUL": "07-31",
        "AUG": "08-31",
        "SEP": "09-30",
        "OCT": "10-31",
        "NOV": "11-30",
        "DEC": "12-31"
    }
    list_of_dates_f = []
    for month in list_of_dates:
        month = month.strip().upper()
        if month in dates:
            dated = dates[month]
            list_of_dates_f.append(f"{meta_year}-{dated}")
        else:
            print(f"Warning: Unknown month '{month}' found. Skipping.")
            sys.stdout.flush()
    return list_of_dates_f

def return_header(rows, trim, year):
    """
    Builds the final header for the output file.
    :param rows: List of rows extracted from input Excel/CSV
    :param trim: Not used currently but kept for compatibility
    :param year: The year to use for month mapping
    :return: List containing header fields
    """
    # Check if rows have enough data
    if not rows or len(rows) < 4:
        print("Warning: Not enough rows to extract header. Returning default header.")
        sys.stdout.flush()
        return ["State", "RTO", "Variant", "OEM", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Total", "Year"]

    # Extract raw months from 4th row (index 3)
    raw_months = rows[3][2:]  # Skipping first two columns: Variant, Maker

    # Filter out any empty or whitespace-only entries
    raw_months = [m for m in raw_months if m and m.strip() != '']

    # Convert raw month names into correct format
    month_dates = en_date(raw_months, year)

    # Final header
    header = ["State", "RTO", "Variant", "OEM"] + month_dates + ["Total", "Year"]
    return header

def return_row(list_of_rows, serial_number, trim, var_ph, rto_ph, state_ph):
    """
    Builds a single row of data aligned with the final header.
    :param list_of_rows: Full list of extracted rows
    :param serial_number: Current processing row index (after header rows)
    :param trim: Not used currently but kept for compatibility
    :param var_ph: Placeholder for variant
    :param rto_ph: Placeholder for rto
    :param state_ph: Placeholder for state
    :return: List containing row data or None if invalid
    """
    try:
        row_data = list_of_rows[3 + serial_number]  # Skip 3 header rows
    except IndexError:
        print(f"Warning: Row {3 + serial_number} is out of range. Skipping.")
        sys.stdout.flush()
        return None

    # Validate row content
    if not row_data or all((cell is None or (isinstance(cell, str) and cell.strip() == '')) for cell in row_data):
        print(f"Warning: Empty or invalid row at index {3 + serial_number}. Skipping.")
        sys.stdout.flush()
        return None

    # Extract necessary fields
    row = row_data[1:]  # Skipping serial no. or unnecessary first column
    maker = row[0].strip() if row[0] and isinstance(row[0], str) else "Unknown Maker"

    # Month values start from 3rd index onward
    month_values_raw = row[2:]

    month_values = []
    for val in month_values_raw:
        if isinstance(val, str):
            val = val.strip()
        try:
            month_values.append(int(val))
        except (ValueError, TypeError):
            month_values.append(0)

    total = sum(month_values)

    # Construct final row
    final_row = [state_ph, rto_ph, var_ph, maker] + month_values + [total, "2024"]  # Hardcoding Year=2024 here; you can make it dynamic
    return final_row
