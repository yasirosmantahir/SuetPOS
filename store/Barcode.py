import random


class BarcodeEAN13:
    def generateRandom(sku_list):


        def calculate_check_digit( number):
            # Calculate the check digit for the random number
            digits = [int(x) for x in str(number)]
            odd_sum = sum(digits[0::2])
            even_sum = sum(digits[1::2])
            total = odd_sum + even_sum * 3
            check_digit = (10 - (total % 10)) % 10
            return check_digit


        def generate_random_barcode():
            # Generate a random 12-digit number

            random_number = random.randint(100000000000, 999999999999)
            check_digit = calculate_check_digit(random_number)
            return str(random_number) + str(check_digit)

        sku = generate_random_barcode()

        while ( sku in sku_list ):
            sku = generate_random_barcode()



        return sku

