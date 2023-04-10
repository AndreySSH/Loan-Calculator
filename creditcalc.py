import argparse
import sys
import math

interest_rate = 0


def main():
    global interest_rate
    if len(sys.argv) - 1 < 4:
        print('Incorrect parameters')

    else:
        if args.interest is None or args.interest < 0:
            print('Incorrect parameters')
        else:
            interest_rate = args.interest / 12 / 100
            if args.type == 'annuity':
                if args.payment is not None and args.principal is not None and args.periods is not None:
                    print('Incorrect parameters')
                else:
                    overpayment = calc_annuity()
                    print(f'Overpayment = {overpayment}')

            elif args.type == 'diff':
                if args.payment is not None:
                    print('Incorrect parameters')
                else:
                    overpayment = calc_diff()
                    print(f'Overpayment = {overpayment}')
            else:
                print('Incorrect parameters')



def calc_diff():
    number_of_periods = args.periods
    loan_principal = args.principal
    if number_of_periods < 0 or loan_principal < 0:
        print('Incorrect parameters')
    else:
        overpayment = -loan_principal
        for month_n in range(0, number_of_periods):
            month_payment_n = math.ceil(loan_principal / number_of_periods
                                        + interest_rate
                                        * (loan_principal - loan_principal * month_n / number_of_periods))
            overpayment += month_payment_n
            print(f'Month {month_n + 1}: payment is {month_payment_n}')
        return overpayment


def calc_annuity():
    loan_principal = args.principal
    number_of_periods = args.periods
    annuity_payment = args.payment

    if args.payment is None:
        # calc payment
        temp = math.pow(1 + interest_rate, number_of_periods)
        annuity_payment = math.ceil(loan_principal * interest_rate * temp / (temp - 1))
        print(f'Your annuity payment = {annuity_payment}!')

    elif args.principal is None:
        # calc principal
        temp = math.pow(1 + interest_rate, number_of_periods)
        loan_principal = math.floor(annuity_payment * (temp - 1) / interest_rate / temp)
        print(f'Your loan principal = {loan_principal}!')

    elif args.periods is None:
        # calc periods

        number_of_periods = math.ceil(
            math.log(annuity_payment / (annuity_payment - interest_rate * loan_principal),
                     1 + interest_rate)
        )

        months = number_of_periods
        years = months // 12
        months %= 12

        time_to_pay = ''
        if years > 0:
            time_to_pay += f"{years} year{'s' if years > 1 else ''}"
            if months > 0:
                time_to_pay += " and "
        time_to_pay += f"{months} month{'s' if months > 1 else ''}"

        print(f'It will take {time_to_pay} to repay this loan!')

    return number_of_periods * annuity_payment - loan_principal



if __name__ == '__main__':
    parse = argparse.ArgumentParser(prog=sys.argv[0], description='Could calculate different loan variants.')
    parse.add_argument('--type', choices=['diff', 'annuity'])
    parse.add_argument('--payment', type=int)  # only with type = 'annuity'
    parse.add_argument('--principal', type=int)
    parse.add_argument('--periods', type=int)
    parse.add_argument('--interest', type=float)  # float

    args = parse.parse_args()

    main()
