
"""
Functions that generate a code for tables and companies,
used to unique create QRCode


"""
def table_code_generator(nbr):
    """
    Function that generate a code for the tables, used to an unique code

    max number of tables : (35^2)/5 = 1 225 / 5  = 245

    ]0000 ; 244[ -> contains all the values with 2 characters for the table

    fct :
    nbr : table number
    (5*nbr)[base 10] -> (nbr*5)[base 36]

    """

    nbr = base36.encode(5*(abs(nbr-244)))
    while len(nbr) <  2 :
        nbr = str(nbr) +  'Z'
    return nbr.upper()


if __name__ == '__main__':
    main()
