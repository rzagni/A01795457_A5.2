# pylint: disable=invalid-name # Keep the name  of file based on requirements

import argparse
import json


class ValidationError(Exception):
    pass


def print_plus(content, file_handler):
    """
    Prints content to both the console and a file.

    Args:
        content (str): The text to print.
        file_handler (file object): The file to write to.
    """
    print(content)
    file_handler.write(content + "\n")


def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not a valid JSON.")
        return None


def validate_price_catalog(price_catalog):
    if not isinstance(price_catalog, list):
        print("Error: Price catalog format is invalid")
        return {}

    extracted_prices = {}
    for index, item in enumerate(price_catalog):
        try:
            if not isinstance(item, dict):
                raise ValidationError(
                    f"Warning: Invalid format at index {index}.\n"
                    "\tProduct will not be included in calculations."
                )
            if "title" not in item or not isinstance(item["title"], str):
                raise ValidationError(
                    f"Warning: Missing title at index {index}.\n"
                    "\tProduct will not be included in calculations."
                )
            if "price" not in item or not isinstance(
                item["price"], (int, float)
            ):
                raise ValidationError(
                    f"Warning: Missing price at index {index}.\n"
                    "\tProduct will not be included in calculations."
                )
            extracted_prices[item["title"]] = item["price"]
        except ValidationError as e:
            print(f"Error: {e}")
    return extracted_prices


def validate_sales_records(sales_records):
    if not isinstance(sales_records, list):
        print("Error: Sales records format is invalid")
        return []

    extracted_sales = []
    for index, sale in enumerate(sales_records):
        try:
            if not isinstance(sale, dict):
                raise ValidationError(
                    f"Warning: Invalid format at index {index}.\n"
                    "\tSale of item(s) will not be included in calculation"
                )
            if "Product" not in sale or not isinstance(sale["Product"], str):
                raise ValidationError(
                    f"Warning: Missing product at index {index}.\n"
                    "\tSale of item(s) will not be included in calculation"
                )
            if "Quantity" not in sale or not isinstance(sale["Quantity"], int):
                raise ValidationError(
                    f"Warning: Missing quantity at index {index}.\n"
                    "\tSale of item(s) will not be included in calculation"
                )
            extracted_sales.append((sale["Product"], sale["Quantity"]))
        except ValidationError as e:
            print(f"Error: {e}")
    return extracted_sales


def compute_total_sales(price_catalog, sales_records):
    total_sales = 0.0
    for product, quantity in sales_records:
        if product in price_catalog:
            total_sales += price_catalog[product] * quantity
        else:
            print(
                f"Warning: Sold product '{product}' not in catalog.\n"
                "\tSale of item(s) will not be included in calculation"
                )
    return total_sales


def main():
    parser = argparse.ArgumentParser(
        description="Compute total sales from price catalog and sales records."
    )
    parser.add_argument("price_catalog",
                        type=str,
                        help="Price Catalog in JSON format")
    parser.add_argument("sales_records",
                        type=str,
                        help="Sales Records in JSON format")
    args = parser.parse_args()

    price_catalog = load_json(args.price_catalog)
    if price_catalog is None:
        print("Exiting")
        return

    extracted_prices = validate_price_catalog(price_catalog)

    sales_records = load_json(args.sales_records)
    if sales_records is None:
        print("Exiting")
        return

    extracted_sales = validate_sales_records(sales_records)
    total = compute_total_sales(extracted_prices, extracted_sales)
    print(f"\nTotal Sales: ${total:,.2f}")


if __name__ == "__main__":
    main()
